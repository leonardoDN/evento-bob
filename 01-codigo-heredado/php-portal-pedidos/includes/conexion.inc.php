<?php
include_once("config.inc.php");

$link = mysql_connect($DB_HOST, $DB_USER, $DB_PASS) or die("No se pudo conectar: " . mysql_error());
mysql_select_db($DB_NAME, $link) or die("No existe la base");
mysql_query("SET NAMES latin1");

function q($sql) {
    global $link;
    $r = mysql_query($sql, $link);
    if (!$r) {
        echo "<!-- ERROR SQL: " . mysql_error() . " -- " . $sql . " -->";
    }
    return $r;
}
?>
