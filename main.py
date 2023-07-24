"""
CLI застосунок для CRUD операцій із базою даних.
Реалізує наступні операції для кожної моделі:
- створення вчителя (студента, групи, дисципліни);
- виведення всіх вчителів (студентів, груп, дисциплін);
- оновлення (заміна) за 'id' даних вчителя (студента, групи, дисципліни);
- видалення вчителя (студента, групи, дисципліни).
"""

import argparse
from src.models import Teacher, Student, Discipline, Group
from src.db import session


parser = argparse.ArgumentParser(description="Data base operations")
parser.add_argument(
    "-a", "--action", dest="action", help="Action: create/list/update/remove", type=str
)  # Введений аргумент поміщається в 'action'
parser.add_argument(
    "-m",
    "--model",
    dest="model",
    help="Model's name: Teacher/Group/Student/Discipline",
    type=str,
)  # Введений аргумент поміщається в 'model'
parser.add_argument(
    "-n",
    "--name",
    dest="name",
    help="Name of Teacher/Group/Student/Discipline",
    type=str,
)  # Введений аргумент поміщається в 'name'
parser.add_argument(
    "--id", dest="id", help="ID of Teacher/Group/Student/Discipline", type=str
)  # Введений аргумент поміщається в 'id'
args = parser.parse_args()  # Збирає разом всі аргументи
# print(args)


def create(model: str, name: str):
    """Створює в таблицях нові об'єкти"""

    if model == 'Teacher':
        teacher = Teacher(fullname=name)
        session.add(teacher)
    elif model == 'Group':
        group = Group(fullname=name)
        session.add(group)
    elif model == 'Student':
        student = Student(fullname=name)
        session.add(student)
    elif model == 'Discipline':
        discipline = Discipline(name=name)
        session.add(discipline)
    session.commit()


def list_(model: str):
    """Виводить дані в термінал (всі моделі)"""

    result = None
    if model == 'Teacher':
        result = session.query(Teacher.fullname).select_from(Teacher).all()
    elif model == 'Group':
        result = session.query(Group.fullname).select_from(Group).all()
    elif model == 'Student':
        result = session.query(Student.fullname).select_from(Student).all()
    elif model == 'Discipline':
        result = session.query(Discipline.name).select_from(Discipline).all()
    return result


def update(model: str, id: int, name: str):
    """Оновлює дані в таблиці"""

    if model == 'Teacher':
        new_name = session.get(Teacher, id)  # Такий синтаксис починаючи з версії SQLAlchemy 2.0)
        new_name.fullname = name
        session.add(new_name)
    elif model == 'Group':
        new_name = session.get(Group, id)
        new_name.fullname = name
        session.add(new_name)
    elif model == 'Student':
        new_name = session.get(Student, id)
        new_name.fullname = name
        session.add(new_name)
    elif model == 'Discipline':
        new_name = session.get(Discipline, id)
        new_name.name = name
        session.add(new_name)
    session.commit()


def remove(model: str, id: int):
    """Видаляє об'єкт з таблиці"""

    if model == 'Teacher':
        i = session.query(Teacher).filter(Teacher.id == id).one()
        session.delete(i)
    elif model == 'Group':
        i = session.query(Group).filter(Group.id == id).one()
        session.delete(i)
    elif model == 'Student':
        i = session.query(Student).filter(Student.id == id).one()
        session.delete(i)
    elif model == 'Discipline':
        i = session.query(Discipline).filter(Discipline.id == id).one()
        session.delete(i)
    session.commit()


def main():
    if args.action == "create":
        create(args.model, args.name)
        print(f"{args.model}: {args.name} created!")
    elif args.action == "list":
        print(list_(args.model))
    elif args.action == "update":
        update(args.model, args.id, args.name)
    elif args.action == "remove":
        remove(args.model, args.id)
        print(f"{args.model} with ID '{args.id}' removed!")


if __name__ == "__main__":
    main()

# --action create -m Teacher --name 'Boris Jonson' створення вчителя
# --action list -m Teacher показати всіх вчителів
# --action update -m Teacher --id 3 --name 'Andry Bezos' оновити дані вчителя з id=3
# --action remove -m Teacher --id 3 видалити вчителя з id=3
