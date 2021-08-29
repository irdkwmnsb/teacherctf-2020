import requests

url = "http://localhost:8080"


def find_ans(r, n):
    g1 = [[True] * n for _ in range(n)]
    for f, t in r:
        g1[f][t] = False
        g1[t][f] = False
    g = [set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if g1[i][j]:
                g[i].add(j)
                g[j].add(i)

    cur_pairs = []
    used = [False] * n

    def find():
        if len(cur_pairs) > 15:
            return False
        found_f = False
        found_t = False
        for f in range(n):
            if not used[f]:
                used[f] = True
                found_f = True
                for t in g[f]:
                    if not used[t]:
                        used[t] = True
                        found_t = True
                        cur_pairs.append([f, t])
                        if find():
                            return True
                        cur_pairs.pop()
                        used[t] = False
                if found_t is False:
                    cur_pairs.append([f])
                    if find():
                        return True
                    cur_pairs.pop()
                used[f] = False
        return not found_f

    find()
    return cur_pairs


with requests.Session() as s:
    p = None
    while True:
        p = s.get(url).text
        if "SICAMP" in p:
            break
        else:
            hates = eval(p.split("var hates = ")[-1].split(";")[0])
            num_students = int(p.split("var student_count = ")[-1].split(";")[0])
            done = int(p.split("var done = ")[-1].split(";")[0])
            total = int(p.split("var total = ")[-1].split(";")[0])
            print(done, total)
            print("remaining", total - done)
            print(num_students)
            print(len(hates))
            ans = find_ans(hates, num_students)
            print(ans)
            r = s.post(url + "/check", json=ans)
            print(r.cookies)
            print(r.text)
            # print(hates)
    print(p)
