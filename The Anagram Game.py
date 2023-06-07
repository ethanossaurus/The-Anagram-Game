import pygame
import random
import json

# Initialize Pygame
pygame.init()

# Initialize Mixer
pygame.mixer.init()

# Load music file
pygame.mixer.music.load("musica.mp3")

# Set the volume
pygame.mixer.music.set_volume(0.3)

# Play music file
pygame.mixer.music.play()

# Set up the display
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Anagram Game")

# Set up colors
CREAM = (255, 245, 245)
BLACK = (0, 0, 0)
YELLOW = (233, 201, 97)
BACKGROUND_COLOR = (0, 102, 204)

JSON_FILE = "dictionary.json"

# Load the JSON dictionary
with open(JSON_FILE) as file:
    dictionary = json.load(file)

# Set up fonts
font_title = pygame.font.Font('SuperMario256.ttf', 60)
font_word = pygame.font.SysFont(None, 60)
font_result = pygame.font.SysFont(None, 30)
font_level = pygame.font.Font('MinecraftRegular-Bmg3.otf', 30)
font_attempts = pygame.font.Font('MinecraftRegular-Bmg3.otf', 20)
font_menu = pygame.font.Font('MinecraftRegular-Bmg3.otf', 30)
font_input = pygame.font.SysFont(None, 32)

# Set up game variables
level = 1
word_length = level + 2

# Pick a word for the current level
def pick_word():
    words = [word for word in dictionary.keys() if len(word) == word_length]
    word = random.choice(words)
    meaning = dictionary[word]
    return word, meaning

# Scramble the word
def scramble_word(word):
    jumbled_word = list(word)
    random.shuffle(jumbled_word)
    return ''.join(jumbled_word)

# Display the word and attempts
def display_gameplay(scrambled_word, attempts):
    word_text = font_word.render(scrambled_word, True, CREAM)
    word_rect = word_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    window.blit(word_text, word_rect)

    attempts_text = font_attempts.render(f"Attempts: {attempts}", True, BLACK)
    attempts_rect = attempts_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(attempts_text, attempts_rect)

    level_text = font_level.render(f"Level: {level}", True, YELLOW)
    level_rect = level_text.get_rect(topright=(WIDTH - 20, 20))
    window.blit(level_text, level_rect)

    pygame.draw.rect(window, YELLOW, give_up_rect.inflate(15, 15))
    window.blit(give_up_text, give_up_rect)

# Display the result
def display_result(result):
    result_text = font_result.render(result, True, YELLOW)
    result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    window.blit(result_text, result_rect)

# Display the menu
def display_menu():
    title_text = font_title.render("The Anagram Game", True, YELLOW)
    play_text = font_menu.render("Press Enter to Play...", True, CREAM)

    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    window.blit(title_text, title_rect)
    window.blit(play_text, play_rect)

# Game states
STATE_MENU = 0
STATE_GAME = 1
STATE_END = 2

# Set the initial game state
game_state = STATE_MENU

# Set up the input rectangle
input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 40)
input_active = False
input_color = BLACK

# Set up the "Give Up" button
give_up_text = font_menu.render("Give Up", True, CREAM)
give_up_rect = give_up_text.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))

# Set up the hint button
hint_text = font_menu.render("Hint", True, BLACK)
hint_rect = hint_text.get_rect(bottomleft=(20, HEIGHT - 20))

# Set up the game clock
clock = pygame.time.Clock()

# Set up the end menu
def display_end_menu(word):
    if level == 11:
        end_text = font_title.render("Congratulations!", True, YELLOW)
        word_text = font_menu.render("You completed all the levels!", True, BLACK)
    else:
        end_text = font_title.render("Game Over!", True, YELLOW)
        word_text = font_menu.render(f"The correct word was: {word}", True, BLACK)
    play_again_text = font_menu.render("Do you want to play again?", True, BLACK)
    yes_text = font_menu.render("Yes", True, BLACK)
    no_text = font_menu.render("No", True, BLACK)

    end_rect = end_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    word_rect = word_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    yes_rect = yes_text.get_rect(center=(WIDTH // 2 - 50, HEIGHT // 2 + 200))
    no_rect = no_text.get_rect(center=(WIDTH // 2 + 50, HEIGHT // 2 + 200))

    pygame.draw.rect(window, YELLOW, yes_rect.inflate(10, 10))
    pygame.draw.rect(window, YELLOW, no_rect.inflate(10, 10))

    window.blit(end_text, end_rect)
    window.blit(word_text, word_rect)
    window.blit(play_again_text, play_again_rect)
    window.blit(yes_text, yes_rect)
    window.blit(no_text, no_rect)

    pygame.display.update()

    return play_again_rect, yes_rect, no_rect

# Run the game loop
running = True
input_rect_clicked = False
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == STATE_MENU:
                if event.key == pygame.K_RETURN:
                    game_state = STATE_GAME
                    level = 1
                    word_length = level + 2
                    word, meaning = pick_word()
                    scrambled_word = scramble_word(word)
                    guess = ""
                    result = ""
                    attempts = 5  # Reset attempts for the new game
            elif game_state == STATE_GAME:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if guess.lower() == word:
                            if level == 10:
                                game_state = STATE_END
                            else:
                                level += 1
                                word_length = level + 2
                                word, meaning = pick_word()
                                scrambled_word = scramble_word(word)
                                guess = ""
                                result = "Correct!"
                                attempts = 5  # Reset attempts for the new level
                        else:
                            attempts -= 1  # Decrease the attempts on a wrong guess
                            if attempts == 0:
                                game_state = STATE_END
                                result = "Game Over!"
                            elif attempts == 1:
                                result = "Wrong! Last attempt!"
                            else:
                                result = "Wrong! Try again."
                        guess = ""  # Clear the guess after processing
                    elif event.key == pygame.K_BACKSPACE:
                        guess = guess[:-1]
                    else:
                        guess += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == STATE_GAME:
                if input_rect.collidepoint(event.pos):
                    input_rect_clicked = True
                if input_rect_clicked:
                    input_active = True
                    input_color = YELLOW
                else:
                    input_active = False
                    input_color = BLACK

            if game_state == STATE_GAME:
                if give_up_rect.collidepoint(event.pos):
                    game_state = STATE_END
                    result = "Game Over!"
                    play_again_rect, yes_rect, no_rect = display_end_menu(word)
                    pygame.display.update()

            elif game_state == STATE_END:
                if yes_rect.collidepoint(event.pos):
                    game_state = STATE_GAME
                    level = 1
                    word_length = level + 2
                    word, meaning = pick_word()
                    scrambled_word = scramble_word(word)
                    guess = ""
                    result = ""
                    attempts = 5  # Reset attempts for the new game
                elif no_rect.collidepoint(event.pos):
                    running = False

    # Clear the window
    window.fill(BACKGROUND_COLOR)

    if game_state == STATE_MENU:
        display_menu()

    elif game_state == STATE_GAME:
        display_gameplay(scrambled_word, attempts)

        pygame.draw.rect(window, input_color, input_rect, 2)
        text_surface = font_input.render(guess, True, BLACK)
        window.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(200, text_surface.get_width() + 10)

        display_result(result)

    elif game_state == STATE_END:
        play_again_rect, yes_rect, no_rect = display_end_menu(word)

    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()