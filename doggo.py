import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DogGo")

PINK = (255, 204, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (255, 182, 193)
BUTTON_HOVER_COLOR = (255, 105, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font_large = pygame.font.Font(None, 80)
font_medium = pygame.font.Font(None, 50)

word_data = [
    {"russian": "Собака", "english": "Dog", "image": "images/dog_go.jpg"},
    {"russian": "Кошка", "english": "Cat", "image": "images/cat_go.jpg"},
    {"russian": "Корова", "english": "Cow", "image": "images/cow_go.jpg"},
    {"russian": "Мышь", "english": "Mouse", "image": "images/mouse_go.jpg"},
    {"russian": "Лошадь", "english": "Horse", "image": "images/hours_go.jpg"},
    {"russian": "Утка", "english": "Duck", "image": "images/duck_go.jpg"},
    {"russian": "Овца", "english": "Sheep", "image": "images/sheep_go.jpg"},
    {"russian": "Свинья", "english": "Pig", "image": "images/pig_go.jpg"},
    {"russian": "Лиса", "english": "Fox", "image": "images/fox_go.jpg"},
    {"russian": "Медведь", "english": "Bear", "image": "images/bear_go.jpg"},
    {"russian": "Тигр", "english": "Tiger", "image": "images/tiger_go.jpg"},
    {"russian": "Лев", "english": "Lion", "image": "images/lion_go.jpg"},
    {"russian": "Волк", "english": "Wolf", "image": "images/wolf_go.jpg"},
    {"russian": "Орёл", "english": "Eagle", "image": "images/eagle_go.jpg"},
    {"russian": "Жираф", "english": "Giraffe", "image": "images/giraffe_go.jpg"},
    {"russian": "Слон", "english": "Elephant", "image": "images/elephant_go.jpg"},
    {"russian": "Обезьяна", "english": "Monkey", "image": "images/monkey_go.jpg"},
    {"russian": "Черепаха", "english": "Turtle", "image": "images/turtle_go.jpg"},
    {"russian": "Акула", "english": "Shark", "image": "images/shark_go.jpg"},
    {"russian": "Лягушка", "english": "Frog", "image": "images/frog_go.jpg"},
    {"russian": "Крокодил", "english": "Crocodile", "image": "images/croc_go.jpg"},
]

phrase_data = [
    {"russian": "Большая собака", "english": "Big dog", "image": "images/big_dog.jpg"},
    {"russian": "Чёрная кошка", "english": "Black cat", "image": "images/black_cat.jpg"},
    {"russian": "Белая корова", "english": "White cow", "image": "images/white_cow.jpg"},
    {"russian": "Серая мышь", "english": "Gray mouse", "image": "images/gray_mouse.jpg"},
    {"russian": "Белая лошадь", "english": "White horse", "image": "images/white_horse.jpg"},
]

def draw_text(text, font, color, x, y):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(x, y))
    screen.blit(rendered_text, text_rect)

def draw_button(text, x, y, width, height, is_hovered):
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=15)
    draw_text(text, font_medium, BLACK, x + width // 2, y + height // 2)
    return pygame.Rect(x, y, width, height)

def get_random_word():
    word = random.choice(word_data)
    correct_answer = word["english"]
    incorrect_answers = [w["english"] for w in word_data if w != word]
    options = [correct_answer] + random.sample(incorrect_answers, 3)
    random.shuffle(options)
    return word, correct_answer, options

def get_random_phrase():
    phrase = random.choice(phrase_data)
    correct_answer = phrase["english"]
    incorrect_answers = [p["english"] for p in phrase_data if p != phrase]
    options = [correct_answer] + random.sample(incorrect_answers, 3)
    random.shuffle(options)
    return phrase, correct_answer, options

def congrats_screen():
    running = True
    while running:
        screen.fill(PINK)
        draw_gradient(screen, (255, 182, 193), (255, 0, 0), WIDTH, HEIGHT)
        draw_text("Congratulations!", font_large, WHITE, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text("Press Next to Continue", font_medium, WHITE, WIDTH // 2, HEIGHT // 2)

        button_next = draw_button("Next", WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 70,
                                  pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 70).collidepoint(pygame.mouse.get_pos()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_next.collidepoint(event.pos):
                    running = False

        pygame.display.flip()

def game_screen_words():
    running = True
    level = 1
    score = 0

    word, correct_answer, options = get_random_word()
    feedback_color = None
    feedback_time = 0

    while running:

        draw_gradient(screen, (255, 182, 193), (255, 0, 0), WIDTH, HEIGHT)

        draw_text("Переведи", font_large, WHITE, WIDTH // 2, 150)
        draw_text(word["russian"], font_large, WHITE, WIDTH // 2, 250)

        image_width, image_height = 200, 200
        image_x = (WIDTH - image_width) // 2
        image_y = (HEIGHT - image_height) // 2
        try:
            image = pygame.image.load(word["image"])
            image = pygame.transform.scale(image, (image_width, image_height))
            screen.blit(image, (image_x, image_y))
        except pygame.error as e:
            print(f"Error loading image: {word['image']}, {e}")

        button_width, button_height = 200, 60

        button_y_start = image_y + image_height + 20
        button_gap = 80

        left_button_positions = [
            (WIDTH // 4 - button_width // 2, button_y_start + i * button_gap)
            for i in range(2)
        ]
        right_button_positions = [
            (3 * WIDTH // 4 - button_width // 2, button_y_start + i * button_gap)
            for i in range(2)
        ]

        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        for i, (x, y) in enumerate(left_button_positions):
            is_hovered = pygame.Rect(x, y, button_width, button_height).collidepoint(mouse_pos)
            button_rect = draw_button(options[i], x, y, button_width, button_height, is_hovered)

            if is_hovered and clicked:
                if options[i] == correct_answer:
                    feedback_color = GREEN
                    score += 1
                    if level % 5 == 0 and score % 5 == 0:
                        congrats_screen()
                    level += 1
                    word, correct_answer, options = get_random_word()
                else:
                    feedback_color = RED
                feedback_time = pygame.time.get_ticks()

        for i, (x, y) in enumerate(right_button_positions):
            is_hovered = pygame.Rect(x, y, button_width, button_height).collidepoint(mouse_pos)
            button_rect = draw_button(options[i + 2], x, y, button_width, button_height, is_hovered)

            if is_hovered and clicked:
                if options[i + 2] == correct_answer:
                    feedback_color = GREEN
                    score += 1
                    if level % 5 == 0 and score % 5 == 0:
                        congrats_screen()
                    level += 1
                    word, correct_answer, options = get_random_word()
                else:
                    feedback_color = RED
                feedback_time = pygame.time.get_ticks()

        if feedback_color and pygame.time.get_ticks() - feedback_time < 1000:
            draw_text("Correct!" if feedback_color == GREEN else "Wrong!", font_medium, feedback_color, WIDTH // 2, 350)
        elif feedback_color:
            feedback_color = None

        pygame.display.flip()

def game_screen_phrases():
    running = True
    level = 1
    score = 0

    phrase, correct_answer, options = get_random_phrase()
    feedback_color = None
    feedback_time = 0

    while running:
        screen.fill(PINK)

        draw_gradient(screen, (255, 182, 193), (255, 0, 0), WIDTH, HEIGHT)

        draw_text("TRANSLATE PHRASE", font_large, WHITE, WIDTH // 2, 150)
        draw_text(phrase["russian"], font_large, WHITE, WIDTH // 2, 250)

        image_width, image_height = 200, 200
        image_x = (WIDTH - image_width) // 2
        image_y = (HEIGHT - image_height) // 2
        try:
            image = pygame.image.load(phrase["image"])
            image = pygame.transform.scale(image, (image_width, image_height))
            screen.blit(image, (image_x, image_y))
        except pygame.error as e:
            print(f"Error loading image: {phrase['image']}, {e}")

        button_width, button_height = 200, 60

        button_y_start = image_y + image_height + 20
        button_gap = 80

        left_button_positions = [
            (WIDTH // 4 - button_width // 2, button_y_start + i * button_gap)
            for i in range(2)
        ]
        right_button_positions = [
            (3 * WIDTH // 4 - button_width // 2, button_y_start + i * button_gap)
            for i in range(2)
        ]

        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        for i, (x, y) in enumerate(left_button_positions):
            is_hovered = pygame.Rect(x, y, button_width, button_height).collidepoint(mouse_pos)
            button_rect = draw_button(options[i], x, y, button_width, button_height, is_hovered)

            if is_hovered and clicked:
                if options[i] == correct_answer:
                    feedback_color = GREEN
                    score += 1
                    if level % 5 == 0 and score % 5 == 0:
                        congrats_screen()
                    level += 1
                    phrase, correct_answer, options = get_random_phrase()
                else:
                    feedback_color = RED
                feedback_time = pygame.time.get_ticks()

        for i, (x, y) in enumerate(right_button_positions):
            is_hovered = pygame.Rect(x, y, button_width, button_height).collidepoint(mouse_pos)
            button_rect = draw_button(options[i + 2], x, y, button_width, button_height, is_hovered)

            if is_hovered and clicked:
                if options[i + 2] == correct_answer:
                    feedback_color = GREEN
                    score += 1
                    if level % 5 == 0 and score % 5 == 0:
                        congrats_screen()
                    level += 1
                    phrase, correct_answer, options = get_random_phrase()
                else:
                    feedback_color = RED
                feedback_time = pygame.time.get_ticks()

        if feedback_color and pygame.time.get_ticks() - feedback_time < 1000:
            draw_text("Correct!" if feedback_color == GREEN else "Wrong!", font_medium, feedback_color, WIDTH // 2, 350)
        elif feedback_color:
            feedback_color = None

        pygame.display.flip()


def draw_gradient(surface, color_start, color_end, width, height):

    for y in range(height):

        blend = y / height
        r = int(color_start[0] * (1 - blend) + color_end[0] * blend)
        g = int(color_start[1] * (1 - blend) + color_end[1] * blend)
        b = int(color_start[2] * (1 - blend) + color_end[2] * blend)
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

def main_menu():
    running = True
    while running:

        draw_gradient(screen, (255, 182, 193), (255, 0, 0), WIDTH, HEIGHT)

        draw_text("DOG GO", font_large, WHITE, WIDTH // 2, HEIGHT // 2 - 100)
        draw_text("Выбери режим", font_medium, WHITE, WIDTH // 2, HEIGHT // 2 - 40)

        button_words = draw_button("Слова", WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 70,
                                   pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 70).collidepoint(pygame.mouse.get_pos()))
        button_phrases = draw_button("Фразы", WIDTH // 2 - 100, HEIGHT // 2 + 230, 200, 70,
                                     pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 230, 200, 70).collidepoint(pygame.mouse.get_pos()))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_words.collidepoint(event.pos):
                    game_screen_words()
                if button_phrases.collidepoint(event.pos):
                    game_screen_phrases()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()