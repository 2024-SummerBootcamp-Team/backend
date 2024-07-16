from anyio import create_task_group, create_memory_object_stream, run, Semaphore, sleep, Lock
from anyio.streams.memory import MemoryObjectReceiveStream
import random


async def process_items(send_stream: MemoryObjectReceiveStream[str], lock: any) -> None:
    async with lock:
        async with send_stream:
            for num in range(10):
                await send_stream.send(f'number {num}')
                await sleep(random.uniform(0.01, 0.1))


async def main():
    # The [str] specifies the type of the objects being passed through the
    # memory object stream. This is a bit of trick, as create_memory_object_stream
    # is actually a class masquerading as a function.
    send_stream, receive_stream = create_memory_object_stream[str]()
    lock = Lock()

    async with create_task_group() as tg:
        tg.start_soon(process_items, send_stream, lock)
        async with receive_stream:
            async for item in receive_stream:
                print('received', item)


run(main)