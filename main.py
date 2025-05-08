import pygame
import random
import time
import json
from collections import OrderedDict

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)
PURPLE = (128, 0, 128)

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BASE_FPS = 10


# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Set up the display



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def get_player_name():
    name = ""
    font = pygame.font.SysFont('arial', 32)
    input_active = True
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isalnum():
                    name += event.unicode
        
        screen.fill(BLACK)
        prompt_text = font.render("Enter your name:", True, WHITE)
        name_text = font.render(name, True, WHITE)
        
        screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 - 50))
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 150, HEIGHT//2, 300, 40), 2)
        screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, HEIGHT//2 + 5))
        
        if not name.strip():
            hint_text = font.render("(Must enter a name)", True, RED)
            screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2, HEIGHT//2 + 50))
        
        pygame.display.flip()
        clock.tick(BASE_FPS)
    
    return name.strip() if name.strip() else "Player"

def select_difficulty():
    """Display difficulty selection screen"""
    difficulties = [
        {"name": "Easy", "fps": BASE_FPS, "color": GREEN, "score_multiplier": 1},
        {"name": "Normal", "fps": BASE_FPS + 5, "color": YELLOW, "score_multiplier": 2},
        {"name": "Hard", "fps": BASE_FPS + 10, "color": RED, "score_multiplier": 3},
        {"name": "High Scores", "fps": BASE_FPS, "color": BLUE, "score_multiplier": 0}
    ]
    selected = 1  # Default to Normal
    
    font_title = pygame.font.SysFont('arial', 48)
    font_options = pygame.font.SysFont('arial', 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    if selected == 3:  # High Scores option
                        if show_high_scores(screen):
                            continue
                        else:
                            return None
                    return difficulties[selected]
        
        screen.fill(BLACK)
        title_text = font_title.render("Select Difficulty", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 50))
        
        for i, diff in enumerate(difficulties):
            color = diff["color"] if i == selected else GRAY
            text = font_options.render(diff["name"], True, color)
            x = WIDTH//2 - text.get_width()//2
            y = 150 + i * 60
            screen.blit(text, (x, y))
            
            if i == selected:
                pygame.draw.rect(screen, color, (x - 20, y - 10, text.get_width() + 40, text.get_height() + 20), 2)
        
        pygame.display.flip()
        clock.tick(BASE_FPS)


def load_high_scores():
    try:
        with open('highscores.json', 'r') as f:
            scores = json.load(f)
            # Convert to list of tuples and sort by score (descending)
            sorted_scores = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
            return OrderedDict(sorted_scores[:7])  # Return only top 7
    except (FileNotFoundError, json.JSONDecodeError):
        return OrderedDict()
#######
def save_high_score(name, score, difficulty):
    scores = load_high_scores()
    
    # Check if player already exists and if new score is better
    if name in scores:
        if score > scores[name]['score']:
            scores[name] = {'score': score, 'difficulty': difficulty}
    else:
        scores[name] = {'score': score, 'difficulty': difficulty}
    
    # Keep only top 10 scores
    sorted_scores = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
    top_scores = OrderedDict(sorted_scores[:7])
    
    with open('highscores.json', 'w') as f:
        json.dump(top_scores, f, indent=4)

def show_high_scores(screen):
    """Display high scores screen with top 7"""
    scores = load_high_scores()
    
    screen.fill(BLACK)
    font_title = pygame.font.SysFont('arial', 48)
    font_header = pygame.font.SysFont('arial', 28)
    font_scores = pygame.font.SysFont('arial', 24)
    
    title_text = font_title.render("TOP 10 SCORES", True, PURPLE)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 30))
    
    if not scores:
        no_scores = font_header.render("No high scores yet!", True, WHITE)
        screen.blit(no_scores, (WIDTH//2 - no_scores.get_width()//2, 120))
    else:
        # Draw headers
        headers = ["Rank", "Name", "Score", "Difficulty"]
        for i, header in enumerate(headers):
            header_text = font_header.render(header, True, YELLOW)
            screen.blit(header_text, (50 + i * 100, 100))
        
        # Draw scores
        for i, (name, data) in enumerate(scores.items()):
            rank_text = font_scores.render(f"{i+1}.", True, WHITE)
            name_text = font_scores.render(name[:15], True, WHITE)  # Limit name length
            score_text = font_scores.render(str(data['score']), True, WHITE)
            diff_text = font_scores.render(data['difficulty'], True, WHITE)
            
            screen.blit(rank_text, (50, 140 + i * 30))
            screen.blit(name_text, (150, 140 + i * 30))
            screen.blit(score_text, (250, 140 + i * 30))
            screen.blit(diff_text, (350, 140 + i * 30))
    
    back_text = font_header.render("Press any key to continue", True, WHITE)
    screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 50))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
    return True

def draw_grid():
    """Draw grid lines for better visibility"""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def show_game_over(screen, score, player_name, difficulty_name):
    # Save the high score
    save_high_score(player_name, score, difficulty_name)
    
    screen.fill(BLACK)
    font_large = pygame.font.SysFont('arial', 48)
    font_medium = pygame.font.SysFont('arial', 32)
    font_small = pygame.font.SysFont('arial', 24)
    
    # Game over text with shadow effect
    game_over_text = font_large.render("GAME OVER", True, RED)
    shadow_text = font_large.render("GAME OVER", True, (50, 50, 50))
    screen.blit(shadow_text, (WIDTH//2 - shadow_text.get_width()//2 + 3, 53))
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 50))
    
    # Player info
    info_y = 120
    for text, value in [("Player:", player_name), 
                       ("Score:", str(score)), 
                       ("Difficulty:", difficulty_name)]:
        label = font_medium.render(text, True, WHITE)
        value_render = font_medium.render(value, True, YELLOW)
        screen.blit(label, (WIDTH//2 - 150, info_y))
        screen.blit(value_render, (WIDTH//2 + 20, info_y))
        info_y += 40
    
    # Menu options
    options = [
        ("R", "Restart Game", GREEN),
        ("H", "High Scores", BLUE),
        ("Q", "Quit Game", RED)
    ]
    
    option_y = 260
    for key, text, color in options:
        key_text = font_small.render(f"[{key}]", True, color)
        text_render = font_small.render(text, True, WHITE)
        screen.blit(key_text, (WIDTH//2 - 120, option_y))
        screen.blit(text_render, (WIDTH//2 - 80, option_y))
        option_y += 40
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_h:
                    show_high_scores(screen)
                    return show_game_over(screen, score, player_name, difficulty_name)
                if event.key == pygame.K_q:
                    return "quit"
        clock.tick(BASE_FPS)
################
class Snake:
    def __init__(self, difficulty):
        self.reset(difficulty)
        
    def reset(self, difficulty):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.length = 1
        self.score = 0
        self.color = GREEN
        self.base_fps = difficulty["fps"]
        self.score_multiplier = difficulty["score_multiplier"]
        self.difficulty_name = difficulty["name"]
        self.grow_pending = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update_direction(self, new_direction):
        """Queue the next direction change to prevent 180-degree turns"""
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.next_direction = new_direction
    
    def update(self):
        """Update snake position and check for collisions"""
        # Update direction at the start of each move
        self.direction = self.next_direction
        
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % GRID_WIDTH
        new_y = (head_y + dir_y) % GRID_HEIGHT
        
        # Check if snake hits itself
        if (new_x, new_y) in self.positions[1:]:
            return False  # Game over
        
        # Move snake
        self.positions.insert(0, (new_x, new_y))
        
        # Handle growth
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            if len(self.positions) > self.length:
                self.positions.pop()
        
        return True  # Game continues
    
    def grow(self):
        self.length += 1
        self.score += 10 * self.score_multiplier
        self.grow_pending += 1  # Delay the actual growth until next move
    
    def draw(self, surface):
        for i, (x, y) in enumerate(self.positions):
            # Gradient color from head (bright green) to tail (dark green)
            color_factor = max(0.3, 1.0 - (i / (self.length * 1.5)))
            color = (0, int(255 * color_factor), 0)
            
            # Head is a different color
            if i == 0:
                color = (0, 255, 0)  # Bright green head
                # Draw eyes
                eye_size = GRID_SIZE // 5
                if self.direction == RIGHT:
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + GRID_SIZE - eye_size*2, y * GRID_SIZE + eye_size*2), eye_size)
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + GRID_SIZE - eye_size*2, y * GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
                elif self.direction == LEFT:
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + eye_size*2, y * GRID_SIZE + eye_size*2), eye_size)
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + eye_size*2, y * GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
                elif self.direction == UP:
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + eye_size*2, y * GRID_SIZE + eye_size*2), eye_size)
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + GRID_SIZE - eye_size*2, y * GRID_SIZE + eye_size*2), eye_size)
                elif self.direction == DOWN:
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + eye_size*2, y * GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
                    pygame.draw.circle(surface, BLACK, (x * GRID_SIZE + GRID_SIZE - eye_size*2, y * GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
            
            pygame.draw.rect(surface, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        self.spawn_time = time.time()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.spawn_time = time.time()
    
    def draw(self, surface):
        x, y = self.position
        # Make food pulse for visual effect
        pulse = int((time.time() - self.spawn_time) * 5) % 2
        size = GRID_SIZE - (pulse * 4)
        offset = (GRID_SIZE - size) // 2
        
        pygame.draw.rect(surface, self.color, 
                        (x * GRID_SIZE + offset, y * GRID_SIZE + offset, size, size))
        pygame.draw.rect(surface, BLACK, 
                        (x * GRID_SIZE + offset, y * GRID_SIZE + offset, size, size), 1)


def main():
    snake_icon = pygame.image.load("snake_icon.jpg") 
    pygame.display.set_icon(snake_icon)
    """Main game loop"""
    # Get player name at the start
    player_name = get_player_name()
    if player_name is None:
        return
    
    # Select difficulty
    difficulty = select_difficulty()
    if difficulty is None:
        return
    
    # Game loop with restart capability
    while True:
        snake = Snake(difficulty)
        food = Food()
        game_active = True
        last_update_time = time.time()
        update_interval = 1.0 / difficulty["fps"]
        
        # Main game loop
        while game_active:
            current_time = time.time()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.update_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.update_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.update_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.update_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        game_active = False
            
            # Update game state at fixed intervals
            if current_time - last_update_time >= update_interval:
                last_update_time = current_time
                game_active = snake.update()
                
                # Check for food collision
                if snake.get_head_position() == food.position:
                    snake.grow()
                    food.randomize_position()
                    while food.position in snake.positions:
                        food.randomize_position()
                
                # Adjust speed based on length (cap at 2x base speed)
                update_interval = max(1.0 / (difficulty["fps"] * 2), 
                                     1.0 / (difficulty["fps"] + snake.length // 3))
            
            # Drawing
            screen.fill(BLACK)
            draw_grid()
            snake.draw(screen)
            food.draw(screen)
            
            # Display game info with better formatting
            font = pygame.font.SysFont('arial', 20)
            info_lines = [
                f"Score: {snake.score}"
            ]
            
            for i, line in enumerate(info_lines):
                text = font.render(line, True, WHITE)
                screen.blit(text, (10, 10 + i * 25))
            
            pygame.display.flip()
            clock.tick(60)  # Cap at 60 FPS for smoothness
        
        # Game over handling
        action = show_game_over(screen, snake.score, player_name, snake.difficulty_name)
        if action == "quit":
            pygame.quit()
            return
        elif action == "restart":
            continue  # Will restart the game loop

if __name__ == "__main__":
    main()
    pygame.quit()