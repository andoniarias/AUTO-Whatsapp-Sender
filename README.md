
# WhatsApp Automated Message Sender for Amazon Product Reviews

This Python script automates the process of sending personalized WhatsApp messages to customers, asking them to leave a review for the products they purchased on Amazon. The script connects to three SQLite databases to retrieve order information, product details (SKU and ASIN), and custom messages based on the product material type.

## Features

- **Automated Messaging:** Sends WhatsApp messages to customers based on their orders from the previous day.
- **Personalized Messages:** Messages are customized based on the product's material type and the customer's country, ensuring relevancy.
- **Error Handling:** Any errors during the process are logged in `error_log.txt`, and the script continues with the next order.
- **Support for Multiple SKUs:** If an order includes multiple SKUs, the script generates a single message with review links for each product.

## Database Structure

This project requires three SQLite databases to function correctly. Below is the structure of each database:

### 1. `pedidos.db` (Orders Database)

This database stores information about customer orders.

- **`id_pedido`** (INTEGER, Primary Key, Auto Increment): Unique identifier for each order.
- **`nombre_cliente`** (TEXT): Name of the customer.
- **`telefono`** (TEXT): Customer's phone number.
- **`pais`** (TEXT): Customer's country.
- **`producto`** (TEXT): Description of the product(s).
- **`sku`** (TEXT): SKU code(s) of the product(s), separated by commas if multiple.
- **`fecha_pedido`** (DATE): Date the order was placed.

#### Example:
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

### 2. `sku_asin.db` (SKU-ASIN Mapping Database)

This database maps SKU codes to their corresponding ASINs on Amazon and includes the material type UUID for each product.

- **`sku`** (TEXT, Primary Key): SKU code of the product.
- **`asin`** (TEXT): Corresponding ASIN on Amazon.
- **`MaterialTipoUUID`** (TEXT): Unique identifier for the product's material type.

#### Example:
```sql
CREATE TABLE sku_asin (
    sku TEXT PRIMARY KEY,
    asin TEXT,
    MaterialTipoUUID TEXT
);
```

### 3. `mensajes.db` (Messages Database)

This database stores the custom message templates based on the material type and Amazon domain.

- **`MaterialTipoUUID`** (TEXT, Primary Key): Unique identifier for the material type.
- **`dominio`** (TEXT): Amazon domain (e.g., `.es`, `.de`, `.co.uk`).
- **`mensaje`** (TEXT): Custom message template for the product material and domain.

#### Example:
```sql
CREATE TABLE mensajes (
    MaterialTipoUUID TEXT PRIMARY KEY,
    dominio TEXT,
    mensaje TEXT
);
```

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/whatsapp-automated-messaging.git
    ```

2. **Install dependencies:**
    ```bash
    pip install pywhatkit
    ```

3. **Prepare the databases:**
   - Create the SQLite databases (`pedidos.db`, `sku_asin.db`, `mensajes.db`) with the structures described above.
   - Populate the databases with your data.

## Usage

Run the script to send messages to customers based on their orders from the previous day:
```bash
python send_messages.py
```

The script will:
- Connect to the databases to retrieve order details.
- Generate personalized WhatsApp messages with review links.
- Send the messages to the customers.
- Log any errors in `error_log.txt` for manual follow-up.

## Error Handling

If any error occurs (e.g., missing data, connection issues), the script logs the error in `error_log.txt` and continues processing the next order.

## Contributions

Feel free to fork this repository and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
