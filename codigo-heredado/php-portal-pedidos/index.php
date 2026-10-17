<?php
include("includes/funciones.inc.php");

if ($_POST['entrar']) {
    $r = q("SELECT * FROM usuarios WHERE usuario = '" . $_POST['usuario'] . "' AND clave = '" . md5($_POST['clave']) . "'");
    if (mysql_num_rows($r) > 0) {
        $u = mysql_fetch_assoc($r);
        $_SESSION['usuario'] = $u['usuario'];
        $_SESSION['id_cliente'] = $u['id_cliente'];
        $_SESSION['es_vendedor'] = $u['vendedor'];
        header("Location: pedido.php");
        exit;
    } else {
        $error = "Usuario o clave incorrectos";
    }
}
?>
<html>
<head>
<title>Portal de Pedidos</title>
<link rel="stylesheet" href="css/estilo.css">
</head>
<body>
<table width="100%" class="encabezado"><tr><td><h2>Portal de Pedidos</h2></td></tr></table>
<center>
<form method="post" action="index.php">
<table class="caja">
<tr><td colspan="2"><b>Acceso</b></td></tr>
<?php if ($error) { ?>
<tr><td colspan="2"><font color="red"><?php echo $error; ?></font></td></tr>
<?php } ?>
<tr><td>Usuario:</td><td><input type="text" name="usuario" value="<?php echo $_POST['usuario']; ?>"></td></tr>
<tr><td>Clave:</td><td><input type="password" name="clave"></td></tr>
<tr><td colspan="2" align="right"><input type="submit" name="entrar" value="Entrar"></td></tr>
</table>
</form>
</center>
</body>
</html>
