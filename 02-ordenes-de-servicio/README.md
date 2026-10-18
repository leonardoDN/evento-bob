# Ejercicio 2: el plan antes del código

Una empresa da servicio a equipo industrial en las plantas de sus clientes: bombas, compresores, calderas y motores. Esta aplicación lleva sus órdenes de servicio: se abre la orden, se asigna un técnico, se registran las refacciones que salen del almacén y al cerrar se calcula el costo de mano de obra y refacciones. Interfaz web, API en Python con FastAPI y base de datos SQLite.

El ejercicio consiste en pedirle a Bob un cambio de negocio de los que tomarían un par de sprints, **en modo Plan**: Bob lee el proyecto sin modificarlo, pregunta lo que no sabe y entrega un plan escrito para revisarlo antes de construir.

¿Aún no tienes Bob? Activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**

> Todo el código y los datos son ficticios. El caso simplifica la normatividad que menciona; no es asesoría de cumplimiento.

## Cómo seguir el ejercicio

1. Abre en Bob **la carpeta `02-ordenes-de-servicio`**, no la raíz del repositorio.
2. Cambia a modo **Plan**. En ese modo Bob solo puede leer.
3. Pídele uno de estos cambios, tal cual o con tus palabras. Ninguno existe hoy en el código y los tres tocan base de datos, API e interfaz:

   **A. Mantenimiento preventivo por horas de operación.** Queremos registrar las lecturas de horómetro de cada equipo y que el sistema abra solo la orden preventiva cuando el equipo llegue a su intervalo de mantenimiento: bombas cada 2,000 horas, compresores cada 4,000 y motores cada 8,000. Las calderas siguen por calendario.

   **B. Equipos sujetos a presión.** Calderas y compresores son recipientes sujetos a presión (NOM-020-STPS-2011). Cada uno debe tener registrado su número de control ante la STPS y la fecha de su próxima prueba de presión. No se puede cerrar una orden sobre uno de esos equipos si le faltan esos datos, y la lista de equipos debe marcar los que tienen la prueba vencida.

   **C. Pólizas de servicio.** Algunos clientes contratan una póliza mensual que incluye cierto número de horas de mano de obra. Al cerrar una orden de un cliente con póliza, las horas se descuentan de las incluidas en el mes y solo se cobra el excedente.

4. Responde las preguntas que te haga. Si no pregunta nada, pídeselo: *"Antes de planear, dime qué decisiones necesitas que tomemos nosotros."*
5. Lee el plan antes de aprobarlo, sobre todo lo que dice que **no** va a hacer.
6. Si quieres construirlo: abre una conversación nueva, cambia a modo **Code** y menciona los archivos del plan con `@`.

## Cómo ejecutar la aplicación

No hace falta para el ejercicio, pero ayuda a ver de qué se trata. Necesitas Python 3.11 o posterior.

```
cd 02-ordenes-de-servicio
python -m venv .venv
.venv\Scripts\activate          (en macOS o Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abre http://localhost:8000. La base se crea sola en `datos/ordenes.db` con clientes, equipos y órdenes de ejemplo; bórrala para empezar de cero.

Pruebas:

```
pytest
```

## Volver al estado inicial

```
git checkout inicio -- 02-ordenes-de-servicio
git clean -fd 02-ordenes-de-servicio
```

El segundo comando borra los archivos nuevos que haya creado el ejercicio, como los planes.
