<?php
include_once("conexion.inc.php");

function trae_cliente($id) {
    $r = q("SELECT * FROM clientes WHERE id_cliente = " . $id);
    return mysql_fetch_assoc($r);
}

function trae_producto($sku) {
    $r = q("SELECT * FROM productos WHERE sku = '" . $sku . "' AND activo = 1");
    return mysql_fetch_assoc($r);
}

// descuento por volumen, depende de la categoria del producto
function descuento_volumen($categoria, $cantidad) {
    $pct = 0;
    if ($categoria == "FER") {
        if ($cantidad >= 50) $pct = 4;
        if ($cantidad >= 200) $pct = 7;
    } elseif ($categoria == "ELE") {
        if ($cantidad >= 100) $pct = 6;
    } elseif ($categoria == "PLO") {
        if ($cantidad > 24) $pct = 3;
    } else {
        if ($cantidad >= 200) $pct = 2;
    }
    return $pct;
}

// descuento adicional para distribuidores
function descuento_distribuidor($cliente, $forma_pago) {
    if ($cliente['tipo'] != "DIS") return 0;
    $pct = 0;
    if ($cliente['nivel'] == 1) $pct = 2;
    if ($cliente['nivel'] == 2) $pct = 3;
    if ($cliente['nivel'] == 3 && $forma_pago == "ANT") $pct = 4;
    return $pct;
}

function es_frontera($cp) {
    global $CP_FRONTERA;
    return in_array(substr($cp, 0, 2), $CP_FRONTERA);
}

function tasa_iva($cliente) {
    if (es_frontera($cliente['cp'])) return IVA_FRONTERA;
    return IVA_GENERAL;
}

// trunca, no redondea (asi lo pidio direccion para no regalar centavos)
function aplica_descuento($importe, $pct) {
    $desc = floor($importe * $pct) / 100;
    return $importe - $desc;
}

function costo_envio($cliente, $subtotal) {
    global $EDOS_SIN_ENVIO_GRATIS;
    if ($cliente['tipo'] == "MOS") return 0;
    if ($subtotal > MONTO_ENVIO_GRATIS && !in_array($cliente['estado'], $EDOS_SIN_ENVIO_GRATIS)) {
        return 0;
    }
    return COSTO_ENVIO;
}

function fecha_entrega() {
    global $DIAS_ENTREGA;
    $dia = date("d") + $DIAS_ENTREGA;
    $mes = date("m");
    $anio = date("Y");
    if ($dia > 28) {
        $dia = $dia - 28;
        $mes = $mes + 1;
    }
    return $anio . "-" . str_pad($mes, 2, "0", STR_PAD_LEFT) . "-" . str_pad($dia, 2, "0", STR_PAD_LEFT);
}

// programa de lealtad 2014
function calcula_puntos($total, $cliente) {
    $puntos = floor($total / 100);
    if ($cliente['tipo'] == "DIS") $puntos = $puntos * 2;
    if (date("m") == 12) $puntos = $puntos * 3;
    return $puntos;
}

function formato($n) {
    return "$" . number_format($n, 2);
}

function siguiente_folio() {
    q("UPDATE folios SET ultimo = ultimo + 1 WHERE serie = 'P'");
    $r = q("SELECT ultimo FROM folios WHERE serie = 'P'");
    $f = mysql_fetch_assoc($r);
    return $f['ultimo'];
}
?>
