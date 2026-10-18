# Ejercicio 5: encuentre el defecto

Una aplicación pequeña pero completa de pedidos B2B con facturación CFDI 4.0: interfaz web, API en Python con FastAPI y base de datos SQLite. El ejercicio tiene dos partes: competir contra Bob buscando defectos en fragmentos de código, y después revisar con el panel de revisión un cambio completo antes de integrarlo.

¿Aún no tienes Bob? Activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**

> Todo el código es ficticio. El timbrado usa un **PAC simulado** que no sale a internet: tarda entre medio segundo y dos y medio, y a veces no responde, como el de verdad. Las credenciales que encuentres son falsas.

## Cómo seguir el ejercicio

Abre en Bob **la carpeta `05-facturacion`**, no la raíz del repositorio.

### Primera parte: las rondas

En `rondas/` hay cuatro fragmentos, cada uno con un defecto real. Abre uno, date un minuto para encontrarlo tú y después pregúntale a Bob en modo **Ask**: *"¿Qué defecto tiene este código y qué pasaría si llega a producción?"*

| Archivo | Pista |
|---|---|
| `ronda1_existencias.py` | Cuenta las piezas que faltan para surtir un pedido |
| `ronda2_conexion_pac.py` | Envía el comprobante al PAC |
| `ronda3_importes_cfdi.py` | Calcula importes y totales del CFDI |
| `ronda4_buscar_cliente.py` | Busca clientes para el autocompletado |

Si encuentras un defecto distinto del que encuentra Bob, probablemente también tienes razón: cada fragmento trae uno menor a propósito.

### Segunda parte: el panel de revisión

La rama `cancelacion-cfdi` agrega la cancelación de facturas que pide el [issue #1](https://github.com/leonardoDN/evento-bob/issues/1).

1. Trae la rama: `git fetch origin cancelacion-cfdi` y `git checkout cancelacion-cfdi`.
2. Abre el panel de revisión con `/review`.
3. Compara la rama `cancelacion-cfdi` contra `main` y, si tienes tu cuenta de GitHub conectada, elige el issue #1 para validar que el cambio cumple lo que se pidió.
4. Pulsa **Start Review** y recorre los hallazgos. Descarta con **Dismiss** lo que no aplique y corrige uno con **Fix with Bob**.

## Cómo ejecutar la aplicación

No hace falta para el ejercicio. Necesitas Python 3.11 o posterior.

```
cd 05-facturacion
python -m venv .venv
.venv\Scripts\activate          (en macOS o Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre http://localhost:8000. La base se crea sola en `datos/pedidos.db` con clientes y productos de ejemplo; bórrala para empezar de cero.

Pruebas:

```
pytest
```

## Volver al estado inicial

```
git checkout main
git checkout inicio -- 05-facturacion
git clean -fd 05-facturacion
```
