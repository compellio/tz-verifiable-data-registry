# Tezos Verifiable Data Registry
This project consists of a collection of smart contracts created for the Tezos public network that allow identification and verification processes as specified by the Verifiable Data Registry component of the W3C [verifiable credentials model](https://www.w3.org/TR/vc-data-model/).
More specifically, the contracts implement two main points of functionality:
- Registration of the identity of organizations (represented as Issuers)
- Registration of verifiable credential schemas that can be used to validate or produce verifiable credentials for a specific domain
- Mapping between issuers and schemas

## Contracts
The following contracts are included in the implementation:

- **issuerRegistry contract**: A contract that implements the storage for the registry of issuers
- **schemaRegistry contract**: A contract that implements the storage for the registry of schemas and the mappings between schemas and issuers.
- **registryLogic contract**: A contract that implements all the logic for managing the registries.
- **registry contract**: A lambda contract that can be use as the main entry point.

### Issuer Registry
The issuerRegistry contract implements a storage contract which contains the following information:
- **issuer_map**:  a BigMap that stores the DID ([Decetralized Identifier](https://www.w3.org/TR/did-core/)) of the issuer as key and a record as value that includes:
  - **issuer_data**: The data associated with the DID. For compliance with W3C, this should store the DID document.
  - **issuer_did**: The DID of the issuer.
  - **issuer_owner**: The wallet address of the owner of the record, meaning the wallet that has permission to modify the record. This is set by the address that created the record.
  - **status**: A value indicating the status of the record, from this set of values: {1:Active, 2:Deprecated, 3:In Conflict}
- **certifier**: The address of the certifier account. This is the account that was defined in the contract origination and it has the authority to perform higher level operations.
- **logic_contract_address**: The address of the logic contract (registryLogic). The issuerRegistry contract accepts call only from it.

### Schema Registry
The schemaRegistry contract implements a storage contract which contains the following information:
- **schema_map**: a BigMap that stores the schema_id as key (an auto-increment number) and a record as value that includes:
  - **schema_data**: The schema definition. For compliance with W3C, this should be a JSON schema definition.
  - **schema_owner**: he wallet address of the owner of the record, meaning the wallet that has permission to modify the record. This is set by the address that created the record.
  - **status**: A value indicating the status of the record, from this set of values: {1:Active, 2:Deprecated}
- **issuer_schema_map**: a BigMap that stores the DID ([Decetralized Identifier](https://www.w3.org/TR/did-core/)) of the issuer as key and another map as value. The internal map contains the schema id as key and the status of the mapping as value.
- **certifier**: The address of the certifier account. This is the account that was defined in the contract origination and it has the authority to perform higher level operations.
- **logic_contract_address**: The address of the logic contract (registryLogic). The issuerRegistry contract accepts call only from it.

### Registry Logic
This contract implements all the code for managing the issuer and schema registry.
Its storage contains the following:
- **certifier**: The address of the certifier account. This is the account that was defined in the contract origination and it has the authority to perform higher level operations.
- **contracts**:  A BigMap that contains the addresses of the storage contracts. The key of the record is the contract name and the value it's address.
- **issuer_statuses**: A BigMap that contains the available statuses for the issuer registry records: {1:Active, 2:Deprecated, 3:In Conflict}
- **schema_statuses**: A BigMap that contains the available statuses for the schema registry records: {1:Active, 2:Deprecated}

This contract's endpoints implement the calls for all registry functionality:
- Issuers
  - add_issuer
  - set_issuer_active
  - set_issuer_deprecated
  - set_issuer_status
  - set_issuer_data
  - set_issuer_owner
- Schemas
  - add_schema
  - bind_issuer_schema
  - set_schema_active
  - set_schema_deprecated
  - set_schema_status
- update_contract_address: Endpoint for updating the address of the storage contracts.

### Registry (Lambda Contract)
This is the contract that does not implement any functionality or has storage. It is used as an immutable entry point so that any re-deployments or changes to the underlying contracts do not disturb the clients that are already in place.

## Installation

You will need to have a **Wallet** on an existing Tezos Testnet. We have used **Ithacanet** for our tests.

1. In the **registryLogic** contract, define the first parameter of **sp.add_compilation_target**, **RegistryLogic** as the address of your **Wallet**.
2. Compile and Originate the **registryLogic** contract.
3. In the **registry** (lambda) contract, define the first parameter of **sp.add_compilation_target**, **Registry** as the address of your originated **registryLogic** contract.
3. In the **registry** (lambda) contract, define the second parameter of **sp.add_compilation_target**, **Registry** as the address of your **Wallet**.
2. Compile and Originate the **registry** contract.
4. In the **Storage** contracts (**issuerRegistry** and **schemaRegistry**), define the first parameter of **sp.add_compilation_target**, **IssuerRegistry** and **SchemaRegistry** as the address of your originated **registryLogic** contract.
5. In the **Storage** contracts (**issuerRegistry** and **schemaRegistry**), define the second parameter of **sp.add_compilation_target**, **IssuerRegistry** and **SchemaRegistry** as the address of your **Wallet**.
6. Compile and Originate the **Storage** contracts
7. Open the **registryLogic** contract in https://better-call.dev/ and interact with the **update_contract_address** entry point, setting the following pairs:
   - `issuer_registry_contract` - **issuerRegistry** contract address
   - `schema_registry_contract` - **schemaRegistry** contract address

### Testing
#### Unit Testing
Unit tests were implemented in testScenarios.py. The unit tests require the storage and logic contract files in order to function:


- registryLogic.py
- schemaRegistry.py
- issuerRegistry.py

The logic is divided across different files, therefore <ins>we use [smartPy IDE](https://smartpy.io/ide) for running the tests</ins>  and not the command line client.

In order to run the tests you will need to:
1. Store the required contracts to the smartPy IDE. This can be done by using the Create Contract functionality. The names of the contracts need to be the same as the file name (eg. registryLogic.py) in order for the tests to load the contracts successfully.
2. Store the testScenario.py to the IDE.
3. Run the testScenario contract.

#### Functionality Testing
There are two ways to test the smart contracts after being deployed on the testnet:
- Open https://better-call.dev/ in your browser, find your contract and navigate to the "Interact" Tab.
- Install our Test suite. Installation instructions can be found [here](https://github.com/compellio/tz-verifiable-data-registry/tree/testnet/test-suite)
