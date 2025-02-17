import pygame
from random import randrange as rnd


WIDTH, HEIGHT = 900, 600
fps = 60

def draw_text_with_outline(screen, text, font, text_color, outline_color, position):
    text_surface = font.render(text, True, text_color)
    outline_surfaces = [
        font.render(text, True, outline_color) for i in range(8)
    ]

    x, y = position
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]

    for surface, offset in zip(outline_surfaces, offsets):
        screen.blit(surface, (x + offset[0], y + offset[1]))

    screen.blit(text_surface, (x, y))


def show_end_screen(screen, text, color):
    font = pygame.font.Font(None, 100)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(color)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.delay(1000)


# Параметры платформы
platform_height = 20
platform_width = 190
platform_speed = 7

# Параметры шарика
BALL_R = 10
BALL_RECT = int(BALL_R * 2 ** 0.5)
ball_speed = 5

# Параметры блоков
BLOCK_WIDTH = 100
BLOCK_HEIGHT = 50
BLOCK_ROWS = 4
BLOCK_COLS = 7

width, height = 800, 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Параметры платформ по бокам
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_SIZE = 20

# Параметры шарика
BALL_R = 10
ball_rect = int(BALL_R * 2 ** 0.5)
ball_speed2 = 5

# Параметры блоков
block_width = 100
block_height = 50
block_rows = 4
block_cols = 10

game_running = False  # Флаг для переключения между меню и игрой
game_2_running = False


def collision(ball_x, ball_y, ball, rect):
    if ball_x > 0:
        chngsx = ball.right - rect.left
    else:
        chngsx = rect.right - ball.left
    if ball_y > 0:
        chngsy = ball.bottom - rect.top
    else:
        chngsy = rect.bottom - ball.top

    if abs(chngsx - chngsy) < 10:
        ball_x, ball_y = -ball_x, -ball_y
    elif chngsx > chngsy:
        ball_y = -ball_y
    elif chngsy > chngsx:
        ball_x = -ball_x
    return ball_x, ball_y


def game():
    global game_running, fps
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # фон
    img_night_mode = pygame.image.load('night.jpg').convert()

    # платформа
    platform = pygame.Rect(WIDTH // 2 - platform_width // 2, HEIGHT - platform_height - 30, platform_width,
                           platform_height)

    # шарик
    ball = pygame.Rect(rnd(BALL_RECT, WIDTH - BALL_RECT), HEIGHT // 2, BALL_RECT, BALL_RECT)
    ball_x, ball_y = 1, -1

    # блоки
    block_list = []
    for i in range(BLOCK_COLS):
        for j in range(BLOCK_ROWS):
            block_list.append(pygame.Rect(15 + 120 * i, 15 + 70 * j, BLOCK_WIDTH, BLOCK_HEIGHT))
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(BLOCK_COLS * BLOCK_ROWS)]

    game_paused = False
    running = True

    while running:
        screen.blit(img_night_mode, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Escape для паузы
                    running = False
                    game_running = False
                if event.key == pygame.K_p:  # "P" для паузы
                    game_paused = not game_paused

        if game_paused:
            font = pygame.font.Font(None, 100)
            draw_text_with_outline(screen, "PAUSED", font, (255, 255, 255), (0, 0, 0),
                                    (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.flip()
            continue

        # Отрисовка блоков, платформы и шарика
        [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(screen, pygame.Color('purple'), platform)
        pygame.draw.circle(screen, pygame.Color('white'), ball.center, BALL_R)

        # Движение шарика
        ball.x += ball_x * ball_speed
        ball.y += ball_y * ball_speed

        # Проверка столкновений
        if ball.centerx < BALL_R or ball.centerx > WIDTH - BALL_R:
            ball_x = -ball_x
        if ball.centery < BALL_R:
            ball_y = -ball_y
        if ball.colliderect(platform) and ball_y > 0:
            ball_x, ball_y = collision(ball_x, ball_y, ball, platform)

        # Проверка столкновения с блоками
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            color_list.pop(hit_index)
            ball_x, ball_y = collision(ball_x, ball_y, ball, hit_rect)
            fps += 2

        # Движение платформы
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and platform.left > 0:
            platform.left -= platform_speed
        if key[pygame.K_RIGHT] and platform.right < WIDTH:
            platform.right += platform_speed

        # Проверка проигрыша/выигрыша
        if ball.bottom > HEIGHT:
            show_end_screen(screen, "GAME OVER!", (255, 0, 0))
            fps = 60
            running = False
            game_running = False
        elif not block_list:
            show_end_screen(screen, "WIN!", (0, 0, 255))
            fps = 60
            running = False
            game_running = False

        pygame.display.flip()
        clock.tick(fps)


def game_2():
    global game_2_running, ball_speed
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Arkanoid 2")

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Параметры платформ
    PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
    BALL_SIZE = 20

    # Начальные позиции
    left_paddle = pygame.Rect(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    # Скорости
    paddle_speed = 5
    ball_speed_x, ball_speed_y = 4, 4

    # Игровой цикл
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed

        # Движение мяча
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Отскоки от верхней и нижней границы
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Отскоки от платформ
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

        # Проверка на проигрыш
        if ball.left <= 0:
            show_end_screen(screen, "PLAYER 1 LOST", (255, 0, 0))
            running = False
        elif ball.right >= WIDTH:
            show_end_screen(screen, "PLAYER 2 LOST", (255, 0, 0))
            running = False

        # Отрисовка
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.display.flip()
        clock.tick(60)


def menu():
    global game_running, game_2_running
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Arkanoid")
    sound = pygame.mixer.Sound("Arkanoid.mp3")
    sound.play(-1)
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
    font_path = 'ofont.ru_Pixel Cyr.ttf'

    while True:
        screen.fill((0, 0, 0))
        image = pygame.image.load('welcome.jpg')
        new_image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        screen.blit(new_image, (0, 0))

        image1 = pygame.image.load('vkl.png')
        new_size = (50, 50)
        image2 = pygame.transform.scale(image1, new_size)
        im = image2.get_rect(center=(850, 550))
        screen.blit(image2, im)

        font = pygame.font.Font(font_path, 70)

        draw_text_with_outline(screen, "Arkanoid", font, (255, 255, 255), (0, 0, 0), (300, 50))

        font = pygame.font.Font(None, 30)
        text = font.render('Play 1', True, (0, 0, 0))
        but1 = pygame.Rect(360, 400, 140, 50)
        pygame.draw.rect(screen, (255, 255, 255), but1)
        text_rect = text.get_rect(center=(430, 425))
        screen.blit(text, text_rect)

        font = pygame.font.Font(None, 30)
        txt = font.render('Play 2', True, (0, 0, 0))
        but2 = pygame.Rect(360, 480, 140, 50)
        pygame.draw.rect(screen, (255, 255, 255), but2)
        text_rec = txt.get_rect(center=(430, 505))
        screen.blit(txt, text_rec)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_running = True

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if but1.collidepoint(event.pos):  # Если нажата кнопка "Играть"
                    game_running = True
                if im.collidepoint(event.pos):  # Если нажата кнопка "Выйти"
                    confirm_exit(screen)
                if but2.collidepoint(event.pos):
                    game_2_running = True

        pygame.display.flip()

        # Запуск игры
        if game_running:
            game()
            game_running = False  # После игры вернуться в меню

        if game_2_running:
            game_2()
            game_2_running = False


def confirm_exit(screen):
    font = pygame.font.Font(None, 40)

    modal_rect = pygame.Rect(240, 230, 420, 200)

    exit_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 30, 100, 50)
    return_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 30, 100, 50)

    while True:
        pygame.draw.rect(screen, (50, 50, 50), modal_rect, border_radius=10)  # Фон окна
        pygame.draw.rect(screen, (200, 0, 0), exit_button, border_radius=5)  # Кнопка "Выйти"
        pygame.draw.rect(screen, (0, 200, 0), return_button, border_radius=5)  # Кнопка "Вернуться"

        # Текст
        text = font.render("Are you sure you want to exit?", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 60))

        exit_text = font.render("Exit", True, (255, 255, 255))
        screen.blit(exit_text, (exit_button.x + 20, exit_button.y + 10))

        return_text = font.render("Back", True, (255, 255, 255))
        screen.blit(return_text, (return_button.x + 5, return_button.y + 10))

        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):  # Если нажата кнопка "Выйти"
                    pygame.quit()
                    exit()
                if return_button.collidepoint(event.pos):  # Если нажата кнопка "Вернуться"
                    return  # Просто закрываем окно подтверждения

if __name__ == "__main__":
    menu()