import pygame
import start
import game
import final


def main():
    '''
    Основная функция
    '''
    pygame.init()
    pygame.display.set_caption('Слабое звено')
    size = 800, 450
    screen = pygame.display.set_mode(size)
    names = []

    if not start.main(names, screen):
        return pygame.quit()

    statistic = game.main(names, screen)

    if not statistic:
        return pygame.quit()

    final.main(screen, statistic)


try:
    if __name__ == '__main__':
        main()

except Exception as e:
    print(e)
    pygame.quit()
