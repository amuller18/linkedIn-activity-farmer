from transformers import AutoModel, AutoTokenizer
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class Analyzer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = AutoModel.from_pretrained('bert-base-uncased')
        self.llm = ChatOpenAI(openai_api_key = 'sk-proj-4IVgddwueZZzyEVyYG1QT3BlbkFJpsrtkYGp8RjldOyb7wUR', temperature=0.8)


    def get_embedding(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors='pt',
            padding=True,
            truncation=True
            )
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()
    
    def train(self, training_data, training_label):
        embeddings = []
        for data in training_data:
            embeddings.append(self.get_embedding(data))

        #flattened_embeddings = self.reduce(embeddings)
        df = pd.DataFrame({
            'Text': training_data,
            'Label' : training_label,
            'Embedding' : embeddings
        })

        df['Categories'] = df.apply(lambda x: self.categorize(x['Label']), axis=1)

        grouped = {key: df.loc[value] for key, value in df.groupby("Label").groups.items()}
        data = [grouped[0]['Embedding'].mean(), grouped[1]['Embedding'].mean(), grouped[2]['Embedding'].mean(), grouped[3]['Embedding'].mean()]

        return data, df
    
    def reduce(self, dataset):
        flattened_embeddings = [embedding.flatten() for embedding in dataset]
        stacked_embeddings = np.stack(flattened_embeddings)
        pca = PCA(n_components=2)
        reduced_output = pca.fit_transform(stacked_embeddings)
        return reduced_output
    
    def categorize(self, label):
        if label == 0:
            return 'Lesson'
        elif label == 1:
            return 'Announcement'
        elif label == 2:
            return 'News'
        else:
            return('Irrelevant')
    
    def predict(self, text, group_data):
        embedding = self.get_embedding(text)
        distance_to_Lesson = np.linalg.norm(embedding - group_data[0])
        distance_to_Announcement = np.linalg.norm(embedding - group_data[1])
        distance_to_News = np.linalg.norm(embedding - group_data[2])
        distance_to_Irrelevant = np.linalg.norm(embedding - group_data[3])
        distances = [distance_to_Lesson, distance_to_Announcement, distance_to_News, distance_to_Irrelevant]
        return distances.index(min(distances))
    
    def generate_comment(self, post, category):
        template = """
        Your task is to analyze a linkedIn post and write a comment on the context of the post to the author. The comment must be 1 sentence long. You will be given a category for each post. Please return only the comment and nothing else
        Post: {post},
        Category : {category}
        """
        prompt = PromptTemplate.from_template(template)
        llm_chain = prompt | self.llm

        answer = llm_chain.invoke({
            'post': post,
            'category': category
        })
        return answer.content
    
    def graph(self, reduced_data):
        #avg_x = [float(i[0]) for i in reduced_averages]
        #avg_y = [float(i[1]) for i in reduced_averages] 
        x = [float(i[0]) for i in reduced_data]
        y = [float(i[1]) for i in reduced_data]

        fig, ax = plt.subplots()

        sc = ax.scatter(x, y, cmap='viridis', marker="o")
        #ax.plot(avg_x, avg_y, linestyle="None", marker = 'o', color='red')
        cbar = plt.colorbar(sc)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Embeddings")

        plt.show()
    