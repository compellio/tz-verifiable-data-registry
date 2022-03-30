# Schema Registry Contract

import smartpy as sp

class SchemaRegistry(sp.Contract):
    def __init__(self, registry_contract_address, logic_contract_address, certifier):
        self.init_type(
            sp.TRecord(
                schema_map = sp.TBigMap(
                    sp.TString,
                    sp.TRecord(
                        schema_data = sp.TString,
                        status = sp.TBool
                    )
                ),
                registry_contract_address = sp.TAddress,
                logic_contract_address = sp.TAddress,
                certifier = sp.TAddress
            )
        )
        self.init(
            schema_map = sp.big_map(),
            registry_contract_address = registry_contract_address,
            logic_contract_address = logic_contract_address,
            certifier = certifier
        )

    @sp.entry_point
    def add(self, schema_id, schema_data):
        sp.set_type(schema_id, sp.TString)
        sp.set_type(schema_data, sp.TString)

        sp.verify(self.data.registry_contract_address == sp.sender, message = "Incorrect caller")

        data = sp.TRecord(schema_id = sp.TString, schema_data = sp.TString, status = sp.TBool)
        contract_data = sp.TRecord(contract = sp.TContract(data), schema_id = sp.TString, schema_data = sp.TString)
        
        logic_contract = sp.contract(contract_data, self.data.logic_contract_address, "add").open_some()
        
        params = sp.record(
            contract = sp.self_entry_point("store"),
            schema_id = schema_id,
            schema_data = schema_data
        )

        sp.transfer(params, sp.mutez(0), logic_contract)
    
    @sp.entry_point
    def store(self, params):
        data = sp.record(
            schema_data = params.schema_data,
            status = params.status
        )

        self.data.schema_map[params.schema_id] = data

    @sp.onchain_view()
    def get(self, schema_id):
        sp.result(self.data.schema_map[schema_id].schema_data)
        
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
    
    sp.add_compilation_target("schemaRegistry",
        SchemaRegistry(
            sp.address('KT1KTnCM9xfy2qYQgXyrgcbGq4SJpnUKeRRB'),
            sp.address('KT1LaMzuwMcNpaApiUqpRErT7GxhPjBXok3j'),
            sp.address('tz1PvnsRQsdhfEUFdFg6Z4CQpeDhWbXEDswm')
        )
    )
