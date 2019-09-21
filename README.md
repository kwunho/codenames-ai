# Codenames AI
In this project I created a fully playable digital version of the popular boardgame Codenames. But there is a twist. The roles of the spymasters are replaced by AI bots using NLP models. 

There are two main files: 

game_functions.py 
This contains all the functions used for the bot.

game_engine.py
This contains the code to create and launch the game. Simply run this file and the game will launch in a new window. It does take 5-10 minutes to load. This is mainly due to loading the NLP models. If the program is being run for the first time, then the NLP models will be downloaded directly from gensim and stored on the local machine. 


Here is an example of first few turns of a game.
The red bot (powered by wiki-gigaword) starts with the hint: **2 opera**.

![Screen Shot 2019-09-21 at 23 30 50](https://user-images.githubusercontent.com/37698146/65380095-b4205380-dccb-11e9-9916-1d54494b76b9.png)

I picked **conductor** and **shakespere**. These turned out to be correct so I ended the turn for red. The blue bot (powered by twitter) then gave the hint: **3 display**.  

![Screen Shot 2019-09-21 at 23 32 53](https://user-images.githubusercontent.com/37698146/65380107-f0ec4a80-dccb-11e9-94fd-3e15ef97ebb9.png)

I went with **tablet** and **wall** which were both blue agents. I wasn't sure on the 3rd word so I ended the turn. 

![Screen Shot 2019-09-21 at 23 35 32](https://user-images.githubusercontent.com/37698146/65380118-16795400-dccc-11e9-89e3-e379e3c714c7.png)

Red's next hint was **cat**. I wonder what that could be? Woof Woof!
