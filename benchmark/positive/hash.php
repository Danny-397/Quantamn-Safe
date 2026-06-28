<?php
$key = openssl_pkey_new(array("private_key_type" => OPENSSL_KEYTYPE_RSA));
$h = md5($data);
$s = hash("sha256", $data);
