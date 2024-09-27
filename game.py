import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arcade Space Shooter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game clock
clock = pygame.time.Clock()

# Player (spaceship) settings
player_width = 50
player_height = 60
player_speed = 5

# Enemy settings
enemy_width = 50
enemy_height = 50
enemy_speed = 3

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7

# Load player image (optional, you can draw a rectangle instead)
# player_image = pygame.image.load('path_to_spaceship_image.png')

# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - player_width // 2
        self.y = SCREEN_HEIGHT - player_height - 10
        self.speed = player_speed
        self.width = player_width
        self.height = player_height
        self.lives = 3

    def draw(self, screen):
        # Drawing the spaceship (you can replace this with an image if needed)
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x + self.speed + self.width < SCREEN_WIDTH:
            self.x += self.speed

    def shoot(self):
        bullets.append(Bullet(self.x + self.width // 2, self.y))

# Bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = bullet_speed

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, bullet_width, bullet_height))

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH - enemy_width)
        self.y = random.randint(-150, -50)
        self.speed = enemy_speed

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, enemy_width, enemy_height))

# Game loop
def game_loop():
    player = Player()
    global bullets
    bullets = []
    enemies = []
    score = 0

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Shooting bullets
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Move and draw bullets
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(screen)
            if bullet.y < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if random.randint(0, 60) == 0:
            enemies.append(Enemy())

        # Move and draw enemies
        for enemy in enemies[:]:
            enemy.move()
            enemy.draw(screen)

            # Check for collision with player
            if (enemy.x < player.x < enemy.x + enemy_width or
                enemy.x < player.x + player.width < enemy.x + enemy_width) and \
               (enemy.y + enemy_height >= player.y):
                running = False  # End game if player collides with an enemy

            # Check for collision with bullets
            for bullet in bullets[:]:
                if (enemy.x < bullet.x < enemy.x + enemy_width) and (enemy.y < bullet.y < enemy.y + enemy_height):
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 1

            # Remove enemies that go off the screen
            if enemy.y > SCREEN_HEIGHT:
                enemies.remove(enemy)

        # Draw the player
        player.draw(screen)

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Run the game
game_loop()

