# datadir = ~/src/geth-fullnode-test/data-fullsync-test/
datadir = ~/data/geth1
# gethbin = geth
gethbin = ~/src/geth-all-mods/tracer-geth/build/bin/geth
# gethbin = ~/src/go-ethereum/build/bin/geth

run:
	$(gethbin) --datadir $(datadir) --syncmode full --gcmode archive console

test: # $(i), $(o)
	$(gethbin) --datadir $(datadir) --exec "if(loadScript('js/$(i)')){output}" attach > results/$(o)

testx:
	touch temp-json-raw.txt
	rm temp-json-raw.txt
	$(gethbin) --datadir $(datadir) --exec "if(loadScript('js/x.js')){output}" attach
