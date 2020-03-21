# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/17 16:55:24 by ecross            #+#    #+#              #
#    Updated: 2020/03/21 11:54:31 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import xlrd
import os
import shutil
from mailmerge import MailMerge
#import win32com.client as win32

#/usr/bin/env python

def exit_func():
    print()
    input('Press any key to exit.')
    exit()

#class with:
#   workbook as openened by xlrd
#   string containing the job ref
#   two lists of tuples, containing:
#       (src folder, src file name, dest folder, dest file name)
#   for files to be copied and those to be merged
#   method to fill lists
#   method to copy files using copy_list
#   method to make merges from merge_list

class Merge:
    
    copy_list = []
    merge_list = []
   
    #init method sets ref attribute to job reference
    #and finds project install.xlsx workbook and merge destination location

    def __init__(self, ref):
        self.ref = ref
        #needs changing to current dir
        dst_root = '../'
        found = 0
        for dirs in os.listdir(dst_root):
            if dirs.startswith(self.ref):
                found = 1
                path = dst_root + dirs
                self.find_workbook(path)
                self.find_dst_path(path)
        #if job folder not found, error and exit
        if found == 0:
            print('ERROR. Could not find job folder for job: ' + self.ref, end='')
            print(' in current location (' + os.path.realpath(__file__) + ')')
            exit_func()
        if self.dst == None or self.workbook == None:
            exit_func()
    
    #method to look in job folder for HOP subfolder, and
    #if found, set as destination for handover pack

    def find_dst_path(self, path):
        for dirs in os.listdir(path):
            if dirs.startswith('Handover'):
                self.dst = os.path.join(path, dirs)
                return
        self.dst = None
        print('ERROR. Could not find output location. Please check \'HOP\' folder', end='')
        print(' exists in job file for ' + self.ref + ' .')
   
    #method to search job folder for install workbook in 'Install' subfolder
    #and, if found, set as the workbook attribute

    def find_workbook(self, path):
        for dirs in os.listdir(path):
            if dirs.startswith('Install'):
                path = os.path.join(path, dirs)
                for files in os.listdir(path):
                    if files.endswith('xlsx'):
                        print('FOUND ' + path + '/' + files)
                        with xlrd.open_workbook(os.path.join(path, files), on_demand = True) as workbook:
                            self.workbook = workbook
                        return
        self.workbook = None
        print('ERROR. Could not find installation spreadsheet. Please check \'Install\' folder', end='')
        print(' exists in job file for ' + self.ref + ' ,')
        print(' and that it contains the installations spreadsheet.')

    def get_col(self, sheet, title):
        i = 0
        for x in sheet.row(0):
            if x.value == title:
                return (i)
            i += 1
        print('ERROR. Could not locate column with title \'' + title + '\' in Install', end='')
        print('spreadsheet. Please check \'HOP Merge\' sheet.')
        exit_func()
        return 0

    def fill_lists(self):
        sheet = self.workbook.sheet_by_name('HOP Merge')
        infile_col = self.get_col(sheet, 'Input Doc')
        outfile_col = self.get_col(sheet, 'Output Doc')
        i = 0
        for x in sheet.col(infile_col):
            if x.value != xlrd.empty_cell.value:
                #need to check on positions and directions of strokes
                src_folder = str(sheet.cell(i, infile_col - 1).value)
                if src_folder[len(src_folder) - 1] != '/':
                    src_folder += '/'
                if self.dst[len(self.dst) - 1] != '/':
                    self.dst += '/'
                #might need to return to a pair with path of each, if complete destination
                #file name is provided in spreadsheet
                tup = (src_folder, str(sheet.cell(i, infile_col).value), self.dst, str(sheet.cell(i, outfile_col).value))
                if sheet.cell(i, outfile_col + 1).value == 'Copy':
                    self.copy_list.append(tup)
                if sheet.cell(i, outfile_col + 1).value == 'Merge':
                    self.merge_list.append(tup)
                #if sheet.cell(i, outfile_col + 1).value == 'Edit':
                    #do something else with visio
            i += 1

    def copy_files(self):
        for tup in self.copy_list:
            shutil.copy(tup[0] + tup[1], tup[2] + tup[3])

    def get_value(self, key, sheet):
        i = 0
        for x in sheet.row(0):
            if key == x.value:
                return str(sheet.cell(1, i).value)
            i += 1

    def make_merges(self):
        
        for doc in self.merge_list:
            with MailMerge(doc[0] + doc[1]) as document:
                mydict = {}
                merge_fields = document.get_merge_fields()
                for f in merge_fields:
                    mydict[f] = self.get_value(f.replace('_', ' '), self.workbook.sheet_by_name('A Merge Data'))
                document.merge(**mydict)
                document.write(doc[2] + doc[3].replace('xxxx', self.ref[2:]))
                print('merged doc------>')
                print(doc[2] + doc[3].replace('xxxx', self.ref[2:]))

#class with:
#   list attribute containing all .doc and .docx files in specified directory
#   list containing all .vsd and .vsdx files
#   method to convert all word docs to pdfs - windows only
#   hpoefully the same for visio - windows only
#   method to merge all generated pdfs into one document - windows only

class Pdf_print:

    word_docs_list = []
    visio_docs_list = []
    pdf_docs_list = []

    def __init__(self, path):
        for f in os.listdir(path):
            if f.endswith('.doc') or f.endswith('.docx'):
                self.word_docs_list.append(os.path.join(path, f))
            if f.endswith('.vsd') or f.endswith('.vsdx'):
                self.visio_docs_list.append(os.path.join(path, f))

    def word_to_pdf(self):
        wdFormatPDF = 17
        for f in self.word_docs_list:
            #word = win32.gencache.EnsureDispatch('Word.Application')
            #doc = word.Documents.Open(f)
            #doc.SaveAs(f[:f.index('.doc')] + '.pdf', FileFormat=wdFormatPDF)
            #need to find safe was of replacing extension
            print(f[:f.index('.doc')] + '.pdf')
            #doc.Close()
            #word.Quit()
    
    def visio_to_pdf(self):
        wdFormatPDF = 17
        for f in self.visio_docs_list:
            #visio = win32.gencache.EnsureDispatch('Visio.Application')
            #doc = visio.Documents.Open(f)
            #doc.SaveAs(f[:f.index('.vsd')] + '.pdf', FileFormat=wdFormatPDF)
            #need to find safe was of replacing extension
            print(f[:f.index('.vsd')] + '.pdf')
            #doc.Close()
            #visio.Quit()

print('\n********Handover Pack Creator********')
print()
job = input('Please enter 4 digits of job number here: TL')
while job.isdigit() == False:
    print('\nIncorrect format. Please enter just the four digits of job number after \'TL\'\n')
    job = input('Please enter 4 digits of job number here: TL')
print()

merge_obj = Merge('TL' + job)
merge_obj.fill_lists()
print('Copy list:')
print(merge_obj.copy_list)
print('Merge list:')
print(merge_obj.merge_list)
merge_obj.copy_files()
merge_obj.make_merges()

pdf_obj = Pdf_print(merge_obj.dst)
pdf_obj.word_to_pdf()
pdf_obj.visio_to_pdf()
