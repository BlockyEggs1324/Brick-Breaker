import random
from time import sleep

import pygame

# Initialize Pygame
pygame.init()

# Game loop
running = True
clock = pygame.time.Clock()

# Set up the game window
WIDTH = 1920
HEIGHT = 1080
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the paddle
paddle_width = 100
paddle_height = 10
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - paddle_height - 50
paddle_speed = 5

# Set up the ball
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-2, 2])
ball_dy = -2
ball_speed = 2

# Set up the blocks
block_width = 70
block_height = 20
block_rows = 30
block_cols = 25
blocks = []

# Set up text
font = pygame.font.Font("freesansbold.ttf", 32)
text = font.render("", True, BLACK, None)
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)


for row in range(block_rows):
  for col in range(block_cols):
    block_x = col * (block_width + 5) + 30
    block_y = row * (block_height + 5) + 30
    blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))

# Define the ball object
class Ball(pygame.Rect):
  def __init__(self, x, y, dx, dy):
    super().__init__(x, y, ball_radius, ball_radius)
    self.dx = dx
    self.dy = dy
    self.type = "normal"

can_multiply = True
  
balls = [Ball(random.choice(range(800)), HEIGHT // 2, random.choice([-2, 2]), -2)]

class Powerup(pygame.sprite.Sprite):
  def __init__(self, x, y, type):
    pygame.sprite.Sprite.__init__(self)
    self.x = x
    self.y = y
    self.type = type
    self.image = pygame.image.load(f"sprites/{type}.png")
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    pygame.transform.scale(self.image, (0.1, 0.1))

powerup_types = ["paddle_big", "ball_multiply", "ball_add", "ball_power"]
dropped_powerups = pygame.sprite.Group(Powerup(100, 40, "paddle_big"), Powerup(100, 40, "paddle_big"), Powerup(100, 40, "paddle_big"))

ball_collide = True
ball_power_timer = 0

game_over_timer = 0
can_game_over = True

def drop_powerup(x,y): 
  dropped_powerups.add(Powerup(x, y, random.choice(powerup_types)))
  
running = True
sleep(2)
while running:

  clock.tick(100)  # Limit the frame rate to 60 FPS
  
  # Manage ball power timer
  
  if ball_power_timer > 0:
      ball_power_timer -= 1
      if ball_power_timer == 0:
          ball_collide = True
          print("ball now collide :)")

  # Manage game over time

  if game_over_timer > 0:
    game_over_timer -= 1
    if game_over_timer == 0:
      running = False

  
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  paddle_x = pygame.mouse.get_pos()[0] - paddle_width // 2

  for powerup in dropped_powerups:
    if powerup.rect.y > HEIGHT:
      dropped_powerups.remove(powerup)
    #if powerup.y == paddle_height and powerup.x > paddle_x - paddle_width // 2 and powerup.x < paddle_x + paddle_width // 2:
    if pygame.Rect(paddle_x,paddle_y, paddle_width, paddle_height).colliderect(powerup):
      if powerup.type == "paddle_big":
        paddle_width = paddle_width + 20
        print("Paddle bigger :)")

      elif powerup.type == "ball_add":
        balls.append(Ball(paddle_x - (paddle_width / 2), paddle_y - 10, -2, -2))
        balls.append(Ball(paddle_x + (paddle_width / 2), paddle_y - 10, 2, -2))
        print("Ball added :)")
        
      elif powerup.type == "ball_multiply":
        if can_multiply:
          print("More balls :)")
          print(len(balls))
          can_multiply = False
          balls_current = balls.copy()
          for ball in balls_current:
            if len(balls_current) < 1000:
              balls.append(Ball(ball.x, ball.y, 2, -2))
              balls.append(Ball(ball.x, ball.y, 2, 2))
              balls.append(Ball(ball.x, ball.y, -2, -2))
              balls.append(Ball(ball.x, ball.y, -2, 2))
            else:
              break
              print(len(balls))
          can_multiply = True
          

      elif powerup.type == "ball_power":
        ball_collide = False
        ball_power_timer = 1000

      dropped_powerups.remove(powerup)
  # Move the paddle
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] and paddle_x > 0:
    paddle_x -= paddle_speed
  if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
    paddle_x += paddle_speed

  for ball in balls:
    #  Move the ball
    ball.x += ball.dx * ball_speed
    ball.y += ball.dy * ball_speed

    # Collisions with the paddle
    if ball.colliderect(
      pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)):
      ball.dy = 0 - 2
      
  # Collisions with the walls
    if ball.x < 0 or ball.x > WIDTH - ball_radius:
      ball.dx = -ball.dx
    if ball.y < 0:
      ball.dy = -ball.dy

  # Check if the player wins or loses
    if ball.y > HEIGHT:
      balls.remove(ball)
      
    if len(blocks) == 0:
      text = font.render("You win!", True, BLACK, None)
      
    if len(balls) == 0:
      text = font.render("You lose!", True, BLACK, None)
      
  # Collisions with the blocks
  for block in blocks:
    for ball in balls:
      if ball.colliderect(block):
        if block in blocks:
          blocks.remove(block)
        if ball_collide:
          ball.dy = -ball.dy
        if random.choice(range(6)) == 1:
          drop_powerup(block.x, block.y)
          break
          
  # Draw the game objects
  
  # Clear the screen
  window.fill(WHITE)

  # Draw the paddle, ball, and blocks
  pygame.draw.rect(window, BLUE,
                   (paddle_x, paddle_y, paddle_width, paddle_height))
  for ball in balls:
    pygame.draw.circle(window, RED, (ball.x, ball.y), ball_radius)
  for block in blocks:
    pygame.draw.rect(window, BLUE, block)
    
  for powerup in dropped_powerups:
    powerup.rect.y += 5
    
  dropped_powerups.update()
  dropped_powerups.draw(window)

  # Draw game over text
  if len(blocks) == 0 or len(balls) == 0:
    window.blit(text, textRect)
    if can_game_over:
      game_over_timer = 300
      can_game_over = False
      
  # Update the display
  pygame.display.flip()

# Quit the game
pygame.quit()
