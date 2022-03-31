
const $ = require("jquery");
const { TezosToolkit} = require('@taquito/taquito');
const { BeaconWallet } = require('@taquito/beacon-wallet');

function initUI() {
    updateUISetting({
        provider: "https://hangzhounet.smartpy.io/",
        contractAddress: "KT1MuadG9MbxSUQaqdUAWaXhJcQfgCwnjJMq"
    });

    // setup UI actions
    $('#btn_issue').click(() => add_schema($('#schema_id').val(), $('#schema_data').val()));
    $('#btn_get').click(() => get_schema($('#schema_id_get').val()));
    $('#btn_issuer_issue').click(() => add_issuer($('#issuer_data').val()));
    $('#btn_issuer_get').click(() => get_issuer($('#issuer_id_get').val()));

    $('#btn_settings').click(() => $('#settings-box').toggle());
    $('#btn_connect').click(() => connectWallet());
}

$( document ).ready(function() {
    connectWallet()
});

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

function reportResult(result, type, itemSelector) {
    return $(itemSelector)
        .html(result)
        .removeClass()
        .addClass("result-bar")
        .addClass(type == "error" ?
            "result-false" :
            type == "ok" ?
            "result-true" :
            "result-load");
}

let tezos, wallet;

// This function will connect your application with the wallet
function connectWallet() {
    const accountSettings = readUISettings();
    tezos = new TezosToolkit(accountSettings.provider);

    const options = {
        name: 'Schema Registry',
        preferredNetwork: "hangzhounet"
    };
    wallet = new BeaconWallet(options);

    wallet
        .requestPermissions({
            network: {
                type: "hangzhounet"
            }
        })
        .then((_) => wallet.getPKH())
        .then((address) => console.log(address))
        .then(() => tezos.setWalletProvider(wallet))
        .then(() => $('.overlay').remove());
    
    

}

function add_schema(schema_id, schema_data) 
{
    const accountSettings = readUISettings();

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            reportResult("Sending...", "info", "#result-bar");
            
            return contract.methods.add_schema(schema_data, schema_id).send();
        })
        .then((op) => {
            reportResult("Waiting for confirmation...", "info", "#result-bar");
            return op.confirmation(1).then(() => op.hash);
        })
        .then(() => {
            reportResult(`Updated entry ${schema_id}`, "ok", "#result-bar");
        })
        .catch((error) => {
            reportResult(error.message, "error", "#result-bar");
        });
}

function get_schema(schema_id) 
{
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.contractAddress;

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            reportResult("Getting...", "info", "#result-bar");
            
            return contract.contractViews.get_schema(schema_id).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            reportResult("Finished", "ok", "#result-bar");
            alert(JSON.stringify(viewResult))
        })
        .catch((error) => {
            reportResult(error.message, "error", "#result-bar");
        });
}

function add_issuer(issuer_data) 
{
    const accountSettings = readUISettings();

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            reportResult("Sending...", "info", "#result-bar");
            
            return contract.methods.add_issuer(issuer_data).send();
        })
        .then((op) => {
            reportResult("Waiting for confirmation...", "info", "#result-bar");
            return op.confirmation(1).then(() => op.hash);
        })
        .then(() => {
            reportResult(`Updated entry`, "ok", "#result-bar");
        })
        .catch((error) => {
            reportResult(error.message, "error", "#result-bar");
        });
}

function get_issuer(issuer_id) 
{
    const accountSettings = readUISettings();
    const contractCallFib = accountSettings.contractAddress;

    return tezos.wallet.at(accountSettings.contractAddress)
        .then((contract) => {
            reportResult("Sending...", "info", "#result-bar");
            
            return contract.contractViews.get_issuer(issuer_id).executeView({ viewCaller: contractCallFib });
        })
        .then((viewResult) => {
            reportResult("Finished", "ok", "#result-bar");
            alert(JSON.stringify(viewResult))
        })
        .catch((error) => {
            reportResult(error.message, "error", "#result-bar");
        });
}

$(document).ready(initUI);

