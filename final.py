import pygame


def main(screen, statistic):
    stat = [['имя', 'правильных ответов', 'ошибок', 'сохранено денег', 'выигрыш']]
    stat.extend(statistic)
    pygame.init()
    font = pygame.font.Font(None, 20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill((40, 0, 45))
        for i in range(5):
            for j in range(8):
                screen.blit(font.render(str(stat[j][i]), True, (255, 255, 255)), (i * 160, j * 50))
        pygame.display.flip()
