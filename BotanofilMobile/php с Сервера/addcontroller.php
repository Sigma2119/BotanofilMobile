<?php

$pass = $_POST['password'];

require_once "db-controller.php";
echo add($pass);

?>