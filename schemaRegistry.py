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
                issuer_schema_map = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        schema_id = sp.TNat,
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
            issuer_schema_map = sp.big_map(),
            schema_last_id = 0,
            logic_contract_address = logic_contract_address,
            certifier = certifier
        )

    @sp.entry_point
    def add(self, parameters):
        # Verifying whether the caller address is our Registry contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        self.data.schema_map[self.data.schema_last_id] = parameters
        self.data.schema_last_id += 1

    @sp.entry_point
    def change_status(self, parameters):
        sp.set_type(parameters.schema_id, sp.TNat)
        sp.set_type(parameters.status, sp.TNat)

        # Verifying whether the caller address is our Registry contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        schema_data = self.data.schema_map[parameters.schema_id]
        
        with sp.modify_record(schema_data, "data") as data:
            data.status = parameters.status

        self.data.schema_map[parameters.schema_id] = schema_data

    @sp.entry_point
    def bind_issuer_schema(self, parameters):
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.schema_binding, sp.TRecord( schema_id = sp.TNat, status = sp.TNat ))

        # Verifying whether the caller address is our Registry contract
        sp.verify(self.data.logic_contract_address == sp.sender, message = "Incorrect caller")

        self.data.issuer_schema_map[parameters.issuer_did] = parameters.schema_binding
        
    @sp.onchain_view()
    def get(self, schema_id):
        sp.result(self.data.schema_map[schema_id])

    @sp.onchain_view()
    def get_schema_owner_address(self, schema_id):
        sp.result(self.data.schema_map[schema_id].schema_owner)

    @sp.entry_point
    def change_logic_contract_address(self, new_logic_contract_address):
        with sp.if_(self.data.certifier != sp.source):
            sp.failwith("Incorrect certifier")
        
        self.data.logic_contract_address = new_logic_contract_address

@sp.add_test(name = "SchemaRegistry")
def test():
    sp.add_compilation_target("schemaRegistry",
        SchemaRegistry(
            sp.address('KT1MWPUKoU4FUVr1nBA4cwjMSoSsxqE3x9kc'),
            sp.address('tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P')
        )
    )
