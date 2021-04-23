<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $post = [
	    'condition' => $_POST['exportCondition'],
      'tMin' => $_POST['tMin'],
      'tMax' => $_POST['tMax'],
      'token' => $_POST['token'],
    ];
  }

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/export');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));

$response = curl_exec($curl);
/*
$lengthinfo = curl_getinfo($curl, CURLINFO_CONTENT_LENGTH_DOWNLOAD);
header("Content-Type: application/octet-stream");
header("Transfer-Encoding: gzip");
header("Content-Length: " . $lengthinfo);*/
print $response;
?>

