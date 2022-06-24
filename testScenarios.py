# Test Scenarios

import smartpy as sp

@sp.add_test(name = "TestScripts")
def test():
    REGISTRY_LOGIC = sp.io.import_stored_contract("registryLogic.py")
    ISSUER_REGISTRY = sp.io.import_stored_contract("issuerRegistry.py")
    SCHEMA_REGISTRY = sp.io.import_stored_contract("schemaRegistry.py")
    certifier_address = sp.test_account("Certifier").address
    operator_A_address = sp.test_account("Operator_A").address
    operator_B_address = sp.test_account("Operator_B").address

    scenario = sp.test_scenario()

    # Registry Logic Contract Instantiation

    registry_logic_contract = REGISTRY_LOGIC.RegistryLogic(
        certifier_address
    )

    scenario += registry_logic_contract

    # Issuer Registry contract instantiation

    issuer_registry_contract = ISSUER_REGISTRY.IssuerRegistry(
        registry_logic_contract.address,
        certifier_address
    )

    scenario += issuer_registry_contract

    # Schema Registry contract instantiation

    schema_registry_contract = SCHEMA_REGISTRY.SchemaRegistry(
        registry_logic_contract.address,
        certifier_address
    )

    scenario += schema_registry_contract

    # Updating Registry Logic Contract with addresses of instantiated storage contracts

    issuer_contract_record = sp.record(
        contract_name = "issuer_registry_contract",
        address = issuer_registry_contract.address
    )

    schema_contract_record = sp.record(
        contract_name = "schema_registry_contract",
        address = schema_registry_contract.address
    )

    registry_logic_contract.update_contract_address(issuer_contract_record).run(valid = True, sender = certifier_address)
    registry_logic_contract.update_contract_address(schema_contract_record).run(valid = True, sender = certifier_address)

    scenario.verify(registry_logic_contract.data.contracts["issuer_registry_contract"] == issuer_registry_contract.address)
    scenario.verify(registry_logic_contract.data.contracts["schema_registry_contract"] == schema_registry_contract.address)

    # Creating a new Schema

    schema = sp.record(
        schema_data = "schema_data",
    )

    # Add Schema
    registry_logic_contract.add_schema(schema).run(valid = True, sender = operator_A_address)

    # Check Schema addition on Schema Registry contract view
    scenario.verify(schema_registry_contract.get(0).schema_owner == operator_A_address)

    # Check Schema addition on Registry Logic contract view
    scenario.verify(registry_logic_contract.get_schema(0).schema_data == "schema_data")

    # Updating the status of Schema

    schema_set_status_deprecated_valid = sp.record(
        schema_id = 0,
        status = 2
    )

    schema_set_status_invalid_id = sp.record(
        schema_id = 999,
        status = 2
    )

    schema_set_status_invalid_status_id = sp.record(
        schema_id = 0,
        status = 999
    )

    # Set and verify setting Schema as deprecated
    registry_logic_contract.set_schema_deprecated(sp.record(schema_id = 0)).run(valid = True, sender = operator_A_address)
    scenario.verify(schema_registry_contract.get(0).status == 2)

    # Set and verify setting Schema as active
    registry_logic_contract.set_schema_active(sp.record(schema_id = 0)).run(valid = True, sender = operator_A_address)
    scenario.verify(schema_registry_contract.get(0).status == 1)

    # Set and verify setting Schema status
    registry_logic_contract.set_schema_status(schema_set_status_deprecated_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(schema_registry_contract.get(0).status == 2)

    # FAIL - Sender is not the owner of the Schema
    registry_logic_contract.set_schema_status(schema_set_status_deprecated_valid).run(valid = False, sender = operator_B_address)

    # FAIL - Schema ID does not exist
    registry_logic_contract.set_schema_status(schema_set_status_invalid_id).run(valid = False, sender = operator_A_address)
    
    # FAIL - Status is incorrect
    registry_logic_contract.set_schema_status(schema_set_status_invalid_status_id).run(valid = False, sender = operator_A_address)

    # Creating a new Issuer

    issuer_did = "did:tz:test_did"

    issuer = sp.record(
        issuer_did = issuer_did,
        issuer_data = "issuer_data",
    )

    # Add Issuer
    registry_logic_contract.add_issuer(issuer).run(valid = True, sender = operator_A_address)

    # Check Issuer addition on Issuer Registry contract view
    scenario.verify(issuer_registry_contract.get(issuer_did).issuer_owner == operator_A_address)

    # Check Issuer addition on Registry Logic contract view
    scenario.verify(registry_logic_contract.get_issuer(issuer_did).issuer_data == "issuer_data")

    # FAIL - Issuer DID already exists
    registry_logic_contract.add_issuer(issuer).run(valid = False, sender = operator_A_address)

    # Updating the Issuer

    issuer_set_status_deprecated_valid = sp.record(
        issuer_did = issuer_did,
        status = 2
    )

    issuer_update_data_valid = sp.record(
        issuer_did = issuer_did,
        issuer_data = "new_data"
    )

    issuer_set_status_invalid_did = sp.record(
        issuer_did = "did:tz:invalid_did",
        status = 2
    )

    issuer_set_status_invalid_status_id = sp.record(
        issuer_did = issuer_did,
        status = 999
    )

    issuer_set_new_owner_valid = sp.record(
        issuer_did = issuer_did,
        new_owner_address = operator_B_address
    )

    # Set and verify setting Issuer as deprecated
    registry_logic_contract.set_issuer_deprecated(sp.record(issuer_did = issuer_did)).run(valid = True, sender = operator_A_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 2)

    # Set and verify setting Issuer as active
    registry_logic_contract.set_issuer_active(sp.record(issuer_did = issuer_did)).run(valid = True, sender = operator_A_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 1)

    # Set Issuer status
    registry_logic_contract.set_issuer_status(issuer_set_status_deprecated_valid).run(valid = True, sender = operator_A_address)

    # Set Issuer data
    registry_logic_contract.set_issuer_data(issuer_update_data_valid).run(valid = True, sender = operator_A_address)
    
    # Verify Issuer status and data setting
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 2)
    scenario.verify(issuer_registry_contract.get(issuer_did).issuer_data == "new_data")

    # FAIL - Sender is not the owner of the Issuer
    registry_logic_contract.set_issuer_status(issuer_set_status_deprecated_valid).run(valid = False, sender = operator_B_address)

    # FAIL - Sender is not the owner of the Issuer
    registry_logic_contract.set_issuer_data(issuer_update_data_valid).run(valid = False, sender = operator_B_address)

    # FAIL - Issuer ID does not exist
    registry_logic_contract.set_issuer_status(issuer_set_status_invalid_did).run(valid = False, sender = operator_A_address)
    
    # FAIL - Status is incorrect
    registry_logic_contract.set_issuer_status(issuer_set_status_invalid_status_id).run(valid = False, sender = operator_A_address)
    
    # FAIL - Sender is not the owner of the Issuer
    registry_logic_contract.set_issuer_owner(issuer_set_new_owner_valid).run(valid = False, sender = operator_B_address)

    # Set and verify new Issuer owner
    registry_logic_contract.set_issuer_owner(issuer_set_new_owner_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).issuer_owner == operator_B_address)

    # FAIL - Sender is not the owner of the Issuer
    registry_logic_contract.set_issuer_owner(issuer_set_new_owner_valid).run(valid = False, sender = operator_A_address)

    bind_issuer_schema_valid = sp.record(
        schema_id = 0,
        issuer_did = issuer_did,
    )

    bind_issuer_schema_invalid_schema_id = sp.record(
        schema_id = 1,
        issuer_did = issuer_did,
    )

    bind_issuer_schema_invalid_issuer_did = sp.record(
        schema_id = 0,
        issuer_did = "did:tz:invalid_did",
    )

    # Bind Issuer to Schema
    registry_logic_contract.bind_issuer_schema(bind_issuer_schema_valid).run(valid = True, sender = operator_B_address)
    
    # FAIL - Sender is not the owner of the Issuer
    registry_logic_contract.bind_issuer_schema(bind_issuer_schema_valid).run(valid = False, sender = operator_A_address)

    # Verify Issuer to Schema binding - Issuer and Schema both exist
    scenario.verify(registry_logic_contract.verify_issuer_schema_binding(bind_issuer_schema_valid) == sp.record(
        binding_exists = True,
        status = 1
    ))

    # Verify Issuer to Schema binding - Issuer exists, Schema does not
    scenario.verify(registry_logic_contract.verify_issuer_schema_binding(bind_issuer_schema_invalid_schema_id) == sp.record(
        binding_exists = False,
        status = 0
    ))

    # Verify Issuer to Schema binding - Issuer and Schema do not exist
    scenario.verify(registry_logic_contract.verify_issuer_schema_binding(bind_issuer_schema_invalid_issuer_did) == sp.record(
        binding_exists = False,
        status = 0
    ))