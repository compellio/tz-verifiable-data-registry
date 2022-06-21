# Tezos Verifiable Data Registry

A collection of contracts implementing a Registry for [Verifiable Data Schemas](https://www.w3.org/TR/vc-data-model/#data-schemas) as described by W3C.

### Instalation

You will need to have a **Wallet** on an existing Tezos Testnet. We have used **Ithacanet** for our tests.

At the current stage of development, the interaction is done directly through the **registryLogic** contract. At a later stage, all interactions will be done through the **registry** Lambda contract. This is to simplify the configuration for testing purposes.

1. In the **registryLogic** contract, define the first parameter of **sp.add_compilation_target**, define the first parameter of **sp.add_compilation_target**, **Registry** as the address of your originated **registryLogic** contract.
2. Compile and Originate the **registryLogic** contract.
3. In the **registry** (lambda) contract, define the second parameter of **sp.add_compilation_target**, **Registry** as the address of your originated **registryLogic** contract.
3. In the **registry** (lambda) contract, define the second parameter of **sp.add_compilation_target**, **Registry** as the address of your **Wallet**.
2. Compile and Originate the **registry** contract.
4. In the **Storage** contracts (**issuerRegistry** and **schemaRegistry**), define the first parameter of **sp.add_compilation_target**, **IssuerRegistry** and **SchemaRegistry** as the address of your originated **registryLogic** contract.
5. In the **Storage** contracts (**issuerRegistry** and **schemaRegistry**), define the second parameter of **sp.add_compilation_target**, **IssuerRegistry** and **SchemaRegistry** as the address of your **Wallet**.
6. Compile and Originate the **Storage** contracts
7. Open the **registryLogic** contract in https://better-call.dev/ and interact with the **update_contract_address** entry point, setting the following pairs:
   - `issuer_registry_contract` - **issuerRegistry** contract address
   - `schema_registry_contract` - **schemaRegistry** contract address

### Testing

There are two ways to test the smart contracts:

- Open https://better-call.dev/ in your browser, find your contract and navigate to the "Interact" Tab.
- Install our Test suite. Installation instructions can be found [here](https://github.com/compellio/tz-verifiable-data-registry/tree/testnet/test-suite)
