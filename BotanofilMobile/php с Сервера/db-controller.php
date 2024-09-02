<?php

function db_connect()
{
    $servername = "localhost";
    $username = "f0782959_davail";
    $password = "davail";
    $database_name = "f0782959_davail";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $database_name);

    // Check connection
    if ($conn->connect_error)
    {
        die("Connection failed: " . $conn->connect_error);
    }

    // mysqli_set_charset($conn, "utf8");

    return $conn;
}

function add($password)
{
    $conn = db_connect();
    $sql = "INSERT INTO `sesorControlers` (`id`, `Data`, `Password`, `Water`, `Light`, `Settings`) VALUES (NULL, '{}', '". $password . "', '0', '0', '{\"Light\": {}, \"Water\": {\"time\":{}, \"value\": -1}}');";
   
    if ($conn->query(($sql)) == TRUE) {
        echo "OK";
    } else {    
        echo $conn->error;
    }

    $conn->close();
}

function update_data($sesor_control_id, $password, $json)
{
    $row = read($sesor_control_id, $password);

    $conn = db_connect();
    $sql = "UPDATE `sesorControlers` SET Data = '" . $json . "' WHERE id=".$sesor_control_id;

    if ($conn->query(($sql)) == TRUE) {
        echo "OK";
    } else {
        echo $conn->error;
    }

    $conn->close();
}

function update_command($sesor_control_id, $password, $command)
{
    $row = read($sesor_control_id, $password);

    $conn = db_connect();

    if ($command == "on_water") {
        $sql = "UPDATE `sesorControlers` SET `Water` = '1' WHERE `sesorControlers`.`id` = ". $sesor_control_id;
    } elseif ($command == "off_water") {
        $sql = "UPDATE `sesorControlers` SET `Water` = '0' WHERE `sesorControlers`.`id` = ". $sesor_control_id;
    } elseif ($command == "on_water_admin") {
        $sql = "UPDATE `sesorControlers` SET `Water` = '2' WHERE `sesorControlers`.`id` = ". $sesor_control_id;
    } elseif ($command == "on_light") {
        $sql = "UPDATE `sesorControlers` SET `Light` = '1' WHERE `sesorControlers`.`id` = ". $sesor_control_id;
    } elseif ($command == "off_light") {
        $sql = "UPDATE `sesorControlers` SET `Light` = '0' WHERE `sesorControlers`.`id` = ". $sesor_control_id;
    } elseif ($command == "on_light_admin") {
        $sql = "UPDATE `sesorControlers` SET `Light` = '2' WHERE `sesorControlers`.`id` = ". $sesor_control_id;
    } else {
        die("invalid command");
    }

    if ($conn->query(($sql)) == TRUE) {
        echo "OK";
    } else {
        echo $conn->error;
    }

    $conn->close();
}

function update_password($sesor_control_id, $password, $new_password)
{
    $row = read($sesor_control_id, $password);

    $conn = db_connect();

    $sql = "UPDATE `sesorControlers` SET `Password` = '" . $new_password . "' WHERE `sesorControlers`.`id` = ". $sesor_control_id;

    if ($conn->query(($sql)) == TRUE) {
        echo "OK";
    } else {
        echo $conn->error;
    }

    $conn->close();
}

function update_settings($sesor_control_id, $password, $settings)
{
    $row = read($sesor_control_id, $password);

    $conn = db_connect();

    $sql = "UPDATE `sesorControlers` SET `Settings` = '" . $settings . "' WHERE `sesorControlers`.`id`=". $sesor_control_id;

    if ($conn->query(($sql)) == TRUE) {
        echo "OK";
    } else {
        echo $conn->error;
    }

    $conn->close();
}

function read($sesor_control_id, $password)
{
    $conn = db_connect();
    
    $sql = "SELECT * FROM sesorControlers WHERE id=".$sesor_control_id;

    $result = $conn->query($sql);
    
    $row = $result->fetch_assoc();

    $conn->close();

    if ($row["Password"] == $password) {
        return $row;
    } else {
        die("Incorrect password or id");
    }
}

?>