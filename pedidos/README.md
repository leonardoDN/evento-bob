# Demostraciones 2 a 6: pedidos y facturación

Una aplicación pequeña pero completa de pedidos B2B con facturación CFDI 4.0: interfaz web, API en Python con FastAPI y base de datos SQLite. Sobre ella ocurren las demostraciones 2 a 6 del evento.

¿Aún no tienes Bob? Activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**

> El timbrado usa un **PAC simulado** que no sale a internet: tarda entre medio segundo y dos y medio, y a veces no responde, como el de verdad. Las credenciales que encuentres en el proyecto son falsas.

## Cómo ejecutarla

Necesitas Python 3.11 o posterior.

```
cd pedidos
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

## Cómo seguir las demostraciones

Abre en Bob **la carpeta `pedidos`**, no la raíz del repositorio.

| Demostración | Qué vas a hacer |
|---|---|
| 2. El plan antes del código | En modo **Plan**, pedir un cambio que atraviese interfaz, API y base de datos, responder las preguntas del agente y revisar el plan antes de construir |
| 3. Escribir sobre el código | Ajustar la llamada al PAC directamente en la línea donde ocurre, con la instrucción escrita en el propio archivo |
| 4. El cambio deja rastro | Revisar lo que quedó registrado después del cambio |
| 5. Encuentre el defecto | Competir contra el agente con los fragmentos de `rondas/` y revisar la rama `cancelacion-cfdi` con `/review` |
| 6. Las reglas de la casa | Ver de dónde salió todo lo anterior y agregar un estándar propio |

Para volver al estado inicial en cualquier momento:

```
git checkout inicio -- pedidos
git clean -fd pedidos
```

El segundo comando borra los archivos nuevos que hayan creado los ejercicios, como planes o bitácoras.
