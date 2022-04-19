# Tezos Verifiable Data Registry Test Suite

You will need to have a **Wallet** on an existing Tezos Testnet. We have used **Hangzhounet** for our tests.

For implementing the test process, we created a test suite that relies on the [Taquito](https://tezostaquito.io/) library in order to design and perform test calls to smart contracts. Interfacing with the **Wallet** is done through the [Beacon SDK](https://github.com/airgap-it/beacon-sdk).

## Installation

For installation of the Test Suite, you will have to use the latest versions of Node.js and npm

1. Navigate to the test-suite folder
2. Open your Command Console
3. Run `npm install`
4. Run `parcel index.html --no-cache`

If the installation was successful, a localhost URL will appear on the console, for example, http://localhost:1234. Open your browser and enter this URL. If there are no errors you can start testing.

## Test scenarios

The scenarios that are currently implemented are the following:

- Upload Schema
- Get Schema
- Upload Issuer
- Get Issuer

This section describes in detail the parameters that are required for each of the test scenarios.

### Upload Schema

The use case for which the client submits their schema to the blockchain.

**Parameters:**

**Schema Data (string)** - A verifiable credential schema in JSON format. The entry will be considered as a string parameter. For example:

```
{ "type": "https://w3c-ccg.github.io/vc-json-schemas/schema/1.0/schema.json", "modelVersion": "1.0", "id": "did:work:MDP8AsFhHzhwUvGNuYkX7T;id=06e126d1-fa44-4882-a243-1e326fbe21db;version=1.0", "name": "EmailCredentialSchema", "author": "did:work:MDP8AsFhHzhwUvGNuYkX7T", "authored": "2018-01-01T00:00:00+00:00", "schema": { "$schema": "http://json-schema.org/draft-07/schema#", "description": "Email", "type": "object", "properties": { "emailAddress": { "type": "string", "format": "email" } }, "required": ["emailAddress"], "additionalProperties": false }, "proof": { "created": "2019-09-27T06:26:11Z", "creator": "did:work:MDP8AsFhHzhwUvGNuYkX7T#key-1", "nonce": "0efba23d-2987-4441-998e-23a9d9af79f0", "signatureValue": "2A7ZF9f9TWMdtgn57Y6dP6RQGs52xg2QdjUESZUuf4J9BUnwwWFNL8vFshQAEQF6ZFBXjYLYNU4hzXNKc3R6y6re", "type": "Ed25519VerificationKey2018" } }
```

### Get Schema

The use case for which the client retrieves a schema from the blockchain

**Parameters:**

**ID (nat)** - This is the ID of the schema namespace indentifier. The identifier is a non-negative number, including zero.

### Upload Issuer

The use case for which the client submits their DID document to the blockchain.

**Parameters:**

**Issuer did (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```

**Issuer Data (string)** - An issuer DID document in JSON format. The entry will be considered as a string parameter. For example:

```
{ "@context": "https://w3id.org/did/v1", "id": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "verificationMethod": [ { "id": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "type": "EcdsaSecp256k1VerificationKey2019", "controller": "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1", "publicKeyJwk": { "kty": "EC", "crv": "secp256k1", "x": "n03trG-1sWidluyYQ2gcKrgYE94rMkLIArZCHjv2GpI", "y": "6__x_vqe0nBGYf7azbQ1_VvvuCafG5MhhUPNvYp-Mak" } } ], "authentication": [ "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1" ], "assertionMethod": [ "did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1" ] }
```
 
### Get Issuer

The use case for which the client retrieves the did document of an issuer.

**Parameters:**

**Issuer did (string)** - A string defining the address of the id of the did document. For example:

```
did:tz:tz1zsSgDXeYPhZ3AuKhTFneDf1
```
