from openpyxl import load_workbook
from decimal import Decimal

class ExcelLibrary(object):
	
	def _read(self, f, r=True): return load_workbook(filename=f, read_only=r)
	def _sheet(self, f, s, r=True): return self._read(f, r)[str(s)]
	def _float(self, s): return float(str(s)) if self._isfloat(s) else s
	def _format(self, s): return str(s).replace('u','').replace('\'','')
	def _isfloat(self, s):
		try: float(str(s)) # for int, long and float
		except ValueError:
			try: complex(str(s)) # for complex
			except ValueError: return False
		return True
	
	def _data(self, file, sheet, noheader=True):
		data = [[self._float(str(x.value)) for x in row] for row in self._sheet(file, sheet).rows]
		header = data[0]
		if noheader: del data[0]
		return data, header
		
	def get_sheet_content_in_list(self, file, sheet, header='True'):
		return self._data(file, sheet, False)[0] if header.lower() == 'true' else self._data(file, sheet)[0]

	def get_sheet_content_in_dict(self, file, sheet):
		data, header = self._data(file, sheet)
		return [dict(zip(header, map(str, row))) for row in data]
		
	def get_row_by_index(self, file, sheet, rowIndex=1):
		for index, row in enumerate(self._data(file, sheet, False)[0]):
			if index == int(rowIndex)-1: return row
		
	def get_row_by_reference(self, file, sheet, refColumn, refValue, index=1):
		listDict = self.get_sheet_content_in_dict(file, sheet)
		for r, dict in enumerate(listDict):
			print(self._format(dict[refColumn]), self._format(refValue), self._format(dict[refColumn]) == self._format(refValue))
			if dict[refColumn] == refValue: return dict.values()
		
	def get_column_by_index(self, file, sheet, rowIndex=1):
		return None
		
	def get_column_by_header(self, file, sheet, refColumn, refValue):
		return None
		
	def get_cell_value_by_index(self, file, sheet, columnIndex=1, rowIndex=1):
		return None
		
	def get_cell_value_by_reference(self, file, sheet, refColumn, refValue, returnColumn):
		return None
	
	def search_column_by_condition(self, file, sheet, column, refValue, condition):
		return None