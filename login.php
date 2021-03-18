<?php
$post = [
	'username' => $argv[1],
	'password' => $argv[2],
];
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/login');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
$response = curl_exec($curl);
var_export($response);