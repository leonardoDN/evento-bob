"""Generación y timbrado de facturas CFDI 4.0."""

from xml.sax.saxutils import quoteattr

from app import pac_simulado
from app.db import conexion

RFC_EMISOR = "XEV261020AA1"
NOMBRE_EMISOR = "EMPRESA DE DEMOSTRACION"
REGIMEN_EMISOR = "601"
LUGAR_EXPEDICION = "64000"


class ErrorTimbrado(Exception):
    pass


def armar_xml(factura: dict, cliente: dict, renglones: list[dict]) -> str:
    conceptos = "".join(
        f'<cfdi:Concepto ClaveProdServ="{r["clave_sat"]}" Cantidad="{r["cantidad"]}" '
        f'ClaveUnidad="{r["unidad_sat"]}" Descripcion={quoteattr(r["descripcion"])} '
        f'ValorUnitario="{r["precio"]:.2f}" Importe="{r["importe"]:.2f}" ObjetoImp="02"/>'
        for r in renglones
    )
    return (
        f'<cfdi:Comprobante Version="4.0" Serie="{factura["serie"]}" Folio="{factura["folio"]}" '
        f'SubTotal="{factura["subtotal"]:.2f}" Total="{factura["total"]:.2f}" Moneda="MXN" '
        f'TipoDeComprobante="I" Exportacion="01" LugarExpedicion="{LUGAR_EXPEDICION}">'
        f'<cfdi:Emisor Rfc="{RFC_EMISOR}" Nombre="{NOMBRE_EMISOR}" RegimenFiscal="{REGIMEN_EMISOR}"/>'
        f'<cfdi:Receptor Rfc="{cliente["rfc"]}" Nombre={quoteattr(cliente["razon_social"])} '
        f'DomicilioFiscalReceptor="{cliente["codigo_postal"]}" UsoCFDI="{cliente["uso_cfdi"]}"/>'
        f"<cfdi:Conceptos>{conceptos}</cfdi:Conceptos>"
        f"</cfdi:Comprobante>"
    )


def timbrar_factura(factura_id: int) -> dict:
    with conexion() as con:
        factura = con.execute(
            "SELECT f.*, p.subtotal, p.total, p.cliente_id FROM facturas f "
            "JOIN pedidos p ON p.id = f.pedido_id WHERE f.id = ?",
            (factura_id,),
        ).fetchone()
        if factura is None:
            raise ErrorTimbrado(f"No existe la factura {factura_id}")
        if factura["estado"] == "timbrada":
            raise ErrorTimbrado("La factura ya está timbrada")
        cliente = con.execute("SELECT * FROM clientes WHERE id = ?", (factura["cliente_id"],)).fetchone()
        renglones = con.execute(
            "SELECT r.*, p.descripcion, p.clave_sat, p.unidad_sat FROM renglones r "
            "JOIN productos p ON p.sku = r.sku WHERE r.pedido_id = ?",
            (factura["pedido_id"],),
        ).fetchall()

    xml = armar_xml(dict(factura), dict(cliente), [dict(r) for r in renglones])

    respuesta = pac_simulado.solicitar_timbre(xml)

    with conexion() as con:
        con.execute(
            "UPDATE facturas SET uuid = ?, fecha_timbrado = ?, estado = 'timbrada' WHERE id = ?",
            (respuesta["uuid"], respuesta["fecha_timbrado"], factura_id),
        )
        con.execute("UPDATE pedidos SET estado = 'facturado' WHERE id = ?", (factura["pedido_id"],))
    return {"factura_id": factura_id, "uuid": respuesta["uuid"], "fecha_timbrado": respuesta["fecha_timbrado"]}
