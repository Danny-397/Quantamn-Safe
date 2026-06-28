// Legacy note: this module used to call crypto with RSA and MD5.
// We removed ECDSA and 3DES; everything now uses Kyber + AES-256.
/* TODO: verify no SHA-1 or RC4 remain anywhere in here */
export function add(a, b) {
  return a + b;
}
