# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    merge.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ecross <marvin@42.fr>                      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/03/17 16:55:24 by ecross            #+#    #+#              #
#    Updated: 2020/03/17 18:49:35 by ecross           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import csv
import xlrd
from mailmerge import MailMerge

def get_value(key, first_line, second_line):
    for s in first_line:
        if key == s:
            return second_line[first_line.index(s)]

with open("sheet.csv", 'r', newline='') as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    first_line = next(csv_data)
    second_line = next(csv_data)
    with MailMerge('06.docx') as document:
        mydict = {}
        merge_fields = document.get_merge_fields()
        for f in merge_fields:
            mydict[f] = get_value(f.replace('_', ' '), first_line, second_line)
        document.merge(**mydict)
        document.write('output.docx')
