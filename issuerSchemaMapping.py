# Issuer Schema Mapping Contract

import smartpy as sp

class IssuerSchemaMapping(sp.Contract):
    def __init__(self, issuer_id, logic_contract_address):
        self.init_type(
            sp.TRecord(
                mapping = sp.TBigMap(
                    sp.TString,
                    sp.TMap(
                        sp.TString,
                        sp.TString
                    )
                ),
                issuer_id = sp.TString,
                logic_contract_address = sp.TString
            )
        )

    @sp.entry_point
    def bind(self, issuer_id, schema_id):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(issuer_id, sp.TString)
        sp.set_type(schema_id, sp.TString)
        
    @sp.entry_point
    def revoke(self, issuer_id, schema_id):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(issuer_id, sp.TString)
        sp.set_type(schema_id, sp.TString)

    @sp.entry_point
    def get_schemas(self, issuer_id):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(issuer_id, sp.TString)
    
    @sp.entry_point
    def is_allowed(self, issuer_id, schema_id):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(issuer_id, sp.TString)
        sp.set_type(schema_id, sp.TString)