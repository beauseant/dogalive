import Queue
import time
import argparse
import logging
import lib.threadping
import datetime
import lib.operacionesDB
import xlwt


def main( queue, log, args ):

	num_hilos 	= args.hilos
	inicio		= args.inicio
	final		= args.final
	direc_base	= args.segmento + '.' 
	
	#generamos los hilos que queremos y en cada uno pasamos la cola como instancia y el identificador:
	for i in range( num_hilos ):
		t = lib.threadping.ThreadPing (queue, i, log )
		t.setDaemon ( True )
		t.start()

	#Metemos en la cola lo que queremos procesar y que sera recogido por los hilos anteriores:
	for host in range ( inicio , int (final) ) :
		queue.put(direc_base + str (host) )

	#Nos quedamos esperando a que no quede nada por procesar:
	queue.join()

	#Recogemos los datos de cada uno de los hilos:
	Salida = {}
	for i in range( num_hilos ):
		Salida.update ( t.getResultados () )



	#Aqui debemos llamar a la libreria que se encarga de grabar el log de las operaciones
	#debemos pasarle, ademas la fecha
	dateToday = datetime.date.today()
	gdb = lib.operacionesDB.operacionesDB ('./', 'sqlite.db', dateToday)


	#Si hemos pasado create como parametro encontes borramos toda la base de datos y la creamos de nuevo:
	if args.create:
		gdb.reiniciarDB()


	id_date 	= gdb.insertarFecha()

	num_items 	= 0
	num_vivos	= 0

	#Mayor velocidad en las insercciones:
	gdb.setTransaccion ( 0 )
	for ip,status in Salida.iteritems ():
		num_items += 1
		try:
			num_vivos += status[1]
			id_host = gdb.insertarHost (ip , status[0])
			gdb.insertarEscaneo(id_host,id_date, status[1])
		except Exception as e:
			print 'No se ha podido registrar el log del host ' + ip

	logging.debug ( "escaneados: %s. Vivos:%s" % ( num_items, num_vivos )	)

	gdb.actualizarTotales ( id_date, num_items, num_vivos )


	#gdb.mostrarHosts()
	#gdb.mostrarFechas()
	#gdb.mostrarEscaneos()
	

if __name__ == "__main__":
	log = 0
	parser    = argparse.ArgumentParser ( description= 'ping con hilos' )
	parser.add_argument('--d', action="store_true", help='imprimir informacion de debug')
	parser.add_argument('--create', action="store_true", help='imprimir informacion de debug')
	parser.add_argument('hilos', type=int, help='numero de hilos a lanzar')
	parser.add_argument('segmento', help='segmento a analizar, ej: 192.168.149')
	parser.add_argument('inicio', type=int, help='maquina inicial, ej:30 empezaria en [segmento].30')
	parser.add_argument('final', type=int, help='maquina final, ej:200')

	args     =    parser.parse_args()

	if args.d:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		log = 1


	queue = Queue.Queue()

	start = time.time()

	main( queue, log, args )


	logging.debug ( "Elapsed Time: %s" % (time.time() - start) )
