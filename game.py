import pygame
print(pygame.__version__)

import random
import sqlite3

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Catch the Circle')
clock = pygame.time.Clock()

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 20])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - 30
        self.change_x = 0

    def update(self):
        self.rect.x += self.change_x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - 50:
            self.rect.x = SCREEN_WIDTH - 50

    def go_left(self):
        self.change_x = -5

    def go_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0

# Define the Circle class
class Circle(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, RED, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = 0 - 30
        self.speed_y = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Enhanced Function to save high score
def save_high_score(name, score):
    try:
        conn = sqlite3.connect('highscores.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO high_scores (name, score) VALUES (?, ?)', (name, score))
        conn.commit()
        conn.close()
        print('Score saved successfully!')
    except Exception as e:
        print('Error saving score:', e)

# Function to get top 5 high scores
def get_top_scores():
    conn = sqlite3.connect('highscores.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, score FROM high_scores ORDER BY score DESC LIMIT 5')
    scores = cursor.fetchall()
    conn.close()
    return scores

# Main game loop
player = Player()
all_sprites = pygame.sprite.Group()
circles = pygame.sprite.Group()
all_sprites.add(player)
score = 0
lives = 3
level = 1
font = pygame.font.SysFont(None, 36)

running = True
while running and lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.go_left()
            elif event.key == pygame.K_RIGHT:
                player.go_right()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stop()

    # Update
    all_sprites.update()
    circle_hit_list = pygame.sprite.spritecollide(player, circles, True)
    for circle in circle_hit_list:
        score += 10 * level
        if score % 100 == 0:  # Level up every 100 points
            level += 1

    if len(circle_hit_list) == 0 and len(circles) == 0:
        lives -= 1

    # Draw
    screen.fill(WHITE)
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(level_text, (10, 70))
    all_sprites.draw(screen)
    pygame.display.flip()

    # Create new circles
    if random.randint(1, 30) == 1:
        circle = Circle(level + 2)  # Increase speed with level
        all_sprites.add(circle)
        circles.add(circle)

    clock.tick(60)

# After game loop ends (game over)
top_scores = get_top_scores()
if not top_scores or score > top_scores[-1][1]:
    # If new high score
    player_name = input('New high score! Enter your name: ')
    save_high_score(player_name, score)

# Display top 5 high scores
print('Top 5 High Scores:')
for s in top_scores:
    print(f'{s[0]}: {s[1]}')

pygame.quit()
