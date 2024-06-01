import pandas as pd
from analyzer import Analyzer
file_path = 'output.csv'

analyzer = Analyzer()

data = pd.read_csv(file_path)
texts = data['Post Text']
embeddings = [analyzer.get_embedding(text) for text in texts]
reduced_embeddings = analyzer.reduce(embeddings)
