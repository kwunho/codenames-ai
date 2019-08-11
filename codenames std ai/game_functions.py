import pandas as pd
from random import sample
import itertools



def opposite_team(color):
    if color == 'blue':
        return 'red'
    elif color == 'red':
        return 'blue'
    else:
        raise Exception(f"Invalid Color Input!\n'{color}' is not red or blue.")
        
        
def generate_board(word_list,first_team=None):
    
    if first_team:
        if first_team in ['red','blue']:
            first_color=first_team
        else:
            raise Exception(f"Invalid Color Input!\n'{first_team}' is not red or blue.")
    else:
        first_color=sample(['red','blue'],1)[0]
    word_sample=sample(word_list,25)
    
    board = {
        first_color: word_sample[0:9],
        opposite_team(first_color): word_sample[9:17],
        'civilian': word_sample[17:-1],
        'assassin': [word_sample[-1]]
    }
    return board,first_color


def reveal_word(word,board):
    board_items=list(board.items())
    for c in board_items:
        if word in c[1]:
            return c[0]
    raise Exception(f"Word '{word}' is not on the board.")
    
def board_remove_word(board,remove_word,card_type):
    #board_c=board.copy()
    
    board[card_type]=[w for w in board[card_type] if w != remove_word]
    #return board_c

def check_board(board,team):
    if not board['blue']:
        return 'blue'
    elif not board['red']:
        return 'red'
    elif not board['assassin']:
        return opposite_team(team)
    else:
        return 
def get_remaining_agents(board):
    return len(board['blue']),len(board['red'])
    
    
    
    
def get_board_words(board):
    return [item for sublist in board.values()  for item in sublist]



    
def bot(player,board,model,min_sim=0.40):
    
    #opp=opposite_team(player)
    
    board_words=get_board_words(board)
    

    avoid_words=board['assassin']
    #single word
    
    datalist=[]
    for i in range(1,min(6,len(board[player])+1)):
        for w in list(itertools.combinations(board[player], i)):
            hints=get_hints(w,avoid_words,board_words,model)
            hints_df=pd.DataFrame(hints,columns=['hint','score'])
            hints_df['number']=i
            #hints_df['postive_words']=','.join(w)
            
            datalist.append(hints_df)
            
    hints_df=pd.concat(datalist).drop_duplicates(['hint','number'])
    
  
    hints_df[['effective','valid_number','sum_sim','target_words']]=hints_df.apply(lambda x: evaluate_hint(player,x.hint,x.number,board,model,min_sim),axis=1)
    
    hint=tuple(hints_df[hints_df.effective==1].sort_values(['valid_number','sum_sim'],ascending=False).iloc[0][['valid_number','hint','target_words']])
    print(f'{player} hint {hint[1]} targeted: {hint[2]}')
    return f'{str(hint[0])}: {hint[1]}'

def get_hints(target_words,avoid_words,board_words,model):
    sim_words=model.most_similar(
                    positive=target_words,
                    negative=avoid_words,
                    topn=20
                    )
    return clean_sim_words(sim_words,board_words)
def clean_sim_words(sim_words,board_words):
    return [sw for sw in sim_words if check_hint(sw[0],board_words)]
     
def check_hint(hint,board_words):
    hint=hint.lower()
    if '_' in hint:
        return False
    for w in board_words:
        if (w in hint)|(hint in w):
            return False
    else:
        return True
    
def evaluate_hint(player,hint,number,board,model,min_sim):
    #return:
    #effective hint
    #valid_number
    #sum of similaities
    #list of target words
    
    df=board_df(board)
    df['hint_sim']=df.word.apply(lambda x: max(model.similarity(hint,x),0))
    df=df[(df.card!=player)|(df.hint_sim>min_sim)].sort_values('hint_sim',ascending=False).head(number)
    return pd.Series([(df.card==player).mean()==1,len(df), df.hint_sim.sum(),','.join(df.word)])
    
def board_df(board):
    datalist=[]
    for k in board.keys():
        datalist.append(pd.DataFrame({'card':k,'word':board[k]}))
    return pd.concat(datalist)