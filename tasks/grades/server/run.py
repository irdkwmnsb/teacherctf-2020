import asyncio
import grades
import sys

asyncio.run(grades.main(sys.argv[1], int(sys.argv[2])))
