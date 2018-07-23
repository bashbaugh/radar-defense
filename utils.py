import pygame.font

pygame.font.init()

def text(screen, text, x, y, size = 50,
            color = (200, 200, 200), font_type = 'data/fonts/Chrobot.otf'):
    try:

        text = str(text)
        font = pygame.font.Font(font_type, size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception, e:
        print 'Font Error, saw it coming'
        raise e
