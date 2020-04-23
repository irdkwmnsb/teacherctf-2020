import random
import itertools


def make_task():
    n = random.randint(26, 28)
    a = list(range(n))
    random.shuffle(a)
    test = []
    for i in range(n - 1):
        if i % 2 == 0:
            l = min(7,  n - i - 2)
            h = min(19, n - i - 2)
            m = random.randint(l, h)
            e = random.sample(a[i + 2:], m)
            test.extend([a[i], j] for j in e)
        else:
            l = min(7,  n - i - 1)
            h = min(19, n - i - 1)
            m = random.randint(l, h)
            e = random.sample(a[i + 1:], m)
            test.extend([a[i], j] for j in e)
    ans = []
    for i in range(n):
        if i % 2 == 0:
            ans.append([])
        ans[-1].append(a[i])
    test_res, test_msg = check_task((n, test), ans)
    assert test_res, test_msg
    return n, test


def check_task(test, answer):
    if len(answer) > 15:
        return False, "Number of desks is more than 15."
    n = test[0]
    studs = set()
    for a in answer:
        if len(a) > 2:
            return False, "You cannot sit more than two people at one desk."
        elif len(a) > 1:
            if not isinstance(a[0], int):
                return False, f"{a[0]} is not integer"
            if not 0 <= a[0] < n:
                return False, f"{a[0]} is not in this class"
            if a[0] in studs:
                return False, f"{a[0]} is already seated"
            studs.add(a[0])
            if not isinstance(a[1], int):
                return False, f"{a[1]} is not integer"
            if not 0 <= a[1] < n:
                return False, f"{a[1]} is not in this class"
            if a[1] in studs:
                return False, f"{a[1]} is already seated"
            studs.add(a[1])
            if [a[0], a[1]] in test or [a[1], a[0]] in test:
                return f"{a[0]} and {a[1]} cannot not be seated together."
        elif len(a) > 0:
            if not isinstance(a[0], int):
                return False, f"{a[0]} is not integer"
            if not 0 <= a[0] < n:
                return False, f"{a[0]} is not in this class"
            if a[0] in studs:
                return False, f"{a[0]} is already seated"
            studs.add(a[0])
    if len(studs) < n:
        return False, f"Got only {len(studs)} students. Expected {n}."
    return True, "All correct"


if __name__ == "__main__":
    while True:
        print(make_task())
