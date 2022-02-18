# Issuer Schema Mapping Logic Contract

import smartpy as sp

class IssuerSchemaMappingLogic(sp.Contract):
    def __init__(self, issuer_id):
        self.init_type(
            sp.TRecord(
                issuer_id = sp.TString
            )
        )

    @sp.entry_point
    def bind(self, issuer_id, schema_id):
        sp.set_type(issuer_id, sp.TString)
        sp.set_type(schema_id, sp.TString)
        
    @sp.entry_point
    def revoke(self, issuer_id, schema_id):
        sp.set_type(issuer_id, sp.TString)
        sp.set_type(schema_id, sp.TString)

    @sp.entry_point
    def is_owner(self, issuer_id, schema_id):
        sp.set_type(issuer_id, sp.TString)
        sp.set_type(schema_id, sp.TString)

@sp.add_test(name = "IssuerSchemaMappingLogic")
def test():
    
    sp.add_compilation_target("issuerSchemaMappingLogic", IssuerSchemaMappingLogic('issuer_id'))