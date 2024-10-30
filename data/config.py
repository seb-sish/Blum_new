from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    USE_TG_BOT: bool = False 
    BOT_TOKEN: str 
    CHAT_ID: int 


    # задержка между подключениями к аккаунтам
    ACC_DELAY: list[int] = [5, 60]


    # использование прокси
    USE_PROXY: bool = True 
    # тип прокси
    PROXY_TYPE: str = "socks5" 


    # играть дроп гейм
    DROP_GAME: bool = True 
    # скок поинтов с игры
    POINTS: list[int] = [150,200] 
    # сон между играми
    SLEEP_GAME_TIME: list[int] = [30,50] 
    # мини задержки
    MINI_SLEEP: list[int] = [3,7] 


    # делать таски
    DO_TASKS: bool = True
    # доп задержка после 8часов 
    SLEEP_8HOURS: list[int] = [360,3600]

    # папка с сессиями (не менять)
    WORKDIR: str = "sessions/"

config = Config()