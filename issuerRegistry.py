# Schema Registry Contract

import smartpy as sp

class IssuerRegistry(sp.Contract):
    def __init__(self, logic_contract_address, certifier):
        self.init_type(
            sp.TRecord(
                issuer_map = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        issuer_did = sp.TString,
                        issuer_data = sp.TString,
                        issuer_owner = sp.TAddress,
                        status = sp.TNat
                    )
                ),
                logic_contract_address = sp.TAddress,
                certifier = sp.TAddress
            )
        )
        self.init(
            issuer_map = sp.big_map(),
            logic_contract_address = logic_contract_address,
            certifier = certifier
        )

    @sp.entry_point
    def add(self, parameters):
        self.data.issuer_map[parameters.issuer_did] = parameters

    @sp.entry_point
    def change_status(self, parameters):
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.status, sp.TNat)

        issuer_data = self.data.issuer_map[parameters.issuer_did]
        
        with sp.modify_record(issuer_data, "data") as data:
            data.status = parameters.status

        self.data.issuer_map[parameters.issuer_did] = issuer_data
    
    @sp.onchain_view()
    def get(self, issuer_did):
        sp.result(self.data.issuer_map[issuer_did])

    @sp.onchain_view()
    def get_issuer_owner_address(self, issuer_did):
        sp.result(self.data.issuer_map[issuer_did].issuer_owner)

    @sp.onchain_view()
    def get_issuer_status(self, issuer_did):
        sp.result(self.data.issuer_map[issuer_did].status)

    @sp.entry_point
    def change_logic_contract_address(self, new_logic_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")
        
        self.data.logic_contract_address = new_logic_contract_address

@sp.add_test(name = "IssuerRegistry")
def test():
    scenario = sp.test_scenario()

    logic_address = sp.address('KT1KsrohW6ZZ1Uj2BjzvBcmKDwx8AS3GY2A3')
    wallet_address = sp.test_account("Valid").address
    nonvalid_address = sp.test_account("NonValid").address

    test_add = sp.record(
        issuer_did = "did:tz:test_did",
        issuer_data = "data",
        issuer_owner = sp.address('tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P'),
        status = 1
    )

    test_status = sp.record(
        issuer_did = "did:tz:test_did",
        status = 2
    )

    c1 = IssuerRegistry(
        logic_address,
        wallet_address
    )

    scenario += c1

    c1.add(test_add).run(valid = True, sender = wallet_address)
    scenario.verify(c1.get("did:tz:test_did").issuer_data == "data")
    c1.change_status(test_status).run(valid = True, sender = wallet_address)

    sp.add_compilation_target("issuerRegistry",
        IssuerRegistry(
            sp.address('KT1HP6Nb4WWPEt4VPVFYUpghLb6zjexEx5J3'),
            sp.address('tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P')
        )
    )
