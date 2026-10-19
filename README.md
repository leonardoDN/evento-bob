# IBM Bob en acción: ejercicios del evento

Material del evento **IBM Bob en acción: el salto de generar código a entregar con confianza** (octubre 2026), de Xatrix. Cada carpeta es un ejercicio que el presentador recorre en vivo y que tú puedes reproducir en tu equipo, a la par.

Seguir los ejercicios es opcional. Si prefieres solo observar, todo se hace en pantalla.

## Antes de empezar

1. Instala IBM Bob y activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**
2. Clona este repositorio:

   ```
   git clone https://github.com/leonardoDN/evento-bob.git
   ```

3. Opcional, para que Bob te responda siempre en español: crea el archivo `%USERPROFILE%\.bob\rules\idioma.md` (en macOS o Linux, `~/.bob/rules/idioma.md`) con este texto:

   ```
   Responde siempre en español de México, incluidos los archivos que generes, por ejemplo AGENTS.md.
   ```

## Ejercicios

Cada ejercicio es independiente: tiene su propio caso y su propia carpeta, y no depende de lo que haya pasado en los anteriores. Si uno no te sale, pasa al siguiente sin problema.

| Carpeta | Ejercicio | El caso |
|---|---|---|
| [`01-codigo-heredado/`](01-codigo-heredado/) | 1. Lo que nadie quiere tocar | Entender sistemas viejos (RPG, COBOL y PHP) sin leerlos línea por línea |
| [`02-ordenes-de-servicio/`](02-ordenes-de-servicio/) | 2. El plan antes del código | Planear un cambio de negocio en las órdenes de servicio de equipo industrial |
| [`03-conciliacion-de-pagos/`](03-conciliacion-de-pagos/) | 3. Escribir sobre el código | Hacer resistente a fallas la consulta al banco en la conciliación de pagos SPEI |
| [`04-nomina/`](04-nomina/) | 4. El cambio deja rastro | Actualizar el cálculo de vacaciones a la reforma de 2023 y ver qué queda registrado |
| [`05-facturacion/`](05-facturacion/) | 5. Encuentre el defecto | Competir contra el agente y revisar una rama de cancelación de CFDI 4.0 |
| [`06-envios/`](06-envios/) | 6. Las reglas de la casa | Reglas, modos y exclusiones que gobiernan al agente en un módulo de logística |

Abre en Bob **la carpeta de cada ejercicio**, no la raíz del repositorio; la única excepción es la segunda parte del ejercicio 5, que lo indica. Cada carpeta trae sus propias instrucciones.

Si algo se descompone, cada carpeta explica cómo volver a su estado inicial con la etiqueta `inicio`.

> **Todo el código es ficticio.** Fue escrito para este evento; no proviene de ningún cliente ni sistema real. Las credenciales que aparecen son falsas a propósito.

## Licencia

MIT. Úsalo libremente para practicar o para enseñar.
