<?php

require_once "db-controller.php";

$row = read("2", "admin");

$data = json_decode(json_encode($row), true);
$hum = json_decode($data['Data'], true)['hum'];
$settings = json_decode($data['Settings'], true);

$low_hum = $settings['Water']['value'];

echo json_encode(number_format($hum));
echo json_encode(number_format($low_hum));

if (number_format($hum) <= number_format($low_hum)) {
        echo 'wdfesgr';
    }

?>