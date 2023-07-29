import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Wymiary przestrzeni
WIDTH, HEIGHT = 400, 400

# Wymiary bloku
BLOCK_WIDTH, BLOCK_HEIGHT = 100, 100

# Kolor tła
BG_COLOR = (255, 255, 255)

# Kolor bloku
BLOCK_COLOR = (0, 0, 255)

# Utworzenie okna aplikacji
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Przesuwany blok")

# Pozycja początkowa bloku
block_x, block_y = 100, 100

# Główna pętla aplikacji
while True:
    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Śledzenie pozycji myszy
    if pygame.mouse.get_pressed()[0]:  # Sprawdzamy, czy lewy przycisk myszy jest wciśnięty
        mouse_x, mouse_y = pygame.mouse.get_pos()
        block_x = mouse_x - BLOCK_WIDTH // 2
        block_y = mouse_y - BLOCK_HEIGHT // 2

        # Ograniczenie przesuwania bloku do przestrzeni
        block_x = max(0, min(block_x, WIDTH - BLOCK_WIDTH))
        block_y = max(0, min(block_y, HEIGHT - BLOCK_HEIGHT))

    # Wypełnienie tła
    screen.fill(BG_COLOR)

    # Narysowanie bloku
    pygame.draw.rect(screen, BLOCK_COLOR, (block_x, block_y, BLOCK_WIDTH, BLOCK_HEIGHT))

    # Wyświetlenie zawartości okna
    pygame.display.flip()
