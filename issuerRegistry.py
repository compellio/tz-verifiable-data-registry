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
         # Defining the parameters' types
        sp.set_type(issuer_did, sp.TAddress)
        sp.set_type(issuer_data, sp.TString)

        # Verifying whether the calller address is our Registry contract
        sp.verify(self.data.registry_contract_address == sp.sender, message = "Incorrect caller")

        # Defining the data of this contract to be passed as a callback
        data = sp.TRecord(issuer_did = sp.TAddress, issuer_data = sp.TString, status = sp.TBool)

        # Defining the data that we expect as a return from the Logic contract
        contract_data = sp.TRecord(contract = sp.TContract(data), issuer_did = sp.TAddress, issuer_data = sp.TString)
        
        # Defining the logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.data.logic_contract_address, "add").open_some()
        
        # Defining the parameters that will be passed to the Logic contract and the callback to this contract
        params = sp.record(
            contract = sp.self_entry_point("store"),
            issuer_did = issuer_did,
            issuer_data = issuer_data
        )

        # Calling the Logic contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)
    
    @sp.entry_point
    def store(self, params):

        # Verifying whether the calller address is our Logic contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")
        
        # Formating the data to be stored
        data = sp.record(
            issuer_data = params.issuer_data,
            status = params.status
        )

        # Storing the data
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
    scenario = sp.test_scenario()
    
    registry_contract_address = sp.address('KT1RTfPB3zYyCq2hZS6ut9tRb7P1KRc1hCCf')
    logic_address = sp.address('KT1P3KZVFRJRWBN9bcxbyEAcuhRwUM5B9i4q')
    wallet_address = sp.test_account("Valid").address
    nonvalid_address = sp.test_account("NonValid").address

    test_record = sp.record(
        issuer_did = wallet_address,
        issuer_data = "Test",
        status = sp.bool(True)
    )

    c1 = IssuerRegistry(
        registry_contract_address,
        logic_address,
        wallet_address
    )

    scenario += c1

    c1.store(test_record).run(valid = False, sender = nonvalid_address)
    c1.store(test_record).run(valid = True, sender = c1.data.logic_contract_address)
    scenario.verify(c1.get(wallet_address) == "Test")

    sp.add_compilation_target("issuerRegistry",
        IssuerRegistry(
            sp.address('KT1RTfPB3zYyCq2hZS6ut9tRb7P1KRc1hCCf'),
            sp.address('KT1P3KZVFRJRWBN9bcxbyEAcuhRwUM5B9i4q'),
            sp.address('tz1PvnsRQsdhfEUFdFg6Z4CQpeDhWbXEDswm')
        )
    )
    