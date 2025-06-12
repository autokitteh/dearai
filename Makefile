.PHONY: count-tokens
count-tokens: digest
	./scripts/count-tokens.sh

.PHONY: digest
digest: dearai
	./scripts/gen-digests.sh

.PHONY: dearai
dearai: data
	./scripts/gen-dearai.sh

.PHONY: data
data:
	./scripts/get-data.sh

.PHONY: clean
clean:
	rm -fR data dearai digests
