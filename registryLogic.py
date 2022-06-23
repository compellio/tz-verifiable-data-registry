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
    
    ###########
    # Helpers #
    ###########
    
    def get_contract_address(self, contract_name):
        return self.data.contracts[contract_name]

    @sp.private_lambda(with_storage="read-only")
    def verify_owner_source_address(self, params):
        sp.set_type(params.owner_address, sp.TAddress)

        sp.if (sp.source == self.data.certifier):
            sp.result(True)
        sp.else:
            sp.if (sp.source == params.owner_address):
                sp.result(True)
            sp.else:
                sp.result(False)


    def get_schema_owner_address(self, schema_id):
        schema_owner_address = sp.view(
            "get_schema_owner_address",
            self.get_contract_address('schema_registry_contract'),
            schema_id,
            t = sp.TAddress
        ).open_some("Invalid view");

        return schema_owner_address

    @sp.private_lambda(with_storage="read-only")
    def verify_issuer_status_change_allowed(self, params):
        sp.set_type(params.owner_address, sp.TAddress)
        sp.set_type(params.current_status, sp.TNat)
        sp.set_type(params.new_status, sp.TNat)

        sp.if (sp.source == self.data.certifier) :
            sp.result(True)
        sp.else:
            sp.if ((sp.source == params.owner_address) & (params.current_status != 3) & (params.new_status != 3)):
                sp.result(True)
            sp.else:
                sp.result(False)

    @sp.private_lambda(with_storage="read-only")
    def verify_issuer_update_allowed(self, params):
        sp.set_type(params.owner_address, sp.TAddress)

        sp.if (sp.source == self.data.certifier) :
            sp.result(True)
        sp.else:
            sp.if (sp.source == params.owner_address):
                sp.result(True)
            sp.else:
                sp.result(False)

    def get_issuer_owner_address(self, issuer_did):
        issuer_owner_address = sp.view(
            "get_issuer_owner_address",
            self.get_contract_address('issuer_registry_contract'),
            issuer_did,
            t = sp.TAddress
        ).open_some("Invalid view");

        return issuer_owner_address

    def get_issuer_status(self, issuer_did):
        issuer_status = sp.view(
            "get_issuer_status",
            self.get_contract_address('issuer_registry_contract'),
            issuer_did,
            t = sp.TNat
        ).open_some("Invalid view");

        return issuer_status

    def check_issuer_exists(self, issuer_did):
        issuer_existance = sp.view(
            "issuer_exists",
            self.get_contract_address('issuer_registry_contract'),
            issuer_did,
            t = sp.TBool
        ).open_some("Invalid view");

        return issuer_existance
            
    @sp.entry_point
    def update_contract_address(self, parameters):
        sp.set_type(parameters.contract_name, sp.TString)
        sp.set_type(parameters.address, sp.TAddress)

        sp.verify(self.data.certifier == sp.source, message = "Incorrect certifier")
        self.data.contracts[parameters.contract_name] = parameters.address

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

    @sp.entry_point
    def set_schema_active(self, parameters):
        sp.set_type(parameters.schema_id, sp.TNat)

        owner_address = self.get_schema_owner_address(parameters.schema_id)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

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
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

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
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Incorrect owner")

        contract_data = sp.TRecord(schema_id = sp.TNat, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.get_contract_address('schema_registry_contract'), "change_status").open_some()

        sp.verify(self.data.schema_statuses.contains(parameters.status), message = "Incorrect status")

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

    @sp.entry_point
    def add_issuer(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.issuer_data, sp.TString)

        # Check if issuer does not exist, does not allow add call otherwise
        # This is to avoid update from unauthorized
        sp.verify(~self.check_issuer_exists(parameters.issuer_did), message = "Issuer did already exists")

        # Defining the data that we expect as a return from the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, issuer_data = sp.TString, issuer_owner = sp.TAddress, status = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.get_contract_address('issuer_registry_contract'), "add").open_some()
        
        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            issuer_did = parameters.issuer_did,
            issuer_data = parameters.issuer_data,
            issuer_owner = sp.source,
            status = 1
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)


    @sp.entry_point
    def set_issuer_data(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.issuer_data, sp.TString)

        # Check if issuer exists, does not allow call otherwise
        sp.verify(self.check_issuer_exists(parameters.issuer_did), message = "Issuer did does not exist")

        #update is allowed only from owner
        owner_address = self.get_issuer_owner_address(parameters.issuer_did)
        sp.verify(self.verify_issuer_update_allowed(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Cannot be called from non-certified addresses")

        # Defining the data that we expect as a return from the Logic contract
        contract_data = sp.TRecord(issuer_did = sp.TString, issuer_data = sp.TString, issuer_owner = sp.TAddress, status = sp.TNat)

        # Defining the Logic contract itself and its entry point for the call
        logic_contract = sp.contract(contract_data, self.get_contract_address('issuer_registry_contract'),
            "update").open_some()

        # Defining the parameters that will be passed to the Storage contract
        params = sp.record(
            issuer_did = parameters.issuer_did,
            issuer_data = parameters.issuer_data,
            issuer_owner = sp.source,
            status = 1
        )

        # Calling the Storage contract with the parameters we defined
        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_active(self, parameters):
        sp.set_type(parameters.issuer_did, sp.TString)

        owner_address = self.get_issuer_owner_address(parameters.issuer_did)
        current_issuer_status = self.get_issuer_status(parameters.issuer_did)
        
        sp.verify(self.verify_issuer_status_change_allowed(
            sp.record(
                owner_address = owner_address,
                current_status = current_issuer_status,
                new_status = 1
            )
        ), message = "Status change not allowed")

        contract_data = sp.TRecord(issuer_did = sp.TString, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.get_contract_address('issuer_registry_contract'), "change_status").open_some()

        params = sp.record(
            issuer_did = parameters.issuer_did,
            status = 1
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_deprecated(self, parameters):
        sp.set_type(parameters.issuer_did, sp.TString)

        owner_address = self.get_issuer_owner_address(parameters.issuer_did)
        current_issuer_status = self.get_issuer_status(parameters.issuer_did)
        
        sp.verify(self.verify_issuer_status_change_allowed(
            sp.record(
                owner_address = owner_address,
                current_status = current_issuer_status,
                new_status = 2
            )
        ), message = "Status change not allowed")

        contract_data = sp.TRecord(issuer_did = sp.TString, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.get_contract_address('issuer_registry_contract'), "change_status").open_some()

        params = sp.record(
            issuer_did = parameters.issuer_did,
            status = 2
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_status(self, parameters):
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.status, sp.TNat)

        owner_address = self.get_issuer_owner_address(parameters.issuer_did)
        current_issuer_status = self.get_issuer_status(parameters.issuer_did)

        sp.verify(self.verify_issuer_status_change_allowed(
            sp.record(
                owner_address = owner_address,
                current_status = current_issuer_status,
                new_status = parameters.status
            )
        ), message = "Status change not allowed")
        
        contract_data = sp.TRecord(issuer_did = sp.TString, status = sp.TNat)
        logic_contract = sp.contract(contract_data, self.get_contract_address('issuer_registry_contract'), "change_status").open_some()

        sp.verify(self.data.issuer_statuses.contains(parameters.status), message = "Incorrect status")

        params = sp.record(
            issuer_did = parameters.issuer_did,
            status = parameters.status
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.entry_point
    def set_issuer_owner(self, parameters):
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.new_owner_address, sp.TAddress)

        owner_address = self.get_issuer_owner_address(parameters.issuer_did)
        sp.verify(self.verify_issuer_update_allowed(
            sp.record(
                owner_address = owner_address,
            )
        ), message = "Cannot be called from non-certified addresses")

        contract_data = sp.TRecord(issuer_did = sp.TString, new_owner_address = sp.TAddress)
        logic_contract = sp.contract(contract_data, self.get_contract_address('issuer_registry_contract'), "change_owner").open_some()

        params = sp.record(
            issuer_did = parameters.issuer_did,
            new_owner_address = parameters.new_owner_address
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def get_issuer(self, issuer_did):
        # Defining the parameters' types
        sp.set_type(issuer_did, sp.TString)
        
        # Defining the parameters' types
        issuer = sp.view(
            "get",
            self.get_contract_address('issuer_registry_contract'),
            issuer_did,
            t = sp.TRecord(
                issuer_did = sp.TString,
                issuer_data = sp.TString,
                issuer_owner = sp.TAddress,
                status = sp.TNat
            )
        ).open_some("Invalid view");

        result_issuer = sp.record(
            issuer_data = issuer.issuer_data,
            status = self.data.issuer_statuses[issuer.status]
        )

        sp.result(result_issuer)

    @sp.entry_point
    def bind_issuer_schema(self, parameters):
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.schema_id, sp.TNat)
        
        sp.verify(self.check_issuer_exists(parameters.issuer_did), message = "Issuer did does not exist")
        
        owner_address = self.get_issuer_owner_address(parameters.issuer_did)
        sp.verify(self.verify_owner_source_address(
            sp.record(
                owner_address=owner_address,
            )
        ), message = "Binding not allowed")

        contract_data = sp.TRecord(issuer_did = sp.TString, schema_binding = sp.TRecord( schema_id = sp.TNat, status = sp.TNat ))
        logic_contract = sp.contract(contract_data, self.get_contract_address('schema_registry_contract'), "bind_issuer_schema").open_some()

        params = sp.record(
            issuer_did = parameters.issuer_did,
            schema_binding = sp.record(
                schema_id = parameters.schema_id,
                status = 1
            )
        )

        sp.transfer(params, sp.mutez(0), logic_contract)

    @sp.onchain_view()
    def verify_issuer_schema_binding(self, parameters):
        # Defining the parameters' types
        sp.set_type(parameters.issuer_did, sp.TString)
        sp.set_type(parameters.schema_id, sp.TNat)

        issuer_did = parameters.issuer_did
        schema_id = parameters.schema_id
        binding_record = sp.record(
            issuer_did = issuer_did,
            schema_id = schema_id
        )

        # Defining the parameters' types
        binding_result = sp.view(
            "verify_issuer_schema_binding",
            self.get_contract_address('schema_registry_contract'),
            binding_record,
            t = sp.TRecord(
                binding_exists = sp.TBool,
                status = sp.TNat
            )
        ).open_some("Invalid view");

        sp.result(binding_result)

@sp.add_test(name = "RegistryLogic")
def test():
    sp.add_compilation_target("registryLogic",
        RegistryLogic(
            sp.address('tz1ZrecJHwQriTBiSjSzLqUnepzyJuYokt5D')
        )
    )