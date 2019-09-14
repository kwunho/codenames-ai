# codenames-ai
In this project I created a fully playable digital version of the popular boardgame Codenames. But there is a twist. The roles of the spymasters are replaced by AI bots using NLP models. 

There are three files. 

requirements.txt 
This has a list of all the dependent python packages. 

game_functions.py 
This contains all the functions used for the bot.

game_engine.py
This contains the code to create and launch the game. Simply run this file and the game will launch in a new window. It does take 5-10 minutes to load. This is mainly due to loading the NLP models. If the program is being run for the first time, then the NLP models will be downloaded directly from gensim and stored on the local machine. 

Menu Screen

Game Screen


