import os
from random import shuffle, randint
from guizero import App, Box, Picture, PushButton, Text
from guizero import warn

# set the path to the emoji folder on your computer
emojis_dir = "emojis"
# create a list of the locations of the emoji images
emojis = [os.path.join(emojis_dir, f) for f in os.listdir(emojis_dir) if os.path.isfile(os.path.join(emojis_dir, f))]
# shuffle the emojis
shuffle(emojis)

player = 1

## Add multiple players
def switch_player():    
    global player 
    global score
    global timer
    if player == 1:
        score = player1_score_num
        timer = player1_timer_num
        player = 2
    else:
        score = player2_score_num
        timer = player2_timer_num
        player = 1

def match_emoji(matched):
    if matched:
        result.value = "correct"
        score.value = int(score.value) + 1 

    else:
        result.value = "incorrect"
        
    setup_round()


def setup_round():
    ##switch between players
    switch_player()

    if int(timer.value) > 0:
        # for each picture and button in the list assign an emoji to its image feature
        for picture in pictures:
            # make the picture a random emoji
            picture.image = emojis.pop()

        for button in buttons:
            # make the image feature of the PushButton a random emoji
            button.image = emojis.pop()
            # set the command to be called and pass False, as these emoji wont be the matching ones
            button.update_command(match_emoji, [False])

        # choose a new emoji
        matched_emoji = emojis.pop()

        # select a number at random
        random_picture = randint(0,8)
        # change the image feature of the Picture with this index in the list of pictures to the new emoji
        pictures[random_picture].image = matched_emoji

        random_button = randint(0,8)
        # change the image feature of the PushButton with this index in the list of buttons to the new emoji
        buttons[random_button].image = matched_emoji
        # set the command to be called and pass True, as this is the matching emoji
        buttons[random_button].update_command(match_emoji, [True])

def counter():
    if int(timer.value) <= 0:
        setup_round()
        if int(timer.value) <= 0:
            timer.cancel(counter)
            # reset the timer
            result.value = "Game Over"
            app.info("Time Out", "{} scored {} points \n{} scored {} points"
                 .format(player1_txt_name.value, player1_score_num.value,
                         player2_txt_name.value, player2_score_num.value))
            # reset timer
            timer.value = "10"
            # reset result
            result.value = ""
            # reset score
            score.value = "0"
            # start new round
            setup_round()
            #restart timer
            timer.repeat(1000, counter)
    else:
            timer.value = int(timer.value) - 1


# setup the app
app = App("emoji match", height = 300, width = 900)

player1_name = app.question("Player 1 name", "Enter player 1 name", initial_value="Player 1")
player2_name = app.question("Player 2 name", "Enter player 1 name", initial_value="Player 2")

result = Text(app)

# create a box to house the grids
game_box = Box(app)

## create a box to house player 1's data
player1_box = Box (game_box, align = "left", layout = "grid")
player1_txt = Text (player1_box, text = "Player 1:", grid = [0,0])
player1_txt_name = Text (player1_box, text = player1_name, grid = [1,0])
player1_score = Text (player1_box, text = "Score", grid = [0,1])
player1_score_num = Text (player1_box, text = "0", grid = [1,1])
player1_timer = Text (player1_box, text = "Remaining time: ", grid = [0,2])
player1_timer_num = Text (player1_box, text = "10", grid = [1,2])

# create a box to house the pictures
pictures_box = Box(game_box, layout="grid", align = "left")

## create a box to house player 2 data
player2_box = Box (game_box, align = "right", layout = "grid")
player2_txt = Text (player2_box, text = "Player 2:", grid = [0,0])
player2_txt_name = Text (player2_box, text = player2_name, grid = [1,0])
player2_score = Text (player2_box, text = "Score", grid = [0,1])
player2_score_num = Text (player2_box, text = "0", grid = [1,1])
player2_timer = Text (player2_box, text = "Remaining time: ", grid = [0,2])
player2_timer_num = Text (player2_box, text = "10", grid = [1,2])
                   
# create a box to house the buttons
buttons_box = Box(game_box, layout="grid", align = "right")

# add in the extra features
extra_features = Box(app)
timer = player1_timer_num

# start the timer
timer.value = 10
timer.repeat(1000,counter)

# create the an empty lists to add the buttons and pictures to
buttons = []
pictures = []
# create 9 PushButtons with a different grid coordinate and add to the list
for x in range(0,3):
    for y in range(0,3):
        # put the pictures and buttons into the lists
        picture = Picture(pictures_box, grid=[x,y])
        pictures.append(picture)
        
        button = PushButton(buttons_box, grid=[x,y])
        buttons.append(button)
    

setup_round()

'''
scoreboard = Box(app) 
label = Text(scoreboard, text="Score", align="left") 
score = Text(scoreboard, text="0", align="left") 
'''

app.display()
