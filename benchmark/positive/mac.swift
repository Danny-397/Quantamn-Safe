import Crypto

func digests(data: Data) {
    let weak = Insecure.MD5.hash(data: data)
    let ok = SHA256.hash(data: data)
}
