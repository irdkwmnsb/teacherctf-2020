import asyncio
import logging
import secrets

from grades import logger as main_logger
from grades.task import Task

FLAG = "SICAMP{nkaOmClQRjqJ1WZNZs5Wagjegffee}"


async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    host, port = writer.get_extra_info('peername')
    logger = main_logger.getChild(f"{host}:{port}")
    logger.info("Connection opened from %s", writer.get_extra_info('peername'))
    writer.write("DNEVNIK-RU-BKEND-62-02\n".encode())
    writer.write("Посчитайте средний балл для каждого ученика\n".encode())
    writer.write("Если ученик не набрал оценок за период следует вывести н/а\n".encode())
    task = Task()
    remaining = 450
    while remaining and not writer.is_closing():
        logger.info(f"{remaining} tasks left")
        writer.write(f"Осталось {remaining} заданий\n".encode())
        try:
            task_s = task.get_task()
            writer.write(task_s.encode())
            line = await reader.readuntil()
            logger.info(f"{len(line)} bytes received")
            try:
                correct = task.check_task(line)
            except Exception as e:
                writer.write("Неверный формат ответа\n".encode())
                logger.info("presentation error")
                continue
            if correct:
                remaining -= 1
                writer.write("Верно\n".encode())
                logger.info("correct")
            else:
                writer.write("Неверно\n".encode())
                logger.info("incorrect")
                break
        except Exception as e:
            writer.write("Непредвиденная ошибка\n".encode())
            logger.error(e)
            break
    if remaining <= 0:
        logger.info("solved")
        flag = FLAG
        writer.write(f"Ваш флаг: {flag}\n".encode())
    writer.write(f"До свидания!\n".encode())
    writer.write_eof()
    await writer.wait_closed()
