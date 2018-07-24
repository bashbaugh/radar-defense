import pygame.font

pygame.font.init()

def text(screen, text, x, y, size = 50, color = (200, 200, 200), font_type = 'data/fonts/Chrobot.otf'):
    text = str(text)
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

        
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
