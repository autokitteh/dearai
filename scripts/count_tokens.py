# from: https://github.com/oelmekki/tiktoken-cli/blob/master/tiktoken-cli

import os
import sys
import tiktoken

content = sys.stdin.read()

default = "gpt-3.5-turbo-0301"
model = os.getenv("TIKTOKEN_MODEL", default)

try:
    encoding = tiktoken.encoding_for_model(model)
except KeyError:
    encoding = tiktoken.get_encoding(default)

print(f"Total of {len(encoding.encode(content))} tokens")
