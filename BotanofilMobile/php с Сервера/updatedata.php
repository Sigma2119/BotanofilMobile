<?php

$data = $_POST['data'];
$pass = $_POST['password'];
$id = $_POST['id'];

require_once "db-controller.php";
echo update_data($id, $pass, $data);

// 123
$row = read($id, $pass);

$data = json_decode(json_encode($row), true);
$settings = json_decode($data['Settings'], true);
$hum = json_decode($data['Data'], true)['hum'];
$water_time = $settings['Water']['time'];
$low_hum = $settings['Water']['value'];
$light_time = $settings['Light'];

echo json_encode($water_time);

$now = time();

$intersection = false;

foreach ($water_time as $i) {
    
    $from = strtotime($i['From']);
    $to = strtotime($i['To']);

    if ($now >= $from && $now <= $to) {
        $intersection = true;
    }
}

if (number_format($hum) <= number_format($low_hum)) {
    $intersection = true;
}

if ($row['Water'] != 2) {
    if ($intersection == true) {
        update_command($id, $pass, "on_water");
    } else {
        update_command($id, $pass, "off_water");
    }   
}

$intersection = false;

foreach ($light_time as $i) {
    
    $from = strtotime($i['From']);
    $to = strtotime($i['To']);

    if ($now >= $from && $now <= $to) {
        $intersection = true;
    }
}

if ($row['Light'] != 2) {
    if ($intersection == true) {
        update_command($id, $pass, "on_light");
    } else {
        update_command($id, $pass, "off_light");
    }
}

?>