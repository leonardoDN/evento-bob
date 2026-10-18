# Ejercicio 1: lo que nadie quiere tocar

Tres módulos de sistemas "de toda la vida", escritos como se escribían entonces: sin documentación, con reglas de negocio enterradas en el código y con cambios de varias manos a lo largo de los años. El reto es entenderlos con ayuda de Bob, sin leerlos línea por línea.

| Carpeta | Tecnología | Qué hace |
|---|---|---|
| `rpg-facturacion/` | RPG IV en formato fijo, DDS y CL (IBM i) | Factura pedidos, aplica descuentos e IVA y actualiza el saldo del cliente |
| `cobol-intereses/` | COBOL, copybooks y JCL (z/OS) | Corrida mensual de intereses ordinarios y moratorios de una cartera de crédito |
| `php-portal-pedidos/` | PHP 5 con `mysql_*` | Portal web donde distribuidores y vendedores capturan pedidos |

¿Aún no tienes Bob? Activa tu cuenta de prueba en **https://bob.ibm.com/trial?bpid=zu2kp7r**

## Cómo seguir el ejercicio

Abre **cada módulo en su propia ventana** de Bob (por ejemplo, la carpeta `rpg-facturacion`). Así Bob trabaja solo con ese código y nada más.

1. Cambia a modo **Ask**.
2. Ejecuta `/init` para que Bob analice el módulo y genere su `AGENTS.md`.
3. Pregúntale lo que le preguntarías a la persona que lo escribió. Por ejemplo:
   - ¿Qué hace este programa, en términos de negocio?
   - ¿Qué reglas de descuento o de cálculo aplica, y en qué casos cambian?
   - ¿Qué pasaría si lo ejecuto en enero? ¿Y en diciembre?
   - ¿Hay partes que nunca se ejecutan?
   - Si tuviera que cambiar el IVA, ¿qué tendría que tocar?

Compara lo que te responde con lo que encuentres tú en el código. Si Bob afirma algo, pídele que te muestre la línea.

Ninguno de los módulos necesita compilarse ni ejecutarse para el ejercicio, ni requiere un servidor IBM i, un mainframe o una base de datos.

## Volver al estado inicial

```
git checkout inicio -- 01-codigo-heredado
git clean -fd 01-codigo-heredado
```

El segundo comando borra los archivos que haya creado el ejercicio, como el `AGENTS.md` de cada módulo.
