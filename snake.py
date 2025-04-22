import pygame
import random
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname = "snake",
    user = "postgres",
    password = "postgres123",
    host = "127.0.0.1",
    port = "5432"
)
cur = conn.cursor()

def get_or_create_user(username):
    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
        cur.execute("""
            SELECT level, score FROM user_score
            WHERE user_id = %s
            ORDER BY saved_at DESC
            LIMIT 1
        """, (user_id,))
        data = cur.fetchone()
        if data:
            return user_id, data[0], data[1]
        else:
            return user_id, 1, 0
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING user_id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id, 1, 0

def save_score(user_id, level, score):
    cur.execute("""
        INSERT INTO user_score (user_id, level, score, saved_at)
        VALUES (%s, %s, %s, %s)
    """, (user_id, level, score, datetime.now()))
    conn.commit()

pygame.init()
width, height = 800, 600
c_size = 20
white = (255, 255, 255)
red = (255, 0, 0)
black = (89,45,0)
green = (255, 192, 203)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")
font_big = pygame.font.SysFont("Arial", 60)
font_small = pygame.font.SysFont("Arial", 30)

class Snake:
    def __init__(self):
        self.body = [(100, 60), (80, 60), (60, 60)]
        self.direction = "RIGHT"
    def move(self):
        head_x, head_y = self.body[0]
        if self.direction == "RIGHT": head_x += c_size
        elif self.direction == "LEFT": head_x -= c_size
        elif self.direction == "UP": head_y -= c_size
        elif self.direction == "DOWN": head_y += c_size
        head_x %= width
        head_y %= height
        new_head = (head_x, head_y)
        if new_head in self.body[1:]:
            return False
        self.body.insert(0, new_head)
        return True
    def grow(self): pass
    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, green, (segment[0], segment[1], c_size, c_size))
    
class Food:
    def __init__(self, snake_body): 
        self.spawn(snake_body)
    def spawn(self, snake_body):
        while True:
            self.x = random.randint(0, (width - c_size) // c_size) * c_size
            self.y = random.randint(0, (height - c_size) // c_size) * c_size
            if (self.x, self.y) not in snake_body: 
                break
        self.weight = 1
        self.spawn_time = pygame.time.get_ticks()
    def draw(self, surface):
        pygame.draw.rect(surface, red, (self.x, self.y, c_size, c_size))
    def disappearing(self, duration=7000):
        return pygame.time.get_ticks() - self.spawn_time > duration 


def game():
    username = input("Write username: ")
    user_id, level, score = get_or_create_user(username)
    speed = 5 + (level - 1) * 2
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake.body)
    running = True
    game_over = False
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != "DOWN":
                    snake.direction = "UP"
                elif event.key == pygame.K_DOWN and snake.direction != "UP":
                    snake.direction = "DOWN"
                elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                    snake.direction = "RIGHT"
                elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                    snake.direction = "LEFT"
                elif event.key == pygame.K_s:
                    save_score(user_id, level, score)
        if not game_over:
            alive = snake.move()
            if not alive:
                game_over = True
            if snake.body[0] == (food.x, food.y):
                score += food.weight
                for _ in range(food.weight): snake.grow()
                food.spawn(snake.body)
                if score // 5 >= level:
                    level += 1
                    speed += 2
            else:
                snake.body.pop()
            if food.disappearing(): food.spawn(snake.body)
        screen.fill(black)
        snake.draw(screen)
        food.draw(screen)
        score_text = font_small.render(f"Score: {score}", True, white)
        level_text = font_small.render(f"Level: {level}", True, white)
        screen.blit(score_text, (width - 150, 20))
        screen.blit(level_text, (width - 150, 50))
        if game_over:
            over_text = font_big.render("GAME OVER!", True, red)
            screen.blit(over_text, (width // 2 - 180, height // 2 - 30))
        pygame.display.update()
    save_score(user_id, level, score)
    pygame.quit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    game()


# cur.execute("CREATE TABLE user_score(user_id SERIAL PRIMARY KEY, level INT NOT NULL, score INT, saved_at TIMESTAMP without TIME ZONE)")
# conn.commit()

# cur.execute("CREATE TABLE users(user_id SERIAL PRIMARY KEY, username VARCHAR(50) NOT NULL)")
# conn.commit()