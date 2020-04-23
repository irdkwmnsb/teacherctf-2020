import asyncio


async def main(loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 1337, loop=loop)
    await reader.readline()
    await reader.readline()
    await reader.readline()

    n_tasks = 0
    while n_tasks != 1:
        tasks = await reader.readline()
        n_tasks = int(tasks.split()[1])
        print("left", n_tasks)

        header = (await reader.readline()).decode()
        print("school", header)

        count = [0]
        sum = [0]
        for _ in range(3):
            await reader.readline()
            await reader.readline()
            i = 0
            while True:
                line = (await reader.readline()).decode()
                if line == "\n":
                    break
                if len(count) <= i:
                    count.append(0)
                    sum.append(0)
                for mark in line.split("|"):
                    mark = mark.strip()
                    if mark.isdecimal():
                        count[i] += 1
                        sum[i] += int(mark)
                i += 1
        print(sum, count)
        ans = ""
        for s, c in zip(sum, count):
            if c == 0:
                ans += "н/а "
            else:
                ans += str(s / c) + " "
        ans = ans.strip()
        print(ans)
        writer.write(ans.encode() + b"\n")
        line = (await reader.readline()).decode()
        print(line.strip())
    flag = (await reader.readline()).decode()
    print(flag.strip())


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()
