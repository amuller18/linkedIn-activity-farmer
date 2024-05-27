from bs4 import BeautifulSoup, Tag
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import pandas as pd
from analyzer import Analyzer
from training_data import X, Y

class Scraper:
    def __init__(self):
        self.driver = uc.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.analyzer = Analyzer()
        self.group_data, self.df = self.analyzer.train(X, Y)        

    def quit_driver(self):
        self.driver.quit()

    def log_in(self, username, password):
        self.driver.get('https://www.linkedin.com/home')
        time.sleep(2)
        self.driver.find_element(By.ID, 'session_key').send_keys(username)
        time.sleep(0.5)
        self.driver.find_element(By.ID, 'session_password').send_keys(password)
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button').click()
        time.sleep(3)
        try:
            self.driver.find_element(By.ID, 'captchaInternalPath')
            print('Solve Captcha')
            time.sleep(10)
        except:
            time.sleep(1)
    
    def switch_accounts_for_commenting(self, new_account):
        self.driver.find_elements(By.CLASS_NAME, )

    def browse_feed(self):
        df = pd.DataFrame(columns=['Post Text', 'Comment', 'Comment Id'])
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        posts_container = soup.find('div', class_ = 'scaffold-finite-scroll__content')
        num = 0
        commented_posts = []
        for i, post in enumerate(posts_container.children):
            if isinstance(post, Tag):
                print(i)
                for descendant in post.descendants:
                    if hasattr(descendant, 'has_attr') and descendant.has_attr('id'):
                        if 'feed-shared-social-action-bar-comment-ember' in descendant.get('id') and descendant.get('id') not in commented_posts:
                            comment_id = descendant.get('id')
                            print(f'Found comment id, {comment_id}')

                texts = [text.text for text in post.find_all(class_ = 'text-view-model')]
                if len(texts) > 1:
                    text = ''
                    for peice in texts[1:]:
                        text += peice
                        print('found text')

                    print(comment_id)
                    if comment_id not in commented_posts:
                        text_category = self.analyzer.predict(text, self.group_data)
                        if text_category in [0,1,2]:
                            comment = self.analyzer.generate_comment(text, text_category)
                            self.comment_on_post(comment, comment_id, post)
                            commented_posts.append(comment_id)
                            num += 1
                            time.sleep(15)
                    else:
                        print('Bad category')

                    #df.loc[len(df)] = [text, comment, comment_id]
        
    def comment_on_post(self, comment, comment_id, post):
        print(comment_id)
        comment_button = self.driver.find_element(By.ID, comment_id)
        actions = ActionChains(self.driver)
        actions.move_to_element(comment_button).perform()        
        time.sleep(1)
        comment_button.click()
        actions.send_keys(str(comment)).perform()
        time.sleep(3)
        elements = self.driver.find_elements(By.TAG_NAME, 'button')
        for element in elements:
            if element.text == 'Post':
                element.get_attribute('id')
                self.driver.find_element(By.ID, element.get_attribute('id')).click()

        print('Commented on post')
