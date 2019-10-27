# BK 10/26/19
# Read/Parse a validated csv file
# Be able to return list of Parent emails

# import csv
import goody

class class_info:
    # {student1: {parent_name: Lien Khong}, {parent_email: btkhong@uci.edu}}
    
    def __init__(self, csv_file: open):
        self.csv_dicts = []
        col_values = []
        # VALIDATING CSV
        
        # CREATING DICT
        for num, line in enumerate(csv_file):
            student_info = {}
            line_info = line.split(',')
            if num == 0:
                for val in line_info:
                    col_values.append(val.strip('\n'))
                    
            else:
                for i in range(0, len(col_values)):
                    student_info[col_values[i]] = line_info[i].strip('\n')
                
                student_info['is_signed'] = False
                self.csv_dicts.append(student_info)
    
    def returninfo(self):
        return self.csv_dicts

if __name__ == '__main__':
    csv_file = goody.safe_open('Enter the file name describing class info csv', 'r', 'Could not find that file')
    x = class_info(csv_file)
    print(x.returninfo())
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    