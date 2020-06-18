## DOCUMENTO DE COMPRECION API RESTFul

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


---

## METODO SENSOR: Esta función es la encargada de recibir el request del sensor al determinar la existencia de un evento. Estos eventos serán tres:
1. El primer evento es donde en sensor es combinado con un usuario; ya en el sensor estará precargado el Device-Id, Device-Type. Este evento se dará a la hora de configurar por primera vez el device del usuario y/o modificaciones del usuario en la DB de device.
2. El segundo evento es donde el sensor mandara una señal periódica, indicando que se encuentra activo. Esto será a través de la variable Status = 1, que indicará que no hay novedad y está activo dentro del sistema.
3. El tercer evento es donde el sensor detecta presencia de gas, y comenzará un proceso interno del sensor a mandar periódicamente reportes del evento e indicará el nivel de alarma que dependerá de la concentración de gas más el tiempo transcurrido en esa situación.  En este sentido la api rest, debe ser capaz de registrar dicho evento en la DB de eventos además de registrar el evento en FIREBASE para que sea capturado por la app. En esta parte del método en sistema debe ser capaz de tomar algunas decisiones en función de tipo de alarma, las cuales se analizarán previamente; sin embargo, los niveles de de Alarma serán los siguientes: Alarm = 0 = S/Event; Alarm = 1 = LOW; Alarm = 2 = MEDIUM; Alarm = 3 = HIGH; Alarm = 4 = ULTRA.
4. El modelo del paquete JSON es el siguiente:

* { 
	“sensor”: {
  		“Device-Id”: “xxxxxxxxxxxxx”,
		“Device-Type”: “xxxxxxxxxxxx”,
		“Status”: “1”
		“Alarm”: ”0”,
		“Acc-Time”: “1”,
		“TimeStamp”: “00000000000000”,
		“Concentración”: “00%”
	}
 }




---
