from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from .db import (
    Base,
)  # "." показує, що це модуль з поточного каталогу (ставити обов'язково!)

# Base = declarative_base() - клас, відповідальний за синхронізацію таблиць бази даних та їх описи в Python-класах


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(20), nullable=False)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120), nullable=False)
    group_id = Column("group_id", ForeignKey("groups.id", ondelete="CASCADE"))
    # ondelete='CASCADE' говорить, що при видаленні запису з таблиці groups, буде автоматично
    # видалено всі пов'язані записи у таблиці students
    group = relationship("Group", backref="students")
    # backref= дозволяє не прописувати відповідний relationship у Group, так прописується двосторонній зв'язок
    # інакше треба використовувати back_populates= в обох зв'язаних класах-таблицях.
    # Читати: у "Group" з'явиться властивість "students".


class Discipline(Base):
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    teacher_id = Column("teacher_id", ForeignKey("teachers.id", ondelete="CASCADE"))
    teacher = relationship("Teacher", backref="disciplines")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column("date_of", Date, nullable=True)
    student_id = Column("student_id", ForeignKey("students.id", ondelete="CASCADE"))
    discipline_id = Column(
        "discipline_id", ForeignKey("disciplines.id", ondelete="CASCADE")
    )
    student = relationship("Student", backref="grade")
    discipline = relationship("Discipline", backref="grade")
