# Registry Contract

import smartpy as sp

class RegistryLogic(sp.Contract):
    def __init__(self, certifier):
        self.init_type(
            sp.TRecord(
                contracts = sp.TBigMap(
                    sp.TString,
                    sp.TAddress
                ),
                issuer_statuses = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
                schema_statuses = sp.TBigMap(
                    sp.TNat,
                    sp.TString
                ),
                certifier = sp.TAddress
            )
        )
        self.init(
            contracts = sp.big_map(),
            issuer_statuses = sp.big_map({
                1: "active",
                2: "deprecated",
                3: "in_conflict"
            }),
            schema_statuses = sp.big_map({
                1: "active",
                2: "deprecated"
            }),
            certifier = certifier
        )

    @sp.entry_point
    def update_contract_address(self, parameters):
        sp.set_type(parameters.contract_name, sp.TString)
        sp.set_type(parameters.address, sp.TAddress)

        sp.verify(self.data.certifier == sp.source, message = "Incorrect certifier")
        self.data.contracts[parameters.contract_name] = parameters.address

    def get_contract_address(self, contract_name):
        return self.data.contracts[contract_name]

    @sp.entry_point
    def add_schema(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.schema_data, sp.TString)

        # Defining the data that we expect as a return from the Logic contract
        contract_data = sp.TRecord(schema_data = sp.TString, schema_owner = sp.TAddress, status = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.get_contract_address('schema_registry_contract'), "add").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            schema_data = parameters.schema_data,
            schema_owner = sp.source,
            status = 1
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    def verify_owner_source_address(self, owner):
        sp.set_type(owner, sp.TAddress)
        return owner == sp.source

    def get_schema_owner_address(self, schema_id):
        schema_owner_address = sp.view(
            "get_schema_owner_address",
            self.get_contract_address('schema_registry_contract'),
            schema_id,
            t = sp.TAddress
        ).open_some("Invalid view");

        return schema_owner_address

    @sp.entry_point
    def set_schema_active(self, parameters):
        sp.set_type(parameters.schema_id, sp.TNat)

        owner_address = self.get_schema_owner_address(parameters.schema_id)
        sp.verify(self.verify_owner_source_address(owner_address), message = "Incorrect owner")

        contract_data = sp.TRecord(schema_id = sp.TNat, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.get_contract_address('schema_registry_contract'), "change_status").open_some()

        params = sp.record(
            schema_id = parameters.schema_id,
            status = 1
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_deprecated(self, parameters):
        sp.set_type(parameters.schema_id, sp.TNat)

        owner_address = self.get_schema_owner_address(parameters.schema_id)
        sp.verify(self.verify_owner_source_address(owner_address), message = "Incorrect owner")

        contract_data = sp.TRecord(schema_id = sp.TNat, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.get_contract_address('schema_registry_contract'), "change_status").open_some()

        params = sp.record(
            schema_id = parameters.schema_id,
            status = 2
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_schema_status(self, parameters):
        sp.set_type(parameters.schema_id, sp.TNat)
        sp.set_type(parameters.status, sp.TNat)

        owner_address = self.get_schema_owner_address(parameters.schema_id)
        sp.verify(self.verify_owner_source_address(owner_address), message = "Incorrect owner")

        contract_data = sp.TRecord(schema_id = sp.TNat, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.get_contract_address('schema_registry_contract'), "change_status").open_some()

        params = sp.record(
            schema_id = parameters.schema_id,
            status = parameters.status
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def get_schema(self, schema_id):
        # Defining the parameters' types
        sp.set_type(schema_id, sp.TNat)
        
        # Defining the parameters' types
        schema = sp.view(
            "get",
            self.get_contract_address('schema_registry_contract'),
            schema_id,
            t = sp.TRecord(
                schema_data = sp.TString,
                schema_owner = sp.TAddress,
                status = sp.TNat
            )
        ).open_some("Invalid view");

        result_schema = sp.record(
            schema_data = schema.schema_data,
            status = self.data.schema_statuses[schema.status]
        )

        sp.result(result_schema)

@sp.add_test(name = "RegistryLogic")
def test():

    sp.add_compilation_target("registryLogic",
        RegistryLogic(
            sp.address('tz1WM1wDM4mdtD3qMiELJSgbB14ZryyHNu7P')
        )
    )