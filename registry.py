# Registry Contract

import smartpy as sp

class Registry(sp.Contract):
    def __init__(self, certifier):
        self.init_type(
            sp.TRecord(
                contracts = sp.TMap(
                    sp.TString,
                    sp.TAddress
                ),
                certifier = sp.TAddress
            )
        )
        self.init(
            contracts = sp.map(),
            certifier = certifier
        )

    @sp.entry_point
    def update_contract_address(self, contract_name, address):
        sp.set_type(contract_name, sp.TString)
        sp.set_type(address, sp.TAddress)

        sp.verify(self.data.certifier == sp.source, message = "Incorrect certifier")
        self.data.contracts[contract_name] = address

    def get_last_active_version(self, contract_name):
        return self.data.contracts[contract_name]

    @sp.entry_point
    def add_schema(self, schema_id, schema_data):
        sp.set_type(schema_id, sp.TString)
        sp.set_type(schema_data, sp.TString)

        contract_data = sp.TRecord(schema_id = sp.TString, schema_data = sp.TString)
        logic_contract = sp.contract(contract_data, self.get_last_active_version('schema_registry_contract'), "add").open_some()
        
        params = sp.record(
            schema_id = schema_id,
            schema_data = schema_data
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def get_schema(self, schema_id):
        sp.set_type(schema_id, sp.TString)
        
        contract_address = sp.local("contract_address", self.get_last_active_version('schema_registry_contract'))
        schema = sp.view("get", contract_address.value, schema_id, t = sp.TString).open_some("Invalid view");
        sp.result(schema)

    @sp.entry_point
    def add_issuer(self, issuer_data):
        sp.set_type(issuer_data, sp.TString)

        issuer_did = sp.source
        contract_data = sp.TRecord(issuer_did = sp.TAddress, issuer_data = sp.TString)
        logic_contract = sp.contract(contract_data, self.get_last_active_version('issuer_registry_contract'), "add").open_some()
        
        params = sp.record(
            issuer_did = issuer_did,
            issuer_data = issuer_data
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def get_issuer(self, issuer_did):
        sp.set_type(issuer_did, sp.TString)
        
        contract_address = sp.local("contract_address", self.get_last_active_version('issuer_registry_contract'))
        issuer = sp.view("get", contract_address.value, issuer_did, t = sp.TString).open_some("Invalid view");
        sp.result(issuer)

@sp.add_test(name = "Registry")
def test():

    sp.add_compilation_target("registry",
        Registry(
            sp.address('tz1PvnsRQsdhfEUFdFg6Z4CQpeDhWbXEDswm')
        )
    )