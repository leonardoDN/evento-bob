# Ejercicio 6: las reglas de la casa

Un módulo de logística que cotiza envíos por peso y zona, genera guías con dos paqueterías y traduce sus estatus de rastreo a uno solo. El código importa poco; lo que importa es **lo que rodea al código**: las reglas, los modos y las exclusiones que deciden qué hace Bob en este proyecto y qué no puede hacer.

Todo eso son archivos de texto dentro del repositorio. Se versionan con el código, llegan a todo el equipo al clonar y sus cambios pasan por revisión como cualquier otro archivo.

¿Aún no tienes Bob? Activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**

> Todo el código es ficticio y las llamadas a las paqueterías están simuladas. Las credenciales de `.env` y `config/credentials.json` son falsas a propósito: están ahí para que veas que Bob no las lee.

## Qué hay en el proyecto

| Archivo | Para qué sirve |
|---|---|
| `.bob/rules/` | Reglas que Bob aplica en toda conversación, en cualquier modo: documentar las funciones y dejar bitácora. Son las mismas del ejercicio 4. |
| `.bob/custom_modes.yaml` | Dos modos propios: **Revisor**, que solo puede leer, y **Documentador**, que solo puede editar archivos Markdown. |
| `.bobignore` | Archivos que Bob no lee ni modifica: `.env`, `secrets/`, `*.key` y `config/credentials.json`. |

## Cómo seguir el ejercicio

1. Abre en Bob **la carpeta `06-envios`**, no la raíz del repositorio.
2. Lee los dos archivos de `.bob/rules/`. Son la respuesta a lo que pasó en el ejercicio 4.
3. **Agrega tu propio estándar.** Crea un archivo en `.bob/rules/` con una regla de tu organización, de esas que están en un documento que nadie abre. Por ejemplo:
   - *Toda llamada a un servicio externo debe tener tiempo de espera y manejo de errores.*
   - *Los mensajes de confirmación deben citar el número de ticket.*
   - *No se usan números de punto flotante para importes de dinero.*

   Luego pídele algo sencillo, como *"agrega a NOTAS.md lo que revisamos hoy"*, y fíjate si respeta tu regla.
4. **El límite duro.** Cambia al modo **Revisor** y pídele que modifique `envios/tarifas.py`. No puede: ese modo no tiene la herramienta de edición. Prueba lo mismo en el modo **Documentador**: puede editar `NOTAS.md`, pero no el código.
5. **Las exclusiones.** Pídele que te muestre el contenido de `config/credentials.json`. No lo lee.

Una precisión que conviene tener clara: `.bobignore` limita lo que Bob lee y modifica a través de sus herramientas; no es un aislamiento a nivel de sistema operativo.

Pruebas:

```
python -m unittest
```

## Volver al estado inicial

```
git checkout inicio -- 06-envios
git clean -fd 06-envios
```

El segundo comando borra los archivos nuevos que haya creado el ejercicio, como reglas propias o entradas de la bitácora.
