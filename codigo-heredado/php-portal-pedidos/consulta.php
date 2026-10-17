<?php
include("includes/funciones.inc.php");

if (!$_SESSION['usuario']) {
    header("Location: index.php");
    exit;
}

$id_cliente = $_SESSION['id_cliente'];
if ($_SESSION['es_vendedor'] && $_GET['id_cliente']) $id_cliente = $_GET['id_cliente'];

$r = q("SELECT * FROM pedidos WHERE id_cliente = " . $id_cliente . " ORDER BY folio DESC LIMIT 50");
?>
<html>
<head>
<title>Mis pedidos</title>
<link rel="stylesheet" href="css/estilo.css">
</head>
<body>
<table width="100%" class="encabezado"><tr>
<td><h2>Mis pedidos</h2></td>
<td align="right"><a href="pedido.php">Nuevo pedido</a> | <a href="salir.php">Salir</a></td>
</tr></table>
<table class="detalle" width="100%" cellspacing="0">
<tr class="titulo"><td>Folio</td><td>Fecha</td><td>Entrega</td><td>Pago</td><td>Total</td><td>Estatus</td></tr>
<?php while ($p = mysql_fetch_assoc($r)) { ?>
<tr>
<td><?php echo $p['folio']; ?></td>
<td><?php echo substr($p['fecha'], 0, 10); ?></td>
<td><?php echo $p['fecha_entrega']; ?></td>
<td><?php echo $p['forma_pago']; ?></td>
<td align="right"><?php echo formato($p['total']); ?></td>
<td><?php
if ($p['estatus'] == 1) echo "Surtido";
elseif ($p['estatus'] == 2) echo "Cancelado";
elseif ($p['estatus'] == 9) echo "Facturado";
else echo "Pendiente";
?></td>
</tr>
<?php } ?>
</table>
</body>
</html>
