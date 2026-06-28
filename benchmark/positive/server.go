package main

import (
	"crypto/dsa"
	"crypto/ecdsa"
)

func run() {
	var d dsa.PrivateKey
	var e ecdsa.PrivateKey
	dh := newDiffieHellman()
	_ = d
	_ = e
	_ = dh
}
