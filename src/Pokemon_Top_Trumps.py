# Pokémon Top Trumps written by Melanie Clark and Emily Gillings Aug 24
import random
import requests
import emoji
# word2number converts written numbers to numbers https://pypi.org/project/word2number/
from word2number import w2n
import csv
import os
import turtle

# https://www.geeksforgeeks.org/python-program-to-print-emojis/
smile_emoji = emoji.emojize(':grinning_face_with_big_eyes:')
crying_emoji = emoji.emojize(':crying_face:')


# Retrieves a random Pokemon
def random_pokemon():
    pokemon_id = random.randint(1, 151)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    pokemon = response.json()

    return {
        'name': pokemon['name'].title(),
        'id': pokemon['id'],
        'height': pokemon['height'],
        'weight': pokemon['weight'],
        'base experience': pokemon['base_experience'],
        'health': pokemon['stats'][0]['base_stat'],
        'attack': pokemon['stats'][1]['base_stat'],
        'defence': pokemon['stats'][2]['base_stat'],
        'special attack': pokemon['stats'][3]['base_stat'],
        'special defence': pokemon['stats'][4]['base_stat'],
        'speed': pokemon['stats'][5]['base_stat']
    }


player_pokemon = random_pokemon()
trainer_red_pokemon = random_pokemon()

trainer_red_sent = f'\nTrainer Red sent out {trainer_red_pokemon["name"]}.'
player_sent = f'\nYou have {player_pokemon["name"]}.'


# Assigns a random Pokémon ID and runs one round of Pokémon Top Trumps
def play_round():
    print('Trainer Red wants to Battle!\n')
    who_picks = input('Would you like to go first? Yes (Y) or No (N): ').strip().upper()[0]

    while who_picks not in ['Y', 'N']:
        who_picks = input('Oops...Invalid entry. Please enter Y or N: '
                          '\nWould you like to go first? Yes (Y) or No (N): ').strip().upper()[0]

    if who_picks == 'Y':
        print(trainer_red_sent, player_sent)

        # Loops through random Pokémon dictionary and prints all stats except name
        for pokemon in random_pokemon():
            if pokemon != 'name':
                print(f' {pokemon.title()}: {player_pokemon[pokemon]} ')

        stat_choice = input(f'\nWhich stat do you want to use?: ').strip().lower()
        print(stat_choice)

    else:
        stat_choice = random.choice(list(trainer_red_pokemon.keys())[1:])  # converts dict keys to list

    while stat_choice not in player_pokemon:
        stat_choice = input(f'Oops...Please enter a valid stat: \nWhich stat do you want to use?: ').strip().lower()

    return stat_choice


def winner(stat):
    # Gets value of chosen stat for both player and trainer red
    player_stat = player_pokemon[stat]
    trainer_red_stat = trainer_red_pokemon[stat]

    print(f'{trainer_red_sent} ({stat.upper()} = {trainer_red_stat})'
          f'{player_sent} ({stat.upper()} = {player_stat})')

    # return added for play_round() function
    if player_stat > trainer_red_stat:
        print(f'** Enemy {trainer_red_pokemon["name"]} has fainted! You Win! {smile_emoji} **')
        return 'player'
    elif player_stat < trainer_red_stat:
        print(f'** Your {player_pokemon["name"]} has fainted! You Lose! {crying_emoji} **')
        return 'trainer_red'
    else:
        print('It\'s a Draw! You both get a point!')


def play_again():
    print('------------------------')
    next_game = input('PLAY AGAIN (Y/N)? ').strip().upper()[0]

    # Exception handling for play again input
    while next_game not in ['Y', 'N']:
        next_game = input('Oops! Enter Y or N....Play again Y/N? ').strip().upper()[0]

    if next_game == 'Y':
        run()
    elif next_game == 'N':
        print(f'Goodbye. See you again next time {smile_emoji} '
              f'\n\nHigh scores have been saved to the \'Pokemon High Scores\' file')
        pikachu_drawing()


filename = 'Pokemon High Scores.csv'
field_names = ['player', 'trainer_red']


def high_scores(pscore, oscore):
    def write_scoreboard():
        with open(filename, 'w+') as csv_file:
            spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
            spreadsheet.writeheader()
            spreadsheet.writerows([{'player': 0, 'trainer_red': 0}])

    def update_score():
        with open(filename, 'r') as csv_file:
            spreadsheet = csv.DictReader(csv_file)
            first_row = next(spreadsheet)

            if pscore > int(first_row['player']):
                player_score = pscore
                print(f'NEW Player High Score: {player_score}')
            else:
                player_score = int(first_row['player'])

            if oscore > int(first_row['trainer_red']):
                trainer_red_score = oscore
                print(f'NEW Trainer Red High Score: {trainer_red_score}')
            else:
                trainer_red_score = int(first_row['trainer_red'])

        with open(filename, 'w+') as csv_file:
            spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
            spreadsheet.writeheader()
            spreadsheet.writerows([{'player': player_score, 'trainer_red': trainer_red_score}])

    if os.path.exists(filename):
        update_score()
    else:
        write_scoreboard()
        update_score()


def reset_high_scores():
    reset = input('\nReset high scores? Y/N: ').strip().upper()[0]

    while reset not in ['Y', 'N']:
        reset = input(f'Oops..Please enter Y or N. Reset high scores Y/N? ').strip().upper()[0]

    if reset == 'Y':
        with open(filename, 'w+') as csv_file:
            spreadsheet = csv.DictWriter(csv_file, fieldnames=field_names)
            spreadsheet.writeheader()
            spreadsheet.writerows([{'player': 0, 'trainer_red': 0}])
        print('\nHigh scores have been reset')


# Main run function that starts game
def run():
    player_count = 0
    trainer_red_count = 0

    # Exception handling https://docs.python.org/3/tutorial/errors.html
    while True:
        try:
            no_of_rounds = w2n.word_to_num(input('How many rounds would you like to play?: '))
            break
        except ValueError:
            print('Oops! Try entering a valid number...')

    # Plays number of rounds input by player
    for number in range(no_of_rounds):

        print(f'\033[1m\033[4m\nROUND {number + 1}\033[0m')  # Bold and underline

        stat = play_round()
        game_winner = winner(stat)

        if game_winner == 'player':
            player_count += 1
        elif game_winner == 'trainer_red':
            trainer_red_count += 1
        else:
            player_count += 1
            trainer_red_count += 1

    print(f'\n------------------------\n'
          f'Game over! Final score: \nYou: {player_count}, Trainer Red: {trainer_red_count}')

    # Game outcome
    if player_count > trainer_red_count:
        print(f'{smile_emoji} You won the game!: {smile_emoji}')
    elif player_count < trainer_red_count:
        print(f'Trainer Red won. Better luck next time!')
    else:
        print('It\'s a draw.')

    high_scores(player_count, trainer_red_count)

    play_again()
    reset_high_scores()


# Draw Pikachu
# https://github.com/saksham0626/Python-Turtle-Projects-Cartoon-Character/blob/main/pikachu.py
def pikachu_drawing():
    def get_position(x, y):
        turtle.setx(x)
        turtle.sety(y)
        print(x, y)

    class Pikachu:

        def __init__(self):
            self.t = turtle.Turtle()
            t = self.t
            t.shape('turtle')
            t.pensize(3)
            t.speed(0)
            t.ondrag(get_position)

        def no_trace_goto(self, x, y):
            self.t.penup()
            self.t.goto(x, y)
            self.t.pendown()

        def left_eye(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t
            t.seth(0)
            t.fillcolor('#333333')
            t.begin_fill()
            t.circle(22)
            t.end_fill()

            self.no_trace_goto(x, y + 10)
            t.fillcolor('#000000')
            t.begin_fill()
            t.circle(10)
            t.end_fill()

            self.no_trace_goto(x + 6, y + 22)
            t.fillcolor('#ffffff')
            t.begin_fill()
            t.circle(10)
            t.end_fill()

        def right_eye(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t
            t.seth(0)
            t.fillcolor('#333333')
            t.begin_fill()
            t.circle(22)
            t.end_fill()

            self.no_trace_goto(x, y + 10)
            t.fillcolor('#000000')
            t.begin_fill()
            t.circle(10)
            t.end_fill()

            self.no_trace_goto(x - 6, y + 22)
            t.fillcolor('#ffffff')
            t.begin_fill()
            t.circle(10)
            t.end_fill()

        def mouth(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t

            t.fillcolor('#88141D')
            t.begin_fill()

            l1 = []
            l2 = []
            t.seth(190)
            a = 0.7
            for _ in range(28):
                a += 0.1
                t.right(3)
                t.fd(a)
                l1.append(t.position())

            self.no_trace_goto(x, y)

            t.seth(10)
            a = 0.7
            for _ in range(28):
                a += 0.1
                t.left(3)
                t.fd(a)
                l2.append(t.position())

            t.seth(10)
            t.circle(50, 15)
            t.left(180)
            t.circle(-50, 15)

            t.circle(-50, 40)
            t.seth(233)
            t.circle(-50, 55)
            t.left(180)
            t.circle(50, 12.1)
            t.end_fill()

            self.no_trace_goto(17, 54)
            t.fillcolor('#DD716F')
            t.begin_fill()
            t.seth(145)
            t.circle(40, 86)
            t.penup()
            for pos in reversed(l1[:20]):
                t.goto(pos[0], pos[1] + 1.5)
            for pos in l2[:20]:
                t.goto(pos[0], pos[1] + 1.5)
            t.pendown()
            t.end_fill()

            self.no_trace_goto(-17, 94)
            t.seth(8)
            t.fd(4)
            t.back(8)

        def left_cheek(self, x, y):
            turtle.tracer(False)
            t = self.t
            self.no_trace_goto(x, y)
            t.seth(300)
            t.fillcolor('#DD4D28')
            t.begin_fill()
            a = 2.3
            for i in range(120):
                if 0 <= i < 30 or 60 <= i < 90:
                    a -= 0.05
                    t.lt(3)
                    t.fd(a)
                else:
                    a += 0.05
                    t.lt(3)
                    t.fd(a)
            t.end_fill()
            turtle.tracer(True)

        def right_cheek(self, x, y):
            t = self.t
            turtle.tracer(False)
            self.no_trace_goto(x, y)
            t.seth(60)
            t.fillcolor('#DD4D28')
            t.begin_fill()
            a = 2.3
            for i in range(120):
                if 0 <= i < 30 or 60 <= i < 90:
                    a -= 0.05
                    t.lt(3)
                    t.fd(a)
                else:
                    a += 0.05
                    t.lt(3)
                    t.fd(a)
            t.end_fill()
            # turtle.tracer(True)

        def color_left_ear(self, x, y):
            t = self.t
            self.no_trace_goto(x, y)
            t.fillcolor('#000000')
            t.begin_fill()
            t.seth(330)
            t.circle(100, 35)
            t.seth(219)
            t.circle(-300, 19)
            t.seth(110)
            t.circle(-30, 50)
            t.circle(-300, 10)
            t.end_fill()

        def color_right_ear(self, x, y):
            t = self.t
            self.no_trace_goto(x, y)
            t.fillcolor('#000000')
            t.begin_fill()
            t.seth(300)
            t.circle(-100, 30)
            t.seth(35)
            t.circle(300, 15)
            t.circle(30, 50)
            t.seth(190)
            t.circle(300, 17)
            t.end_fill()

        def body(self):
            t = self.t

            t.fillcolor('#F6D02F')
            t.begin_fill()

            t.penup()
            t.circle(130, 40)
            t.pendown()
            t.circle(100, 105)
            t.left(180)
            t.circle(-100, 5)

            t.seth(20)
            t.circle(300, 30)
            t.circle(30, 50)
            t.seth(190)
            t.circle(300, 36)

            t.seth(150)
            t.circle(150, 70)

            t.seth(200)
            t.circle(300, 40)
            t.circle(30, 50)
            t.seth(20)
            t.circle(300, 35)
            # print(t.pos())

            t.seth(240)
            t.circle(105, 95)
            t.left(180)
            t.circle(-105, 5)

            t.seth(210)
            t.circle(500, 18)
            t.seth(200)
            t.fd(10)
            t.seth(280)
            t.fd(7)
            t.seth(210)
            t.fd(10)
            t.seth(300)
            t.circle(10, 80)
            t.seth(220)
            t.fd(10)
            t.seth(300)
            t.circle(10, 80)
            t.seth(240)
            t.fd(12)
            t.seth(0)
            t.fd(13)
            t.seth(240)
            t.circle(10, 70)
            t.seth(10)
            t.circle(10, 70)
            t.seth(10)
            t.circle(300, 18)

            t.seth(75)
            t.circle(500, 8)
            t.left(180)
            t.circle(-500, 15)
            t.seth(250)
            t.circle(100, 65)

            t.seth(320)
            t.circle(100, 5)
            t.left(180)
            t.circle(-100, 5)
            t.seth(220)
            t.circle(200, 20)
            t.circle(20, 70)

            t.seth(60)
            t.circle(-100, 20)
            t.left(180)
            t.circle(100, 20)
            t.seth(300)
            t.circle(10, 70)

            t.seth(60)
            t.circle(-100, 20)
            t.left(180)
            t.circle(100, 20)
            t.seth(10)
            t.circle(100, 60)

            t.seth(180)
            t.circle(-100, 10)
            t.left(180)
            t.circle(100, 10)
            t.seth(5)
            t.circle(100, 10)
            t.circle(-100, 40)
            t.circle(100, 35)
            t.left(180)
            t.circle(-100, 10)

            t.seth(290)
            t.circle(100, 55)
            t.circle(10, 50)

            t.seth(120)
            t.circle(100, 20)
            t.left(180)
            t.circle(-100, 20)

            t.seth(0)
            t.circle(10, 50)

            t.seth(110)
            t.circle(100, 20)
            t.left(180)
            t.circle(-100, 20)

            t.seth(30)
            t.circle(20, 50)

            t.seth(100)
            t.circle(100, 40)

            t.seth(200)
            t.circle(-100, 5)
            t.left(180)
            t.circle(100, 5)
            t.left(30)
            t.circle(100, 75)
            t.right(15)
            t.circle(-300, 21)
            t.left(180)
            t.circle(300, 3)

            t.seth(43)
            t.circle(200, 60)

            t.right(10)
            t.fd(10)

            t.circle(5, 160)
            t.seth(90)
            t.circle(5, 160)
            t.seth(90)

            t.fd(10)
            t.seth(90)
            t.circle(5, 180)
            t.fd(10)

            t.left(180)
            t.left(20)
            t.fd(10)
            t.circle(5, 170)
            t.fd(10)
            t.seth(240)
            t.circle(50, 30)

            t.end_fill()
            self.no_trace_goto(130, 125)
            t.seth(-20)
            t.fd(5)
            t.circle(-5, 160)
            t.fd(5)

            self.no_trace_goto(166, 130)
            t.seth(-90)
            t.fd(3)
            t.circle(-4, 180)
            t.fd(3)
            t.seth(-90)
            t.fd(3)
            t.circle(-4, 180)
            t.fd(3)

            self.no_trace_goto(168, 134)
            t.fillcolor('#F6D02F')
            t.begin_fill()
            t.seth(40)
            t.fd(200)
            t.seth(-80)
            t.fd(150)
            t.seth(210)
            t.fd(150)
            t.left(90)
            t.fd(100)
            t.right(95)
            t.fd(100)
            t.left(110)
            t.fd(70)
            t.right(110)
            t.fd(80)
            t.left(110)
            t.fd(30)
            t.right(110)
            t.fd(32)

            t.right(106)
            t.circle(100, 25)
            t.right(15)
            t.circle(-300, 2)
            ##############
            # print(t.pos())
            t.seth(30)
            t.fd(40)
            t.left(100)
            t.fd(70)
            t.right(100)
            t.fd(80)
            t.left(100)
            t.fd(46)
            t.seth(66)
            t.circle(200, 38)
            t.right(10)
            t.fd(10)
            t.end_fill()

            t.fillcolor('#923E24')
            self.no_trace_goto(126.82, -156.84)
            t.begin_fill()

            t.seth(30)
            t.fd(40)
            t.left(100)
            t.fd(40)
            t.pencolor('#923e24')
            t.seth(-30)
            t.fd(30)
            t.left(140)
            t.fd(20)
            t.right(150)
            t.fd(20)
            t.left(150)
            t.fd(20)
            t.right(150)
            t.fd(20)
            t.left(130)
            t.fd(18)
            t.pencolor('#000000')
            t.seth(-45)
            t.fd(67)
            t.right(110)
            t.fd(80)
            t.left(110)
            t.fd(30)
            t.right(110)
            t.fd(32)
            t.right(106)
            t.circle(100, 25)
            t.right(15)
            t.circle(-300, 2)
            t.end_fill()

            t.hideturtle()

            self.cap(-134.07, 147.81)
            self.mouth(-5, 25)
            self.left_cheek(-126, 32)
            self.right_cheek(107, 63)
            self.color_left_ear(-250, 100)
            self.color_right_ear(140, 270)
            self.left_eye(-85, 90)
            self.right_eye(50, 110)

            # --------MELANIE AND EMILY ADDITIONAL CODE BEGINS --------------------------------------------------
            t.color('#CD0000')
            self.letter_E(-20, -150, 1.5)
            self.letter_M(10, -150, 1.5)

            self.letter_M(-20, -115, 1.5)
            self.letter_L(-0, -185)

            t.color('black')
            turtle.tracer(1)  # turns automatic screen update off
            self.letter_G(-300, -260)
            self.letter_A(-290, -300)
            self.letter_M(-255, -300, 1)
            self.letter_E(-215, -300, 1)

            self.letter_O(200, -300)
            self.letter_V(210, -260)
            self.letter_E(250, -300, 1)
            self.letter_R(290, -300)

        def letter_M(self, x, y, size):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(90)  # sets turtle to North (default 0 = East)
            t.forward(40 / size)
            t.right(135)
            t.forward(22 / size)
            t.left(90)
            t.forward(22 / size)
            t.right(135)
            t.forward(40 / size)

        def letter_E(self, x, y, size):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(0)
            t.forward(30 / size)
            t.backward(30 / size)
            t.left(90)
            t.forward(40 / size)
            t.right(90)
            t.forward(30 / size)

            t.backward(30 / size)
            t.right(90)
            t.forward(20 / size)
            t.left(90)
            t.forward(25 / size)

        def letter_L(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(180)
            t.forward(20)
            t.right(90)
            t.forward(26.67)

        def letter_G(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(180)  # sets turtle to West (default 0 = East)
            t.forward(25)
            t.left(90)
            t.forward(40)
            t.left(90)
            t.forward(25)
            t.left(90)
            t.forward(17)
            t.left(90)
            t.forward(10)

        def letter_A(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(90)  # sets turtle to N (default 0 = East)
            t.forward(40)
            t.right(90)
            t.forward(25)
            t.right(90)
            t.forward(40)
            t.backward(20)
            t.right(90)
            t.forward(25)

        def letter_O(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(180)
            t.forward(25)
            t.right(90)
            t.forward(40)
            t.right(90)
            t.forward(25)
            t.right(90)
            t.forward(40)

        def letter_V(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(0)
            t.right(67.5)
            t.forward(42.5)
            t.left(135)
            t.forward(42.5)

        def letter_R(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t

            t.setheading(90)  # sets turtle to N (default 0 = East)
            t.forward(40)
            t.right(90)
            t.forward(25)
            t.right(90)
            t.forward(20)
            t.right(90)
            t.forward(25)
            t.left(140)
            t.forward(32.5)

        # ---------MELANIE AND EMILY ADDITIONAL CODE ENDS ----------------------------------------------------------

        def cap(self, x, y):
            self.no_trace_goto(x, y)
            t = self.t
            t.fillcolor('#CD0000')
            t.begin_fill()
            t.seth(200)
            t.circle(400, 7)
            t.left(180)
            t.circle(-400, 30)
            t.circle(30, 60)
            t.fd(50)
            t.circle(30, 45)
            t.fd(60)
            t.left(5)
            t.circle(30, 70)
            t.right(20)
            t.circle(200, 70)
            t.circle(30, 60)
            t.fd(70)
            # print(t.pos())
            t.right(35)
            t.fd(50)
            t.circle(8, 100)
            t.end_fill()
            self.no_trace_goto(-168.47, 185.52)
            t.seth(36)
            t.circle(-270, 54)
            t.left(180)
            t.circle(270, 27)
            t.circle(-80, 98)

            t.fillcolor('#444444')
            t.begin_fill()
            t.left(180)
            t.circle(80, 197)
            t.left(58)
            t.circle(200, 45)
            t.end_fill()

            self.no_trace_goto(-58, 270)
            t.pencolor('#228B22')
            t.dot(35)

            self.no_trace_goto(-30, 280)
            t.fillcolor('#228B22')
            t.begin_fill()
            t.seth(100)
            t.circle(30, 180)
            t.seth(190)
            t.fd(15)
            t.seth(100)
            t.circle(-45, 180)
            t.right(90)
            t.fd(15)
            t.end_fill()
            t.pencolor('#000000')

        def start(self):
            self.body()

    def main():
        wn = turtle.Screen()
        wn.tracer(0)  # turns on screen updates, so drawing appears instantaneously

        turtle.screensize(800, 800)
        turtle.title('Pikachu written by Saksham Aggarwal')
        pikachu = Pikachu()
        pikachu.start()

        turtle.Screen().exitonclick()  # Ends process correctly when user clicks on exit

    if __name__ == '__main__':
        main()


run()
