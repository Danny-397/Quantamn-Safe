require "openssl"
require "digest"

key = OpenSSL::PKey::RSA.new(2048)
fp = Digest::MD5.hexdigest("data")
