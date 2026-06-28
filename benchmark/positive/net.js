const crypto = require("crypto");
const tls = require("tls");

const { publicKey } = crypto.generateKeyPairSync("rsa", { modulusLength: 2048 });
const ctx = tls.createSecureContext({ secureProtocol: "TLSv1_method" });
const cipher = crypto.createCipheriv("aes-128-gcm", key, iv);
