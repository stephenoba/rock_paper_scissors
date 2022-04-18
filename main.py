#!/usr/bin/env python3

import random
import enum

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


class Color(enum.Enum):
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'

    @classmethod
    def get_colors(cls):
        colors = [color.value for color in cls]
        return colors


class Player:
    def __init__(self):
        self.score = 0
        self.last_move = ''
        self.opponent_last_move = ''

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass

    def update_score(self, score):
        score = int(score)
        self.score += score
        return self.score


class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


class ReflectPlayer(Player):
    def move(self):
        move_to_make = self.suggest_move()
        return move_to_make

    def suggest_move(self):
        """
        Gets the opponents previous move if one exist and returns it
        """
        if self.opponent_last_move:
            return self.opponent_last_move
        return random.choice(moves)

    def learn(self, my_move, their_move):
        self.opponent_last_move = their_move


class CyclePlayer(Player):
    def move(self):
        move_to_make = self.suggest_move()
        return move_to_make

    def suggest_move(self):
        """
        Gets the players previous move and plays the next in the list of moves
        """
        if not self.last_move:
            return random.choice(moves)
        # get the index of the last played move in the moves list
        current_index = moves.index(self.last_move)
        # if the last move is the last item  on the moves list
        # return the first item
        if current_index+1 >= len(moves):
            return moves[0]
        # if all conditions are not met return the next item
        return moves[current_index+1]

    def learn(self, my_move, their_move):
        self.last_move = my_move


class HumanPlayer(Player):
    def move(self):
        player_choice = self.valid_choice(
            "Enter your choice ('Rock', 'Paper', or 'Scissors'): "
        )
        return player_choice

    def valid_choice(self, prompt):
        while True:
            option = input(prompt).lower()
            if option in moves:
                return option
            print(f"sorry the option '{option}' is invalid. Try again!")


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2, rounds=3):
        self.rounds = rounds
        self.p1 = p1
        self.p2 = p2
        self.winner = None

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        self.check_game(move1, move2)
        print(f"Player 1: {self.p1.score} | Player 2: {self.p2.score}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def get_winner(self):
        p1_score = self.p1.score
        p2_score = self.p2.score
        print("Final Score: "
              f"Player 1: {p1_score} | "
              f"Player 2: {p2_score}")
        if p1_score > p2_score:
            print("Player 1 wins!!!")
        elif p1_score < p2_score:
            print("Player 2 wins!!!")
        else:
            print("The game is a tie!!!")

    def play_game(self):
        print("Game start!")
        colors = Color.get_colors()
        for round in range(1, self.rounds+1):
            color = random.choice(colors)
            print(f"\n{color}Round {round}:")
            self.play_round()
        print("Game over!")
        self.get_winner()

    def check_game(self, move1, move2):
        if beats(move1, move2):
            # updates the score of player 1
            print("Player 1 wins this round.")
            self.p1.update_score(1)
        elif beats(move2, move1):
            # updates the score of player 2
            print("Player 2 wins this round.")
            self.p2.update_score(1)
        else:
            print("This round is a tie.")


if __name__ == '__main__':
    Computer = random.choice([CyclePlayer, ReflectPlayer, RandomPlayer])
    try:
        game = Game(HumanPlayer(), Computer(), rounds=5)
        game.play_game()
    except (KeyboardInterrupt, EOFError):
        print("\nThanks for playing...")
