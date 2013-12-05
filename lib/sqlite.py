#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import logging
import argparse
import date


class SQLite:
	_name	= 'sqlite.db'
	_con	= None
	_dir	= ''
	
	def __init__ ( self, direct ):

		self._dir = direct

		try:
		    self._con = lite.connect( self._name )            
		    
		except lite.Error, e:
		    
		    print "Error %s:" % e.args[0]
		    sys.exit(1)    

	def __del__ ( self ):
		if self._con:
			self._con.close()


	def crearTablaHosts ( self ):
		with self._con:  
			#Creando tabla con los distintos hosts
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS hosts")
			sql_sen = '''CREATE TABLE hosts (
				id_host INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
				ip VARCHAR(15) NOT NULL, 
				name VARCHAR(30))'''
			cur.execute(sql_sen)
			self._con.commit()

	def crearTablaFechas ( self ):
		with self._con:  
			#Creando tabla de fechas
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS dates")
			sql_sen = '''CREATE TABLE dates (
				id_date INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
				date DATE NOT NULL)'''
			cur.execute(sql_sen)
			self._con.commit()


	def crearTablaEscaneo ( self ):
		with self._con:  
			#Creando tabla con la fecha de realizacion de los distintos pings a los hosts
			#State 0=No responde 1=Activo
			cur = self._con.cursor()    
			cur.execute("DROP TABLE IF EXISTS escaneo")
			sql_sen = '''CREATE TABLE escaneo (
				id INTEGER NOT NULL, 
				date INTEGER NOT NULL, 
				state INT(1) NOT NULL,
				PRIMARY KEY (id,date),
				FOREIGN KEY (id) REFERENCES hosts(id_host),
				FOREIGN KEY (date) REFERENCES dates(id_date)
				)'''   
			cur.execute(sql_sen)
			self._con.commit()

	def crearTablas ( self, db ):
		db.crearTablaHosts()
		db.crearTablaFechas()
		db.crearTablaEscaneo()


	'''def insertarHosts( self ):
		with self._con:    
			cur = self._con.cursor()
			cur.executemany ("INSERT INTO hosts (id_host, name) VALUES (?,?)", item)
			self._con.commit()'''
	

if __name__ == "__main__":

	parser	= argparse.ArgumentParser ( description= '' )
	parser.add_argument('--d', action="store_true", help='imprimir informacion de debug')

	args	 =	parser.parse_args()

	if args.d:
		logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

	db = SQLite ('SQLitePrueba/')

	r = db.crearTablas ( db )
	print 'Fin del proceso'






