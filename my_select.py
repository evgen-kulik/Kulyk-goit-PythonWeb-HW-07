from sqlalchemy import (
    func,
    desc,
    select,
    and_,
)  # інструменти агрегації (min, max, avg, round)

# desc - для реверсу наданих даних
# select, and_ - для виконання підзапиту
# and_ - для запису кількох .filter в одну строку

from src.models import Teacher, Student, Discipline, Grade, Group
from src.db import session


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""

    result = (
        session.query(
            Student.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    # Отримати Student.fullname, Grade.grade (середній бал (func.avg) округлений до 2 знаків після коми;
    # 'label' - ORM іменує поле, із середнім балом, за допомогою оператора AS;
    # Запит робити (select_from) у Grade, приєднавши (join) Student;
    # Сортувати (order_by) за 'avg_grade' в зворотньому порядку (desc);
    # Групувати (group_by) за Student.id; лімітувати (limit) вивід даних 5 одиницями.
    return result


def select_2(discipline_id: int):
    """Знайти студента із найвищим середнім балом з певного предмета."""

    result = (
        session.query(
            Discipline.name,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .filter(Discipline.id == discipline_id)
        .group_by(Student.id, Discipline.name)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    return result


def select_3(discipline_id: int):
    """Знайти середній бал у групах з певного предмета."""

    result = (
        session.query(
            Group.fullname,
            Discipline.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .join(Discipline)
        .filter(Discipline.id == discipline_id)
        .group_by(Group.fullname, Discipline.name)
        .order_by("avg_grade")
        .all()
    )
    return result


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""

    result = (
        session.query(func.round(func.avg(Grade.grade), 2)).select_from(Grade).all()
    )
    return result


def select_5(teacher_id: int):
    """Знайти, які курси читає певний викладач."""

    result = (
        session.query(Teacher.fullname, Discipline.name)
        .select_from(Teacher)
        .join(Discipline)
        .filter(Teacher.id == teacher_id)
        .group_by(Teacher.fullname, Discipline.name)
        .order_by(Discipline.name)
        .all()
    )
    return result


def select_6(group_id: int):
    """Знайти список студентів у певній групі."""

    result = (
        session.query(Group.fullname, Student.fullname)
        .select_from(Group)
        .join(Student)
        .filter(Group.id == group_id)
        .group_by(Group.fullname, Student.fullname)
        .order_by(Student.fullname)
        .all()
    )
    return result


def select_7(group_id: int, discipline_id: int):
    """Знайти оцінки студентів в окремій групі з певного предмета."""

    result = (
        session.query(Group.fullname, Discipline.name, Grade.grade)
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .join(Discipline)
        .filter(Group.id == group_id)
        .filter(Discipline.id == discipline_id)
        .group_by(Group.fullname, Discipline.name, Grade.grade)
        .all()
    )
    return result


def select_8(teacher_id: int):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""

    result = (
        session.query(
            Teacher.fullname,
            Discipline.name,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Discipline)
        .join(Teacher)
        .join(Grade)
        .filter(Teacher.id == teacher_id)
        .group_by(Teacher.fullname, Discipline.name)
        .order_by("avg_grade")
        .all()
    )
    return result


def select_9(student_id: int):
    """Знайти список курсів, які відвідує певний студент."""

    result = (
        session.query(Student.fullname, Discipline.name)
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .filter(Student.id == student_id)
        .group_by(Student.fullname, Discipline.name)
        .order_by(Student.fullname)
        .all()
    )
    return result


def select_10(student_id: int, teacher_id: int):
    """Список курсів, які певному студенту читає певний викладач."""

    result = (
        session.query(Student.fullname, Teacher.fullname, Discipline.name)
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Teacher)
        .filter(Teacher.id == teacher_id)
        .filter(Student.id == student_id)
        .group_by(Student.fullname, Teacher.fullname, Discipline.name)
        .order_by(Discipline.name)
        .all()
    )
    return result


def select_11(student_id: int, teacher_id: int):
    """Середній бал, який певний викладач ставить певному студентові."""

    result = (
        session.query(
            Teacher.fullname,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label("avg_grade"),
        )
        .select_from(Student)
        .join(Grade)
        .join(Discipline)
        .join(Teacher)
        .filter(Student.id == student_id)
        .filter(Teacher.id == teacher_id)
        .group_by(Teacher.fullname, Student.fullname)
        .all()
    )
    return result


def select_12(discipline_id: int, group_id: int):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""

    subquery = (
        select(Grade.date_of)
        .join(Student)
        .join(Group)
        .where(and_(Grade.discipline_id == discipline_id, Group.id == group_id))
        .order_by(desc(Grade.date_of))
        .limit(1)
        .scalar_subquery()
    )

    result = (
        session.query(
            Discipline.name,
            Student.fullname,
            Group.fullname,
            Grade.date_of,
            Grade.grade,
        )
        .select_from(Grade)
        .join(Student)
        .join(Discipline)
        .join(Group)
        .filter(
            and_(
                Discipline.id == discipline_id,
                Group.id == group_id,
                Grade.date_of == subquery,
            )
        )
        .order_by(desc(Grade.date_of))
        .all()
    )
    # .group_by або не вказувати зовсім, або перелічити в ньому всі дані
    return result


if __name__ == "__main__":
    # print(select_1())
    # print(select_2(1))
    # print(select_3(2))
    # print(select_4())
    # print(select_5(1))
    # print(select_6(2))
    # print(select_7(1, 5))
    # print(select_8(2))
    # print(select_9(4))
    # print(select_10(5, 2))
    # print(select_11(1, 2))
    print(select_12(5, 1))
