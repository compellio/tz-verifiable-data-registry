# Registry Contract

import smartpy as sp

class Registry(sp.Contract):
    def __init__(self, certifier, logic_contract):
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
        sp.set_type(address, sp.TAddress)

        sp.verify(self.data.certifier == sp.source, message = "Incorrect certifier")
        self.data.logic_contract = address

    @sp.entry_point
    def add_schema(self, schema_data):
        # Defining the parameters' types
        sp.set_type(schema_data, sp.TString)

        # Defining the data that we expect as a return from the Logic contract
        contract_data = sp.TRecord(schema_data = sp.TString)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "add_schema").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            schema_data = schema_data
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_active(self, schema_id):
        sp.set_type(schema_id, sp.TNat)

        contract_data = sp.TRecord(schema_id = sp.TNat)
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_schema_active").open_some()

        params = sp.record(
            schema_id = schema_id,
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_deprecated(self, schema_id):
        sp.set_type(schema_id, sp.TNat)

        contract_data = sp.TRecord(schema_id = sp.TNat)
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_schema_deprecated").open_some()

        params = sp.record(
            schema_id = schema_id,
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_status(self, schema_id, status):
        sp.set_type(schema_id, sp.TNat)
        sp.set_type(status, sp.TNat)

        contract_data = sp.TRecord(schema_id = sp.TNat, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.data.logic_contract, "set_schema_status").open_some()

        params = sp.record(
            schema_id = schema_id,
            status = status
        )

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

@sp.add_test(name = "Registry")
def test():

    sp.add_compilation_target("registry",
        Registry(
            sp.address('tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P'),
            sp.address('KT1HMCMW1GZKJT4B6zmc3DQL6yQ5xZPbVtg4')
        )
    )