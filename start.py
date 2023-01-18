import pygame


class Names:
    def __init__(self, names: list):
        self.names = names
        self.borders = [(100, 40 + 40 * i, 600, 20) for i in range(8)]

        for i in range(8):
            self.names.append('')

        self.checked = -1

    def get_coords(self, cur_pos):
        num = -1
        if cur_pos[0] in range(100, 700):
            for i in range(8):
                if cur_pos[1] in range(self.borders[i][1], self.borders[i][3] + self.borders[i][1]):
                    num = i

        if cur_pos[0] in range(350, 450) and cur_pos[1] in range(355, 385):
            num = -2

        self.checked = num
        return num == -2

    def on_key_pressed(self, key, mod):
        if (key in range(97, 123) or key in range(48, 58) or key == 32) and self.checked != -1:
            self.names[self.checked] += chr(key).upper() if mod in (4097, 4098, 12288) else chr(key).lower()

        elif key == 8:
            self.names[self.checked] = self.names[self.checked][:-1]


def main(names, screen):
    def draw():
        screen.fill((40, 0, 45))
        font = pygame.font.Font(None, 40)
        screen.blit(font.render('Введите имена игроков', True, (0, 0, 255)), (230, 0))
        screen.blit(font.render('Далее', True, (0, 0, 255)), (350, 355))

        for i in range(8):
            font = pygame.font.Font(None, 30)
            pygame.draw.rect(screen, (0, 0, 255), window.borders[i])
            pygame.draw.rect(screen, (40, 0, 45), [(window.borders[i][j] + 1) if j < 2 else (window.borders[i][j] - 2)
                                                   for j in range(4)])
            screen.blit(font.render(names[i], True, (0, 0, 255)), (window.borders[i][0] + 5, window.borders[i][1]))

        pygame.display.flip()

    window = Names(names)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if window.get_coords(event.pos) and all(window.names):
                    return 1

            if event.type == pygame.KEYDOWN:
                window.on_key_pressed(event.key, event.mod)

        draw()
