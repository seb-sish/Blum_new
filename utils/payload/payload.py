import subprocess
import asyncio

async def get_payload(gameId, points):
    process = await asyncio.create_subprocess_exec('node', 'utils/payload/blum.mjs', gameId, str(points), stdout=asyncio.subprocess.PIPE)
    output, _ = await process.communicate()
    payload = output.decode('utf-8').strip()
    return payload

if __name__ == '__main__':
    r = asyncio.run(get_payload("46cbf86f-b8f2-428d-b652-83168f4551d4", 203))
    print(r)
