.PHONY: count-tokens
count-tokens: digest
	cd scripts && uv run --with tiktoken count_tokens.py < ../dearai.txt

.PHONY: digest
digest: dearai
	uvx gitingest dearai --output dearai_.txt
	cat src/_DIGEST_PREMABLE.md dearai_.txt > dearai.txt
	rm -f dearai_.txt

.PHONY: dearai
dearai: data
	./scripts/gen-dearai.sh

.PHONY: data
data:
	./scripts/get-data.sh

.PHONY: clean
clean:
	rm -fR data dearai
