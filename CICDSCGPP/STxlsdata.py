#!/usr/bin/python
import xlrd
import xlutils
from xlutils.copy import copy


filename = '/Users/StevenLee/Documents/PY Projects/CICDSCGPP/TestDataBook.xlsx'


def get_data(a, b):
    wb = xlrd.open_workbook(filename)
    cb = copy(wb)
    # cb.save('/Users/StevenLee/Desktop/test1.xls')
    wb.sheet_names()
    cSheet = cb.get_sheet(0)
    # cSheet.write(1,1,'no')
    wSheet = wb.sheet_by_index(0)
    wSheet.cell(1, 1)
    data = wSheet.cell_value(a, b)
    return data


def write_data(a, b, c):
    wb = xlrd.open_workbook(filename)
    cb = copy(wb)
    # wb.sheet_names()
    cSheet = cb.get_sheet(0)
    cSheet.write(a, b, c)
    cb.save('/Users/StevenLee/Desktop/testnew.xls')
    #wSheet = wb.sheet_by_index(0)
    # wSheet.cell(1,1)
    #data = wSheet.cell_value(a,b)
