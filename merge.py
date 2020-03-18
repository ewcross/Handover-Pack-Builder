# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/17 16:55:24 by ecross            #+#    #+#              #
#    Updated: 2020/03/18 16:22:46 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import xlrd
import os
import shutil
from mailmerge import MailMerge

class Merge:
    
    copy_list = []
    merge_list = []

    def __init__(self, workbook):
        self.workbook = workbook
        sheet = workbook.sheet_by_name('A Merge Data')
        self.ref = sheet.cell(1, 1).value
        dst_root = '../'
        for d in os.listdir(dst_root):
            if d.startswith(self.ref):
                for f in os.listdir(dst_root + d):
                    if f.startswith('HOP'):
                        self.dst = dst_root + d + '/' + f
                        return
        self.dst = None
        print('Could not find output location.')

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
                #need to check on positions and directions of strokes
                src_folder = str(sheet.cell(i, ind - 1).value)
                if src_folder[len(src_folder) - 1] != '/':
                    src_folder += '/'
                if self.dst[len(self.dst) - 1] != '/':
                    self.dst += '/'
                #might need to return to a pair with path of each, if complete destination
                #file name is provided in spreadsheet
                tup = (src_folder, str(sheet.cell(i, ind).value), self.dst, str(sheet.cell(i, ind).value))
                if sheet.cell(i, ind + 1).value == 'Copy':
                    self.copy_list.append(tup)
                if sheet.cell(i, ind + 1).value == 'Merge':
                    self.merge_list.append(tup)
            i += 1

    def copy_files(self):
        for tup in self.copy_list:
            shutil.copy(tup[0] + tup[1], tup[2] + tup[3])

    def make_merges(self):
        
        def get_value(key, sheet):
            i = 0
            for x in sheet.row(0):
                if key == x.value:
                    return str(sheet.cell(1, i).value)
                i += 1

        for doc in self.merge_list:
            with MailMerge(doc[0] + doc[1]) as document:
                mydict = {}
                merge_fields = document.get_merge_fields()
                for f in merge_fields:
                    mydict[f] = get_value(f.replace('_', ' '), self.workbook.sheet_by_name('A Merge Data'))
                first_space = doc[1].index(' ')
                document.merge(**mydict)
                document.write(doc[2] + doc[3][:first_space] + ' ' + self.ref +  doc[3][first_space:])
                print('merged doc------>')
                print(doc[2] + doc[3][:first_space] + ' ' + self.ref +  doc[3][first_space:])
 
#object with:
#   workbook as openened by xlrd
#   string containing the job ref
#   two lists of tuples, containing:
#       (src folder, src file name, dest folder, dest file name)
#   for files to be copied and those to be merged
#   method to fill lists
#   method to copy files using copy_list
#   method to make merges from merge_list

with xlrd.open_workbook('book.xlsx', on_demand = True) as workbook:
    merge_obj = Merge(workbook)
    if merge_obj.dst == None:
        exit()
    merge_obj.fill_lists()
    #print(merge_obj.copy_list)
    #print(merge_obj.merge_list)
    merge_obj.copy_files()
    merge_obj.make_merges()
