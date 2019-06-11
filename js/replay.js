// input: var block
loadScript("js/block.js")

txlist = eth.getBlock(block).transactions
// trace contract transactions to "temp-json-raw.txt"
if (txlist.length > 0) {
    last = txlist[txlist.length - 1]
    debug.traceTransaction(last, {tracer: '{step: function() {}, result: function() {return "tx done"}, fault: function() {}}'})
}

// output: var result
output = txlist