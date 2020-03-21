# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    pdf.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/21 09:56:28 by ecross            #+#    #+#              #
#    Updated: 2020/03/21 10:49:28 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import win32com.client as win32

#in_file = 'C:\\Users\\PWC\\Documents\\python_testing\\test.docx'
#out_file = 'C:\\Users\\PWC\\Documents\\python_testing\\out.pdf'
in_file = 'python_testing\\test.docx'
in_file = 'python_testing\\test.pdf'
wdFormatPDF = 17

word = win32.gencache.EnsureDispatch('Word.Application')
doc = word.Documents.Open(in_file)
doc.SaveAs(out_file, FileFormat=wdFormatPDF)
doc.Close()
word.Quit()
input('Any key to exit')
