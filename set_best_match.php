<?php
$post = [
	'quote_id' => $argv[1],
	'match_id' => $argv[2],
];
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/set_best_match');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
$response = curl_exec($curl);
var_export($response);