// unstable tests go here
// please move to another js file when it gets stable
// to interface with Makefile, the var "output" is reserved for return value

// txhash = "0xeb9fd4c42edb0f292a0ccd7016cc7b6eb009dea5bea6e8e4d88aa380aed34f1b"; // testing a simple success (it was the 2nd contract tx!)
// txhash = "0x0e9b552b7b8e1b3fa27f0208884e2b5d30afbf0e07a31913d27afd52b8041e04"; // testing a simple failure (it was the 3rd)
// txhash = "0x0ec3f2488a93839524add10ea229e773f6bc891b4eb4794c3337d4495263790b"; // testing reentrancy! (it was the 1st)
// txhash = "0x86c93b68e882ffb5825b44be2e3034d09218120ed7040d326b6d943e3f7fd49d"; // testing a contract creation (it was the 1st)
// txhash = "0x02f8ad1bb2a21b558ecc3ee98101fb1bb3683687720aee568064feccbfaeca12"
// txhash = "0x1e1a9cdf9f728b4006c55b86c2d9b3e336a4fe2a34318c0c9cd3687858d03b0d"

// the "jsStringify.py" program turns {xx}.js into {xx}Str.js"
// loadScript("js/tracerStr.js")

// output = debug.traceTransaction(txhash)
// output = debug.traceTransaction(txhash, {tracer: '{step: function() {}, result: function() {return "tx done"}, fault: function() {}}'})
// blockNumber = 1155199
// key = {tracer: '{step: function() {}, result: function() {return "tx done"}, fault: function() {}}'}

// output = debug.traceBlockByNumber("0x" + blockNumber.toString(16), key).length
// tick = new Date().getTime()
output = "Success"
for (i=1155190; i<1155199; i++) {
    txlist = eth.getBlock(i).transactions
    if (txlist.length > 0) {
        last = txlist[txlist.length - 1]
        try {
            debug.traceTransaction(last, {tracer: '{step: function() {}, result: function() {return "tx done"}, fault: function() {}}'})
        } catch(error) {
            output = "Block " + i + ": " + error
            break
        }
    }
}
// tock = new Date().getTime()
// output = tock - tick