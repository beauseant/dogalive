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
			ws 		= wb.add_sheet('Resultados Pings',cell_overwrite_ok=True)

			ws.write(0, 2, 'FICHERO EXCEL CON LOS RESULTADOS DE LOS PINGS A HOSTS', estilo_titulo)
			ws.write(1,4, 'Fecha: %s'%fecha, estilo_titulo)

			ws.write(5, 0, 'IP', estilo_cab)
			ws.write(5, 1, 'Nombre', estilo_cab)
			ws.write(5, 2, 'Status (20 ultimos pings)', estilo_cab)

			hosts = gdb.recuperarHosts()
			cont_exc_host = 6;

			for host in hosts:
				ws.write(cont_exc_host, 0, host[1])
				ws.write(cont_exc_host, 1, host[2])
				ultimos_escaneos = gdb.recuperarUltimosEscaneosPorHost( host[0], corte )
				cont_exc_status = 2

				for escaneo in ultimos_escaneos:

					if (escaneo[0] == 1):
						ws.write (cont_exc_host, cont_exc_status, escaneo[0], estilo_vivo)
					else:
						ws.write (cont_exc_host, cont_exc_status, escaneo[0])
					cont_exc_status = cont_exc_status + 1

				total_escaneos = gdb.recuperarEscaneosPorHost( host[0])
				cont_vivos = 0
				cont_total = 0
				for escaneo in total_escaneos:
					if (escaneo[0] == 1):
						cont_vivos = cont_vivos + 1
					cont_total = cont_total + 1

				ws.write(5, len(ultimos_escaneos)+2, 'Vivos/Total', estilo_cab)
				ws.write (cont_exc_host, len(ultimos_escaneos)+2, str(cont_vivos) + '/' + str(cont_total))
				cont_exc_host = cont_exc_host + 1

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



