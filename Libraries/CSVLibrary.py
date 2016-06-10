import csv
from collections import defaultdict

class CSVLibrary(object):

	def read_csv_file(self, filename, header='FALSE'):
		'''
		Returns a list of rows, with each row being a list of the data in each column
		Specify header as 'True' will show header row\n
		I.e. Given data.csv\n
			Name,Age,Title\n
			Lex,30,QC\n
			Dora,28,QC\n
		
			read csv file     data.csv | true
			>>>	[['Name','Age','Title'],['Lex','30','QC'],['Dora','28','QC']]
		'''

		data = []
		with open(filename) as f:
			reader = csv.reader(f, skipinitialspace=True)
			for row in reader:
				data.append(row)
				
			if header.lower() == 'false':
				del data[0]
			
		return data

	def read_csv_file_dict(self, filename):
		'''
		Returns a list of dictionary from csv content\n
		I.e. Given data.csv\n
			Name,Age,Title\n
			Lex,30,QC\n
			Dora,28,QC\n
		
			read csv file dict     data.csv
			>>>	[['Name':'Lex','Age':'30','Title':'QC'],['Name':'Dora','Age':'28','Title':'QC']]
		'''

		with open(filename) as f:
			reader = csv.reader(f, skipinitialspace=True)
			header = next(reader)
			data = [dict(zip(header, map(str, row))) for row in reader]
		return data

	def get_csv_column(self, filename, column):
		'''
		Return a full column from csv file\n
		I.e. Given data.csv\n
			Name,Age,Title\n
			Lex,30,QC\n
			Dora,28,QC\n
			Alan,26,Dev\n
			Lex,30,Dev\n
		
			get csv column     data.csv | Name
			>>>	['Lex',''Dora,'Alan','Lex']
		'''
		
		data = defaultdict(list)
		
		with open(filename) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				for k, v in row.items():
					data[k].append(v)
					
		return data[column]
		
	def lookup_csv_value(self, filename, lookupKey, lookupVal, returnKey, index=1):
		'''
        Return the value of the desired column base on a reference of lookup value
		Specify the index for the no of returned value\n
		I.e. Given data.csv\n
			Name,Age,Title\n
			Lex,30,QC\n
			Dora,28,QC\n
			Alan,26,Dev\n
			Lex,30,Dev\n
		
			lookup csv value     data.csv | Name | Lex | Title | 2
			>>>	Dev
		'''

		with open(filename) as f:
			reader = csv.reader(f, skipinitialspace=True)
			header = next(reader)
			listDict = [dict(zip(header, map(str, row))) for row in reader]
		
		count = 0
		if index < 1: index = 1
		
		for d in listDict:
			if d[lookupKey] == lookupVal:
				count = count + 1
			if count >= int(index):
				return d[returnKey]
		
		return None

	def lookup_csv_list(self, filename, lookupKey, lookupVal, returnKey):
		'''
		Return a list of values match a lookup refecence\n
		I.e. Given data.csv\n
			Name,Age,Title\n
			Lex,30,QC\n
			Dora,28,QC\n
			Alan,26,Dev\n
			Lex,30,Dev\n

			lookup csv list     data.csv | Name | Lex | Title
			>>>	['QC','Dev']
		'''
		
		list = []
		with open(filename) as f:
			reader = csv.reader(f, skipinitialspace=True)
			header = next(reader)
			data = [dict(zip(header, map(str, row))) for row in reader]
		
		for sRow in data:
			if sRow[lookupKey] == lookupVal:
				list.append(sRow[returnKey])
		return list		
		
	def lookup_csv_row(self, filename, lookupKey, lookupVal, index=1):
		'''
        Return a row base on a reference of lookup value
		Specify the index for the no of returned row\n
		I.e. Given data.csv\n
			Name,Age,Title\n
			Lex,30,QC\n
			Dora,28,QC\n
			Lex,30,Dev\n

			lookup csv row     data.csv | Name | Lex | 2
			>>>	['Name':'Lex','Age':'30','Title':'Dev']
		'''

		with open(filename) as f:
			reader = csv.reader(f, skipinitialspace=True)
			header = next(reader)
			listDict = [dict(zip(header, map(str, row))) for row in reader]
		
		count = 0
		if index < 1: index = 1
		
		for d in listDict:
			if d[lookupKey] == lookupVal:
				count = count + 1
			if count >= int(index):
				return d
		
		return None