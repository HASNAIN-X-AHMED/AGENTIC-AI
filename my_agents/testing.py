# sync example :

import time

# # step 1
# print("pani ubalna shuru !")
# time.sleep(3)
# print("Pani ubal gaya")

# print("roti banana shuru !")
# time.sleep(3)
# print("roti ban gayi")

import asyncio

async def pani_ubalo():
    print("pani ubalna shuru... !")
    await asyncio.sleep(3)
    print("Pani ubal gaya")


async def roti_banao():
    print("roti banana shuru... !")
    await asyncio.sleep(5)
    print("roti ban gayi")


async def main():
    await asyncio.gather(
        pani_ubalo(),
        roti_banao()
    )

asyncio.run(main())    