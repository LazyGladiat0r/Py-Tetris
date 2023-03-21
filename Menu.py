import pygame
import TetrisMain

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris Menu")

font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 24)

background_color = (0, 0, 0)
text_color = (255, 255, 255)
highlight_color = (200, 200, 200)

menu_options = [
    {"text": "Single Player", "highlighted": True},
    {"text": "2 Player", "highlighted": False},
    {"text": "High Score", "highlighted": False},
    {"text": "Exit", "highlighted": False},
]
menu_option_height = font.get_height() + 10
menu_option_spacing = 20
menu_top_margin = (screen_height - (len(menu_options) * menu_option_height + (len(menu_options) - 1) * menu_option_spacing)) / 2

running = True
selected_option = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:
                    # Start game
                    print("Starting Single Player game...")
                    exec(open("TetrisMain.py").read())
                elif selected_option == 1:
                    # Start 2 player Game
                    print("Starting Multiplayer Game...")
                    exec(open("MultiTetris.py").read())
                elif selected_option == 2:
                    # Show settings
                    print("Showing Highscore...")
                elif selected_option == 3:
                    # Exit
                    running = False
    
    screen.fill(background_color)
    
    for i, option in enumerate(menu_options):
        text = font.render(option["text"], True, text_color)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.top = menu_top_margin + i * (menu_option_height + menu_option_spacing)
        
        if i == selected_option:
            pygame.draw.rect(screen, highlight_color, (text_rect.left - 5, text_rect.top - 5, text_rect.width + 10, text_rect.height + 10))
        
        screen.blit(text, text_rect)
    
    pygame.display.flip()

pygame.quit()