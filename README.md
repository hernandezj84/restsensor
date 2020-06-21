# DOCUMENTO DE COMPRESION API RESTFul

El siguiente documento tiene como objetivo, desarrollar las bases de compresión de cada método a desarrollar para el funcionamiento del modelo.
Este api, será encargado de gestionar todas las transacciones tanto REQUEST como RESPONSE, de cada entidad interviniente en el sistema.
Toda la transmisión de datos será a través de paquetes JSON, la cuales tendrán una característica primaria y no podrá ser cambiada, al menos que se decida en un comité designado para lo mismo.
Estructura JSON: La estructura de los paquetes JSON será header, en el cual solo habrá características del paquete destinada a la caracterización del mismo, para ser interpretada por el sistema. En el body del paquete, irá todas las variables necesarias para el consumo por parte de las diferentes entidades del sistema. A continuación, se desarrolla un ejemplo:

* { 
	“sensor”: {
  		“Device-Id”: “xxxxxxxxxxxxx”,
		“Device-Type”: “xxxxxxxxxxxx”,
	}
 }
## IDs y serializacion de productos
Los ID son los códigos responsables de las transacciones de datos con las bases de datos. En este sentido se propone una estructura para el manejo interno de los mismos. Por otra parte la serialización de los productos será la cadena responsable de tener monitoreado los productos en manos del usuario. La serializacion será generada en una base de datos y se asignará su uso cuando el producto este listo para salir al mercado.

* **ENTIDADES:** Las entidades son los registros que tendrán un nombre propio dentro de los sistemas el cual se les es asignado mediante los ID.
* **ID USUARIO:** es una cadena única para cada usuario que será su identificador en el sistema. Esta cadena es para uso interno del sistema. Esta cadena estará compuesta por un sufijo fijo que se propone IOTUSER + una mascara de 8 dígitos.
* **DEVICE-TYPE:** cadena de texto que identifica el tipo de producto que es, compuesta por 6 caracteres en mayúscula. Por ejemplo el Sensor de fuga de gas glp sería, SFGGLP.
* **DEVICE-ID:** Este id debe utilizar la cadena de texto del DEVICE-TYPE, descrita en el punto anterior mas una mascara de 8 dígitos. Ver ejemplos
* **SERIALIZACION:** La serializacion es la cadena de texto que dará salida del producto para ser comercializado. El mismo estará compuesto por una cadena de texto + unamascara de 8 dígitos.

## Ejemplos
**DEVICE-ID**

*   **CADENA:** TTTTT-LLLL-NNNNN
*   "TTTTTT" es lo mismo que para el device type.
*   "LLLL" puede ser utilizado como referencia de ubicación del producto (4 caracteres alphanuméricos).
*   "NNNNN" es el número de identidad del producto (5 caracteres numéricos).
* Nota: Total 15 caracteres

**DEVICE-TYPE:**

*   **CADENA:** TTTTTT-AAAA-MMMM
*   "TTTTTT" es el tipo de sensor (6 caracteres). Por ejemplo: SFGLPG.
*   "AAAA" es un campo para especificar alguna aplicación en particular (4 caracteres).
*   "MMMM" es un campo para describir el modelo utilizado (4 caracteres).
* Nota: Los caracteres son alfanuméricos - Total 14 caracteres

**USER-ID**

* **CADENA:** IOTPTYUSER00000001
* Nota: Total 16 caracteres

**SERIALIZACION**

* **CADENA:** IOTSN-00000001

----------
### **BLOQUES E REGIONES PARA CONFORMACION DEL device_id**

SFGGLP-205-000001
SE LEERIA sensor de fuga de gas glp-panama-000001

**AMERICA DEL NORTE**

- 100 CANADA
- 101 EEUU
- 102 MEXICO

**CENTROAMERICA**

- 200 COSTA RICA
- 201 EL SALVADOR
- 202 GUATEMALA
- 203 HONDURAS
- 204 NICARAGUA
- 205 PANAMA

**AMERICA DEL SUR**

- 300 ARGENTINA
- 301 BOLIVIA
- 302 BRASIL
- 303 CHILE
- 304 COLOMBIA
- 305 ECUADOR
- 306 PARAGUAY
- 307 PERU
- 308 SURINAM
- 309 URUGUAY
- 310 VENEZUELA

**EL CARIBE Y LAS ANTILLAS**

- 400 CARIBE

---

# METODOS

## metodoJsonSensor() 

### Esta función es la encargada de recibir el request del sensor al determinar la existencia de un evento. Estos eventos serán tres:
1. El primer evento es donde en sensor es combinado con un usuario; ya en el sensor estará precargado el Device-Id, Device-Type. Este evento se dará a la hora de configurar por primera vez el device del usuario y/o modificaciones del usuario en la DB de device.
2. El segundo evento es donde el sensor mandara una señal periódica, indicando que se encuentra activo. Esto será a través de la variable Status = 1, que indicará que no hay novedad y está activo dentro del sistema.
3. El tercer evento es donde el sensor detecta presencia de gas, y comenzará un proceso interno del sensor a mandar periódicamente reportes del evento e indicará el nivel de alarma que dependerá de la concentración de gas más el tiempo transcurrido en esa situación.  En este sentido la api rest, debe ser capaz de registrar dicho evento en la DB de eventos además de registrar el evento en FIREBASE para que sea capturado por la app. En esta parte del método en sistema debe ser capaz de tomar algunas decisiones en función de tipo de alarma, las cuales se analizarán previamente; sin embargo, los niveles de de Alarma serán los siguientes: Alarm = 0 = NORMAL; Alarm = 1 = LOW; Alarm = 2 = MEDIUM; Alarm = 3 = HIGH; Alarm = 4 = ULTRA.
4. El modelo del paquete JSON es el siguiente:

## Paquete JSON

- **"device_id":** "string", --> 17 char
- **"alarm_level":** int, entre 0 y 4
- **"gas_percent":** int, entre 0 y 100,
- **"measured_volts":** float, 0 y 5
- **"acc_time":** int,
- **"gas_type":** int, 0 y 2
- **"time_stamp":** unix_time,
- **"battery_level":** int, 0 y 100
- **"rssi":** int, %
- **"jocker":** "string"


## Ejemplo

* { 
"device_id": "TTTTTT-LLLL-IIIII",
"alarm_level": 1,
"gas_percent": 75,
"measured_volts": 3.02,
"acc_time": 100,
"gas_type": 1,
"time_stamp": 1592605050,
"battery_level": 30,
"rssi": -90,
"jocker": "seudonimo"
}




---
