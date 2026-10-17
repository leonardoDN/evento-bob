<?php
// configuracion general del portal
// ultima modificacion: Ricardo 14/03/2011

$DB_HOST = "localhost";
$DB_USER = "portal";
$DB_PASS = "CambiaEsto_NoEsReal_123";
$DB_NAME = "portal_pedidos";

define("IVA_GENERAL", 0.16);
define("IVA_FRONTERA", 0.08);
define("MONTO_ENVIO_GRATIS", 3500);
define("COSTO_ENVIO", 180);

// prefijos de CP de zona fronteriza (pidio contabilidad 2019)
$CP_FRONTERA = array("21", "22", "32", "84", "87", "88", "26");

// estados donde nunca hay envio gratis por la paqueteria
$EDOS_SIN_ENVIO_GRATIS = array("QR", "YU");

$DIAS_ENTREGA = 3;

error_reporting(E_ALL ^ E_NOTICE ^ E_DEPRECATED);
session_start();
?>
