<?php
$contents = 'localhost:5000/get_matches_by_headword';
$curl_handle=curl_init();
curl_setopt($curl_handle, CURLOPT_URL,$contents);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, true);
curl_setopt($curl_handle, CURLOPT_HEADER, false);
curl_setopt($curl_handle, CURLOPT_CONNECTTIMEOUT, 2);
curl_setopt($curl_handle, CURLOPT_USERAGENT, 'SJD');

$result = curl_exec($curl_handle);
curl_close($curl_handle);

echo $result;
?>
