import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
pink = (255, 105, 180)

# Initialize screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Clock and font
clock = pygame.time.Clock()
snake_block = 5
cat_size = 70
snake_speed = 60  # Render FPS
# Move one full cell per step to keep body positions stable.
move_speed = cat_size
move_interval_ms = 170  # Lower = faster snake
font_style = pygame.font.SysFont("bahnschrift", 25)
end_font_style = pygame.font.SysFont("comicsansms", 30, bold=True)
win_font_style = pygame.font.SysFont("comicsansms", 48, bold=True)
menu_font_style = pygame.font.SysFont("comicsansms", 42, bold=True)
menu_info_font = pygame.font.SysFont("comicsansms", 30, bold=True)
score_font = pygame.font.SysFont("LOVEDAYS-2V7OE.TTF", 35)

# Load images from the repo assets directory
base_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(base_dir, "assets")
cat_image = pygame.image.load(os.path.join(assets_dir, "pink_cat.png"))
cat_image = pygame.transform.scale(cat_image, (cat_size, cat_size))

# Load the mouse image for food
mouse_image = pygame.image.load(os.path.join(assets_dir, "mouse_pink.png"))
mouse_image = pygame.transform.scale(mouse_image, (cat_size // 2, cat_size // 2))

def create_background_surface():
    bg = pygame.Surface((width, height))
    cx = width / 2
    cy = height / 2
    for y in range(height):
        for x in range(width):
            # Rectangular vignette to mimic soft pink edges and light center.
            dx = abs((x - cx) / cx)
            dy = abs((y - cy) / cy)
            edge = max(dx, dy)
            t = min(1.0, edge ** 1.8)
            r = int(248 + (255 - 248) * t)
            g = int(242 + (205 - 242) * t)
            b = int(248 + (224 - 248) * t)
            bg.set_at((x, y), (r, g, b))
    return bg

background_image = create_background_surface()

def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, blue)
    screen.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        # Draw the pink cat image instead of a green rectangle
        screen.blit(cat_image, (x[0], x[1]))

def message(msg, color):
    lines = msg.split("\n")
    line_height = end_font_style.get_linesize() + 6
    start_y = (height // 2) - (line_height * (len(lines) - 1) // 2)
    for i, line in enumerate(lines):
        mesg = end_font_style.render(line, True, color)
        mesg_rect = mesg.get_rect(center=(width // 2, start_y + i * line_height))
        screen.blit(mesg, mesg_rect)

def spawn_food(snake_list):
    # Keep food one full cell away from edges so it is never on borders/corners.
    x_positions = range(cat_size, width - (2 * cat_size) + 1, cat_size)
    y_positions = range(cat_size, height - (2 * cat_size) + 1, cat_size)
    snake_cells = {tuple(seg) for seg in snake_list}
    candidates = [(x, y) for x in x_positions for y in y_positions if (x, y) not in snake_cells]
    if not candidates:
        return cat_size, cat_size
    return random.choice(candidates)

def make_confetti(count):
    colors = [
        (255, 105, 180),
        (255, 182, 193),
        (255, 20, 147),
        (255, 153, 204),
        (255, 240, 245),
    ]
    confetti = []
    for _ in range(count):
        confetti.append({
            "x": random.uniform(0, width),
            "y": random.uniform(-height, 0),
            "size": random.randint(4, 9),
            "speed": random.uniform(1.0, 3.2),
            "drift": random.uniform(-1.2, 1.2),
            "color": random.choice(colors),
            "shape": random.choice(("rect", "circle")),
        })
    return confetti

def update_and_draw_confetti(confetti):
    for piece in confetti:
        piece["y"] += piece["speed"]
        piece["x"] += piece["drift"]
        if piece["y"] > height + 10:
            piece["y"] = random.uniform(-120, -10)
            piece["x"] = random.uniform(0, width)
        if piece["x"] < -10:
            piece["x"] = width + 5
        if piece["x"] > width + 10:
            piece["x"] = -5

        if piece["shape"] == "rect":
            pygame.draw.rect(
                screen,
                piece["color"],
                pygame.Rect(int(piece["x"]), int(piece["y"]), piece["size"], piece["size"] + 2),
            )
        else:
            pygame.draw.circle(
                screen,
                piece["color"],
                (int(piece["x"]), int(piece["y"])),
                max(2, piece["size"] // 2),
            )

def draw_centered_single_line(text, color, base_font, max_width):
    font_size = base_font.get_height()
    font_name = "comicsansms"
    text_surface = pygame.font.SysFont(font_name, font_size, bold=True).render(text, True, color)
    while text_surface.get_width() > max_width and font_size > 18:
        font_size -= 2
        text_surface = pygame.font.SysFont(font_name, font_size, bold=True).render(text, True, color)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(text_surface, text_rect)

def show_start_menu(last_highscore):
    button_width = 320
    button_height = 90
    button_rect = pygame.Rect(
        (width - button_width) // 2,
        (height // 2) - 70,
        button_width,
        button_height,
    )

    while True:
        clock.tick(snake_speed)
        screen.blit(background_image, (0, 0))

        # Button
        pygame.draw.rect(screen, (255, 182, 193), button_rect, border_radius=20)
        pygame.draw.rect(screen, pink, button_rect, 4, border_radius=20)
        label = menu_font_style.render("Start Game", True, (255, 20, 147))
        label_rect = label.get_rect(center=button_rect.center)
        screen.blit(label, label_rect)

        # Last highscore info under the button
        if last_highscore == 20:
            info_text = "Happy Birthday"
        else:
            info_text = "Last highscore: " + str(last_highscore)
        info = menu_info_font.render(info_text, True, pink)
        info_rect = info.get_rect(center=(width // 2, button_rect.bottom + 55))
        screen.blit(info, info_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True
                if event.key == pygame.K_q:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return True

def gameLoop():
    game_over = False
    game_close = False
    game_win = False

    x1 = (width // 2 // cat_size) * cat_size
    y1 = (height // 2 // cat_size) * cat_size

    dir_x = 0
    dir_y = 0
    next_dir_x = 0
    next_dir_y = 0

    snake_list = [[x1, y1]]
    prev_snake_list = [[x1, y1]]
    length_of_snake = 1
    move_accumulator = 0
    confetti = make_confetti(140)

    foodx, foody = spawn_food(snake_list)

    while not game_over:
        dt = clock.tick(snake_speed)

        while game_close:
            clock.tick(snake_speed)
            screen.blit(background_image, (0, 0))
            message("You Lost!\nPress Q to Quit or C to Play Again", pink)
            your_score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return None
                    if event.key == pygame.K_c:
                        return length_of_snake - 1

        while game_win:
            clock.tick(snake_speed)
            screen.blit(background_image, (0, 0))
            update_and_draw_confetti(confetti)
            draw_centered_single_line("Happy 20th Birthday Mia Maus", pink, win_font_style, width - 40)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return None
                    if event.key == pygame.K_c:
                        return 20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dir_x != 1:
                    next_dir_x, next_dir_y = -1, 0
                elif event.key == pygame.K_RIGHT and dir_x != -1:
                    next_dir_x, next_dir_y = 1, 0
                elif event.key == pygame.K_UP and dir_y != 1:
                    next_dir_x, next_dir_y = 0, -1
                elif event.key == pygame.K_DOWN and dir_y != -1:
                    next_dir_x, next_dir_y = 0, 1

        move_accumulator += dt
        while move_accumulator >= move_interval_ms and not game_close:
            move_accumulator -= move_interval_ms
            prev_snake_list = [segment[:] for segment in snake_list]

            dir_x, dir_y = next_dir_x, next_dir_y
            if dir_x == 0 and dir_y == 0:
                break

            x1 += dir_x * move_speed
            y1 += dir_y * move_speed

            if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
                game_close = True
                break

            snake_head = [x1, y1]
            snake_list.append(snake_head)
            if len(snake_list) > length_of_snake:
                del snake_list[0]
            if snake_head in snake_list[:-1]:
                game_close = True
                break

            head_rect = pygame.Rect(x1, y1, cat_size, cat_size)
            food_rect = pygame.Rect(foodx, foody, cat_size // 2, cat_size // 2)
            if head_rect.colliderect(food_rect):
                foodx, foody = spawn_food(snake_list)
                length_of_snake += 1
                if (length_of_snake - 1) >= 20:
                    game_win = True
                    break
                if len(prev_snake_list) < len(snake_list):
                    prev_snake_list.insert(0, prev_snake_list[0][:])

        screen.blit(background_image, (0, 0))
        screen.blit(mouse_image, (foodx, foody))

        alpha = move_accumulator / move_interval_ms if move_interval_ms > 0 else 1
        render_snake = []
        for i, seg in enumerate(snake_list):
            if i < len(prev_snake_list):
                prev_seg = prev_snake_list[i]
            else:
                prev_seg = snake_list[i - 1]
            rx = prev_seg[0] + (seg[0] - prev_seg[0]) * alpha
            ry = prev_seg[1] + (seg[1] - prev_seg[1]) * alpha
            render_snake.append([rx, ry])

        our_snake(snake_block, render_snake)
        your_score(length_of_snake - 1)

        pygame.display.update()

    return length_of_snake - 1

def main():
    last_highscore = 0
    running = True
    while running:
        start = show_start_menu(last_highscore)
        if not start:
            break
        result = gameLoop()
        if result is None:
            break
        if result > last_highscore:
            last_highscore = result

    pygame.quit()
    quit()

main()
