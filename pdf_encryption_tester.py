# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    pdf_encryption_tester.py                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/22 14:08:55 by ecross            #+#    #+#              #
#    Updated: 2020/03/22 15:00:02 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
from PyPDF2 import PdfFileReader

def error_exit():
    input('Press any key to exit.')
    exit()

path = input('Please give path to directory to be checked: \n')
    
def check_dir(path):
    try:
        os.listdir(path)
    except FileNotFoundError:
        return 0
    return 1

while check_dir(path) == 0:
    path = input('Directory doesn\'t exist or couldn\'t be opened, please try again: \n')
print('-------')
button = 0
for f in os.listdir(path):
    if f.endswith('.pdf'):
        with open(os.path.join(path, f), 'rb') as pdf:
            reader = PdfFileReader(pdf)
            if reader.isEncrypted:
                button = 1
                print('File: ')
                print(f + ' ---------> Is encrypted.\n-------')

if button == 0:
    print('No encrypted files were found.')
