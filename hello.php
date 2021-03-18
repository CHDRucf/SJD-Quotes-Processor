<?php
$curl = curl_init();
curl_setopt($curl, CURLOPT_URL, 'http://localhost:5000/hello');
curl_exec($curl);
curl_close($curl);