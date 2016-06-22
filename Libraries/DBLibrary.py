#!/usr/bin/python
# -*- coding: <ascii> -*-

import pymssql
import csv
from collections import defaultdict
from robot.api import logger

class DBLibrary(object):
	def __init__(self):
		self._dbconnection = None
	
	def connect_to_database(self, dbServer, dbUser, dbPass, dbDatabase, dbPort=1433, dbQTimeout=0, dbLoginTimeout=60, charSet='UTF-8'):
		try:
			self._dbconnection = pymssql.connect(server=dbServer, user=dbUser, password=dbPass, database=dbDatabase, port=dbPort, timeout=dbQTimeout, login_timeout=dbLoginTimeout, charset=charSet, as_dict=False)
		except Exception as e:
			logger.error(e)
	
	def connect_to_database_by_cfFile(self, filename):
		dict = {}
		
		f = open(filename)
		for lines in f:
			items = lines.split('=', 1)
			dict[items[0]]=items[1].rstrip('\n')
		
		try:
			self._dbconnection = pymssql.connect(server=dict.get('dbServer'), user=dict.get('dbUser'), password=dict.get('dbPassword'), database=dict.get('dbDataBase'), timeout=int(dict.get('dbQueryTimeout')), login_timeout=int(dict.get('dbLoginTimeout')), charset='UTF-8', as_dict=False, port=int(dict.get('dbPort')))
		except Exception as e:
			logger.error(e)
	
	def disconnect_from_database(self):
		self._dbconnection.close()
	
	def get_query_result_csv(self, sql, csvFile):
		cur = self._dbconnection.cursor()  
		cur.execute(sql + ';')
		rows = cur.fetchall()
		
		columns = []
		for column in cur.description:
			columns.append(column[0])
		
		with open(csvFile, "wb") as outfile:
			writer = csv.writer(outfile)
			writer.writerow(columns)
			for row in rows:
				writer.writerow([unicode(s).encode("utf-8") for s in row])