import asyncio

from pypjlink import Projector

async def main():
  async with await Projector.from_address('kbox-il-dev-01') as projector:
    res = await projector.authenticate()
    res = await projector.get_power()
    print(res)



asyncio.run(main())