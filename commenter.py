from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(openai_api_key = 'sk-proj-4IVgddwueZZzyEVyYG1QT3BlbkFJpsrtkYGp8RjldOyb7wUR', temperature=0.8)

template = """
Your task is to analyze a linkedIn post and write a comment on the context of the post to the author. The comment must be 1 sentence long. You will be given a category for each post. Please return only the comment and nothing else
Post: {post},
Category : {category}
"""

prompt = PromptTemplate.from_template(template)
llm_chain = prompt | llm

post = '''
🚀 Amazon Q, the most capable generative AI-powered assistant designed for accelerating software development and leveraging company knowledge and data is now generally available on AWS.With Amazon Q, employees can get answers to questions across their business, such as company policies, product information, business results, code base, employees, and many other topics by connecting to enterprise data repositories to summarize the data logically, analyze trends, and engage in dialog about the data. https://lnkd.in/ePjAvhBS .
'''
category = 'Announcement'

answer = llm_chain.invoke({
    'post': post,
    'category': category
})
answer.content