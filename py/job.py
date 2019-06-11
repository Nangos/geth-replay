import os
import sys
import json

def main(block, tx_fn, trace_fn, out_dir):
    with open(tx_fn, "r") as f:
        txlist = json.load(f)
    if len(txlist) == 0: # no tx in the block, simply return
        return
    
    # the first traverse
    # filter for contract transactions and count the calls
    with open(trace_fn, "r") as f:
        i = 0
        counter = [0]
        code_txlist = []
        for line in f:
            l = line[:-1] # take out "\n"
            if l == "TAG NO_CODE":
                i += 1
            elif l == "TAG EXTERNAL":
                counter[-1] += 1
                counter.append(0)
                code_txlist.append(txlist[i])
                i += 1
            elif l == "TAG INTERNAL":
                counter[-1] += 1

    if len(code_txlist) == 0:
        return
    block_dir = "%s%.8d/" % (out_dir, block)
    os.mkdir(block_dir)
    with open(block_dir + "txlist.json", "w") as g:
        json.dump(code_txlist, g)

    def _next(cursor):
        a, b = cursor
        b += 1
        if counter[a] == b:
            return (a+1, 0)
        else:
            return (a, b)

    # the second traverse
    # write to a newfile
    with open(block_dir + "tracelist.json", "w") as g:
        with open(trace_fn, "r") as f:
            cursor = (0, 0)
            head = False
            g.write("[\n  [\n    {")
            for line in f:
                l = line[:-1]
                if l == "TAG EXTERNAL" or l == "TAG INTERNAL":
                    if cursor[0] != 0 and cursor[1] == 0:
                        g.write("\n    }\n  ],\n  [\n    {")
                    elif cursor[1] != 0:
                        g.write("\n    },\n    {")
                    head = True
                    cursor = _next(cursor)
                elif l == "TAG NO_CODE" or l == "":
                    pass
                elif head:
                    g.write("\n      ")
                    g.write(l)
                    head = False
                else:
                    g.write(",\n      ")
                    g.write(l)
            g.write("\n    }\n  ]\n]\n")



if __name__ == "__main__":
    me, block, tx_fn, trace_fn, out_dir = sys.argv
    block = int(block)
    main(block, tx_fn, trace_fn, out_dir)