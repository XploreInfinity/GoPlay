import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class gameRecommender:
    def __init__(self):
        #Load the games dataset:
        self.df = pd.read_csv('main/datasets/goodSteam.csv')
        #create the combined_features list:
        combined_features = self.df['genres']+' '+self.df['name']
        #Convert text features into numeric feature matrix:
        vectorizer = TfidfVectorizer()
        feature_vectors = vectorizer.fit_transform(combined_features)
        # getting the similarity scores using cosine similarity:
        self.similarity = cosine_similarity(feature_vectors)
    
    def getRecommendedGames(self,favGame):
        allTitles = self.df["name"].tolist()
        close_matches = difflib.get_close_matches(favGame, allTitles)
        favGame = close_matches[0]
        gameIndex = self.df[self.df.name == favGame].values[0][0]
        #get the similarity values for user's favourite game:
        similarity_score = list(enumerate(self.similarity[gameIndex]))
        #sort the games based on their similarity score:
        sorted_similar_games = sorted(similarity_score, key = lambda x:x[1], reverse = True)
        #store each game's chars in a tuple within this list:
        result = []
        num_games = 0
        for game in sorted_similar_games:
            idx = game[0]
            #recommend Only the top 10 games
            if num_games>10:
                break
            recrd = self.df.iloc[idx]
            result.append((recrd["appid"],recrd["name"],recrd["developer"],recrd["genres"].split(";"),int(recrd["weighted_score"]*100)))
            num_games+=1
        #the first recommended game will very likely be the user's input favorite game, remove it:
        result.pop(0)
        return result
          

        