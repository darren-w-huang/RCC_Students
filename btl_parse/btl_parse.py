# -*- coding: utf-8 -*-
"""
Created on Wed May  8 22:41:51 2019
@author: Darren
"""
from datetime import datetime
import csv, os
import re

# Change path to match wherever your files are located. For example, if located in C:/Users/TempName/btl, then the following would state path = ("C:/Users/TempName/btl")
path = ("C:/btl");
os.chdir(path);

files_in_dir = [f for f in os.listdir(path) if f.endswith('btl')];
print(files_in_dir);

SPACES = 11 * " "
month_len = 7
index = 0
rowLength = 0
rowNum = 0

for f in files_in_dir:
  index = f.find('.btl');
  fileName = f[index - 3 : index] + ".txt"; 
  file = open(path + f, "r");
  new = open(path + fileName, 'w');
  print(path + fileName);
  dataBegin = False;
  init_col = True;
  counter = 0;

  for line in file:
      li=line.strip()    
      if (not li.startswith("#") and not li.startswith("*")):
                            text = line.rstrip()
                            if (init_col):
                              dCol = re.search('Date', text[:35])
                              index = dCol.start();
                              date_len = 4; 
                              text = text[:index] + SPACES + text[index:];
                              init_col = False;

                            # Formats month
                            month = re.search('\w\w\w\s\d\d\s\d\d\d\d', text[:35])
                            if (month):                           
                                index = month.start() + month_len
                                fm = datetime.strptime(month.group(), '%b %d %Y').strftime('%Y-%m-%d')

                            counter += 1;
                            # First line where dateTime appears
                            if (counter == 3):
                                dataBegin = True;

                            if (dataBegin):
                                    times = file.readline(); 
                                    date = re.search('(\d\d):(\d\d):(\d\d)', times.rstrip()[:35])
                                    # Format Datetime
                                    insert =  fm + "T" + date.group() + "00Z"
                                    text = text[:index - 7] + insert + text[index + 4:]

                            # Format for tab seperation
                            if (counter == 1):
                              text = re.sub(' +', '\t', text[4:]) 
                            elif (counter == 2): 
                              text = re.sub(' +', '\t', text[2:])
                            elif(counter >= 12):
                              text = re.sub('\s+', '\t', text[5:])    
                            else:
                              text = re.sub('\s+', '\t', text[6:]) 

                            if (counter != 2):                                
                                new.write(text + "\n");
  new.close()   

  txt_file = '%s%s' % (path, fileName)
  csv_file = "%s%s.csv" % (path, fileName[:-4])
  print(csv_file, txt_file);
  with open(txt_file, "r") as infile:
        reader = csv.reader(infile, dialect="excel-tab")
        with open(csv_file, "w", newline = '') as outfile:
            writer = csv.writer(outfile, delimiter = ',')
            for row in reader:
                writer.writerow(row)
