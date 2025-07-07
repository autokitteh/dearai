# Systems Tests

This directory runs end-to-end "black-box" system tests of the autokitteh CLI,
functioning both as a server and as a client.

It can also control other tools, dependencies, and in-memory fixtures (e.g.
Temporal, databases, caches, and HTTP webhooks).

Test cases are defined as [txtar](https://pkg.go.dev/golang.org/x/tools/txtar)
files in the [testdata](./testdata/) directory tree. Their structure and
