<?php

$id = $_POST['id'];
$pass = $_POST['password'];

require_once "db-controller.php";
$row = read($id, $pass);

echo "{\"Data\":" . $row['Data'] . ", \"Commands\": {\"Water\":" . $row['Water'] . ", \"Light\":" . $row['Light'] . "}, \"Settings\":" . $row['Settings'] . "}";

?>