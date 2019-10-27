# function to view a specific table on easyslipdb
# function to create a new permission slip (Python) -> update PermissionSlip table (sqlalchemy) -> cockroach db
# function to break down csv (use csv_reader), -> update Student table (sqlalchemy) -> cockraoch db

# TO-DO: functions to update, functions to pull down 
# Automate IDs

from cockroach_tables import PermissionSlip, Student, PermissionSlip_Student
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
import csv_reader

Base = declarative_base()

# Create an engine to communicate with the database. The
# "cockroachdb://" prefix for the engine URL indicates that we are
# connecting to CockroachDB using the 'cockroachdb' dialect.

engine = create_engine(
    'cockroachdb://bk:123@aws-us-east-1.easyslip-1.crdb.io:26257/easyslipdb?sslmode=verify-full&sslrootcert=/Users/brandonkhong/cockroach-v19.1.5/certs/easyslip-1-ca.crt',
    echo=True                   # Log SQL queries to stdout
    
)


def insert_student(class_info : [{}]):
    all_info = []
    for student in class_info:
        
        base = "Student(parent_email = {}, parent_name = {}, student_name = {}, student_id = {}, is_signed = {})".format(
            student['parent_email'], student['parent_name'], student['student_name'], student['student_id'], student['is_signed'])
        
        all_info.append(base)
    
    for push in base:
        session.add(eval(push))
    
    session.commit()


def insert_permissionslip(given_name: str, given_due: str):
    session.add(name = given_name, given_due)
    session.commit()
    

def insert_permissionslip_student():
    # query down from other tables to create this table
    pass

def query_permissionslip():
    pass


def query_student():
    connection = engine.connect()
    results = connection.execute("select * from student")
    for row in results:
        print(row)
    connection.close()


def query_permissionslip_student():
    pass

if __name__ == '__main__':
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    