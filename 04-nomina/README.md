# Ejercicio 4: el cambio deja rastro

El área de nómina calcula con este módulo las prestaciones de ley de la plantilla: antigüedad, días de vacaciones, prima vacacional, aguinaldo y horas extra. Hay un problema que nadie ha corregido: **los días de vacaciones siguen calculándose con la tabla anterior a la reforma de 2023 a la Ley Federal del Trabajo**, la de "vacaciones dignas". Un trabajador con un año cumplido recibe 6 días en lugar de 12.

El ejercicio es pedirle a Bob ese cambio y después revisar qué quedó registrado: en el código, en el proyecto y en el control de versiones. Es el tipo de cambio que un auditor va a querer rastrear.

¿Aún no tienes Bob? Activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**

> Todo el código y los datos son ficticios. El cálculo está simplificado para el ejercicio; no es asesoría laboral.

## Cómo seguir el ejercicio

No necesitas instalar nada más que Python 3.11 o posterior.

1. Abre en Bob **la carpeta `04-nomina`**, no la raíz del repositorio.
2. Mira el cálculo actual:

   ```
   python calcular_prestaciones.py 2026-10-20
   ```

3. En modo **Code**, pídele el cambio con tus palabras. Por ejemplo: *"Actualiza el cálculo de días de vacaciones a la reforma de 2023 de la Ley Federal del Trabajo."*

   Si prefieres otro cambio: *"Agrega el cálculo de la prima dominical: 25 % del salario diario por cada domingo trabajado."*

4. Cuando termine, revisa tres cosas:
   - La función que cambió o que se creó.
   - La carpeta `bitacora/`.
   - El mensaje de confirmación que te propone Bob en el panel de control de versiones.

5. Pregúntate qué le faltaría a ese registro para que lo acepte tu auditor.

¿Por qué pasó lo que pasó, si nadie lo pidió? Lo vemos en el ejercicio 6.

Pruebas:

```
python -m unittest
```

## Volver al estado inicial

```
git checkout inicio -- 04-nomina
git clean -fd 04-nomina
```

El segundo comando borra los archivos nuevos que haya creado el ejercicio, como las entradas de la bitácora.
