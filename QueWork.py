from Que import Spider,Test
from App import logs
import sys,asyncio


def main():
    asyncio.ensure_future(Spider.Queue().work())
    asyncio.ensure_future(Test.Queue().work())
 
    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    except:
        main()
    finally:
        loop.close()
 
if __name__ == '__main__':
    main()