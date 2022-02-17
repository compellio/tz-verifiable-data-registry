# Schema Registry Contract

import smartpy as sp

class SchemaRegistry(sp.Contract):
    def __init__(self, schema_id, logic_contract_address):
        self.init_type(
            sp.TRecord(
                mapping = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        schema_data = sp.TRecord(
                            sp.TString,
                            sp.TString
                        ),
                        status = sp.TString
                    )
                ),
                schema_id = sp.TString,
                logic_contract_address = sp.TString
            )
        )

    @sp.entry_point
    def add(self, schema_id, schema_data):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(schema_id, sp.TString)
        sp.set_type(schema_data, sp.TString)
        
    @sp.entry_point
    def revoke(self, schema_id):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(schema_id, sp.TString)

    @sp.entry_point
    def get_data(self, schema_id):
        self.update_initial_storage(mapping = sp.big_map())
        sp.set_type(schema_id, sp.TString)