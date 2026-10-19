# Ejercicio 3: escribir sobre el código

Tesorería recibe cada día decenas de pagos por SPEI y tiene que conciliarlos contra las facturas por cobrar. Este programa lo hace: por cada pago consulta al banco si la transferencia quedó liquidada y luego la cruza con la factura que trae en la referencia.

El problema: el servicio del banco a veces tarda y a veces no contesta. Cuando eso pasa, la conciliación se cae a la mitad y hay que volver a correrla completa. El ejercicio es arreglarlo **escribiendo la instrucción en la línea exacta del código** donde ocurre la llamada, sin abrir el chat.

¿Aún no tienes Bob? Activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**

> Todo el código y los datos son ficticios. El banco es un simulador que no sale a internet: tarda hasta poco más de un segundo y falla una de cada cuatro consultas, como el de verdad en un mal día.

## Cómo seguir el ejercicio

No necesitas instalar nada más que Python 3.11 o posterior.

1. Abre en Bob **la carpeta `03-conciliacion-de-pagos`**, no la raíz del repositorio.
2. Corre la conciliación un par de veces para ver el problema:

   ```
   python conciliar.py
   ```

3. Abre `conciliacion.py` y coloca el cursor en esta línea, dentro de `conciliar_pago`:

   ```python
   estado = banco_simulado.consultar_transferencia(pago["clave_rastreo"])
   ```

4. Activa la escritura asistida con el icono de varita, escribe la instrucción en la línea y pulsa **Generate**. Por ejemplo:

   *Reintentar hasta tres veces, esperando más entre cada intento; si aun así no responde, marcar el pago como por revisar y seguir con los demás.*

   Si solo pides el reintento, la conciliación todavía puede caerse cuando el banco falla tres veces seguidas; por eso conviene decirle también qué hacer en ese caso.

   Para probar dos instrucciones a la vez, inserta una línea justo arriba de la llamada al banco y escribe ahí: *Antes de consultar al banco, imprimir en pantalla la clave de rastreo y el importe del pago.* Pegada a la línea del `def`, Bob tiende a tomarla como descripción de la función.

5. Revisa el diferencial antes de aceptarlo y vuelve a correr `python conciliar.py`.

La escritura asistida dentro del archivo es una funcionalidad que IBM documenta como **vista previa** y trabaja sobre un archivo a la vez. Para cambios que cruzan varios archivos está el modo Agent.

Pruebas:

```
python -m unittest
```

## Volver al estado inicial

```
git checkout inicio -- 03-conciliacion-de-pagos
git clean -fd 03-conciliacion-de-pagos
```
