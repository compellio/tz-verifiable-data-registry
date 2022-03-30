# Issuer Registry Logic Contract

import smartpy as sp

class IssuerRegistryLogic(sp.Contract):
    def __init__(self):
        self.init();

    @sp.entry_point
    def add(self, input_data):
        sp.set_type(input_data.issuer_did, sp.TAddress)
        sp.set_type(input_data.issuer_data, sp.TString)
        
        output_data = sp.record(
            issuer_did = input_data.issuer_did,
            issuer_data = input_data.issuer_data,
            status = sp.bool(True)
        )

        sp.transfer(output_data, sp.mutez(0), input_data.contract)
    
    @sp.entry_point
    def revoke(self, issuer_did):
        sp.set_type(issuer_did, sp.TString)

@sp.add_test(name = "IssuerRegistryLogic")
def test():
    
    sp.add_compilation_target("issuerRegistryLogic", IssuerRegistryLogic())