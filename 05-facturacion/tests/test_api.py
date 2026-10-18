def test_crear_pedido_calcula_totales_y_saldo(cliente_http):
    saldo_antes = cliente_http.get("/api/clientes/2").json()["saldo"]
    r = cliente_http.post(
        "/api/pedidos",
        json={"cliente_id": 2, "renglones": [{"sku": "TUB-PVC-4", "cantidad": 2}, {"sku": "CEM-GRS-50", "cantidad": 10}]},
    )
    assert r.status_code == 201
    pedido = r.json()
    assert float(pedido["subtotal"]) == 3233.00
    assert float(pedido["iva"]) == 517.28
    assert float(pedido["total"]) == 3750.28
    assert cliente_http.get("/api/clientes/2").json()["saldo"] == saldo_antes + 3750.28


def test_pedido_con_producto_inexistente(cliente_http):
    r = cliente_http.post("/api/pedidos", json={"cliente_id": 1, "renglones": [{"sku": "NO-EXISTE", "cantidad": 1}]})
    assert r.status_code == 422


def test_pedido_con_cantidad_cero(cliente_http):
    r = cliente_http.post("/api/pedidos", json={"cliente_id": 1, "renglones": [{"sku": "TUB-PVC-4", "cantidad": 0}]})
    assert r.status_code == 422


def test_facturar_y_timbrar(cliente_http):
    pedido = cliente_http.post("/api/pedidos", json={"cliente_id": 1, "renglones": [{"sku": "VAR-38-12", "cantidad": 5}]}).json()
    r = cliente_http.post(f"/api/facturas/desde-pedido/{pedido['id']}")
    assert r.status_code == 201
    assert len(r.json()["uuid"]) == 36
    assert cliente_http.get(f"/api/pedidos/{pedido['id']}").json()["estado"] == "facturado"


def test_no_timbra_dos_veces(cliente_http):
    pedido = cliente_http.post("/api/pedidos", json={"cliente_id": 1, "renglones": [{"sku": "VAR-38-12", "cantidad": 1}]}).json()
    factura = cliente_http.post(f"/api/facturas/desde-pedido/{pedido['id']}").json()
    r = cliente_http.post(f"/api/facturas/{factura['factura_id']}/timbrar")
    assert r.status_code == 409


def test_rfc_duplicado(cliente_http):
    r = cliente_http.post("/api/clientes", json={"rfc": "DNO920315AB1", "razon_social": "X", "codigo_postal": "64000"})
    assert r.status_code == 409
