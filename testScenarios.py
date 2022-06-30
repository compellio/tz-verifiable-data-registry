# Test Scenarios

import smartpy as sp

@sp.add_test(name = "TestScripts")
def test():
    REGISTRY_LOGIC = sp.io.import_stored_contract("registryLogic.py")
    ISSUER_REGISTRY = sp.io.import_stored_contract("issuerRegistry.py")
    SCHEMA_REGISTRY = sp.io.import_stored_contract("schemaRegistry.py")
    certifier = sp.test_account("Certifier")
    operator_A = sp.test_account("Operator_A")
    operator_B = sp.test_account("Operator_B")

    certifier_address = certifier.address
    operator_A_address = operator_A.address
    operator_B_address = operator_B.address

    scenario = sp.test_scenario()
    scenario.h1("Preparation")
    scenario.table_of_contents()

    scenario.h2("Accounts")
    scenario.show([certifier, operator_A, operator_B])

    scenario.h2("Contracts List")

    # Registry Logic Contract Instantiation

    scenario.h3("Registry Logic contract")

    registry_logic_contract = REGISTRY_LOGIC.RegistryLogic(
        certifier_address
    )

    scenario += registry_logic_contract

    # Issuer Registry contract instantiation

    scenario.h3("Issuer Registry contract")

    issuer_registry_contract = ISSUER_REGISTRY.IssuerRegistry(
        registry_logic_contract.address,
        certifier_address
    )

    scenario += issuer_registry_contract

    # Schema Registry contract instantiation

    scenario.h3("Schema Registry contract")

    schema_registry_contract = SCHEMA_REGISTRY.SchemaRegistry(
        registry_logic_contract.address,
        certifier_address
    )

    scenario += schema_registry_contract

    # Updating Registry Logic Contract with addresses of instantiated storage contracts

    scenario.h2("Updating Registry Logic contract storage")

    issuer_contract_record = sp.record(
        contract_name = "issuer_registry_contract",
        address = issuer_registry_contract.address
    )

    schema_contract_record = sp.record(
        contract_name = "schema_registry_contract",
        address = schema_registry_contract.address
    )

    scenario.h3("Setting Issuer Registry contract address")
    registry_logic_contract.update_contract_address(issuer_contract_record).run(valid = True, sender = certifier_address)

    scenario.h3("Setting Issuer Schema contract address")
    registry_logic_contract.update_contract_address(schema_contract_record).run(valid = True, sender = certifier_address)

    scenario.verify(registry_logic_contract.data.contracts["issuer_registry_contract"] == issuer_registry_contract.address)
    scenario.verify(registry_logic_contract.data.contracts["schema_registry_contract"] == schema_registry_contract.address)

    scenario.h1("Testing")
    
    # Creating a new Schema
    scenario.h2("Schema")

    schema = sp.record(
        schema_data = "schema_data",
    )

    # Add Schema
    scenario.h3("Adding a Schema")
    registry_logic_contract.add_schema(schema).run(valid = True, sender = operator_A_address)

    # Check Schema addition on Schema Registry contract view
    scenario.verify(schema_registry_contract.get(0).schema_owner == operator_A_address)

    # Check Schema addition on Registry Logic contract view
    scenario.verify(registry_logic_contract.get_schema(0).schema_data == "schema_data")

    # Updating the status of Schema
    scenario.h3("Updating Schema Status")

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

    scenario.show([schema_set_status_deprecated_valid, schema_set_status_invalid_id, schema_set_status_invalid_status_id], stripStrings = True)

    # Set and verify setting Schema as deprecated
    scenario.h4("Setting Schema as deprecated")
    registry_logic_contract.set_schema_deprecated(sp.record(schema_id = 0)).run(valid = True, sender = operator_A_address)
    scenario.verify(schema_registry_contract.get(0).status == 2)

    # Set and verify setting Schema as active
    scenario.h4("Setting Schema as active")
    registry_logic_contract.set_schema_active(sp.record(schema_id = 0)).run(valid = True, sender = operator_A_address)
    scenario.verify(schema_registry_contract.get(0).status == 1)

    # Set and verify setting Schema status
    scenario.h4("Setting Schema status")
    registry_logic_contract.set_schema_status(schema_set_status_deprecated_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(schema_registry_contract.get(0).status == 2)

    # FAIL - Sender is not the owner of the Schema
    scenario.h4("FAIL - Setting Schema status, non-valid Operator")
    registry_logic_contract.set_schema_status(schema_set_status_deprecated_valid).run(valid = False, sender = operator_B_address)

    # FAIL - Schema ID does not exist
    scenario.h4("FAIL - Setting Schema status, non-valid Schema ID")
    registry_logic_contract.set_schema_status(schema_set_status_invalid_id).run(valid = False, sender = operator_A_address)
    
    # FAIL - Status is incorrect
    scenario.h4("FAIL - Setting Schema status, non-valid status ID")
    registry_logic_contract.set_schema_status(schema_set_status_invalid_status_id).run(valid = False, sender = operator_A_address)

    # Creating a new Issuer
    scenario.h2("Issuer")

    issuer_did = "did:tz:test_did"

    issuer = sp.record(
        issuer_did = issuer_did,
        issuer_data = "issuer_data",
    )

    scenario.h3("Adding an Issuer")

    # Add Issuer
    scenario.h4("Adding an Issuer with a valid DID")
    registry_logic_contract.add_issuer(issuer).run(valid = True, sender = operator_A_address)

    # Check Issuer addition on Issuer Registry contract view
    scenario.verify(issuer_registry_contract.get(issuer_did).issuer_owner == operator_A_address)

    # Check Issuer addition on Registry Logic contract view
    scenario.verify(registry_logic_contract.get_issuer(issuer_did).issuer_data == "issuer_data")

    # FAIL - Issuer DID already exists
    scenario.h4("FAIL - Adding an Issuer, DID already exits")
    registry_logic_contract.add_issuer(issuer).run(valid = False, sender = operator_A_address)

    # Updating the Issuer status
    scenario.h3("Updating Issuer status")

    issuer_set_status_deprecated_valid = sp.record(
        issuer_did = issuer_did,
        status = 2
    )

    issuer_set_status_in_conflict_valid = sp.record(
        issuer_did = issuer_did,
        status = 3
    )

    issuer_set_status_invalid_did = sp.record(
        issuer_did = "did:tz:invalid_did",
        status = 2
    )

    issuer_set_status_invalid_status_id = sp.record(
        issuer_did = issuer_did,
        status = 999
    )

    scenario.show([
        issuer_set_status_deprecated_valid,
        issuer_set_status_in_conflict_valid,
        issuer_set_status_invalid_did,
        issuer_set_status_invalid_status_id,
    ], stripStrings = True)

    # Set and verify setting Issuer as deprecated
    scenario.h4("Setting Issuer status as deprecated")
    registry_logic_contract.set_issuer_deprecated(sp.record(issuer_did = issuer_did)).run(valid = True, sender = operator_A_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 2)

    # Set and verify setting Issuer as active
    scenario.h4("Setting Issuer status as active")
    registry_logic_contract.set_issuer_active(sp.record(issuer_did = issuer_did)).run(valid = True, sender = operator_A_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 1)

    # Set Issuer status
    scenario.h4("Setting Issuer status")
    registry_logic_contract.set_issuer_status(issuer_set_status_deprecated_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 2)

    # FAIL - Sender is not the owner of the Issuer
    scenario.h4("FAIL - Setting Issuer status, non-valid Operator")
    registry_logic_contract.set_issuer_status(issuer_set_status_deprecated_valid).run(valid = False, sender = operator_B_address)

    # FAIL - Issuer ID does not exist
    scenario.h4("FAIL - Setting Issuer status, Issuer ID does not exist")
    registry_logic_contract.set_issuer_status(issuer_set_status_invalid_did).run(valid = False, sender = operator_A_address)
    
    # FAIL - Status is incorrect
    scenario.h4("FAIL - Setting Issuer status, status ID does not exist")
    registry_logic_contract.set_issuer_status(issuer_set_status_invalid_status_id).run(valid = False, sender = operator_A_address)

    # Updating the Issuer data
    scenario.h3("Updating Issuer data")

    issuer_update_data_valid = sp.record(
        issuer_did = issuer_did,
        issuer_data = "new_data"
    )

    # Set Issuer data
    scenario.h4("Setting Issuer data")
    registry_logic_contract.set_issuer_data(issuer_update_data_valid).run(valid = True, sender = operator_A_address)
    
    # Verify Issuer status and data setting
    scenario.verify(issuer_registry_contract.get(issuer_did).issuer_data == "new_data")

    # FAIL - Sender is not the owner of the Issuer
    scenario.h4("FAIL - Setting Issuer data, Operator is not the owner of the Issuer")
    registry_logic_contract.set_issuer_data(issuer_update_data_valid).run(valid = False, sender = operator_B_address)
    
    # Updating the Issuer owner
    scenario.h3("Updating Issuer owner")

    issuer_set_new_owner_A_valid = sp.record(
        issuer_did = issuer_did,
        new_owner_address = operator_A_address
    )

    issuer_set_new_owner_B_valid = sp.record(
        issuer_did = issuer_did,
        new_owner_address = operator_B_address
    )

    scenario.show([
        issuer_set_new_owner_A_valid,
        issuer_set_new_owner_B_valid,
    ], stripStrings = True)

    # Set and verify new Issuer owner
    scenario.h4("Setting Issuer owner, Issuer owner operator")

    registry_logic_contract.set_issuer_owner(issuer_set_new_owner_B_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).issuer_owner == operator_B_address)

    scenario.h4("Setting Issuer owner, Certifier operator")
    registry_logic_contract.set_issuer_owner(issuer_set_new_owner_A_valid).run(valid = True, sender = certifier_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).issuer_owner == operator_A_address)

    # FAIL - Sender is not the owner of the Issuer
    scenario.h4("FAIL - Setting Issuer owner, non-valid Operator")
    registry_logic_contract.set_issuer_owner(issuer_set_new_owner_B_valid).run(valid = False, sender = operator_B_address)

    # Setting an Issuer as "In conflict"
    scenario.h3("Setting Issuer status as \"In conflict\"")

    # FAIL - Only administrator can set Issuer status "In conflict"
    scenario.h4("FAIL - Setting Issuer status as \"In conflict\", non-Certifier operator")
    registry_logic_contract.set_issuer_status(issuer_set_status_in_conflict_valid).run(valid = False, sender = operator_A_address)

    # Set Issuer status "In conflict" as Certifier
    scenario.h4("Setting Issuer status as \"In conflict\"")
    registry_logic_contract.set_issuer_status(issuer_set_status_in_conflict_valid).run(valid = True, sender = certifier_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 3)

    # FAIL - Only administrator can set Issuer status when current status is "In Conflict"
    scenario.h4("FAIL - Setting Issuer as deprecated, Current status \"In conflict\", no status changes allowed by non-Certifier operators")
    registry_logic_contract.set_issuer_active(sp.record(issuer_did = issuer_did)).run(valid = False, sender = operator_A_address)

    # FAIL - Only administrator can set Issuer status when current status is "In Conflict"
    scenario.h4("FAIL - Setting Issuer as active, Current status \"In conflict\", no status changes allowed by non-Certifier operators")
    registry_logic_contract.set_issuer_deprecated(sp.record(issuer_did = issuer_did)).run(valid = False, sender = operator_A_address)

    # Set Issuer status "Active" as Certifier
    scenario.h4("Setting Issuer status as active, when current status is \"In conflict\", Certifier operator")
    registry_logic_contract.set_issuer_active(sp.record(issuer_did = issuer_did)).run(valid = True, sender = certifier_address)
    scenario.verify(issuer_registry_contract.get(issuer_did).status == 1)

    # Issuer-Schema binding
    scenario.h2("Issuer-Schema binding")
    scenario.h3("Creating an Issuer-Schema binding")

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

    scenario.show([
        bind_issuer_schema_valid,
        bind_issuer_schema_invalid_schema_id,
        bind_issuer_schema_invalid_issuer_did,
    ], stripStrings = True)

    # Bind Issuer to Schema
    scenario.h4("Bind Schema to Issuer")
    registry_logic_contract.bind_issuer_schema(bind_issuer_schema_valid).run(valid = True, sender = operator_A_address)
    
    # FAIL - Sender is not the owner of the Issuer
    scenario.h4("FAIL - Bind Schema to Issuer, non-valid operator")
    registry_logic_contract.bind_issuer_schema(bind_issuer_schema_valid).run(valid = False, sender = operator_B_address)

    # Verify Issuer to Schema binding - Issuer and Schema both exist
    scenario.verify(registry_logic_contract.verify_binding(bind_issuer_schema_valid) == sp.record(
        binding_exists = True,
        status = 1
    ))

    # Verify Issuer to Schema binding - Issuer exists, Schema does not
    scenario.verify(registry_logic_contract.verify_binding(bind_issuer_schema_invalid_schema_id) == sp.record(
        binding_exists = False,
        status = 0
    ))

    # Verify Issuer to Schema binding - Issuer and Schema do not exist
    scenario.verify(registry_logic_contract.verify_binding(bind_issuer_schema_invalid_issuer_did) == sp.record(
        binding_exists = False,
        status = 0
    ))

    scenario.h3("Updating Issuer-Schema binding status")

    set_binding_status_valid = sp.record(
        schema_id = 0,
        issuer_did = issuer_did,
        status = 2
    )

    set_binding_status_invalid = sp.record(
        schema_id = 0,
        issuer_did = issuer_did,
        status = 999
    )

    scenario.show([
        set_binding_status_valid,
        set_binding_status_invalid,
    ], stripStrings = True)

    # Set and verify setting Issuer-Schema binding as deprecated
    scenario.h4("Setting Issuer-Schema binding as deprecated")
    registry_logic_contract.set_binding_deprecated(bind_issuer_schema_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(registry_logic_contract.verify_binding(bind_issuer_schema_valid) == sp.record(
        binding_exists = True,
        status = 2
    ))

    # Set and verify setting Issuer-Schema binding as active
    scenario.h4("Setting Issuer-Schema binding as active")
    registry_logic_contract.set_binding_active(bind_issuer_schema_valid).run(valid = True, sender = operator_A_address)
    scenario.verify(registry_logic_contract.verify_binding(bind_issuer_schema_valid) == sp.record(
        binding_exists = True,
        status = 1
    ))

    # Set Issuer status
    scenario.h4("Setting Issuer-Schema binding status")
    registry_logic_contract.set_binding_status(set_binding_status_valid).run(valid = True, sender = operator_A_address)

    # FAIL - Sender is not the owner of the Issuer
    scenario.h4("FAIL - Setting Issuer-Schema binding status, non-valid operator")
    registry_logic_contract.set_binding_status(set_binding_status_invalid).run(valid = False, sender = operator_B_address)

    # FAIL - Status ID does not exist
    scenario.h4("FAIL - Setting Issuer-Schema binding status, status ID does not exist")
    registry_logic_contract.set_binding_status(set_binding_status_invalid).run(valid = False, sender = operator_A_address)