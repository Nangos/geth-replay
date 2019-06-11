# replay.sh replays blocks in the range [start, end) and generate raw traces
# pre-requisite: make run in another console!

start=$1 # start block (inclusive)
end=$2 # end block (exclusive)

datadir=/home/guannan/src/geth-fullnode-test/data-fullsync-test/
gethbin=/home/guannan/src/geth-all-mods/tracer-geth/build/bin/geth
tracedir=/home/guannan/data/gethtrace/rawtraces/

block=$start
while [ $block -lt $end ]; do # for each block in the range:
    # feed the replay js program:
    echo "block = $block" > js/block.js
    $gethbin --datadir $datadir --exec "if(loadScript('js/replay.js')){output}" attach > temp-txlist.json
    # post processing:
    touch temp-json-raw.txt
    python py/job.py $block temp-txlist.json temp-json-raw.txt $tracedir
    # clearance:  
	rm temp-json-raw.txt
    rm temp-txlist.json
    # block++:
    echo "Block $block completed!"
    block=`expr $block + 1`
done