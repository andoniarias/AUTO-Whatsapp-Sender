
# Envío Automatizado de Mensajes por WhatsApp para Reseñas de Productos en Amazon

Este script en Python automatiza el proceso de envío de mensajes personalizados por WhatsApp a los clientes, solicitándoles que dejen una reseña para los productos que compraron en Amazon. El script se conecta a tres bases de datos SQLite para recuperar la información de los pedidos, los detalles de los productos (SKU y ASIN), y los mensajes personalizados según el tipo de material del producto.

## Características

- **Mensajería Automatizada:** Envía mensajes por WhatsApp a los clientes según sus pedidos del día anterior.
- **Mensajes Personalizados:** Los mensajes se personalizan según el tipo de material del producto y el país del cliente, asegurando relevancia.
- **Manejo de Errores:** Cualquier error durante el proceso se registra en `error_log.txt`, y el script continúa con el siguiente pedido.
- **Soporte para Múltiples SKUs:** Si un pedido incluye múltiples SKUs, el script genera un solo mensaje con enlaces de reseña para cada producto.

## Estructura de las Bases de Datos

Este proyecto requiere tres bases de datos SQLite para funcionar correctamente. A continuación se describe la estructura de cada base de datos:

### 1. `pedidos.db` (Base de Datos de Pedidos)

Esta base de datos almacena la información sobre los pedidos de los clientes.

- **`id_pedido`** (INTEGER, Primary Key, Auto Increment): Identificador único de cada pedido.
- **`nombre_cliente`** (TEXT): Nombre del cliente.
- **`telefono`** (TEXT): Número de teléfono del cliente.
- **`pais`** (TEXT): País del cliente.
- **`producto`** (TEXT): Descripción del/los producto(s).
- **`sku`** (TEXT): Código SKU del/los producto(s), separados por comas si hay múltiples.
- **`fecha_pedido`** (DATE): Fecha en la que se realizó el pedido.

#### Ejemplo:
```sql
CREATE TABLE pedidos (
    id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_cliente TEXT,
    telefono TEXT,
    pais TEXT,
    producto TEXT,
    sku TEXT,
    fecha_pedido DATE
);
```

### 2. `sku_asin.db` (Base de Datos de Mapeo SKU-ASIN)

Esta base de datos mapea los códigos SKU a sus correspondientes ASIN en Amazon e incluye el UUID del tipo de material para cada producto.

- **`sku`** (TEXT, Primary Key): Código SKU del producto.
- **`asin`** (TEXT): ASIN correspondiente en Amazon.
- **`MaterialTipoUUID`** (TEXT): Identificador único del tipo de material del producto.

#### Ejemplo:
```sql
CREATE TABLE sku_asin (
    sku TEXT PRIMARY KEY,
    asin TEXT,
    MaterialTipoUUID TEXT
);
```

### 3. `mensajes.db` (Base de Datos de Mensajes)

Esta base de datos almacena las plantillas de mensajes personalizados basados en el tipo de material y el dominio de Amazon.

- **`MaterialTipoUUID`** (TEXT, Primary Key): Identificador único del tipo de material.
- **`dominio`** (TEXT): Dominio de Amazon (por ejemplo, `.es`, `.de`, `.co.uk`).
- **`mensaje`** (TEXT): Plantilla de mensaje personalizado para el material y el dominio.

#### Ejemplo:
```sql
CREATE TABLE mensajes (
    MaterialTipoUUID TEXT PRIMARY KEY,
    dominio TEXT,
    mensaje TEXT
);
```

## Instalación

1. **Clona el repositorio:**
    ```bash
    git clone https://github.com/yourusername/whatsapp-automated-messaging.git
    ```

2. **Instala las dependencias:**
    ```bash
    pip install pywhatkit
    ```

3. **Prepara las bases de datos:**
   - Crea las bases de datos SQLite (`pedidos.db`, `sku_asin.db`, `mensajes.db`) con las estructuras descritas anteriormente.
   - Poblá las bases de datos con tus datos.

## Uso

Ejecuta el script para enviar mensajes a los clientes según sus pedidos del día anterior:
```bash
python send_messages.py
```

El script hará lo siguiente:
- Conectará a las bases de datos para recuperar los detalles de los pedidos.
- Generará mensajes personalizados de WhatsApp con enlaces de reseña.
- Enviará los mensajes a los clientes.
- Registrará cualquier error en `error_log.txt` para seguimiento manual.

## Manejo de Errores

Si ocurre algún error (por ejemplo, datos faltantes, problemas de conexión), el script registrará el error en `error_log.txt` y continuará procesando el siguiente pedido.

## Contribuciones

Siéntete libre de hacer un fork de este repositorio y enviar pull requests. ¡Las contribuciones son bienvenidas!

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.
