<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $post = [
	    'token' => $_POST['token'],
    ];
  }

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/logout');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
curl_setopt($curl, CURLOPT_POST, true);
$response = curl_exec($curl);
print $response;
?>
