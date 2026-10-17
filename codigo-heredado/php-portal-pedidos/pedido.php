<?php
include("includes/funciones.inc.php");

if (!$_SESSION['usuario']) {
    header("Location: index.php");
    exit;
}

// el vendedor puede capturar para cualquier cliente
if ($_SESSION['es_vendedor'] && $_REQUEST['id_cliente']) {
    $id_cliente = $_REQUEST['id_cliente'];
} else {
    $id_cliente = $_SESSION['id_cliente'];
}
$cliente = trae_cliente($id_cliente);

if (!is_array($_SESSION['carrito'])) $_SESSION['carrito'] = array();

if ($_POST['agregar']) {
    $sku = strtoupper(trim($_POST['sku']));
    $cant = $_POST['cantidad'];
    if ($sku != "" && $cant > 0) {
        if (isset($_SESSION['carrito'][$sku])) {
            $_SESSION['carrito'][$sku] += $cant;
        } else {
            $_SESSION['carrito'][$sku] = $cant;
        }
    }
}
if ($_GET['quitar']) {
    unset($_SESSION['carrito'][$_GET['quitar']]);
}
if ($_POST['vaciar']) {
    $_SESSION['carrito'] = array();
}

$forma_pago = $_POST['forma_pago'] ? $_POST['forma_pago'] : "CRE";
?>
<html>
<head>
<title>Captura de pedido</title>
<link rel="stylesheet" href="css/estilo.css">
<script>
function valida() {
    if (document.f.sku.value == "") { alert("Captura el SKU"); return false; }
    return true;
}
</script>
</head>
<body>
<table width="100%" class="encabezado"><tr>
<td><h2>Captura de pedido</h2></td>
<td align="right">Usuario: <?php echo $_SESSION['usuario']; ?> | <a href="consulta.php">Mis pedidos</a> | <a href="salir.php">Salir</a></td>
</tr></table>

<table class="caja" width="100%">
<tr><td><b>Cliente:</b> <?php echo $cliente['id_cliente'] . " - " . $cliente['razon_social']; ?></td>
<td><b>Tipo:</b> <?php echo $cliente['tipo']; if ($cliente['tipo'] == "DIS") echo " nivel " . $cliente['nivel']; ?></td>
<td><b>CP:</b> <?php echo $cliente['cp']; ?> (<?php echo $cliente['estado']; ?>)</td></tr>
</table>
<br>

<form name="f" method="post" action="pedido.php" onsubmit="return valida()">
<input type="hidden" name="id_cliente" value="<?php echo $id_cliente; ?>">
SKU: <input type="text" name="sku" size="12">
Cantidad: <input type="text" name="cantidad" size="5" value="1">
<input type="submit" name="agregar" value="Agregar">
</form>

<form method="post" action="pedido.php">
<input type="hidden" name="id_cliente" value="<?php echo $id_cliente; ?>">
<table class="detalle" width="100%" cellspacing="0">
<tr class="titulo"><td>SKU</td><td>Descripcion</td><td>Cant.</td><td>Precio</td><td>Desc.</td><td>Importe</td><td></td></tr>
<?php
$subtotal = 0;
$total_desc = 0;
$renglones = array();
$pct_dist = descuento_distribuidor($cliente, $forma_pago);
foreach ($_SESSION['carrito'] as $sku => $cant) {
    $p = trae_producto($sku);
    if (!$p) {
        echo "<tr><td>" . $sku . "</td><td colspan='6'><font color='red'>No existe</font></td></tr>";
        continue;
    }
    $precio = $p['precio_lista'];
    if ($cliente['lista'] == 2) $precio = $p['precio_mayoreo'];
    $importe = $precio * $cant;
    $pct = descuento_volumen($p['categoria'], $cant) + $pct_dist;
    $neto = aplica_descuento($importe, $pct);
    $total_desc += $importe - $neto;
    $subtotal += $neto;
    $renglones[] = array($sku, $cant, $precio, $pct, $neto);
?>
<tr>
<td><?php echo $sku; ?></td>
<td><?php echo $p['descripcion']; ?></td>
<td align="right"><?php echo $cant; ?></td>
<td align="right"><?php echo formato($precio); ?></td>
<td align="right"><?php echo $pct; ?>%</td>
<td align="right"><?php echo formato($neto); ?></td>
<td><a href="pedido.php?quitar=<?php echo $sku; ?>&id_cliente=<?php echo $id_cliente; ?>">quitar</a></td>
</tr>
<?php
}

$envio = costo_envio($cliente, $subtotal);
$iva = round(($subtotal + $envio) * tasa_iva($cliente), 2);
$total = $subtotal + $envio + $iva;
if ($cliente['tipo'] == "MOS") {
    $total = round($total);
}
?>
<tr><td colspan="5" align="right">Subtotal:</td><td align="right"><?php echo formato($subtotal); ?></td><td></td></tr>
<tr><td colspan="5" align="right">Ahorro:</td><td align="right"><?php echo formato($total_desc); ?></td><td></td></tr>
<tr><td colspan="5" align="right">Envio:</td><td align="right"><?php echo $envio == 0 ? "GRATIS" : formato($envio); ?></td><td></td></tr>
<tr><td colspan="5" align="right">IVA (<?php echo tasa_iva($cliente) * 100; ?>%):</td><td align="right"><?php echo formato($iva); ?></td><td></td></tr>
<tr><td colspan="5" align="right"><b>Total:</b></td><td align="right"><b><?php echo formato($total); ?></b></td><td></td></tr>
</table>
<br>
Forma de pago:
<select name="forma_pago" onchange="this.form.submit()">
<option value="CRE" <?php if ($forma_pago == "CRE") echo "selected"; ?>>Credito</option>
<option value="ANT" <?php if ($forma_pago == "ANT") echo "selected"; ?>>Pago anticipado</option>
<option value="CON" <?php if ($forma_pago == "CON") echo "selected"; ?>>Contado</option>
</select>
Entrega estimada: <b><?php echo fecha_entrega(); ?></b>
<br><br>
<input type="submit" name="vaciar" value="Vaciar">
<input type="submit" name="confirmar" value="Confirmar pedido">
</form>

<?php
if ($_POST['confirmar'] && count($renglones) > 0) {
    $folio = siguiente_folio();
    q("INSERT INTO pedidos (folio, id_cliente, fecha, fecha_entrega, forma_pago, subtotal, envio, iva, total, usuario)
       VALUES (" . $folio . ", " . $id_cliente . ", NOW(), '" . fecha_entrega() . "', '" . $forma_pago . "', "
       . $subtotal . ", " . $envio . ", " . $iva . ", " . $total . ", '" . $_SESSION['usuario'] . "')");
    foreach ($renglones as $r) {
        q("INSERT INTO pedidos_det (folio, sku, cantidad, precio, pct_desc, importe)
           VALUES (" . $folio . ", '" . $r[0] . "', " . $r[1] . ", " . $r[2] . ", " . $r[3] . ", " . $r[4] . ")");
    }
    if ($forma_pago == "CRE") {
        q("UPDATE clientes SET saldo = saldo + " . $total . " WHERE id_cliente = " . $id_cliente);
    }
    $_SESSION['carrito'] = array();
    echo "<script>alert('Pedido " . $folio . " registrado'); location.href='consulta.php';</script>";
}
?>
</body>
</html>
