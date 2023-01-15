import pygame
import start
import game
import final


def main():
    pygame.init()
    pygame.display.set_caption('Слабое звено')
    size = 800, 400
    screen = pygame.display.set_mode(size)
    names = []
    if not start.main(names, screen):
        return pygame.quit()
    pygame.quit()


try:
    if __name__ == '__main__':
        main()
except Exception as e:
    print(e, e.args)
    pygame.quit()
