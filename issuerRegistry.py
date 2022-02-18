# Issuer Registry Contract

import smartpy as sp

class IssuerRegistry(sp.Contract):
    def __init__(self, issuer_did, logic_contract_address):
        self.init_type(
            sp.TRecord(
                mapping = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        issuer_data = sp.TString,
                        status = sp.TString
                    )
                ),
                issuer_did = sp.TString
            )
        )
        self.init(
            issuer_did = issuer_did
        )

    @sp.entry_point
    def add(self, issuer_did, issuer_data):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(issuer_did, sp.TString)
        sp.set_type(issuer_data, sp.TString)
        
    @sp.entry_point
    def revoke(self, issuer_did):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(issuer_did, sp.TString)

    @sp.entry_point
    def get_data(self, issuer_did):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(issuer_did, sp.TString)

@sp.add_test(name = "IssuerRegistry")
def test():
    
    sp.add_compilation_target("issuerRegistry", IssuerRegistry('issuer_did', 'logic_contract_address'))
    