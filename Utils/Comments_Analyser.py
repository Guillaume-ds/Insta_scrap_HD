import pandas as pd
import numpy as np
import re 
from transformers import pipeline



class commentsAnalyser():
    def __init__(self,postId):
        self.postId=postId
        self.answers = []

        self.pos_index = []
        self.neg_index = []
        self.simple_answers_indexes = []

        self.complexe_answers_df = []

        self.classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

    def get_dataset(self):
        try:
            self.answers = pd.read_csv(f"./data/{self.postId}_comments.csv")
            return True
        except FileNotFoundError:
            return False

    def get_yesno_responses(self,pos=True):
        # Créer une expression régulière pour rechercher "oui" comme un mot complet, avec de la ponctuation, des emojis ou d'autres caractères
        if pos:
            word = "oui"
        else:
            word = "non"
        regex = fr'\b{word}\b|\b{word}[.,!?]+\b|\b{word}\b[^\w\s]+|\b{word}\b\S+'
        
        # Filtrer les réponses du DataFrame en utilisant l'expression régulière et en excluant les réponses avec d'autres mots
        responses = self.answers[self.answers['answers'].str.contains(regex, flags=re.IGNORECASE, regex=True) &
                                self.answers['answers'].str.match(fr'^\b{word}\b[.,!?]*\W*$', flags=re.IGNORECASE)]

        return responses.index

        
    def get_simple_answers(self):
        print(self.answers.shape)
        self.pos_index = self.get_yesno_responses(True)
        self.neg_index = self.get_yesno_responses(False)
        self.simple_answers_indexes = np.concatenate([self.pos_index,self.neg_index])
        return (len(self.pos_index),len(self.neg_index),len(self.simple_answers_indexes))

    def analyse_complexe_answers(self):
        self.complexe_answers_df = self.answers[~(self.answers.index.isin(self.simple_answers_indexes))]
        sequence_to_classify = list(self.complexe_answers_df.answers.values)
        candidate_labels = ["pour","contre","neutre"]
        output = self.classifier (sequence_to_classify, candidate_labels, multi_label=False)
        labels = [answer['labels'][0] for answer in output]
        self.complexe_answers_df['labels'] = labels
        scores = [answer['scores'][0] for answer in output]
        self.complexe_answers_df['scores'] = scores
        
        self.answers = self.answers.merge(self.complexe_answers_df,how='outer')
        return self.complexe_answers_df

    def save_df(self):
        self.answers .to_csv(path_or_buf=f"./data/{self.postId}_comments.csv",index=False)