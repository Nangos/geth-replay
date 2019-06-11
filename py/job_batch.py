import os
import sys
import json

def main(block, tx_fn, trace_fn, out_dir, sz):
    with open(tx_fn, "r") as f:
        txlist_s = json.load(f)
    if len(txlist_s) == 0: # no blocks, simply return
        print("ok")
        return
    if txlist_s[0] == "ERROR":
        print("block=%d, b=%d, %s" % (txlist_s[1], txlist_s[2], txlist_s[3]))
        return

    tx_counts = [len(t) for t in txlist_s] # how many tx for each block?
    if sum(tx_counts) == 0: # no tx in the blocks, simply return
        print("ok")
        return

    # the first traverse
    # filter for contract transactions and count the calls
    with open(trace_fn, "r") as f:
        i, j = 0, 0 # j-th tx at i-th block
        counter_s = []
        code_txlist_s = []

        counter = [0]
        code_txlist = []
        for line in f:
            while i < sz and j == tx_counts[i]:
                counter_s.append(counter)
                code_txlist_s.append(code_txlist)
                counter = [0]
                code_txlist = []
                i, j = i+1, 0

            l = line[:-1] # take out "\n"
            if l == "TAG NO_CODE":
                j += 1
            elif l == "TAG EXTERNAL":
                counter[-1] += 1
                counter.append(0)
                code_txlist.append(txlist_s[i][j])
                j += 1
            elif l == "TAG INTERNAL":
                counter[-1] += 1

        while i < sz and j == tx_counts[i]:
            counter_s.append(counter)
            code_txlist_s.append(code_txlist)
            counter = [0]
            code_txlist = []
            i, j = i+1, 0

    code_tx_counts = [len(t) for t in code_txlist_s]
    if sum(code_tx_counts) == 0:
        print("ok")
        return

    block_dir_s = []
    for i in range(sz):
        if code_tx_counts[i] == 0:
            block_dir_s.append(None)
            continue
        block_dir = "%s%.8d/" % (out_dir, block + i)
        os.mkdir(block_dir)
        with open(block_dir + "txlist.json", "w") as g:
            json.dump(code_txlist_s[i], g)
        block_dir_s.append(block_dir)

    def _next(cursor):
        a, b, c = cursor # a-th dir, b-th tx, c-th call
        c += 1
        if counter_s[a][b] == c:
            b, c = b+1, 0
            while a < sz and counter_s[a][b] == c:
                a, b = a+1, 0
        return (a, b, c)

    def _init():
        a = 0
        while a < sz and counter_s[a][0] == 0:
            a += 1
        return (a, 0, 0)

    # the second traverse
    # write to new files
    with open(trace_fn, "r") as f:
        cursor = _init()
        new_file = True
        head = False
        g = None

        for line in f:
            l = line[:-1]
            if l == "TAG EXTERNAL" or l == "TAG INTERNAL":
                if new_file:
                    a = cursor[0]
                    block_dir = block_dir_s[a]
                    if g:
                        g.write("\n    }\n  ]\n]\n")
                        g.close()
                    g = open(block_dir + "tracelist.json", "w")
                    g.write("[\n  [\n    {")
                    new_file = False
                if cursor[1] != 0 and cursor[2] == 0:
                    g.write("\n    }\n  ],\n  [\n    {")
                elif cursor[2] != 0:
                    g.write("\n    },\n    {")
                head = True
                cursor = _next(cursor)
                if cursor[0] > a:
                    new_file = True
            elif l == "TAG NO_CODE":
                pass
            elif head:
                g.write("\n      ")
                g.write(l)
                head = False
            else:
                g.write(",\n      ")
                g.write(l)

        g.write("\n    }\n  ]\n]\n")
        g.close()

    print("ok")
    return


if __name__ == "__main__":
    me, block, tx_fn, trace_fn, out_dir, sz = sys.argv
    block = int(block)
    sz = int(sz)
    main(block, tx_fn, trace_fn, out_dir, sz)