import requests
from pycube.components import *
from pycube.core import Application
import time 
from .helper import get_coins

class App(Application):
    def onStart(self):
        self.coins = VScrollView((10,10), width=SCREEN_WIDTH, height=SCREEN_HEIGHT, border=2, borderColor=WHITE)
        self.container.add_child(self.coins)
        self.last_time = time.time()
        self.first_run = True
        self.job_id = self.tasker.add_job(get_coins).get_id()
        spinner = Spinner((200,100), width=50, height=50)
        self.spinner_container = Container((10,10), width=SCREEN_WIDTH-20, height=SCREEN_HEIGHT -20)
        self.spinner_container.add_child(spinner)
        self.coins.add_child(self.spinner_container)
        #self.update_coins(self.get_coins())

    def run(self):
        if self.job_id:
            try:
                job = self.tasker.get_job(self.job_id)
                if job.is_finished:
                    self.logger.info("Job done")
                    self.coins.remove_child(self.spinner_container)
                    self.update_coins(job.result)
                    self.job_id = None
                else:
                    self.logger.info("Job in process")
            except Exception as e:
                self.logger.info("Something happened")
                self.logger.info(e)
                self.job_id = None
    
    def get_coins(self):
        try:
            coins = ["bitcoin","ethereum","litecoin"]
            coin_data = []
            for c in coins:
                coin = requests.get(f"https://api.coingecko.com/api/v3/coins/{c}").json()
                coin_data.append(coin)
            return coin_data
        except Exception as e:
            self.logger.warning(e)
            return []

    def update_coins(self, coins):
        self.coins.clear_children()
        for coin in coins:
            name = Label((0,0), text=f"{coin['symbol']} | {coin['name']}", size=20)
            rank = VBox((0,0), width=50, height=50)
            rank.add_child(Label((0,0), text="Rank"))
            rank.add_child(Label((0,0), text=f"{coin['market_cap_rank']}"))
            price = VBox((0,0), width=50, height=50)
            price.add_child(Label((0,0), text="Price"))
            price.add_child(Label((0,0), text=f"{coin['market_data']['current_price']['usd']}"))
            hbox = HBox((0,0), width=350, height=50)
            hbox.add_child(rank)
            hbox.add_child(price)
            container = VBox((0,0), width= SCREEN_WIDTH, height=90)
            container.add_child(name)
            container.add_child(hbox)
            container.add_child(Line((0,0), width=SCREEN_WIDTH - 20, height=2, color=WHITE))
            self.coins.add_child(container)
        