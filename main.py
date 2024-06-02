from scraper import Scraper
from analyzer import Analyzer
import time
from trainer import Trainer

user = 'alexjm1818@gmail.com'
password = '@mu11eR1818'

scraper = Scraper()
scraper.log_in(user, password)
scraper.browse_feed()
scraper.quit_driver()
'''

trainer = Trainer()
trainer.log_in(user, password)
trainer.get_samples()
trainer.quit_driver()

