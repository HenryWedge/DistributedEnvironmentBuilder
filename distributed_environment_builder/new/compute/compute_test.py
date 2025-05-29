import asyncio
import time
from threading import Thread

from compute import Compute

def monitor(compute):
    while True:
        print(compute.get_utilization())
        time.sleep(0.1)

async def request_queue(compute):
    print("start")
    await compute.submit(lambda: 2 + 5)
    await compute.submit(lambda: 3 + 3)
    await compute.submit(lambda: 3 + 3)
    await compute.submit(lambda: 3 + 3)
    await compute.submit(lambda: 3 + 3)

class ComputeTest:

    async def test(self):
        testee = Compute(2)
        monitor_thread = Thread(target=lambda: monitor(testee))
        monitor_thread.start()
        loop = asyncio.new_event_loop()
        loop2 = asyncio.new_event_loop()


        task1 = asyncio.create_task(request_queue(testee))
        task2 = asyncio.create_task(request_queue(testee))
        await asyncio.wait([task1, task2])

        #asyncio.set_event_loop(loop)
        #asyncio.set_event_loop(loop2)
#
        #loop.run_until_complete(request_queue(testee))
        #loop2.run_until_complete(request_queue(testee))
        #loop.close()
        #loop2.close()

        #request_queue1 = Thread(target=lambda: await request_queue(testee))
        #request_queue2 = Thread(target=lambda: await request_queue(testee))
        #request_queue1.start()
        #time.sleep(0.2)
        #request_queue2.start()
        #request_queue1.join()
        #request_queue2.join()
        monitor_thread.join()

if __name__ == '__main__':
    asyncio.run(ComputeTest().test())