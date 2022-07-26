
const $ = require("jquery");
const { TezosToolkit, Operation } = require('@taquito/taquito');
const { BeaconWallet } = require('@taquito/beacon-wallet');

function initUI() {
    updateUISetting({
        provider: "https://jakartanet.ecadinfra.com",
        contractAddress: "KT1Qtbq2gUJ6GpCj5JXuu88bZ23GY5CRXWR9"
    });

    // setup UI actions

    // Add schema
    $("#btn_add_schema").click(() => add_schema($("#schema_data").val()));

    // Set schema status
    $("#btn_schema_activate").click(() => set_schema_status($("#schema_id_status").val(), "activate"));
    $("#btn_schema_deactivate").click(() => set_schema_status($("#schema_id_status").val(), "deactivate"));
    $("#btn_schema_set_status").click(() => set_schema_status($("#schema_id_status").val(), "set", $("#schema_status_id").val()));

    // Get schema
    $("#btn_get").click(() => get_schema($("#schema_id_get").val()));

    // Add / Update issuer
    $("#btn_issuer_issue").click(() => add_issuer($("#issuer_did").val(), $("#issuer_data").val()));
    $("#btn_issuer_update_data").click(() => update_issuer_data($("#issuer_did").val(), $("#issuer_data").val()));

    // Update issuer owner
    $("#btn_issuer_owner_update").click(() => set_issuer_owner($("#issuer_did").val(), $("#issuer_owner").val()));

    // Get issuer
    $("#btn_issuer_get").click(() => get_issuer($("#issuer_did").val()));

    // Set issuer status
    $("#btn_issuer_activate").click(() => set_issuer_status($("#issuer_did").val(), "activate"));
    $("#btn_issuer_deactivate").click(() => set_issuer_status($("#issuer_did").val(), "deactivate"));
    $("#btn_issuer_set_status").click(() => set_issuer_status($("#issuer_did").val(), "set", $("#issuer_status_id").val()));

    // Add binding
    $("#btn_bind").click(() => bind_issuer_schema($("#binding_issuer_did").val(), $("#binding_schema_id").val()));

    // Set binding status
    $("#btn_binding_activate").click(() => set_binding_status($("#binding_issuer_did").val(), $("#binding_schema_id").val(), "activate"));
    $("#btn_binding_deactivate").click(() => set_binding_status($("#binding_issuer_did").val(), $("#binding_schema_id").val(), "deactivate"));
    $("#btn_binding_set_status").click(() => set_binding_status($("#binding_issuer_did").val(), $("#binding_schema_id").val(), "set", $("#binding_status_id").val()));

    // Verify binding
    $("#btn_check_binding").click(() => verify_binding($("#binding_issuer_did").val(), $("#binding_schema_id").val()));

    // Settings / Wallet
    $("#btn_settings").click(() => $("#settings-box").toggleClass('d-none'));
    $("#btn_connect").click(() => connectWallet());
}

function updateUISetting(accountSettings) {
    $('#provider').val(accountSettings.provider);
    $('#contractAddress').val(accountSettings.contractAddress);
}

function readUISettings() {
    return {
        provider: $('#provider').val(),
        contractAddress: $('#contractAddress').val()
    };
}

function showViewResult(result)
{
    $("#result-loader").addClass('d-none').removeClass('d-flex')
    $("#view-result-pre").html(result)
    $("#view-result").addClass('d-flex').removeClass('d-none')
}

function showResultAlert(result, type)
{
    if (type === 'alert-danger') {
        $("#result-loader").addClass('d-none').removeClass('d-flex')
    }

    $("#alert-result").attr('class', `alert ${type}`);
    $("#alert-result").html(result)
}

function clearAll()
{
    $("#view-result").addClass('d-none')
    $("#view-result-pre").html("")
    $("#alert-result").attr('class', 'd-none');
    $("#alert-result").html("")
}

function isASCII(str)
{
    return /^[\x00-\x7F]*$/.test(str);
}

function activateTabs()
{
    var pillElements = document.querySelectorAll('button[data-bs-toggle="pill"]')
    pillElements.forEach(function(pillElement) {
        pillElement.addEventListener('shown.bs.tab', function () {
            clearAll()
        })
    });
}

let tezos, wallet, current_operation_hash;
let browser_operations_url = "https://jakartanet.tzkt.io/" 
let non_ascii_char_message = 'Input string contains characters not allowed in Michelson. For more info see the <a target="_blank" href="https://tezos.gitlab.io/michelson-reference/#type-string">Michelson reference for type string</a>' 

// This function will connect your application with the wallet
function connectWallet() {
    const accountSettings = readUISettings();
    tezos = new TezosToolkit(accountSettings.provider);

    const options = {
        name: 'Schema Registry',
        preferredNetwork: "jakartanet"
    };
    
    wallet = new BeaconWallet(options);

    wallet
        .requestPermissions({
            network: {
                type: "jakartanet"
            }
        })
        .then((_) => wallet.getPKH())
        .then((address) => console.log(address))
        .then(() => tezos.setWalletProvider(wallet))
        .then(() => $('#app-overlay').remove())
        .then(() => $('#settings-pills').removeClass("d-none"))
        .then(() => activateTabs());
}

function add_schema(schema_data) {
    const accountSettings = readUISettings();

    if (isASCII(String(schema_data)) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
        return;
    }

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            return contract.methods.add_schema(String(schema_data)).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation().then(() => op);
        })
        .then((op) => {
            current_operation_hash = op.opHash
            return op.transactionOperation();
        })
        .then((data) => {
            let schema_id = data.metadata.internal_operation_results[1].result.storage[2]["int"] - 1
            
            showResultAlert(`Created new Schema with ID ${schema_id} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + current_operation_hash}">See Operation</a>`, "alert-success");
            get_schema(schema_id, false);
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function set_schema_status(schema_id, status_operation, status_id = 0) {
    const accountSettings = readUISettings();

    let method;

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            switch(status_operation) {
                case "activate":
                    method = contract.methods.set_schema_active(parseInt(schema_id))
                    break;
                case "deactivate":
                    method = contract.methods.set_schema_deprecated(parseInt(schema_id))
                    break;
                case "set":
                    method = contract.methods.set_schema_status(parseInt(schema_id), parseInt(status_id))
                    break;
              }

            return method.send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Status for Schema with ID ${schema_id} Status <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            get_schema(schema_id, false);
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function get_schema(schema_id, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.contractAddress;

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", "alert-info");

            return contract.contractViews.get_schema(schema_id).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", "alert-success");
            showViewResult(JSON.stringify(viewResult))
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function add_issuer(issuer_did, issuer_data) {
    const accountSettings = readUISettings();

    if (
        isASCII(String(issuer_did)) === false
        ||
        isASCII(String(issuer_data)) === false
    ) {
        showResultAlert(non_ascii_char_message, "alert-danger")
        return;
    }

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            return contract.methods.add_issuer(String(issuer_data), String(issuer_did)).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Created new Issuer with DID ${issuer_did} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            get_issuer(issuer_did, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function update_issuer_data(issuer_did, issuer_data) {
    const accountSettings = readUISettings();

    if (
        isASCII(String(issuer_did)) === false
        ||
        isASCII(String(issuer_data)) === false
    ) {
        showResultAlert(non_ascii_char_message, "alert-danger")
        return;
    }

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            return contract.methods.set_issuer_data(String(issuer_data), String(issuer_did)).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Data for Issuer with DID ${issuer_did} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            get_issuer(issuer_did, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function set_issuer_owner(issuer_did, issuer_address) {
    const accountSettings = readUISettings();

    if (isASCII(String(issuer_did)) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            return contract.methods.set_issuer_owner(String(issuer_did), issuer_address).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Owner Address to ${issuer_address} for Issuer with DID ${issuer_did} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            get_issuer(issuer_did, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function set_issuer_status(issuer_did, status_operation, status_id = 0) {
    const accountSettings = readUISettings();

    if (isASCII(String(issuer_did)) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    let method;

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            switch(status_operation) {
                case "activate":
                    method = contract.methods.set_issuer_active(String(issuer_did))
                    break;
                case "deactivate":
                    method = contract.methods.set_issuer_deprecated(String(issuer_did))
                    break;
                case "set":
                    method = contract.methods.set_issuer_status(String(issuer_did), parseInt(status_id))
                    break;
              }

            return method.send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Status for Issuer with DID ${issuer_did} Status <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            get_issuer(issuer_did, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function get_issuer(issuer_did, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.contractAddress;

    if (isASCII(String(issuer_did)) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", "alert-info");

            return contract.contractViews.get_issuer(String(issuer_did)).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", "alert-success");
            showViewResult(JSON.stringify(viewResult))
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function bind_issuer_schema(issuer_did, schema_id) {
    const accountSettings = readUISettings();

    if (isASCII(String(issuer_did)) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            return contract.methods.bind_issuer_schema(String(issuer_did), parseInt(schema_id)).send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Created new Binding of Issuer with DID ${issuer_did} and Schema with ID ${schema_id} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            verify_binding(issuer_did, schema_id, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function set_binding_status(issuer_did, schema_id, status_operation, status_id = 0) {
    const accountSettings = readUISettings();

    if (isASCII(String(issuer_did)) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    let method;

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            clearAll()
            showResultAlert("Sending...", "alert-info");

            switch(status_operation) {
                case "activate":
                    method = contract.methods.set_binding_active(String(issuer_did), parseInt(schema_id))
                    break;
                case "deactivate":
                    method = contract.methods.set_binding_deprecated(String(issuer_did), parseInt(schema_id))
                    break;
                case "set":
                    method = contract.methods.set_binding_status(String(issuer_did), parseInt(schema_id), parseInt(status_id))
                    break;
              }

            return method.send();
        })
        .then((op) => {
            showResultAlert("Waiting for confirmation...", "alert-info");
            return op.confirmation(1).then(() => op);
        })
        .then((data) => {
            showResultAlert(`Updated Binding Status of Issuer with DID ${issuer_did} and Schema with ID ${schema_id} <a class="btn btn-success ms-2" target="_blank" href="${browser_operations_url + data.opHash}">See Operation</a>`, "alert-success");
            verify_binding(issuer_did, schema_id, false)
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

function verify_binding(issuer_did, schema_id, show_alert = true) {
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.contractAddress;

    if (isASCII(String(issuer_did)) === false) {
        showResultAlert(non_ascii_char_message, "alert-danger")
    }

    $("#result-loader").addClass('d-flex').removeClass('d-none')

    var record = {
        "issuer_did": String(issuer_did),
        "schema_id": parseInt(schema_id)
    }

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            if (show_alert) clearAll()
            if (show_alert) showResultAlert("Getting...", "alert-info");

            return contract.contractViews.verify_binding(record).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            if (show_alert) showResultAlert("Finished", "alert-success");
            showViewResult(JSON.stringify(viewResult))
        })
        .catch((error) => {
            showResultAlert(error.message, "alert-danger");
        });
}

$(document).ready(initUI);

