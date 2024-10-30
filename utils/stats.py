from utils.blum import Blum
from utils.core import logger
from data.config import config
import datetime
import pandas as pd
from utils.telegram import Accounts
import asyncio


async def stats():
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
                tasks.append(asyncio.create_task(Blum(account=account, thread=thread, proxy=proxy_dict[account]).stats()))
            else:
                tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).stats()))
    else:
        for thread, account in enumerate(accounts):
            tasks.append(asyncio.create_task(Blum(account=account, thread=thread,proxy = None).stats()))

    # for thread, account in enumerate(accounts):
    #     tasks.append(asyncio.create_task(Blum(session_name=account["session_name"], phone_number=account["phone_number"], 
    #                                              thread=thread, proxy=account["proxy"]).stats()))

    data = await asyncio.gather(*tasks)

    path = f"statistics/statistics_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
    columns = ['Name', 'Points', 'Play passes', 'Referrals', 'Proxy (login:password@ip:port)']

    df = pd.DataFrame(data, columns=columns)
    df['Name'] = df['Name'].astype(str)
    df.to_csv(path, index=False, encoding='utf-8-sig')

    logger.success(f"Saved statistics to {path}")