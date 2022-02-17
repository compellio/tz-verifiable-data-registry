# Schema Registry Logic Contract

import smartpy as sp

class SchemaRegistryLogic(sp.Contract):
    def __init__(self, schema_id):
        self.init_type(
            sp.TRecord(
                schema_id = sp.TString
            )
        )

    @sp.entry_point
    def add(self, schema_id, schema_data):
        sp.set_type(schema_id, sp.TString)
        sp.set_type(schema_data, sp.TString)
        
    @sp.entry_point
    def revoke(self, schema_id):
        sp.set_type(schema_id, sp.TString)