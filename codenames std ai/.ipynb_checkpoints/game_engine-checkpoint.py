import gensim.downloader as api

#glove-wiki-gigaword-300
#glove-twitter-200
#fasttext-wiki-news-subwords-300
#conceptnet-numberbatch-17-06-300

red_model = api.load("glove-wiki-gigaword-300")
blue_model = api.load("glove-twitter-200")

player_bot={'blue':blue_model,
            'red':red_model}

print('Models loaded')
import pickle
import game_functions as gf
from random import shuffle


card_cood=pickle.load(open('card_cood.p','rb'))

word_list=pickle.load(open('cn_std_word_list.p','rb'))





#dimensions
card_width=180
card_height=120
display_width = 1400
display_height = 775

#colors
black = (0,0,0)
white = (255,255,255)
beige=(245,245,220)
beige_sel=(217,179,130)
red=(255,0,0)
dark_red=(139,0,0)
blue=(0,0,255)
dark_blue=(0,0,139)
grey=(169,169,169)
snow=(255,255,250)

card_color={'red':red,
            'blue':blue,
            'civilian':grey,
            'assassin':black
    }

end_turn_col={'blue':[blue,dark_red],
              'red':[dark_blue,red]
    
}

team_end_turn={'blue':40,
              'red':1240}




import pygame
import time

pygame.init()


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Codenames AI')
clock = pygame.time.Clock()

def pick_card(word,x,y):
    card_type=gf.reveal_word(word,board)
    card_col=card_color[card_type]
    pygame.draw.rect(gameDisplay, card_col,(x,y,card_width+10,card_height+10))
    pygame.display.update()
    
    

def text_objects(text, font,color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()


def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    
    click = pygame.mouse.get_pressed()
    #print(click)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action == pick_card: 
            pick_card(msg,x,y)
        elif click[0] == 1 and action != None:
            action() 
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect) 
    
def box(msg,x,y,w,h,ic,f_size,f_col=black):
    pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.Font("freesansbold.ttf",f_size)
    textSurf, textRect = text_objects(msg, smallText,f_col)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect) 
    
    
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Codenames_AI", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        
        
        button('Play',610, 445,180,120,beige,beige_sel,game_loop)
        
        pygame.display.update()
        clock.tick(15)

def game_loop():
    
    board,cur_team=gf.generate_board(word_list)
    print(board)

    board_words=gf.get_board_words(board)
    shuffle(board_words)
    picked_words=[]

    blue_agents,red_agents=gf.get_remaining_agents(board)
    
    card_col=[beige]*25
    card_col_sel= [beige_sel]*25
    
    intro = True
    
    hint={cur_team:'thinking...',
         gf.opposite_team(cur_team):''}
    
                            
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if (event.type == pygame.MOUSEBUTTONDOWN):
                
                mouse = pygame.mouse.get_pos()
                for i,(c,word) in enumerate(zip(card_cood,board_words)):#click on card
                    
                    if c[0]+card_width > mouse[0] > c[0] and c[1]+ card_height> mouse[1] > c[1] and word not in picked_words:
                        picked_words.append(word)
                        card_type=gf.reveal_word(word,board)
                        card_col[i]=card_color[card_type]
                        card_col_sel[i]=card_color[card_type]
                        gf.board_remove_word(board,word,card_type)
                        if card_type=='blue':
                            blue_agents-=1
                        if card_type=='red':
                            red_agents-=1
                        if card_type!=cur_team:
                            cur_team=gf.opposite_team(cur_team)
                            hint[cur_team]='thinking...'
                            hint[gf.opposite_team(cur_team)]=''
                        
                if team_end_turn[cur_team]+120 > mouse[0] > team_end_turn[cur_team] and 550+ 60> mouse[1] > 550: 
                    cur_team=gf.opposite_team(cur_team)
                    hint[cur_team]='thinking...'
                    hint[gf.opposite_team(cur_team)]=''
                    
                #game restart
                if 1250+100 > mouse[0] > 1250 and 700+ 50> mouse[1] > 700:
                    game_loop()
                    
                
        gameDisplay.fill(white)

        for c,word,col,col_sel in zip(card_cood,board_words,card_col,card_col_sel):
            button(word,c[0],c[1],card_width,card_height,col,col_sel)
        box(f"It's {cur_team}'s turn!",200,710,1000,50,white,30, card_color[cur_team])
        
        box('Blue Agents Remaining:',25,165,150,25,white,15) #blue team agents
        box(str(blue_agents),25,190,150,50,white,35,blue)
        box('Red Agents Remaining:',1225,165,150,25,white,15) #red team agents
        box(str(red_agents),1225,190,150,50,white,35,red)
        
        
        
        
        box(hint['blue'],25,315,150,100,snow,25) #blue team hint
        box(hint['red'],1225,315,150,100,snow,25) #red team hint
        
        
        button('End Turn',40,550,120,60,end_turn_col[cur_team][0],dark_blue) #blue team end
        button('End Turn',1240,550,120,60,end_turn_col[cur_team][1],dark_red) #red team end
        
        button('Restart',1250,700,100,50,beige,beige_sel)
        
        winner=gf.check_board(board,cur_team)
        if winner:
            box(f'{cur_team.upper()} WINS!!!',200,710,1000,50,white,30,card_color[cur_team])
            pygame.display.update()
            time.sleep(2)
            game_loop()
            
        pygame.display.update()
        clock.tick(15)
        if 'thinking...' in list(hint.values()):
            hint[cur_team]=gf.bot(cur_team,board,player_bot[cur_team])
        
        
        pygame.display.update()
        clock.tick(15)
    
game_intro()  

pygame.quit()



