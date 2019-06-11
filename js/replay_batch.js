// input: var block, sz
loadScript("js/block.js")

end = block + sz
txlists = []
try {
    for (b = block, i = 0; b < end; b++, i++){
        txlist = eth.getBlock(b).transactions
        // trace contract transactions to "temp-json-raw.txt"
        if (txlist.length > 0) {
            last = txlist[txlist.length - 1]
            debug.traceTransaction(last, {tracer: '{step: function() {}, result: function() {return "tx done"}, fault: function() {}}'})
        }
        txlists[i] = txlist
    }
    output = txlists
} catch (error) {
    output = ["ERROR", block, b, "" + error]
}