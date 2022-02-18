# Issuer Registry Logic Contract

import smartpy as sp

class IssuerRegistryLogic(sp.Contract):
    def __init__(self, issuer_did):
        self.init_type(
            sp.TRecord(
                issuer_did = sp.TString
            )
        )

    @sp.entry_point
    def add(self, issuer_did, issuer_data):
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(issuer_data, sp.TString)
        
    @sp.entry_point
    def revoke(self, issuer_did):
        sp.set_type(issuer_did, sp.TString)

@sp.add_test(name = "IssuerRegistryLogic")
def test():
    
    sp.add_compilation_target("issuerRegistryLogic", IssuerRegistryLogic('issuer_did'))