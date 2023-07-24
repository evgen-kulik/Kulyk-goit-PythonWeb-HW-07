"""Скрипт наповнення бази даних"""
from datetime import date, datetime, timedelta
from random import randint, choice
import faker
from sqlalchemy import select

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def date_range(start: date, end: date) -> list:
    """
    Повертає список дат в інтервалі від початкової до кінцевої,
    з виключенням вихідних днів
    """
    result = []
    current_date = start
    while current_date <= end:
        if current_date.isoweekday() < 6:
            result.append(current_date)
        current_date += timedelta(1)
    return result


def fill_data():
    """Створює списки дисциплін і груп"""

    disciplines = [
        "Вища математика",
        "Дискретна математика",
        "Лінійна алгебра",
        "Програмування",
        "Теорія імовірності",
        "Історія України",
        "Англійська мова",
        "Креслення",
    ]
    groups = ["E331", "TP-05-1", "KN-51"]
    number_of_teachers = 5
    numbers_of_students = 50
    fake = faker.Faker()

    def seed_teachers():
        """Додає 5 рандомних вчителів до таблиці"""

        for _ in range(number_of_teachers):
            teacher = Teacher(fullname=fake.name())
            session.add(teacher)
        session.commit()

    def seed_disciplines():
        """Додає дисципліни рандомно до таблиці"""

        teacher_ids = session.scalars(
            select(Teacher.id)
        ).all()  # Метод scalar() повертає перше значення першого рядка результату.
        for discipline in disciplines:
            session.add(Discipline(name=discipline, teacher_id=choice(teacher_ids)))
        session.commit()

    def seed_groups():
        """Додає групи до таблиці в рандомному порядку"""

        for group in groups:
            session.add(Group(fullname=group))
        session.commit()

    def seed_students():
        """Додає 50 рандомних студентів до таблиці"""

        group_ids = session.scalars(select(Group.id)).all()
        for _ in range(numbers_of_students):
            student = Student(fullname=fake.name(), group_id=choice(group_ids))
            session.add(student)
        session.commit()

    def seed_grades():
        """Додає рандомно оцінки до таблиць"""

        # дата початку навчального процесу
        start_date = datetime.strptime("2023-01-09", "%Y-%m-%d")
        # дата закінчення навчального процесу
        end_date = datetime.strptime("2023-06-01", "%Y-%m-%d")
        # визначимо список дат, коли відбувалося навчання
        d_range = date_range(start=start_date, end=end_date)
        # ...............
        discipline_ids = session.scalars(select(Discipline.id)).all()
        student_ids = session.scalars(select(Student.id)).all()

        for d in d_range:
            # choice обирає рандомно одне значення зі списку
            random_id_discipline = choice(discipline_ids)
            random_ids_student = [choice(student_ids) for _ in range(5)]
            # згенеруємо оцінки для студентів
            for student_id in random_ids_student:
                grade = Grade(
                    grade=randint(1, 12),
                    date_of=d,
                    student_id=student_id,
                    discipline_id=random_id_discipline,
                )
                session.add(grade)
        session.commit()

    seed_teachers()
    seed_disciplines()
    seed_groups()
    seed_students()
    seed_grades()


if __name__ == "__main__":
    fill_data()
