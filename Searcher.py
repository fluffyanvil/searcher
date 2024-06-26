
import csv
import argparse
import os
import time
from datetime import datetime

parser = argparse.ArgumentParser(description="Compare two .csv files",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o", "--old", help="old .csv file, example, old.csv", required=True)
parser.add_argument("-n", "--new", help="new .csv file, examlpe new.csv", required=True)
args = parser.parse_args()
config = vars(args)
path_old = args.old
path_new = args.new
file_new =os.path.splitext(os.path.basename(path_new))[0]
file_old =os.path.splitext(os.path.basename(path_old))[0]
folder = os.path.dirname(path_old)

column_to_compare = 4

######Part1#####################################################
# populate WBS with WON2SAP data
start_time = time.time()
with open(path_new, encoding="utf-8") as newFile:
    new_csv_reader = csv.reader(newFile, delimiter='|')
    now = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    filename = os.path.join(folder, f'NEW_wbs_{now}.csv')
    
    modified_input = filename;
    with open(filename, 'w', newline='', encoding="utf-8") as outfile:

        output_csv_writer = csv.writer(outfile, delimiter='|')

        with open(path_old, encoding="utf-8") as oldFile:      
            old_csv_reader = csv.reader(oldFile, delimiter='|')

            rows_old = list(old_csv_reader)
            rows_new = list(new_csv_reader)

#index with ProjectNumber and ResellerCode
            old_index = {}
            new_index = {}
            data = []
# fill index for full match (ProjectNumber + ResellerCode)
            for rowfd in rows_old:
                old_index[rowfd[column_to_compare]] = rowfd
                
            for idx, rowfd in enumerate(rows_new):
                rowfd.append(idx+1)
                new_index[rowfd[column_to_compare]] = rowfd
                
            new_rows = list(new_index.keys())
            old_rows = list(old_index.keys())
            
            excepted = list(set(new_rows) - set(old_rows))
                
# counters for fillings

            targetRows = []           
            
            for key in excepted:
                newrow = new_index[key]
                targetRows.append(newrow)
                
            new_list = sorted(targetRows, key=lambda x: x[len(x)-1], reverse=False)
            
            if len(targetRows) > 0:           
                output_csv_writer.writerows(new_list)


print("--- NEW FILE ROWS = %s, OLD FILE ROWS = %s, EXCEPT = %s ---" % (len(new_rows), len(old_rows), len(excepted)))
print("--- %s seconds ---" % (time.time() - start_time))
                    




