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

    @sp.onchain_view()
    def get_schema(self, schema_id):
        # Defining the parameters' types
        sp.set_type(schema_id, sp.TNat)
        
        # Defining the parameters' types
        contract_address = sp.local("contract_address", self.data.logic_contract)
        schema = sp.view("get_schema", contract_address.value, schema_id, t = sp.TRecord(schema_data = sp.TString, status = sp.TString)).open_some("Invalid view");
        sp.result(schema)

@sp.add_test(name = "Registry")
def test():

    sp.add_compilation_target("registry",
        Registry(
            sp.address('tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P'),
            sp.address('KT1NEoBGaMBwNMRDYZYoRtvTni3mjFN1td3S')
        )
    )