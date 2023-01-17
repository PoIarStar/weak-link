import pygame
from random import shuffle
import sqlite3


class Window:
    def __init__(self, names):
        self.round = 5
        self.players = [[True, (200 + 300 * (i % 2), 10 + i // 2 * 50), names[i]] for i in range(8)]
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
        self.turned = 0

    def get_coords(self, coords):
        if coords[0] in range(750, 800) and coords[1] in range (450, 500) and not self.timer:
            self.start()
        elif coords


def main(names, screen):
    def draw():
        screen.fill((40, 0, 45))
        font = pygame.font.Font(None, 20)
        for i in window.bank:
            able = i['enable'] if window.bank.index(i) < window.enable else i['disable']
            pygame.draw.ellipse(screen, (255, 20, 20) if window.bank.index(i) == window.enable else (20, 20, 255),
                                able)
            screen.blit(font.render(str(i['value']), True, (255, 255, 255)), (able[0] + 35, able[1] + 20))
        for i in window.players:
            pygame.draw.rect(screen, (20, 20, 255), (*i[1], 250, 40))
            pygame.draw.rect(screen, (40, 0, 45), (*(j + 1 for j in i[1]), 248, 38))
            screen.blit(font.render(i[2], True, (255, 255, 255)),
                        (i[1][0] + 35, i[1][1] + 20))

        pygame.display.flip()

    window = Window(names)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        draw()
