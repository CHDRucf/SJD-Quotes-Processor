<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $post = [
	    'quote_id' => $_POST['quote_id'],
      'tMin' => $_POST['tMin'],
      'tMax' => $_POST['tMax'],
      'searchCorpus' => $_POST['searchCorpus'],
    ];
  }

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/get_quote_matches');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
curl_setopt($curl, CURLOPT_POST, true);
$response = curl_exec($curl);
print $response;
?>
