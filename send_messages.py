import sqlite3
import pywhatkit
import time
from datetime import datetime, timedelta

# Conexión a las bases de datos
conn_pedidos = sqlite3.connect('pedidos.db')
conn_sku_asin = sqlite3.connect('sku_asin.db')
conn_mensajes = sqlite3.connect('mensajes.db')
cursor_pedidos = conn_pedidos.cursor()
cursor_sku_asin = conn_sku_asin.cursor()
cursor_mensajes = conn_mensajes.cursor()

# Diccionario para mapear países a prefijos telefónicos y dominios de Amazon
pais_prefijo_dominio = {
    "España": {"prefijo": "34", "dominio": ".es"},
    "Alemania": {"prefijo": "49", "dominio": ".de"},
    "Reino Unido": {"prefijo": "44", "dominio": ".co.uk"},
    "Francia": {"prefijo": "33", "dominio": ".fr"},
    "Italia": {"prefijo": "39", "dominio": ".it"},
    # Añade más países aquí
}

# Obtener la fecha del día anterior
fecha_ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

# Consultar los pedidos del día anterior
cursor_pedidos.execute("SELECT nombre_cliente, telefono, pais, producto, sku FROM pedidos WHERE fecha_pedido = ?", (fecha_ayer,))
pedidos = cursor_pedidos.fetchall()

# Tiempo entre mensajes en segundos
delay = 60

# Hora y minuto inicial para enviar el primer mensaje
hora_inicio = 10
minuto_inicio = 0

# Archivo de log para registrar errores
log_file = open("error_log.txt", "a")

# Función para obtener el ASIN y MaterialTipoUUID a partir del SKU
def obtener_asin_y_tipo(sku):
    cursor_sku_asin.execute("SELECT asin, MaterialTipoUUID FROM sku_asin WHERE sku=?", (sku,))
    result = cursor_sku_asin.fetchone()
    return result if result else (None, None)

# Función para obtener el mensaje a partir del MaterialTipoUUID y el dominio
def obtener_mensaje(material_tipo_uuid, dominio):
    cursor_mensajes.execute("SELECT mensaje FROM mensajes WHERE MaterialTipoUUID=? AND dominio=?", (material_tipo_uuid, dominio))
    result = cursor_mensajes.fetchone()
    return result[0] if result else None

# Procesar y enviar los mensajes para los pedidos obtenidos
for pedido in pedidos:
    try:
        nombre = pedido[0]
        telefono = pedido[1]
        pais = pedido[2]
        producto = pedido[3]
        sku_list = pedido[4].split(',')  # Suponiendo que los SKUs están separados por comas

        # Obtener el prefijo y el dominio de Amazon según el país
        info_pais = pais_prefijo_dominio.get(pais)
        if not info_pais:
            raise ValueError(f"No se encontró información para el país {pais}")

        prefijo = info_pais["prefijo"]
        dominio = info_pais["dominio"]
        
        # Formatear el número de teléfono
        telefono_formateado = f"+{prefijo}{telefono}"

        # Construir la lista de enlaces de reseña y el mensaje personalizado
        enlaces_resena = []
        mensaje_completo = ""
        
        for sku in sku_list:
            asin, material_tipo_uuid = obtener_asin_y_tipo(sku)
            if asin:
                enlaces_resena.append(f"https://www.amazon{dominio}/review/create-review/?asin={asin}")
            else:
                enlaces_resena.append(f"https://www.amazon{dominio}/review/create-review?ie=UTF8&asin=&channel=glance-detail&ref_=cm_cr_dp_d_wr_but_top&"
                                      f"opt=1&pc=*&seller=A3A88YXYJWT44W")
            
            # Obtener el mensaje para el MaterialTipoUUID y el dominio
            mensaje = obtener_mensaje(material_tipo_uuid, dominio)
            if mensaje:
                mensaje_completo = mensaje.format(nombre=nombre, producto=producto, enlaces_resena=' | '.join(enlaces_resena))
            else:
                raise ValueError(f"No se encontró mensaje para MaterialTipoUUID {material_tipo_uuid} y dominio {dominio}")

        # Enviar el mensaje
        pywhatkit.sendwhatmsg(telefono_formateado, mensaje_completo, hora_inicio, minuto_inicio, 15, True, 2)
        print(f"Mensaje enviado a {nombre} ({telefono_formateado}) para los productos con SKU {pedido[4]}")
        
        # Incrementar el tiempo y esperar el delay
        minuto_inicio += delay // 60
        if minuto_inicio >= 60:
            minuto_inicio = minuto_inicio % 60
            hora_inicio += 1
        time.sleep(delay)

    except Exception as e:
        # Registrar el error en el log y continuar con el siguiente pedido
        log_file.write(f"Error con el cliente {nombre}, teléfono: {telefono_formateado}, producto: {producto}, SKU: {pedido[4]} - Error: {str(e)}\n")
        print(f"Error con el cliente {nombre}, teléfono: {telefono_formateado}. Error: {str(e)}")

# Cerrar el archivo de log y las conexiones a las bases de datos
log_file.close()
conn_pedidos.close()
conn_sku_asin.close()
conn_mensajes.close()
