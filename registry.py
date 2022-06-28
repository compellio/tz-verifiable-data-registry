# Registry Contract

import smartpy as sp

class Registry(sp.Contract):
    def __init__(self, logic_contract, certifier):
        self.init_type(
            sp.TRecord(
                logic_contract = sp.TAddress,
                certifier = sp.TAddress
            )
        )
        self.init(
            logic_contract = logic_contract,
            certifier = certifier
        )

    @sp.entry_point
    def update_logic_contract_address(self, address):
        # Defining the parameters' types
        sp.set_type(address, sp.TAddress)

        sp.verify(self.data.certifier == sp.source, message = "Incorrect certifier")
        self.data.logic_contract = address

    @sp.entry_point
    def add_schema(self, schema_data):
        # Defining the parameters' types
        sp.set_type(schema_data, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(schema_data = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "add_schema").open_some()
        
        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            schema_data = schema_data
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_active(self, schema_id):
        # Defining the parameters' types
        sp.set_type(schema_id, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(schema_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_schema_active").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            schema_id = schema_id,
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_deprecated(self, schema_id):
        # Defining the parameters' types
        sp.set_type(schema_id, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(schema_id = sp.TNat)
        
        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_schema_deprecated").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            schema_id = schema_id,
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_status(self, schema_id, status):
        # Defining the parameters' types
        sp.set_type(schema_id, sp.TNat)
        sp.set_type(status, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(schema_id = sp.TNat, status = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_schema_status").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            schema_id = schema_id,
            status = status
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def get_schema(self, schema_id):
        # Defining the parameters' types
        sp.set_type(schema_id, sp.TNat)
        
        # Defining the parameters' types
        schema = sp.view(
            "get_schema",
            self.data.logic_contract,
            schema_id,
            t = sp.TRecord(
                schema_data = sp.TString,
                status = sp.TString
            )
        ).open_some("Invalid view");
        
        sp.result(schema)
    
    @sp.entry_point
    def add_issuer(self, issuer_did, issuer_data):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(issuer_data, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, issuer_data = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "add_issuer").open_some()
        
        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            issuer_data = issuer_data
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_data(self, issuer_did, issuer_data):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(issuer_data, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, issuer_data = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_data").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            issuer_data = issuer_data
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_active(self, issuer_did):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_active").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_deprecated(self, issuer_did):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_deprecated").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_status(self, issuer_did, status):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(status, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, status = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_status").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            status = status
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_owner(self, issuer_did, owner_address):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(owner_address, sp.TAddress)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, owner_address = sp.TAddress)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_status").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            owner_address = owner_address
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def get_issuer(self, issuer_did):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        
        # Defining the parameters' types
        issuer = sp.view(
            "get_issuer",
            self.data.logic_contract,
            issuer_did,
            t = sp.TRecord(
                issuer_did  = sp.TString,
                issuer_data = sp.TString,
                status = sp.TString
            )
        ).open_some("Invalid view");
        
        sp.result(issuer)

    @sp.entry_point
    def bind_issuer_schema(self, issuer_did, schema_id):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(schema_id, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, schema_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "bind_issuer_schema").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            schema_id = schema_id
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_schema_binding_active(self, issuer_did, schema_id):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(schema_id, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, schema_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_schema_binding_active").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            schema_id = sp.TNat
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_schema_binding_deprecated(self, issuer_did, schema_id):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(schema_id, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, schema_id = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_schema_binding_deprecated").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            schema_id = sp.TNat
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_schema_binding_status(self, issuer_did, schema_id, status):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(schema_id, sp.TNat)
        sp.set_type(status, sp.TNat)

        # Defining the data expected by the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, schema_id = sp.TNat, status = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_issuer_schema_binding_status").open_some()

        # Defining the parameters that will be passed to the Logic contract
        params = sp.record(
            issuer_did = issuer_did,
            schema_id = sp.TNat,
            status = sp.TNat
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def verify_issuer_schema_binding(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.schema_id, sp.TNat)

        issuer_did = parameters.issuer_did
        schema_id = parameters.schema_id
        binding_record = sp.record(
            issuer_did = issuer_did,
            schema_id = schema_id
        )

        # Defining the parameters' types
        binding_result = sp.view(
            "verify_issuer_schema_binding",
            self.data.logic_contract,
            binding_record,
            t = sp.TRecord(
                binding_exists = sp.TBool,
                status = sp.TNat
            )
        ).open_some("Invalid view");
        
        sp.result(binding_result)

@sp.add_test(name = "Registry")
def test():

    sp.add_compilation_target("registry",
        Registry(
            sp.address('KT1_contract_address'),
            sp.address('tz1_certifier_address')
        )
    )