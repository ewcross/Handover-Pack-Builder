# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/17 16:55:24 by ecross            #+#    #+#              #
#    Updated: 2020/04/06 16:49:07 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import time
import shutil
import xlrd
from mailmerge import MailMerge
#import win32com.client as win32
from PyPDF2 import PdfFileReader, PdfFileMerger

#*********Basic Process*********
#
#   asks user for job number as input
#   searches 'Sales' directory (currently specified by current working
#       directory of script) for 'Handover' and 'Install' locations
#   sets 'Handover' location as merge destination
#   looks for newest .xlsx spreadsheet in 'Install' folder and imports this,
#       checking that the job ref within matches that provided by the user initially
#   uses the 'HOP Merge' sheet to find which files need to be copied into 'Handover'
#       and which will need to be merged first
#   copies across the copy files
#   merges the .doc files using data from the 'A Merge Data' sheet (first and second row)
#       and saves these merged documents with new names in 'Handover'
#   converts each .docx and .vsdx document now found in 'Handover' to pdf form
#   merges all pdfs into a final Handover Pack document, saving this in the same folder
#

def check_path(path, msg=1):
    if not os.path.exists(path):
        print_error('File or folder does not exist: \'' + path + '\'. ')
        if msg == 1:
            print('Please check.')
        else:
            print('Please check ' + msg)
        exit_func()

def check_workbook(workbook):
    sheets = [global_merge_worksheet, global_template_worksheet]
    for x in sheets:
        try:
            workbook.sheet_by_name(x)
        except:
            print_error(f'The XL file being processed does not contain the worksheet {x}. Please check it is the correct file.')
            return 0
    return 1

def print_error(msg):
    print()
    print('ERROR. ' + msg)

def exit_func(path=0):
    print()
    print('Aborting...')
    input('Press any key to exit.')
    say_msg_dot('Bye')

def say_msg_dot(msg):
    print(msg, end='\r')
    time.sleep(0.4)
    print(msg + '.', end='\r')
    time.sleep(0.4)
    print(msg + '..', end='\r')
    time.sleep(0.4)
    print(msg + '...')
    time.sleep(0.4)
    if msg == 'Bye':
        exit()

class Merge:
    
    copy_list = []
    merge_list = []
   
    #init method sets ref attribute to job reference
    #and finds project install.xlsx workbook and merge destination location

    def __init__(self, ref):
        self.ref = ref
        #
        #needs changing to absolute path to Sales folder
        #or can be taken from ini file
        #
        dst_root = global_sales_folder_path
        found = 0
        check_path(dst_root)
        for dirs in os.listdir(dst_root):
            if dirs.startswith(self.ref) and '.' not in dirs:
                found = 1
                path = os.path.join(dst_root, dirs)
                check_path(path)
                self.find_workbook(path)
                self.find_dst_path(path)
        #if job folder not found, error and exit
        if found == 0:
            print_error('Could not find job folder for job: ' + self.ref + ' in current location \'' + global_sales_folder_path + '\'')
            exit_func()
        if self.dst == None or self.workbook == None:
            exit_func()
    
    #method to look in job folder for Handover subfolder, and
    #if found, set as destination for handover pack

    def find_dst_path(self, path):
        for dirs in os.listdir(path):
            if dirs.startswith(global_handover_folder):
                self.dst = os.path.join(path, dirs)
                check_path(self.dst)
                return
        self.dst = None
        print_error('Could not find output location. Please check \'Handover\' folder exists in job file for ' + self.ref + ' .')
   
    #method to search job folder for install workbook in 'Install' subfolder
    #and, if found, set as the workbook attribute

    def find_workbook(self, path):
        found = 0
        for dirs in os.listdir(path):
            if dirs.startswith(global_install_folder):
                found = 1
                install_dir = dirs
        if found == 0:
            print_error('Could not find \'Install\' folder in job file for ' + self.ref + '.')
            self.workbook = None
            return
        else:
            path = os.path.join(path, install_dir)
            xl_docs = [f for f in os.listdir(path) if '.xls' in f]
            if len(xl_docs) > 0:
                xl_docs_times = []
                for f in xl_docs:
                    xl_docs_times.append(time.ctime(os.path.getmtime(os.path.join(path, f))))
                #########
                print('PRINTING XL DOC TIMES: ')
                for f in xl_docs_times:
                    print(f)
                #########
                book = xl_docs[xl_docs_times.index(max(xl_docs_times))]
                print(f'Now processing spreadsheet \'{os.path.join(path, book)}\'.')
                with xlrd.open_workbook(os.path.join(path, book), on_demand = True) as workbook:
                    if not check_workbook(workbook):
                        exit_func()
                    sheet = workbook.sheet_by_name(global_merge_worksheet)
                    if sheet.cell(1, 1).value != self.ref:
                        print_error('Project ref in cell B2 of \'A Merge Data\' sheet does not match job ref. Stopping merge.')
                        self.workbook = None
                    else:
                        self.workbook = workbook
            else:
                self.workbook = None
                print_error('Could not find installation spreadsheet in \'Install\' folder for job ' + self.ref + '.')

    def get_col(self, sheet, title):
        i = 0
        for x in sheet.row(0):
            if x.value == title:
                return (i)
            i += 1
        print_error('Could not locate column with title \'' + title + '\' in Install spreadsheet. Please check \'HOP Merge\' sheet.')
        exit_func()
        return 0

    def fill_lists(self):
        sheet = self.workbook.sheet_by_name(global_template_worksheet)
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
                check_path(src_folder, 'Column F of \'HOP Merge\' sheet.')
                tup = (src_folder, str(sheet.cell(i, infile_col).value), self.dst, str(sheet.cell(i, outfile_col).value))
                check_path(tup[0] + tup[1], f'that the file \'{tup[1]}\' exists.')
                if sheet.cell(i, outfile_col + 1).value == 'Copy':
                    self.copy_list.append(tup)
                if sheet.cell(i, outfile_col + 1).value == 'Merge':
                    self.merge_list.append(tup)
            i += 1

    def copy_files(self):
        for tup in self.copy_list:
            try:
                shutil.copy(os.path.join(tup[0], tup[1]), os.path.join(tup[2], tup[3]))
            except:
                print_error(f'Could not copy file \'{tup[1]}\' to location \'{tup[2]}\'.')
                exit_func(self.dst)
            print('Fetched file: \'' + tup[1] + '\'.')

    def get_value(self, key, sheet):
        i = 0
        for x in sheet.row(0):
            if key == x.value:
                return str(sheet.cell(1, i).value)
            i += 1

    def make_merges(self):
        error = 0
        for doc in self.merge_list:
            with MailMerge(doc[0] + doc[1]) as document:
                mydict = {}
                merge_fields = document.get_merge_fields()
                sheet = self.workbook.sheet_by_name(global_merge_worksheet)
                for f in merge_fields:
                    mydict[f] = self.get_value(f.replace('_', ' '), sheet)
                document.merge(**mydict)
                try:
                    document.write(os.path.join(doc[2], doc[3].replace('xxxx', self.ref[2:])))
                except:
                    print_error('Could not save merged doc \'' + doc[3].replace('xxxx', self.ref[2:]) + '\'. \
Please make sure a file of this name does not already exist.')
                    error = 1
            if error == 1:
                exit_func(self.dst)
            print('Merged \'' + doc[3].replace('xxxx', self.ref[2:]) + '\'.')

#class with:
#   list attribute containing all .doc and .docx files in specified directory
#   list containing all .vsd and .vsdx files
#   method to convert all word and visio docs to pdfs - windows only

class Pdf_print:

    word_doc_list = []
    visio_doc_list = []
    pdf_doc_list = []

    def __init__(self, ref, path):
        self.ref = ref
        self.path = path
        for f in os.listdir(path):
            if '.doc' in f:
                self.word_doc_list.append(os.path.join(path, f))
            if '.vsd' in f:
                self.visio_doc_list.append(os.path.join(path, f))

    def word_to_pdf(self):
        error = 0
        wdFormatPDF = 17
        try:
            word = win32.gencache.EnsureDispatch('Word.Application')
        except:
            word.Quit()
            print_error('Could not open MS Word. Please check it is installed and working.')
            exit_func(self.path)
        for f in self.word_doc_list:
            try:
                doc = word.Documents.Open(f)
                try:
                    doc.SaveAs(f[:f.index('.')] + '.pdf', FileFormat=wdFormatPDF)
                    print('Converted \'' + os.path.basename(f) + '\' to pdf.')
                except:
                    error = 1
                    print_error(f'Unable to open word file \'{os.path.basename(f)}\' for pdf conversion. \
Please check it is not open elsewhere or corrupted.')
                doc.Close()
            except:
                error = 1
                print_error(f'Unable to open word file \'{os.path.basename(f)}\' for pdf conversion. Please check it is not open elsewhere or corrupted.')
        word.Quit()
        if error == 1:
            exit_func(self.path)
    
    def get_pdf_list(self):
        for f in os.listdir(self.path):
            if f.endswith('.pdf'):
                self.pdf_doc_list.append(os.path.join(self.path, f))
        self.pdf_doc_list.sort()

    def merge_pdfs(self):
        merger = PdfFileMerger()
        exit = 0
        for pdf in self.pdf_doc_list:
            with open(pdf, 'rb') as f:
                reader = PdfFileReader(f)
                if reader.isEncrypted:
                    print('\n*****Encryption Error*****\n')
                    print('The file: ' + os.path.basename(pdf) + ' is encrypted and ', end='')
                    print('cannot be processed.\nPlease create an unencrypted copy by printing ', end='')
                    print('the original as a new pdf, and then save this in its place.')
                    merger.close()
                    exit_func(self.path)
                else:
                    merger.append(pdf)
        with open(os.path.join(self.path, self.ref + ' Handover Pack Full.pdf'), 'wb') as f:
            merger.write(f)
        merger.close()

global_sales_folder_path = os.getcwd()
global_handover_folder = 'Handover Pack'
global_install_folder = 'Install'
global_merge_worksheet = 'A Merge Data'
global_template_worksheet = 'HOP Merge'
global_eic_worksheet = 'EIC Merge'

try:
    with open('merge info.txt', 'r') as f:
        for line in f:
            if '1. ' in line:
                global_sales_folder_path = line[line.index('\'') + 1 :line.index('\'', line.index('\'') + 1)]
                global_sales_folder_path.strip()
            if '2. ' in line:
                global_handover_folder = line[line.index('\'') + 1 :line.index('\'', line.index('\'') + 1)]
                global_handover_folder.strip()
            if '3. ' in line:
                global_install_folder = line[line.index('\'') + 1 :line.index('\'', line.index('\'') + 1)]
                global_install_folder = line[line.index('\'') + 1 :line.index('\'', line.index('\'') + 1)]
                global_install_folder.strip()
            if '4. ' in line:
                global_merge_worksheet = line[line.index('\'') + 1 :line.index('\'', line.index('\'') + 1)]
                global_merge_worksheet.strip()
            if '5. ' in line:
                global_template_worksheet = line[line.index('\'') + 1 :line.index('\'', line.index('\'') + 1)]
                global_template_worksheet.strip()
            if '6. ' in line:
                global_eic_worksheet = line[line.index('\'') + 1 :line.index('\'', line.index('\'') + 1)]
                global_eic_worksheet.strip()
except FileNotFoundError:
    print_error(f'Could not find ini file \'merge info.txt\' in \'{os.getcwd()}\'. Continuing with default values.')
except:
    print_error('Problem with \'merge info.txt\'. Continuing with default values.')

print('\n********Handover Pack Creator********')
print()

def get_job_number():
    job = ''
    words = 'P'
    while job.isdigit() == False or len(job) != 4:
        print(f'{words}lease enter 4 digits of job number here (or press enter to exit) --> ', end='')
        job = input('TL:')
        if not job:
            say_msg_dot('Bye')
        words = 'Incorrect format. P'
    print()
    return job

while True:
    job = get_job_number()
    merge_obj = Merge('TL' + job)
    merge_obj.fill_lists()
    print()
    merge_obj.copy_files()
    print()
    merge_obj.make_merges()
    pdf_obj = Pdf_print(merge_obj.ref, merge_obj.dst)
    print()
    pdf_obj.word_to_pdf()
    pdf_obj.get_pdf_list()
    pdf_obj.merge_pdfs()
    print()
    say_msg_dot('Merge complete')
