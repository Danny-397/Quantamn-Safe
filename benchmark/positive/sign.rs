use rsa::RsaPrivateKey;
use sha1::Sha1;

fn sign() {
    let key = RsaPrivateKey::new(&mut rng, 2048);
    let mut hasher = Sha1::new();
}
