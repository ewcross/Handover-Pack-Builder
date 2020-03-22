# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/17 16:55:24 by ecross            #+#    #+#              #
#    Updated: 2020/03/22 16:46:52 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import xlrd
import os
import shutil
from mailmerge import MailMerge
#import win32com.client as win32
from PyPDF2 import PdfFileReader, PdfFileMerger

#/usr/bin/env python

def check_path(path):
    if not os.path.exists(path):
        print('ERROR. File location does not exist: \'' + path + '\'')
        exit_func()

def exit_func():
    print()
    input('Press any key to exit.')
    exit()

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
        check_path(dst_root)
        for dirs in os.listdir(dst_root):
            if dirs.startswith(self.ref):
                found = 1
                path = os.path.join(dst_root, dirs)
                check_path(path)
                self.find_workbook(path)
                self.find_dst_path(path)
        #if job folder not found, error and exit
        if found == 0:
            print('ERROR. Could not find job folder for job: ' + self.ref, end='')
            print(' in current location \'' + os.getcwd() + '\'')
            exit_func()
        if self.dst == None or self.workbook == None:
            exit_func()
    
    #method to look in job folder for Handover subfolder, and
    #if found, set as destination for handover pack

    def find_dst_path(self, path):
        for dirs in os.listdir(path):
            if dirs.startswith('Handover'):
                self.dst = os.path.join(path, dirs)
                check_path(self.dst)
                return
        self.dst = None
        print('ERROR. Could not find output location. Please check \'Handover\' folder', end='')
        print(' exists in job file for ' + self.ref + ' .')
   
    #method to search job folder for install workbook in 'Install' subfolder
    #and, if found, set as the workbook attribute

    def find_workbook(self, path):
        found = 0
        for dirs in os.listdir(path):
            if dirs.startswith('Install'):
                found = 1
                install_dir = dirs
        if found == 0:
            print('ERROR. Could not find \'Install\' folder', end='')
            print(' in job file for ' + self.ref + '.')
            self.workbook = None
            return
        else:
            path = os.path.join(path, install_dir)
            for f in os.listdir(path):
                if f.endswith('xlsx') or f.endswith('xls'):
                    #need to find better way of selecting spreadsheet
                    with xlrd.open_workbook(os.path.join(path, f), on_demand = True) as workbook:
                        self.workbook = workbook
                    return
            self.workbook = None
            print('Could not find installation spreadsheet in \'Install\' ', end='')
            print('folder for job ' + self.ref + '.')

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
            if i == 0:
                i += 1
                continue
            if x.value != xlrd.empty_cell.value:
                src_folder = str(sheet.cell(i, infile_col - 1).value)
                src_folder = os.path.join(src_folder, '')
                check_path(src_folder)
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

    word_doc_list = []
    visio_doc_list = []
    pdf_doc_list = []

    def __init__(self, ref, path):
        self.ref = ref
        self.path = path
        for f in os.listdir(path):
            if f.endswith('.doc') or f.endswith('.docx'):
                self.word_doc_list.append(os.path.join(path, f))
            if f.endswith('.vsd') or f.endswith('.vsdx'):
                self.visio_doc_list.append(os.path.join(path, f))

    def word_to_pdf(self):
        wdFormatPDF = 17
        for f in self.word_doc_list:
            #word = win32.gencache.EnsureDispatch('Word.Application')
            #doc = word.Documents.Open(f)
            #doc.SaveAs(f[:f.index('.doc')] + '.pdf', FileFormat=wdFormatPDF)
            #need to find safe was of replacing extension
            print('converted a .docx to .pdf')
            #doc.Close()
            #word.Quit()
    
    def visio_to_pdf(self):
        wdFormatPDF = 17
        for f in self.visio_doc_list:
            #visio = win32.gencache.EnsureDispatch('Visio.Application')
            #doc = visio.Documents.Open(f)
            #doc.SaveAs(f[:f.index('.vsd')] + '.pdf', FileFormat=wdFormatPDF)
            #need to find safe was of replacing extension
            print('converted a .vsdx to .pdf')
            #doc.Close()
            #visio.Quit()

    def get_pdf_list(self):
        for f in os.listdir(self.path):
            if f.endswith('.pdf'):
                self.pdf_doc_list.append(os.path.join(self.path, f))
        self.pdf_doc_list.sort()

    def merge_pdfs(self):
        merger = PdfFileMerger()
        for pdf in self.pdf_doc_list:
            print('processing --> ' + pdf)
            with open(pdf, 'rb') as f:
                reader = PdfFileReader(f)
                if reader.isEncrypted:
                    print('\n*****Encryption Error*****')
                    print('The file: ' + pdf + ' is encrypted and ', end='')
                    print('cannot be processed.\nPlease create an unencrypted copy by printing ', end='')
                    print('the original as a new pdf, and then save this in its place.')
                    print('Aborting...')
                    exit_func()
                else:
                    print('wasnt encrytped so merging')
                    merger.append(pdf)
        with open(self.path + self.ref + ' ' + 'Handover Pack Full.pdf', 'wb') as f:
            merger.write(f)
        merger.close()


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

pdf_obj = Pdf_print(merge_obj.ref, merge_obj.dst)
pdf_obj.word_to_pdf()
pdf_obj.visio_to_pdf()
pdf_obj.get_pdf_list()
for f in pdf_obj.pdf_doc_list:
  print(f)
pdf_obj.merge_pdfs()
