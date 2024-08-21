# WhatsApp Automated Message Sender for Amazon Product Reviews

This Python script automates the process of sending personalized WhatsApp messages to customers, asking them to leave a review for the products they purchased on Amazon. The script connects to three SQLite databases to retrieve order information, product details (SKU and ASIN), and custom messages based on the product material type.

## Features

- **Automated Messaging:** Sends WhatsApp messages to customers based on their orders from the previous day.
- **Personalized Messages:** Messages are customized based on the product's material type and the customer's country, ensuring relevancy.
- **Error Handling:** Any errors during the process are logged in `error_log.txt`, and the script continues with the next order.
- **Support for Multiple SKUs:** If an order includes multiple SKUs, the script generates a single message with review links for each product.

## Database Structure

### 1. `pedidos.db` (Orders Database)
- **`id_pedido`** (INTEGER, Primary Key, Auto Increment): Unique identifier for each order.
- **`nombre_cliente`** (TEXT): Name of the customer.
- **`telefono`** (TEXT): Customer's phone number.
- **`pais`** (TEXT): Customer's country.
- **`producto`** (TEXT): Description of the product(s).
- **`sku`** (TEXT): SKU code(s) of the product(s), separated by commas if multiple.
- **`fecha_pedido`** (DATE): Date the order was placed.

### 2. `sku_asin.db` (SKU-ASIN Mapping Database)
- **`sku`** (TEXT, Primary Key): SKU code of the product.
- **`asin`** (TEXT): Corresponding ASIN on Amazon.
- **`MaterialTipoUUID`** (TEXT): Unique identifier for the product's material type.

### 3. `mensajes.db` (Messages Database)
- **`MaterialTipoUUID`** (TEXT, Primary Key): Unique identifier for the material type.
- **`dominio`** (TEXT): Amazon domain (e.g., `.es`, `.de`, `.co.uk`).
- **`mensaje`** (TEXT): Custom message template for the product material and domain.

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
