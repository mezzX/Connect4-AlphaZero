import pygame
import sys
import math
import timeit
from copy import copy
from connect4 import Connect4
from agent_zero import Connect4Zero

class Gui:

    def __init__(self, player1='Human', player2='AI'):
        self.board_colour = (0, 0, 255)
        self.bg_colour = (0, 0, 0)
        self.p1_piece_colour = (255, 0, 0)
        self.p2_piece_colour = (255, 255, 0)
        self.piece_colour = self.p1_piece_colour
        self.num_rows = 6
        self.num_columns = 7
        self.win_cond = 4
        self.square_size = 100
        self.width = self.num_columns * self.square_size
        self.height = (self.num_rows + 1) * self.square_size
        self.piece_size = int(self.square_size / 2 - 5)

        self.original_game = Connect4(
            (self.num_columns, self.num_rows), self.win_cond)
        self.game = copy(self.original_game)
        self.player1 = player1
        self.player2 = player2
        self.cur_player = player1
        self.player = self.game.player
        self.agent = Connect4Zero()
        self.last_dropped = 0
        self.end = False

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.draw_board()
        pygame.display.update()
        pygame.init()
        self.game_font = pygame.font.SysFont('Candara', 75)


    def draw_board(self):
        for x in range(self.num_columns):
            for y in range(self.num_rows):
                pygame.draw.rect(self.screen, self.board_colour,
                    (x * self.square_size, y * self.square_size + self.square_size,
                    self.square_size, self.square_size))

                pygame.draw.circle(self.screen, self.bg_colour, 
                    (int(x * self.square_size + self.square_size / 2),
                    int((1 + y) * self.square_size + self.square_size /2)),
                    self.piece_size)


    def draw_hover_piece(self, event):
        pygame.draw.rect(self.screen, self.bg_colour,
                        (0, 0, self.width, self.square_size))
        pos_x = event.pos[0]
        pygame.draw.circle(self.screen, self.piece_colour,
                            (pos_x, int(self.square_size / 2)), self.piece_size)
        pygame.display.update()


    def drop_piece(self, event):
        pygame.draw.rect(self.screen, self.bg_colour,
                        (0, 0, self.width, self.square_size))
        pos_x = event.pos[0]
        self.last_dropped = pos_x
        col = int(math.floor(pos_x / self.square_size))
        success = self.game.move(col)
        return success


    def draw_move(self):
        x, y = self.game.last_move
        pygame.draw.circle(self.screen, self.piece_colour, 
            (int(x * self.square_size + self.square_size / 2),
            self.height - int(y * self.square_size + self.square_size / 2)),
            self.piece_size)
        pygame.display.update()


    def end_game(self):
        self.end = True
        label = self.game_font.render(self.victor, 1, self.piece_colour)
        self.screen.blit(label, (40, 10))
        pygame.display.update()


    def check_score(self):
        if self.game.score is None:
            return

        if self.game.score == 1:
            self.victor = 'Player 1 Wins!'

        elif self.game.score == -1:
            self.victor = 'Player 2 Wins!'

        else:
            self.victor = 'No More Moves Left... It\'s a Tie.'

        self.end_game()

    def end_turn(self):
        self.check_score()
        self.player = self.game.player
        self.piece_colour = self.p1_piece_colour if self.player == 1 else self.p2_piece_colour
        self.cur_player = self.player1 if self.player == 1 else self.player2


    def human_turn(self, event):
        success = False
        if event.type == pygame.MOUSEMOTION:
            self.draw_hover_piece(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            success = self.drop_piece(event)

        return success

    def ai_move(self, move):
        pix_x = int(move * self.square_size)
        diff = pix_x - self.last_dropped
        step = int(math.floor(diff / 4))
        for i in range(4):
            pos = (step * i, 50)
            r_x = 1 if step > 0 else -1
            rel = (r_x, 0)
            ar = {
                'pos' : pos,
                'rel' : rel,
                'buttons' : (0, 0, 0),
                'window' : None
            }
            e = pygame.event.Event(pygame.MOUSEMOTION, ar)
            self.draw_hover_piece(e)


    def ai_drop(self, move):
        pix_x = int(move * self.square_size)
        ar = {
            'pos' : (pix_x, 100),
            'button' : 1,
            'window' : None
        }
        e = pygame.event.Event(pygame.MOUSEBUTTONDOWN, ar)
        success = self.drop_piece(e)

        return success


    def ai_turn(self):
        time_millis = lambda: 1000 * timeit.default_timer()
        move_start = time_millis()
        time_left = lambda: self.agent.TIME_LIMIT_MILLIS-(time_millis()-move_start)
        move = self.agent.search(self.game, time_left)
        self.ai_move(move)
        success = self.ai_drop(move)

        return success


    def start_game(self):
        while not self.end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if self.cur_player == 'Human':
                    success = self.human_turn(event)

                elif self.cur_player == 'AI':
                    success = self.ai_turn()

                if success:
                    self.draw_move()
                    self.end_turn()

            if self.end:
                pygame.time.wait(3000)

if __name__ == '__main__':
    game = Gui()
    game.start_game()