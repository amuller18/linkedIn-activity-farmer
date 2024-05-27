from bs4 import BeautifulSoup, Tag
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import pandas as pd
from analyzer import Analyzer
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from training_data import X, Y

class Trainer:
    def __init__(self):
        self.driver = uc.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.analyzer = Analyzer()
        self.group_data, self.df = self.analyzer.train(X, Y) 
        self.llm = ChatOpenAI(openai_api_key = 'sk-proj-4IVgddwueZZzyEVyYG1QT3BlbkFJpsrtkYGp8RjldOyb7wUR', temperature=0.8)
       

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

    def get_samples(self):
        for i in range(100):
            for i in range(10):
                self.driver.find_element(By.XPATH, '/html').send_keys(Keys.PAGE_DOWN)
        df = pd.DataFrame(columns=['Post Text', 'Comment', 'Text Category', 'Chatgpt Category'])
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        posts_container = soup.find('div', class_ = 'scaffold-finite-scroll__content')
        for i, post in enumerate(posts_container.children):
            if isinstance(post, Tag):
                texts = [text.text for text in post.find_all(class_ = 'text-view-model')]
                if len(texts) > 1:
                    text = ''
                    for peice in texts[1:]:
                        text += peice

                    text_category = self.analyzer.predict(text, self.group_data)
                    comment = self.analyzer.generate_comment(text, text_category)
                    chatgpt_category = self.chatgpt_category(text)

                    df.loc[len(df)] = [text, comment, text_category, chatgpt_category]
                    time.sleep(15)
                else:
                    print('Bad category')

        df1 = pd.read_csv('output.csv')
        df1 = pd.concat([df, df1], ignore_index=True)
        df1.to_csv('output.csv')
    
    def chatgpt_category(self, text):
        template = """
        Your take is to categorize the text I give you into 4 categories. 1: Lessons/Insights, 2: Personal/Proffesional Announcements, 3: Current News/Events, 4: Other/Ads. Once you have categorized, Please return ONLY the number correspeonding to the category you choose.
        text: {text},
        """
        prompt = PromptTemplate.from_template(template)
        llm_chain = prompt | self.llm

        answer = llm_chain.invoke({
            'text': text,
        })
        return answer.content.strip('[]').replace(' ', '').split(',')

