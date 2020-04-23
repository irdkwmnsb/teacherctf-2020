import logging
import asyncio
import sys

logger = logging.getLogger("grades")
logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter("[%(asctime)s] [%(name)8s] [%(levelname)-5.5s] --- %(message)s")

file_handler = logging.FileHandler("./latest.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

async def main(host="127.0.0.1", port=8888, **kwargs):
    import grades.server
    server = await asyncio.start_server(grades.server.handle_connection, host, port, **kwargs)

    addr = server.sockets[0].getsockname()
    logger.info("Serving on %s", addr)

    async with server:
        await server.serve_forever()
