# Tezos Verifiable Data Registry

The future of the Verifiable Data Registry smart contract on tezos.

### Instalation

You will need to have a **Wallet** on an existing Tezos Testnet. We have used **Hangzhounet** for our tests.

1. Compile and Originate the **Logic** contracts. For now only **issuerRegistryLogic** and **schemaRegistryLogic** can be tested.
2. In the **Registry** contract, define the first parameter of **sp.add_compilation_target**, **Registry** as the address of your **Wallet**.
3. Compile and Originate the **Registry** contract.
4. In the **Storage** contracts (**issuerRegistry** and **schemaRegistry**), define the first parameter of **sp.add_compilation_target**, **IssuerRegistry** and **SchemaRegistry** as the address of your originated **Registry** contract.
5. In the **Storage** contracts (**issuerRegistry** and **schemaRegistry**), define the second parameter of **sp.add_compilation_target**, **IssuerRegistry** and **SchemaRegistry** as the address of your originated **Logic** contracts. **IssuerRegistryLogic** address to **IssuerRegistry** and **SchemaRegistryLogic** address to **SchemaRegistry**.
6. In the **Storage** contracts (**issuerRegistry** and **schemaRegistry**), define the third parameter of **sp.add_compilation_target**, **IssuerRegistry** and **SchemaRegistry** as the address of your **Wallet**.
7. Compile and Originate the **Storage** contracts
8. Open the **Registry** contract in https://better-call.dev/ and interact with the **update_contract_address** entry point, setting the following pairs:
   - `issuer_registry_contract` - **IssuerRegistry** address
   - `schema_registry_contract` - **SchemaRegistry** address

### Testing

There are two ways to test the smart contracts:

- Open https://better-call.dev/ in your browser, find your contract and navigate to the "Interact" Tab.
- Navigate to the `test-suite` folder. Run `npm install` and then `parcel index.html --no-cache`. Open the URL shown in your CMD and go to "Toggle Settings", insert your **Registry** contract address and test.
