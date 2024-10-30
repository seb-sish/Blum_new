from utils.core import create_sessions
from utils.telegram import Accounts
from utils.blum import Blum
from utils.stats import stats
from data.config import config
import asyncio
import sys
import os


async def main():
    action = get_action()
    if not os.path.exists('sessions'): os.mkdir('sessions')
    if not os.path.exists('statistics'): os.mkdir('statistics')
    # if not os.path.exists('sessions/accounts.json'):
    #     with open("sessions/accounts.json", 'w') as f:
    #         f.write("[]")

    match action:
        case 3: await stats()
        case 2: await create_sessions()

        case 1:
            accounts = await Accounts().get_accounts()
                    
            tasks = []
            if config.USE_PROXY:
                proxy_dict = {}
                with open('proxy.txt','r',encoding='utf-8') as file:
                    proxy = [i.strip().split() for i in file.readlines() if len(i.strip().split()) == 2]
                    for prox,name in proxy:
                        proxy_dict[name] = prox
                for thread, account in enumerate(accounts):
                    if account in proxy_dict:
                        tasks.append(asyncio.create_task(Blum(account=account, thread=thread, proxy=proxy_dict[account]).main()))
                    else:
                        tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).main()))
            else:
                for thread, account in enumerate(accounts):
                    tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).main()))
            await asyncio.gather(*tasks)

def get_action():
    if len(sys.argv) == 2: action = sys.argv[1]
    else: action = input("Select action:\n1. Start soft\n2. Create sessions\n3. Get statistics\n\n> ")
    
    if action in ["1", "2", "3"]: return int(action)
    else: 
        print("Wrong value! Try again...\n")
        return get_action()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
