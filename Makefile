.PHONY: digest
digest: dearai
	uvx gitingest dearai --output dearai.txt

.PHONY: dearai
dearai: data
	./scripts/gen-dearai.sh

.PHONY: data
data:
	./scripts/get-data.sh

.PHONY: clean
clean:
	rm -fR data dearai
