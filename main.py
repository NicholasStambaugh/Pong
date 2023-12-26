import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1100, 700
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 85
BALL_SIZE = 15
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create the Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit = False  # New attribute to track hit state

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += 5

        # Reset hit state after a certain duration
        if self.hit:
            self.hit = False

# Create the Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed = [random.choice([-5, 5]), random.choice([-5, 5])]
        self.speed_multiplier = 1.05  # Initial speed multiplier

    def update(self):
        self.rect.x += int(self.speed[0] * self.speed_multiplier)
        self.rect.y += int(self.speed[1] * self.speed_multiplier)

        # Bounce off the top and bottom edges
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]

# Initialize game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Set window icon
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pong.png')
icon_surface = pygame.image.load(icon_path)
pygame.display.set_icon(icon_surface)

# Create sprite groups
all_sprites = pygame.sprite.Group()
paddles = pygame.sprite.Group()
ball_group = pygame.sprite.Group()

# Create paddles and add to sprite groups
player_paddle = Paddle(PADDLE_WIDTH, HEIGHT // 2)
ai_paddle = Paddle(WIDTH - PADDLE_WIDTH, HEIGHT // 2)
all_sprites.add(player_paddle, ai_paddle)
paddles.add(player_paddle, ai_paddle)

# Create ball and add to sprite groups
ball = Ball()
all_sprites.add(ball)
ball_group.add(ball)

# Score variables
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True
player_scored_timer = 0
ai_scored_timer = 0
speed_increase_interval = FPS * 5  # Increase speed every 5 seconds
speed_increase_timer = speed_increase_interval
hit_duration = FPS // 2  # Flash green for 0.5 seconds
hit_timer = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # AI control
    if ball.rect.centery < ai_paddle.rect.centery and ai_paddle.rect.top > 0:
        ai_paddle.rect.y -= 5
    elif ball.rect.centery > ai_paddle.rect.centery and ai_paddle.rect.bottom < HEIGHT:
        ai_paddle.rect.y += 5

    # Check for collisions
    if pygame.sprite.spritecollide(player_paddle, ball_group, False):
        ball.speed[0] = -ball.speed[0]
        player_paddle.hit = True
        hit_timer = hit_duration

    if pygame.sprite.spritecollide(ai_paddle, ball_group, False):
        ball.speed[0] = -ball.speed[0]
        ai_paddle.hit = True
        hit_timer = hit_duration

    # Check for scoring
    if ball.rect.left <= 0:
        # AI scores
        ai_score += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed = [random.choice([-5, 5]), random.choice([-5, 5])]
        ai_scored_timer = FPS * 2

    elif ball.rect.right >= WIDTH:
        # Player scores
        player_score += 1
        ball.rect.center = (WIDTH // 2, HEIGHT // 2)
        ball.speed = [random.choice([-5, 5]), random.choice([-5, 5])]
        player_scored_timer = FPS * 2  # Display message for 2 seconds

    # Check for game end
    if player_score == 5 or ai_score == 5:
        running = False

    # Increase ball speed over time
    if speed_increase_timer <= 0:
        ball.speed_multiplier += 0.1
        speed_increase_timer = speed_increase_interval

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # Draw scores
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    ai_text = font.render(f"AI: {ai_score}", True, WHITE)
    screen.blit(player_text, (20, 20))
    screen.blit(ai_text, (WIDTH - ai_text.get_width() - 20, 20))

    # Draw player scored message
    if player_scored_timer > 0:
        player_scored = font.render("Player scored!", True, WHITE)
        screen.blit(player_scored, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        player_scored_timer -= 1

    if ai_scored_timer > 0:
        ai_scored = font.render("Bot Scored! NOOB!", True, WHITE)
        screen.blit(ai_scored, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        ai_scored_timer -= 1

    # Flash green when hit
    if hit_timer > 0:
        for paddle in paddles:
            if paddle.hit:
                paddle.image.fill(GREEN)
        hit_timer -= 1
    else:
        # Reset paddle color to white
        for paddle in paddles:
            paddle.image.fill(WHITE)

    # Refresh screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

    # Decrement the speed increase timer
    speed_increase_timer -= 1

# Quit the game
pygame.quit()
