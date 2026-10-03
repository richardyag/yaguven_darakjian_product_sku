# Darakjian — Auto SKU

## Qué problema resuelve

En Odoo 16, Darakjian generaba el "Internal Reference" (SKU / referencia interna) de
cada producto nuevo de forma automática, usando una app de terceros comprada hace
años: **`product_auto_sku`** (Globalteckz). El cliente no sabía que era un módulo
custom — lo daba por hecho como parte de Odoo. Al migrar a Odoo 19 ese módulo no vino,
y hoy el SKU se carga a mano.

## La mecánica real (confirmada contra la configuración viva de V16, no adivinada)

El registro de configuración real de `product_auto_sku` en V16 tiene:

```
sku_by_supplier   = apagado
sku_by_product    = "short_code" (usa un campo "Short Code" cargado a mano en cada categoría)
sku_by_attribute  = apagado
sequence          = 8 dígitos
hyphens (separador) = activado ('.')
```

Con eso, la fórmula de hoy es:

```
{Short Code de la categoría}.{siguiente número de UNA secuencia global de 8 dígitos}
```

Ejemplo real: categoría "Diamond Rings" tiene Short Code `DRNG` → `DRNG.00085941`.

La secuencia (`ir.sequence`, nombre "Product Sequence") es **una sola para todo el
catálogo**, nunca se reinicia por categoría. Los códigos viejos de 3 partes que
todavía se ven en el catálogo (ej. `BE.WATC.0053094`) son de una época en que
`sku_by_supplier` SÍ estaba activo (usaba las 2 primeras letras del proveedor); se
apagó en algún momento y los productos ya creados quedaron como estaban — no se
regeneran solos.

## Qué construye este módulo

Replica exactamente esa fórmula (la parte que de verdad usan hoy — el segmento de
proveedor y de atributos, que ya estaban apagados, no se reproducen; es fácil
agregarlos después si hiciera falta) como código propio, sin depender de Globalteckz
ni de ningún módulo de terceros:

- Campo **Short Code** en Categoría de Producto (Inventario > Configuración >
  Categorías de Producto) — se carga a mano, una vez por categoría.
- Un interruptor único por compañía (Inventario > Configuración > Auto SKU) para
  prender/apagar la generación automática.
- Al crear un producto nuevo: si el interruptor está activo, el producto no tiene ya
  una referencia cargada, y su categoría tiene un Short Code asignado, se le asigna
  automáticamente `{ShortCode}.{siguiente número}`. Si falta cualquiera de esas tres
  condiciones, no hace nada — se puede seguir cargando a mano sin problema.
- **Nunca pisa** una referencia ya cargada a mano o por una importación.
- La secuencia arranca en `11.000.000` — por encima del número más alto encontrado en
  TODO el catálogo migrado (10.042.892, incluyendo códigos viejos/no estándar), así
  que no hay forma de que choque con algo ya existente.

## Lo que falta para que funcione de punta a punta

El campo "Short Code" nace vacío en todas las categorías de "el test" — hay que
cargarlo. La forma más rápida es copiarlo directo de Odoo 16 (ya están cargados ahí
para la mayoría de las categorías) en vez de tipearlo a mano de nuevo; eso se puede
hacer con un script aparte, una sola vez, después de instalar este módulo.

## Qué NO hace (a propósito)

- No reproduce el segmento de proveedor ni el de atributos del módulo viejo — hoy
  Darakjian no los usa (los tenía apagados), así que no hay necesidad de construirlos
  todavía.
- No toca ningún producto ya existente ni le asigna una referencia retroactivamente —
  solo actúa en productos NUEVOS, de acá en adelante.
- No se instaló en ningún lado todavía. Este README y el código están listos para
  mostrarle a Gabriel antes de instalar nada, como se acordó.
