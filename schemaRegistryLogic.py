# Schema Registry Logic Contract

import smartpy as sp

class SchemaRegistryLogic(sp.Contract):
    def __init__(self):
        self.init();

    @sp.entry_point
    def add(self, input_data):
        sp.set_type(input_data.schema_id, sp.TString)
        sp.set_type(input_data.schema_data, sp.TString)
        
        output_data = sp.record(
            schema_id = input_data.schema_id,
            schema_data = input_data.schema_data,
            status = sp.bool(True)
        )

        sp.transfer(output_data, sp.mutez(0), input_data.contract)
    
    @sp.entry_point
    def revoke(self, schema_id):
        sp.set_type(schema_id, sp.TString)

@sp.add_test(name = "SchemaRegistryLogic")
def test():
    
    sp.add_compilation_target("schemaRegistryLogic", SchemaRegistryLogic())