# Registry Contract

import smartpy as sp

class Registry(sp.Contract):
    def __init__(self, address):
        self.init_type(
            sp.TRecord(
                mapping = sp.TMap(
                    sp.TString,
                    sp.TMap(
                        sp.TString,
                        sp.TRecord(
                            contract_address = sp.TString,
                            status = sp.TString
                        )
                    )
                ),
                address = sp.TString
            )
        )
        self.init(
            address = address
        )

    @sp.entry_point
    def update_status(self, contract_name, version, status):
        self.data.mapping[contract_name] = {
            version : sp.record(
                contract_address = self.data.address,
                status = status
            ) 
        }
        
    @sp.entry_point
    def get_last_active_version(self, contract_name):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(contract_name, sp.TString)

    @sp.entry_point
    def add_issuer(self, version, issuer_did, issuer_data):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(issuer_data, sp.TString)

    @sp.entry_point
    def get_issuer(self, version, issuer_did):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(issuer_did, sp.TString)

    @sp.entry_point
    def revoke_issuer(self, version, issuer_did):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(issuer_did, sp.TString)

    @sp.entry_point
    def add_schema(self, version, schema_id, schema):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(schema_id, sp.TString)
        sp.set_type(schema, sp.TString)

    @sp.entry_point
    def get_schema(self, version, schema_id):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(schema_id, sp.TString)

    @sp.entry_point
    def revoke_schema(self, version, issuer_did):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(issuer_did, sp.TString)

    @sp.entry_point
    def set_owner(self, version, issuer_did, schema_id):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(schema_id, sp.TString)

    @sp.entry_point
    def revoke_membership(self, version, issuer_did, schema_id):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(schema_id, sp.TString)

    @sp.entry_point
    def is_allowed(self, version, issuer_did, schema_id):
        self.update_initial_storage(mapping = sp.map())
        sp.set_type(version, sp.TString)
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(schema_id, sp.TString)
    
@sp.add_test(name = "Registry")
def test():
    c1 = Registry('address')
    scenario = sp.test_scenario()
    scenario.h1("Registry")
    scenario += c1
    c1.update_status(contract_name = 'contract_name', version = 'version', status = 'status')
    scenario.verify(c1.data.mapping['contract_name']['version'] == sp.record(contract_address = 'address', status = 'status'))

    sp.add_compilation_target("registry", Registry('address'))