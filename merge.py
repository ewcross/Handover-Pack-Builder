# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/17 16:55:24 by ecross            #+#    #+#              #
#    Updated: 2020/03/17 21:17:39 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import xlrd
from mailmerge import MailMerge

def get_file_lists(sheet):
    ind = 0
    for x in sheet.row(0):
        if x.value == 'Document':
            break
        ind += 1
    i = 0
    for x in sheet.col(ind):
        if x.value != xlrd.empty_cell.value:
            if sheet.cell(i, ind + 1).value == 'Copy':
                copy_list.append(str(sheet.cell(i, ind - 1).value) + '\\' + str(sheet.cell(i, ind).value))
            if sheet.cell(i, ind + 1).value == 'Merge':
                merge_list.append(str(sheet.cell(i, ind - 1).value) + '\\' + str(sheet.cell(i, ind).value))
        i += 1

def get_value(key, sheet):
    i = 0
    for x in sheet.row(0):
        if key == x.value:
            return str(sheet.cell(1, i).value)
        i += 1

def make_merges(sheet, file_list):
    ref = sheet.cell(1, 1).value
    for doc in file_list:
        with MailMerge(doc) as document:
            mydict = {}
            merge_fields = document.get_merge_fields()
            for f in merge_fields:
                mydict[f] = get_value(f.replace('_', ' '), sheet)
            print(mydict)
            #document.merge(**mydict)
            #document.write(doc[:2] + '_merged.docx')
            print(doc[:2] + '_' + ref + '_merged.docx')

copy_list = []
merge_list = []
dummy_merge_list = ['06.docx']

with xlrd.open_workbook('book.xlsx', on_demand = True) as workbook:
    get_file_lists(workbook.sheet_by_name('HOP Merge'))
    make_merges(workbook.sheet_by_name('A Merge Data'), dummy_merge_list)
print('copy_list:')
for x in copy_list:
  print(x)
print('merge_list:')
for x in merge_list:
  print(x)
