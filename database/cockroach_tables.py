from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey

Base = declarative_base()

class PermissionSlip(Base):
    __tablename__ = 'permissionslip'
    slip_id = Column(Integer, primary_key=True, nullable = False)
    name = Column(String, nullable = False)
    due = Column(String, nullable = False)


class Student(Base):
    __tablename__ = 'student'
    parent_email = Column(String, nullable = False)
    parent_name = Column(String, nullable = False)
    student_name = Column(String, nullable = False)
    student_id = Column(String, primary_key = True, nullable = False)
    is_signed = Column(Boolean, nullable = False)

class PermissionSlip_Student(Base):
    __tablename__ = 'permissionslip_student'
    slip_id = Column(Integer, ForeignKey('slip.id'), primary_key=True, nullable = False)
    student_id = Column(String, ForeignKey('student_id'), primary_key = True, nullable = False)