<?php

$command = $_POST['command'];
$pass = $_POST['password'];
$id = $_POST['id'];

require_once "db-controller.php";
echo update_command($id, $pass, $command); // on_water/off_water | on_light/off_light

?>