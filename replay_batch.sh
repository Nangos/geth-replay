# replay_batch.sh replays blocks in the range [start, end) and generate raw traces
# feed sz blocks at once
# note: if (end-start) is not a multiple of sz, it runs beyond
# pre-requisite: make run in another console!

start=$1 # start block (inclusive)
end=$2 # end block (exclusive)
sz=$3 # batch size

# datadir=/home/guannan/src/geth-fullnode-test/data-fullsync-test/
datadir=/home/guannan/data/geth1
gethbin=/home/guannan/src/geth-all-mods/tracer-geth/build/bin/geth
# tracedir=/home/guannan/data/gethtrace/rawtraces/
tracedir=/home/guannan/data/gethtrace/testrawtraces/

# clean what is left last time
[ -e temp-json-raw.txt ] && rm temp-json-raw.txt

block=$start
maxretry=5
retry=0
while [ $block -lt $end ]; do # for each block in the range:
    # feed the replay js program:
    echo "block = $block\nsz = $sz" > js/block.js
    $gethbin --datadir $datadir --exec "if(loadScript('js/replay_batch.js')){output}" attach > temp-txlist.json
    # post processing:
    touch temp-json-raw.txt
    error=`python py/job_batch.py $block temp-txlist.json temp-json-raw.txt $tracedir $sz`
    if [ "$error" = "ok" ]; then
        retry=0
        echo "$sz blocks starting at $block completed!"
    else
        retry=`expr $retry + 1`
        bug=`cat temp-txlist.json | awk '{print $3}' | grep -oE "[0-9]+"`
        echo "$sz blocks starting at $block failed on $bug!"
        cat temp-txlist.json >> errors.txt # keep the error msg
        if [ $retry -lt $maxretry ]; then
            [ -e temp-json-raw.txt ] && rm temp-json-raw.txt
            echo "retrying... ($retry/$maxretry)"
            continue
        else
            echo "retry attempts exceeded, please restart the program at $block!"
            break
        fi
        # retry:
        # continue
        ## recursively replay the rest (skipping $bug):
        # sh replay_batch.sh $block $bug `expr $bug - $block`
        # sh replay_batch.sh `expr $bug + 1` `expr $block + $sz` `expr $block + $sz - $bug - 1`
    fi
    # clearance:  
	[ -e temp-json-raw.txt ] && rm temp-json-raw.txt
    [ -e temp-txlist.json ] && rm temp-txlist.json
    # increase block
    block=`expr $block + $sz`
done
echo "go restart the program at $block next time!"