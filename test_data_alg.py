import pandas as pd
from analyzer import Analyzer
file_path = 'output.csv'

analyzer = Analyzer()
analyzer.train_model()
data = pd.read_csv(file_path)
data['Post Text'].apply(lambda x: print(f'\n{analyzer.predict(x)} is the label for {x}'))
#data.apply(lambda x: print(x['Post Text']))