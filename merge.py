# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/17 16:55:24 by ecross            #+#    #+#              #
#    Updated: 2020/03/18 10:45:58 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import xlrd
from mailmerge import MailMerge

def get_value(key, sheet):
    i = 0
    for x in sheet.row(0):
        if key == x.value:
            return str(sheet.cell(1, i).value)
        i += 1

class Merge:
    
    copy_list = []
    merge_list = []
    dummy_merge_list = [('06.docx', '06.docx')]

    def __init__(self, workbook):
        self.workbook = workbook
        sheet = workbook.sheet_by_name('A Merge Data')
        self.ref = sheet.cell(1, 1).value

    def fill_lists(self):
        sheet = self.workbook.sheet_by_name('HOP Merge')
        ind = 0
        for x in sheet.row(0):
            if x.value == 'Document':
                break
            ind += 1
        i = 0
        for x in sheet.col(ind):
            if x.value != xlrd.empty_cell.value:
                folder = str(sheet.cell(i, ind - 1).value) + '\\'
                #second member of pair to be changed to desired path of final file
                pair = (folder + str(sheet.cell(i, ind).value), str(sheet.cell(i, ind).value))
                if sheet.cell(i, ind + 1).value == 'Copy':
                    self.copy_list.append(pair)
                if sheet.cell(i, ind + 1).value == 'Merge':
                    self.merge_list.append(pair)
            i += 1

    def copy_files(self):
        for pair in self.copy_list:
            shutil.copy(pair[0], pair[1])

    def make_merges(self):
        #need to change from dummy here
        for doc in self.dummy_merge_list:
            with MailMerge(doc[0]) as document:
                mydict = {}
                merge_fields = document.get_merge_fields()
                for f in merge_fields:
                    mydict[f] = get_value(f.replace('_', ' '), self.workbook.sheet_by_name('A Merge Data'))
                #print(mydict)
                #document.merge(**mydict)
                #document.write(doc[:2] + '_merged.docx')
                print(doc[1][:2] + '_' + self.ref + '_merged.docx')

    
#object with:
#   workbook as openened by xlrd
#   string containing the job ref
#   two lists of tuple pairs, corresponding to the source file and destination filename
#   for files to be copied and those to be merged
#   method to fill lists
#   method to copy files using copy_list
#   method to make merges from merge_list

with xlrd.open_workbook('book.xlsx', on_demand = True) as workbook:
    merge_obj = Merge(workbook)
    print(merge_obj.ref)
    merge_obj.fill_lists()
    print(merge_obj.copy_list)
    print(merge_obj.merge_list)
    merge_obj.make_merges()

print(copy_list)
print(merge_list)
