Dogalive
========

Programa en Python utilizado para comprobar si los nodos de una red se encuentran activos.

--------------

Programa que recorre los nodos de una red mediante hilos y escanea su estado (vivo o muerto). La información de los hosts y escaneos se almacena en una base de datos SQLite. Dogalive permite generar reportes en formato excel.

**Condiciones iniciales:**

- Tener instaladas las librerias de Python: 
	- xlwt (generación de reportes)
	- sqlite3 (base de datos SQLite)
	- datetime

**Objetivos**

- Crear una librería que permita analizar de manera automatizada el estado de los nodos de una red.
- Generar reportes con la información recogida en la base datos y que faciliten el análisis de la información.
- Permitir un alto de grado de personalización en las características de los escaneos a realizar por el usuario (especificación del número de hilos, rango de IPs, base de datos, etc.).

Dogalive permite hacer más sencilla la tarea de comprobación de estado de un gran número de nodos. Mediante el uso de hilos, el escaneo se ve optimizado y el tiempo de ejecución necesario es reducido. El número de hilos es definido por el usuario en función de sus preferencias, al igual que el rango de IPs que se quieren comprobar. 
La base de datos SQLite es portable y no requiere configuración inicial, por lo que el usuario no necesita crear nuevos usuarios y contraseñas.


**Comandos**

scan.py [--d] [--create] hilos segmento inicio final
		--d: Imprime la información de debug.
		--create: Se reinicia la base de datos. Se borran todos los datos.
		segmento: Segmento IP en el cual se recorrerán los nodos.
		inicio: IP de inicio.
		final: IP de fin.
		

report.py [--d] db fs n
		--d: Imprime la información de debug.
		db: Se debe especificar la ruta de la base de datos a consultar en el reporte.
		fs: El fichero de salida en el cual se almacenará la información recogida de la base de datos. Debe ser un .xls.
		n: Solo se recogen los n últimos pings realizados. 


Para cambiar la base de datos en la cual se están almacenando los distintos escaneos de los nodos se debe modificar la línea de código:
		gdb = lib.operacionesDB.operacionesDB ('./', 'sqlite.db', dateToday)


**Ejecución de los ejemplos**

        Ejemplo 1:
        python scan.py 5 192.168.135 10 50
        Realiza un escaneo con 5 hilos del rango de IPs: 192.198.135.10 - 192.168.135.50

        Ejemplo2:
        python scan.py --d 15 192.168.126 0 145
        Modo debug. Realiza un escaneo mediante 15 hilos del rango de IPs: 192.168.126.0 - 192.168.126.145.

        Ejemplo3:
        python scan.py --d --create 4 192.168.151 8 20
        

        Ejemplo4:
        report.py --d sqlite.db reporte.xls 1
        Genera un reporte de los escaneos almacenados en la base de datos sqlite.db (que se encuentra en el mismo directorio) y lo exporta como reporte.xls. El reporte contiene el último escaneo realizado.

	Ejemplo5:
        report.py ../bases_datos/sqlite.db 15-02-13.xls 35
        Genera un reporte de los escaneos almacenados en la base de datos sqlite.db (que se encuentra en el directorio ../bases_datos/) y lo exporta como 15-02-13.xls. El reporte contiene los últimos 35 escaneos realizados.
        

NOTA: Este programa no requiere de ficheros de configuración.





