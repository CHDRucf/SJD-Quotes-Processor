<?php
$post = [
	'headword' => $argv[1],
];
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/get_matches_by_headword');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
$response = curl_exec($curl);
var_export($response);