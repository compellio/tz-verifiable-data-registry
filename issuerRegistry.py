# Issuer Registry Contract

import smartpy as sp

class IssuerRegistry(sp.Contract):
    def __init__(self, registry_contract_address, logic_contract_address, certifier):
        self.init_type(
            sp.TRecord(
                issuer_map = sp.TBigMap(
                    sp.TAddress,
                    sp.TRecord(
                        issuer_data = sp.TString,
                        status = sp.TBool
                    )
                ),
                registry_contract_address = sp.TAddress,
                logic_contract_address = sp.TAddress,
                certifier = sp.TAddress
            )
        )
        self.init(
            issuer_map = sp.big_map(),
            registry_contract_address = registry_contract_address,
            logic_contract_address = logic_contract_address,
            certifier = certifier
        )

    @sp.entry_point
    def add(self, issuer_did, issuer_data):
        sp.set_type(issuer_did, sp.TAddress)
        sp.set_type(issuer_data, sp.TString)

        sp.verify(self.data.registry_contract_address == sp.sender, message = "Incorrect caller")

        data = sp.TRecord(issuer_did = sp.TAddress, issuer_data = sp.TString, status = sp.TBool)
        contract_data = sp.TRecord(contract = sp.TContract(data), issuer_did = sp.TAddress, issuer_data = sp.TString)
        
        logic_contract = sp.contract(contract_data, self.data.logic_contract_address, "add").open_some()
        
        params = sp.record(
            contract = sp.self_entry_point("store"),
            issuer_did = issuer_did,
            issuer_data = issuer_data
        )

        sp.transfer(params, sp.mutez(0), logic_contract)
    
    @sp.entry_point
    def store(self, params):
        data = sp.record(
            issuer_data = params.issuer_data,
            status = params.status
        )

        self.data.issuer_map[params.issuer_did] = data

    @sp.onchain_view()
    def get(self, issuer_did):
        sp.result(self.data.issuer_map[issuer_did].issuer_data)
        
    @sp.entry_point
    def revoke(self, issuer_did):
        self.update_initial_storage(issuer_map = sp.big_map())
        sp.set_type(issuer_did, sp.TString)

    @sp.entry_point
    def change_logic_contract_address(self, new_logic_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")
        
        self.data.logic_contract_address = new_logic_contract_address

@sp.add_test(name = "IssuerRegistry")
def test():
    
    sp.add_compilation_target("issuerRegistry",
        IssuerRegistry(
            sp.address('KT1MuadG9MbxSUQaqdUAWaXhJcQfgCwnjJMq'),
            sp.address('KT1P3KZVFRJRWBN9bcxbyEAcuhRwUM5B9i4q'),
            sp.address('tz1PvnsRQsdhfEUFdFg6Z4CQpeDhWbXEDswm')
        )
    )
    