def test_ciclo_completo_de_una_orden(cliente_http):
    orden = cliente_http.post(
        "/api/ordenes", json={"equipo_id": 4, "tipo": "correctiva", "falla_reportada": "Vibración y ruido en rodamientos"}
    ).json()
    assert orden["estado"] == "abierta"

    assert cliente_http.post(f"/api/ordenes/{orden['id']}/asignar", json={"tecnico_id": 3}).status_code == 200
    existencias_antes = next(r for r in cliente_http.get("/api/refacciones").json() if r["clave"] == "ROD-6310")["existencias"]
    r = cliente_http.post(f"/api/ordenes/{orden['id']}/refacciones", json={"clave": "ROD-6310", "cantidad": 2})
    assert r.status_code == 201
    existencias_despues = next(r for r in cliente_http.get("/api/refacciones").json() if r["clave"] == "ROD-6310")["existencias"]
    assert existencias_despues == existencias_antes - 2

    r = cliente_http.post(
        f"/api/ordenes/{orden['id']}/cerrar", json={"diagnostico": "Cambio de rodamientos lado acople", "horas_mano_obra": 3.5}
    )
    assert r.status_code == 200
    cierre = r.json()
    assert float(cierre["costo_mano_obra"]) == 2975.00
    assert float(cierre["costo_refacciones"]) == 2480.00
    assert float(cierre["iva"]) == 872.80
    assert float(cierre["total"]) == 6327.80

    historial = cliente_http.get("/api/equipos/4").json()["historial"]
    assert historial[0]["id"] == orden["id"]
    assert historial[0]["estado"] == "cerrada"


def test_no_cierra_sin_tecnico(cliente_http):
    orden = cliente_http.post("/api/ordenes", json={"equipo_id": 2, "tipo": "preventiva", "falla_reportada": "Servicio"}).json()
    r = cliente_http.post(f"/api/ordenes/{orden['id']}/cerrar", json={"diagnostico": "Listo", "horas_mano_obra": 1})
    assert r.status_code == 409


def test_refaccion_sin_existencias(cliente_http):
    orden = cliente_http.post("/api/ordenes", json={"equipo_id": 3, "tipo": "correctiva", "falla_reportada": "No enciende"}).json()
    r = cliente_http.post(f"/api/ordenes/{orden['id']}/refacciones", json={"clave": "TERM-K", "cantidad": 1})
    assert r.status_code == 422


def test_no_se_modifica_una_orden_cerrada(cliente_http):
    orden = cliente_http.post("/api/ordenes", json={"equipo_id": 1, "tipo": "correctiva", "falla_reportada": "Fuga"}).json()
    cliente_http.post(f"/api/ordenes/{orden['id']}/asignar", json={"tecnico_id": 1})
    cliente_http.post(f"/api/ordenes/{orden['id']}/cerrar", json={"diagnostico": "Apriete de bridas", "horas_mano_obra": 1})
    r = cliente_http.post(f"/api/ordenes/{orden['id']}/refacciones", json={"clave": "EMP-GRAF", "cantidad": 1})
    assert r.status_code == 409


def test_serie_duplicada(cliente_http):
    r = cliente_http.post(
        "/api/equipos",
        json={"cliente_id": 1, "numero_serie": "bc-2019-0441", "tipo": "bomba", "marca": "X", "modelo": "Y",
              "ubicacion": "Z", "fecha_instalacion": "2024-01-01"},
    )
    assert r.status_code == 409
