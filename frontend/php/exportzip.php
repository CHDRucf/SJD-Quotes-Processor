<?php
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    $post = [
	    'filepath' => $_GET['filepath'],
      'token' => $_GET['token'],
    ];
  }
  
  $attachment_location = $post['filepath'];
        if (file_exists($attachment_location)) {

            header($_SERVER["SERVER_PROTOCOL"] . " 200 OK");
            header("Cache-Control: public"); // needed for internet explorer
            header("Content-Type: application/zip");
            header("Content-Transfer-Encoding: Binary");
            header("Content-Length:".filesize($attachment_location));
            header("Content-Disposition: attachment; filename=BestMatchExport" . date("Y-m-d-Hi") . ".zip");
            readfile($attachment_location);
            die();        
        } else {
            die("Error: File not found.");
        } 
/*
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/export');
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));
$response = curl_exec($curl);

print $response;*/
?>