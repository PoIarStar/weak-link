import pygame
from random import shuffle
import sqlite3
from time import time


class Window:
    '''
    Класс, отвечающий за игру
    '''
    def __init__(self, names):
        self.round = 5
        self.players = [[True, (200 + 300 * (i % 2), 10 + i // 2 * 50), names[i], 0, 0, 0, 0] for i in range(8)]
        self.bank = [{'value': 0, 'disable': (50, 400, 100, 50), 'enable': (50, 400, 100, 50)},
                     {'value': 1000, 'disable': (50, 350, 100, 50), 'enable': (50, 370, 100, 50)},
                     {'value': 2000, 'disable': (50, 300, 100, 50), 'enable': (50, 340, 100, 50)},
                     {'value': 5000, 'disable': (50, 250, 100, 50), 'enable': (50, 310, 100, 50)},
                     {'value': 10000, 'disable': (50, 200, 100, 50), 'enable': (50, 280, 100, 50)},
                     {'value': 20000, 'disable': (50, 150, 100, 50), 'enable': (50, 250, 100, 50)},
                     {'value': 30000, 'disable': (50, 100, 100, 50), 'enable': (50, 220, 100, 50)},
                     {'value': 40000, 'disable': (50, 50, 100, 50), 'enable': (50, 190, 100, 50)},
                     {'value': 50000, 'disable': (50, 0, 100, 50), 'enable': (50, 180, 100, 50)}]
        self.enable = 1
        self.con = sqlite3.connect('questions.db')
        self.cur = self.con.cursor()
        self.cur.execute('SELECT * FROM questions')
        self.questions = self.cur.fetchall()
        shuffle(self.questions)
        self.cur.execute('SELECT * FROM taunts')
        self.taunts = self.cur.fetchall()
        shuffle(self.taunts)
        self.moved = 0
        self.round = 0
        self.timer = 0
        self.counter = 0
        self.question = []
        self.final = [0] * 10

    def get_coords(self, coords):
        if coords[0] in range(700, 800) and coords[1] in range(400, 500) and not self.timer:
            if self.round == sum([not j[0] for j in self.players]):
                self.start()
            return

        if coords[0] in range(595, 695) and coords[1] in range(400, 500):
            self.banking()
            return

        for i in range(1, 4):
            if self.question and (self.timer or self.round == 7):
                if self.question[i]:
                    if coords[0] in range(20 + 180 * i, 190 + 180 * i) and coords[1] in range(270, 340):
                        self.check_correct(i)
                        return

        for i in self.players:
            if not self.timer and 7 > self.round > sum([not j[0] for j in self.players]):
                if coords[0] in range(i[1][0], i[1][0] + 250) and coords[1] in range(i[1][1], i[1][1] + 40):
                    i[0] = False
                    self.players.append(self.players.pop(self.players.index(i)))
                    self.moved = 0
                    return

    def start(self):
        self.round += 1
        if self.round < 7:
            self.timer = 150 - self.round * 10
        self.question = self.questions[self.counter]

    def check_correct(self, num):
        if self.round < 7:
            self.players[self.moved][3 if self.question[4] == num else 4] += 1
            self.moved = (self.moved + 1) % sum([i[0] for i in self.players])
            self.enable = self.enable + 1 if self.question[4] == num else 1
            self.counter += 1
            self.question = self.questions[self.counter]

        else:
            for i in range(10):
                if self.final[i] == 0:
                    if self.question[4] == num:
                        self.final[i] = 1
                        self.players[self.moved][3] += 1
                    else:
                        self.final[i] = 2
                        self.players[self.moved][4] += 1
                    self.counter += 1
                    self.question = self.questions[self.counter]
                    break

        self.moved += 1

    def banking(self):
        if self.enable > 1:
            self.bank[0]['value'] += self.bank[self.enable - 1]['value'] * (2 if self.round == 6 else 1)
            self.enable = 1


def main(names, screen):
    '''
    Обработка игровых процессов
    '''
    def draw():
        screen.fill((40, 0, 45))
        font = pygame.font.Font(None, 20)
        if window.round < 7:
            for i in window.bank:
                able = i['enable'] if window.bank.index(i) < window.enable else i['disable']
                pygame.draw.ellipse(screen, (255, 20, 20) if window.bank.index(i) == window.enable else (20, 20, 255),
                                    able)
                screen.blit(font.render(str(i['value']), True, (255, 255, 255)), (able[0] + 35, able[1] + 20))

        else:
            for i in range(10):
                if not window.final[i]:
                    color = (100, 100, 100)
                elif window.final[i] == 1:
                    color = (20, 255, 20)
                else:
                    color = (255, 20, 20)
                pygame.draw.circle(screen, color, (200 + i // 2 * 20, 350 + i % 2 * 20), 5)

        for i in window.players:
            pygame.draw.rect(screen, (20, 20, 255), (*i[1], 250, 40))
            pygame.draw.rect(screen, (40, 0, 45), (*(j + 1 for j in i[1]), 248, 38))
            screen.blit(font.render(i[2], True, ((255, 255, 255) if i[0] else (100, 100, 100))),
                        (i[1][0] + 35, i[1][1] + 20))

        if window.round < 7:
            pygame.draw.ellipse(screen, (20, 20, 255), (700, 400, 100, 50))
            text = f'{window.timer // 60}:{window.timer % 60}' if window.timer else 'Начать раунд'
            screen.blit(font.render(text.center(12), True, (255, 255, 255)),
                        (710, 420))

        if window.timer or window.round == 7:
            screen.blit(font.render(window.question[0], True, (255, 255, 255)),
                        (175, 225))
            for i in range(1, 4):
                if window.question[i]:
                    pygame.draw.ellipse(screen, (255, 255, 0), (20 + 180 * i, 270, 170, 70))
                    pygame.draw.ellipse(screen, (0, 0, 255), (20 + 180 * i + 5, 275, 160, 60))
                    screen.blit(font.render(window.question[i].center(32), True, (255, 255, 255)),
                                (20 + 180 * i + 10, 300))

        elif window.round:
            screen.blit(font.render(window.taunts[window.round][0], True, (255, 255, 255)),
                        (175, 225))

        if window.question and window.round < 7:
            pygame.draw.ellipse(screen, (20, 20, 255), (595, 400, 100, 50))
            screen.blit(font.render('Банк'.center(12), True, (255, 255, 255)),
                        (605, 420))

        pygame.display.flip()

    window = Window(names)

    t_prev = int(time())
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                window.get_coords(event.pos)

        draw()
        if int(time()) > t_prev:
            if window.timer:
                window.timer -= 1
            t_prev = int(time())

        if all(window.final):
            window.players[0][-1] = window.bank[0]['value']
            players = [window.players[i][-5:] for i in range(8)]
            return players
