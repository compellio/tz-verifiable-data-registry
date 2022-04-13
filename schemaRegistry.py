# Schema Registry Contract

import smartpy as sp

class SchemaRegistry(sp.Contract):
    def __init__(self, logic_contract_address, certifier):
        self.init_type(
            sp.TRecord(
                schema_map = sp.TBigMap(
                    sp.TNat,
                    sp.TRecord(
                        schema_data = sp.TString,
                        schema_owner = sp.TAddress,
                        status = sp.TNat
                    )
                ),
                schema_last_id = sp.TNat,
                logic_contract_address = sp.TAddress,
                certifier = sp.TAddress
            )
        )
        self.init(
            schema_map = sp.big_map(),
            schema_last_id = 0,
            logic_contract_address = logic_contract_address,
            certifier = certifier
        )

    @sp.entry_point
    def add(self, parameters):
        self.data.schema_map[self.data.schema_last_id] = parameters
        self.data.schema_last_id += 1
    
    @sp.onchain_view()
    def get(self, schema_id):
        sp.result(self.data.schema_map[schema_id])
        
    @sp.entry_point
    def revoke(self, schema_id):
        self.update_initial_storage(schema_map = sp.big_map())
        sp.set_type(schema_id, sp.TString)

    @sp.entry_point
    def change_logic_contract_address(self, new_logic_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")
        
        self.data.logic_contract_address = new_logic_contract_address

@sp.add_test(name = "SchemaRegistry")
def test():
    scenario = sp.test_scenario()

    logic_address = sp.address('KT1KsrohW6ZZ1Uj2BjzvBcmKDwx8AS3GY2A3')
    wallet_address = sp.test_account("Valid").address
    nonvalid_address = sp.test_account("NonValid").address

    test_record = sp.record(
        schema_id = "test_id",
        schema_data = "Test",
        status = 1
    )

    c1 = SchemaRegistry(
        logic_address,
        wallet_address
    )

    scenario += c1

    sp.add_compilation_target("schemaRegistry",
        SchemaRegistry(
            sp.address('KT1KsrohW6ZZ1Uj2BjzvBcmKDwx8AS3GY2A3'),
            sp.address('tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P')
        )
    )
