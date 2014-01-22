import Queue
import time
import argparse
import logging
import lib.threadping
import datetime
import lib.operacionesDB
from lib.xlwt import *
import os


class report:

	def main( queue, log, args ):

		base_datos = args.db
		fichero_excel = args.fs
		corte = args.n

		if (not os.path.isfile(base_datos)):
			print 'La base de datos especificada no existe'
			logging.debug ('La base de datos especificada no existe')

		else:

			#Aqui debemos llamar a la libreria que se encarga de realizar las operaciones de la base de datos
			#debemos pasarle, ademas la fecha
			dateToday = datetime.date.today()
			gdb = lib.operacionesDB.operacionesDB ('./', base_datos, dateToday)
			fecha = dateToday.strftime("%Y-%m-%d")

		
			wb = Workbook()
			estilo_titulo 	= easyxf('font: bold on')
			estilo_cab 	= easyxf('font: color white, bold on; pattern: pattern solid, pattern_fore_colour black, pattern_back_colour black')
			estilo_vivo 	= easyxf('pattern: pattern solid, pattern_fore_colour lime, pattern_back_colour lime')
			estilo_muerto 	= easyxf('pattern: pattern solid, pattern_fore_colour pale_blue, pattern_back_colour pale_blue')
			estilo_vacio 	= easyxf('pattern: pattern solid, pattern_fore_colour light_orange, pattern_back_colour light_orange')
			ws 		= wb.add_sheet('Resultados Pings',cell_overwrite_ok=True)

			ws.write(0, 2, 'FICHERO EXCEL CON LOS RESULTADOS DE LOS PINGS A HOSTS', estilo_titulo)
			ws.write(1,4, 'Fecha: %s'%fecha, estilo_titulo)

			ws.write(5, 0, 'IP', estilo_cab)
			ws.write(5, 1, 'Nombre', estilo_cab)


			cont_exc_host = 6;
			fechas_dict = {}
			hosts_dict = {}

			fechas = gdb.recuperarFechas()
			for fecha in fechas:	
				fechas_dict [fecha[0]] = fecha[3]

			tamanyo = len(fechas)

			hosts = gdb.recuperarHosts()
			for host in hosts:
				hosts_dict [host[0]] = host [1]

			print fechas_dict.keys()
			for h in hosts_dict.keys():
				cont_vivos = 0
				cont_total = 0
				ws.write(cont_exc_host, 0, hosts_dict[h])
				host_nombre = gdb.recuperarHostPorId (h)
				ws.write(cont_exc_host, 1, host_nombre[0][2])
				total_escaneos = gdb.recuperarEscaneosPorHost( h)
				ulti_escaneos = gdb.recuperarEscaneosPorHost( h )
				cont_exc_status = 2
				cont_corte = 0

				cont_vivos = 0
				cont_total = 0

				for escaneo in total_escaneos:
					if (escaneo[2] == 1):
						cont_vivos = cont_vivos + 1
					cont_total = cont_total + 1

				for f in reversed(fechas_dict.keys()):
					ws.write(5, cont_exc_status, fechas_dict[f], estilo_cab)
					ws.write (cont_exc_host, cont_exc_status, "X", estilo_vacio)
					for escaneo in reversed(ulti_escaneos):
						if (f == escaneo[1]):
							if (escaneo[2]==1):
								ws.write (cont_exc_host, cont_exc_status, escaneo[2], estilo_vivo)
							elif (escaneo[2]==0):
								ws.write (cont_exc_host, cont_exc_status, escaneo[2], estilo_muerto)
					cont_exc_status = cont_exc_status + 1	
					cont_corte = cont_corte + 1

					if (cont_corte >= corte):
						break;

				ws.write (cont_exc_host, cont_corte+2, str(cont_vivos) + '/' + str(cont_total))
				cont_exc_host = cont_exc_host + 1

			ws.write(5, cont_corte+2, 'Vivos/Total', estilo_cab)
			wb.save(fichero_excel)
	

	if __name__ == "__main__":
		log = 0
		parser    = argparse.ArgumentParser ( description= 'report excel pings realizados' )
		parser.add_argument('--d', action="store_true", help='imprimir informacion de debug')
		parser.add_argument('db', help='ruta de la base de datos')
		parser.add_argument('fs', help='ruta fichero de salida')
		parser.add_argument('n', type=int, help='recoger ultimos n pings realizados')

		args     =    parser.parse_args()

		if args.d:
			logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
			log = 1


		queue = Queue.Queue()

		start = time.time()

		main( queue, log, args )


		logging.debug ( "Elapsed Time: %s" % (time.time() - start) )



