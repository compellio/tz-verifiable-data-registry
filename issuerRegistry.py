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
        # Verifying whether the caller address is our Registry contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        self.data.issuer_map[parameters.issuer_did] = parameters

    @sp.entry_point
    def change_data(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.issuer_data, sp.TString)

        # Verifying whether the caller address is our Registry contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        issuer_data = self.data.issuer_map[parameters.issuer_did]
        
        with sp.modify_record(issuer_data, "data") as data:
            data.issuer_data = parameters.issuer_data

        self.data.issuer_map[parameters.issuer_did] = issuer_data

    @sp.entry_point
    def change_status(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.status, sp.TNat)

        # Verifying whether the caller address is our Registry contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        issuer_data = self.data.issuer_map[parameters.issuer_did]
        
        with sp.modify_record(issuer_data, "data") as data:
            data.status = parameters.status

        self.data.issuer_map[parameters.issuer_did] = issuer_data

    @sp.entry_point
    def change_owner(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.new_owner_address, sp.TAddress)

        # Verifying whether the caller address is our Registry contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        issuer_data = self.data.issuer_map[parameters.issuer_did]
        
        with sp.modify_record(issuer_data, "data") as data:
            data.issuer_owner = parameters.new_owner_address

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

    @sp.onchain_view()
    def issuer_exists(self, issuer_did):
        sp.result(self.data.issuer_map.contains(issuer_did))

    @sp.entry_point
    def change_logic_contract_address(self, new_logic_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")
        
        self.data.logic_contract_address = new_logic_contract_address

@sp.add_test(name = "IssuerRegistry")
def test():
    sp.add_compilation_target("issuerRegistry",
        IssuerRegistry(
            sp.address('KT1_contract_address'),
            sp.address('tz1_certifier_address')
        )
    )
