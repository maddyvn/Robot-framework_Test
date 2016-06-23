#!/usr/bin/python
# -*- coding: <uat-8> -*-

import pymssql
import csv
from xlsxwriter import Workbook
from collections import defaultdict
from robot.api import logger

class DBLibrary(object):
	"""
		Database Library for Robot-Framework
			Prequisite:
				- xlsxwriter (Excel file library) #http://xlsxwriter.readthedocs.io/index.html
				- pymssql 2.1.1 (Microsoft SQL Server API library) #http://www.pymssql.org/en/latest/ref/pymssql.html
				
			Install from cmd:
				pip install pymssql==2.1.1
				pip install xlsxwriter
	"""
	
	def __init__(self):
		self._dbconnection = None	#Database connection
	
	def connect_to_database(self, dbServer, dbUser, dbPass, dbDatabase, dbPort=1433, dbQTimeout=0, dbLoginTimeout=60, charSet='UTF-8'):
		"""
			Connect to database. Must be called before calling any query actions.
		"""
	
		try:
			self._dbconnection = pymssql.connect(server=dbServer, user=dbUser, password=dbPass, database=dbDatabase, port=int(dbPort), timeout=int(dbQTimeout), login_timeout=int(dbLoginTimeout), charset=charSet, as_dict=False)
		except Exception as e:
			logger.error(e)
	
	def connect_to_database_by_cfFile(self, filename):
		"""
			Connect to database. Must be called before calling any query actions.
			Format:
				dbServer=
				dbPort=
				dbUser=
				dbPassword=
				dbDataBase=
				dbQueryTimeout=0
				dbLoginTimeout=60
		"""
		
		dict = {}
		f = open(filename)
		for lines in f:
			items = lines.split('=', 1)
			dict[items[0]]=items[1].rstrip('\n')
			
		self.connect_to_database(dict.get('dbServer'), dict.get('dbUser'), dict.get('dbPassword'), dict.get('dbDataBase'), dict.get('dbPort'), dict.get('dbQueryTimeout'), dict.get('dbLoginTimeout'))
	
	def disconnect_from_database(self):
		"""
			Disconnect from current database connection. Should be called after finishing all query actions.
		"""
		self._dbconnection.close()
	
	def get_query_result_csv(self, sql, csvFile):
		"""
			Build a csv file from result set of the sql command
		"""
		
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
				
	def get_query_result_excel(self, sql, excelFile):
		"""
			Build an excel file from result set of the sql command
		"""
		
		cur = self._dbconnection.cursor()
		cur.execute(sql + ';')
		rows = cur.fetchall()
		
		columns = []
		for column in cur.description:
			columns.append(column[0])
		
		workbook = Workbook(excelFile)
		sheet = workbook.add_worksheet()
		for r, row in enumerate(rows):
			for c, col in enumerate(row):
				sheet.write(r, c, col)