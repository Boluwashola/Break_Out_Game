import pygame
import asyncio
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 15
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

class Paddle:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 8
        
    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            
    def move_right(self):
        if self.x < SCREEN_WIDTH - PADDLE_WIDTH:
            self.x += self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, CYAN, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT), 2)

class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = random.choice([-4, 4])
        self.dy = -4
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
    def bounce_x(self):
        self.dx = -self.dx
        
    def bounce_y(self):
        self.dy = -self.dy
        
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), BALL_SIZE)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), BALL_SIZE, 2)

class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.destroyed = False
        
    def draw(self, screen):
        if not self.destroyed:
            pygame.draw.rect(screen, self.color, (self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT))
            pygame.draw.rect(screen, WHITE, (self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT), 1)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset_game()
        
    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + 5) + 35
                y = row * (BRICK_HEIGHT + 5) + 50
                color = colors[row % len(colors)]
                self.bricks.append(Brick(x, y, color))
    
    def handle_collisions(self):
        if self.ball.x <= BALL_SIZE or self.ball.x >= SCREEN_WIDTH - BALL_SIZE:
            self.ball.bounce_x()
        if self.ball.y <= BALL_SIZE:
            self.ball.bounce_y()
            
        if (self.ball.y + BALL_SIZE >= self.paddle.y and
            self.ball.x >= self.paddle.x and
            self.ball.x <= self.paddle.x + PADDLE_WIDTH):
            self.ball.bounce_y()
            hit_pos = (self.ball.x - self.paddle.x) / PADDLE_WIDTH
            self.ball.dx = (hit_pos - 0.5) * 8
            
        for brick in self.bricks:
            if not brick.destroyed:
                if (self.ball.x + BALL_SIZE >= brick.x and
                    self.ball.x - BALL_SIZE <= brick.x + BRICK_WIDTH and
                    self.ball.y + BALL_SIZE >= brick.y and
                    self.ball.y - BALL_SIZE <= brick.y + BRICK_HEIGHT):
                    brick.destroyed = True
                    self.ball.bounce_y()
                    self.score += 10
                    break
                    
        if self.ball.y > SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball = Ball()
                
        if all(brick.destroyed for brick in self.bricks):
            self.won = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
            
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER - Press R to Restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        elif self.won:
            win_text = self.font.render("YOU WIN! - Press R to Restart", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(win_text, text_rect)
            
        pygame.display.flip()
    
    async def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and (self.game_over or self.won):
                        self.reset_game()
            
            if not self.game_over and not self.won:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.paddle.move_left()
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.paddle.move_right()
                
                self.ball.move()
                self.handle_collisions()
            
            self.draw()
            self.clock.tick(60)
            await asyncio.sleep(0)
        
        pygame.quit()

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())