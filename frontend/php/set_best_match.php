<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $post = [
      'token' => $_POST['token'],
	    'quote_id' => $_POST['quote_id'],
      'match_id' => $_POST['match_id'],
      'work_metadata_id' => $_POST['work_metadata_id'],
    ];
  }

$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/set_best_match');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
curl_setopt($curl, CURLOPT_POST, true);
$response = curl_exec($curl);
print $response;
?>
