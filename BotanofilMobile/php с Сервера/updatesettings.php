<?php

$settings = $_POST['settings'];
$pass = $_POST['password'];
$id = $_POST['id'];

require_once "db-controller.php";
echo update_settings($id, $pass, $settings);

?>