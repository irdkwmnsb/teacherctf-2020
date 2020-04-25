import random

schools = [i.strip() for i in open("grades/schools.txt").readlines()]
surnames = [i.strip() for i in open("grades/surnames.txt").readlines()]
subjects_list = {"Чистописание": [1],
                 "Чтение": range(1, 5),
                 "Труд": range(1, 5),
                 "Природоведение": range(1, 6),
                 "Математика": range(1, 7),
                 "Музыка": range(1, 8),
                 "ИЗО": range(1, 9),
                 "Руссский язык": range(1, 12),
                 "Физкультура": range(1, 12),
                 "Иностранный язык": range(4, 12),
                 "Граждановедение": range(5, 8),
                 "Краеведение": range(5, 8),
                 "История": range(5, 12),
                 "Литература": range(5, 12),
                 "ОБЖ": range(5, 12),
                 "Технология": range(5, 12),
                 "География": range(6, 11),
                 "Биология": range(6, 12),
                 "Информатика": range(6, 12),
                 "Обществознание": range(6, 12),
                 "Черчение": range(7, 9),
                 "Алгебра": range(7, 12),
                 "Геометрия": range(7, 12),
                 "Физика": range(7, 12),
                 "Химия": range(8, 12),
                 "Астрономия": range(11, 12)}
classcount = [(3, 10),  # 1
              (3, 8),  # 2
              (3, 5),  # 3
              (3, 5),  # 4
              (3, 4),  # 5
              (3, 4),  # 6
              (3, 4),  # 7
              (3, 4),  # 8
              (3, 4),  # 9
              (3, 4),  # 10
              (3, 3)]  # 11
months = [("Январь", 1, 31, [], []),
          ("Февраль", 2, 29, [], []),
          ("Март", 3, 28, [], [])]
import datetime

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 3, 29)
while start != end:
    if start.isoweekday() >= 6:
        months[start.month - 1][start.isoweekday() - 6 + 3].append(start.day - 1)
    start += datetime.timedelta(days=1)


# https://www.examen.ru/add/manual/materialyi-dlya-shkolnikov/spisok-predmetov/

class Task():
    def __init__(self):
        self.state = self.tasks_generator()
        self.current_task, self.current_ans = next(self.state)
        self.is_ended = False

    def tasks_generator(self):
        while True:
            school = random.choice(schools)
            is_school_on_sat = random.randint(1, 3) == 1
            classes_count = [random.randint(i, j) for i, j in classcount]
            for grade, cur_classes_count in enumerate(classes_count):
                subjects = [i for i, r in subjects_list.items() if grade + 1 in r]
                for class_name in [str(grade + 1) + letter for letter, _ in
                                   zip("АБВГДЕЖЗИКЛМН", range(cur_classes_count))]:
                    num_students = random.randint(18, 30)
                    students = sorted(random.sample(surnames, num_students))
                    max_surname_len = max(7, max(len(i) for i in students))
                    for subject in subjects:
                        if random.randint(1, 3) == 1:
                            continue
                        count = [0] * num_students
                        sum = [0] * num_students
                        table = f"{school} класс {class_name} предмет {subject}\n"
                        for month, month_num, day_count, sats, sunds in months:
                            days = [i for i in range(day_count) if
                                    datetime.datetime(2020, month_num, i + 1).isoweekday() < 6 - is_school_on_sat]
                            weekends = sunds.copy()
                            if not is_school_on_sat:
                                weekends += sats
                            table += f"|{' ' * max_surname_len}|{month.center(day_count * 3 - 1)}|\n"
                            table += f"|{'Фамилия'.ljust(max_surname_len)}|" + '|'.join(
                                str(i).rjust(2) for i in range(1, day_count + 1)) + "|\n"
                            tests = random.sample(days, random.randint(1, len(days) // 3))
                            for i, lastname in enumerate(students):
                                table += f"|{lastname.ljust(max_surname_len)}|"
                                sick_chance = 40
                                mark_chance = 8
                                is_sick = False
                                for day in range(day_count):
                                    mark = " "
                                    if random.randint(1, sick_chance) == 1:
                                        if not is_sick:
                                            sick_chance = 1
                                        is_sick = True
                                        sick_chance += 1
                                    else:
                                        if is_sick:
                                            sick_chance *= 2
                                        is_sick = False
                                    if day not in weekends:
                                        if is_sick:
                                            mark = "Б"
                                        elif day in days:
                                            if day in tests:
                                                mark = random.choice([5, 5, 5, 5, 4, 4, 4, 3, 3, 2])
                                            else:
                                                if random.randint(1, mark_chance) == 1:
                                                    mark = random.choice([5, 5, 5, 5, 4, 4, 4, 3, 3, 2])
                                                    mark_chance = 9
                                                mark_chance -= 1
                                        if isinstance(mark, int):
                                            sum[i] += mark
                                            count[i] += 1
                                    table += str(mark).rjust(2) + "|"
                                table += "\n"
                            table += "\n"
                        avg = [s / c if c else None for s, c in zip(sum, count)]
                        yield table, avg

    def get_task(self):
        return self.current_task

    def check_task(self, answer):
        answer = answer.split()
        if len(answer) != len(self.current_ans):
            return False
        correct = True
        for i, j in zip(answer, self.current_ans):
            if j is None:
                if i != "н/а":
                    correct = False
            else:
                if abs(j - float(i)) > 1e-5:
                    correct = False
        self.current_task, self.current_ans = next(self.state)
        return correct


if __name__ == "__main__":
    while True:
        a = Task()
        print(a.get_task())
        print(a.current_ans)
        if None in a.current_ans:
            break
