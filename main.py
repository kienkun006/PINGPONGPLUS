#PINGPONG GAME PLUS BY TEAM 9 - ANH TRAI C2
import pygame
import sys
import random


# Khởi tạo pygame (Trang)
pygame.init()

screen_width = 1300
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong PLUS+- NHÓM 9")

background_image = pygame.image.load("background/football_background.jpg.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
menu_background = pygame.image.load("background/nenmenu.png")
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))

def play_background_music():
    pygame.mixer.music.load("Last Pích Cà Pô Xmas - Đì Va Quanh Ta (youtube).mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

play_background_music()

# Thanh trượt (Việt Anh)
white = (255, 255, 255)
paddle_width = 20
paddle_height = 110
paddle1_y = screen_height / 2 - paddle_height / 2
paddle2_y = screen_height / 2 - paddle_height / 2
paddle_speed = 7

# Hàm vẽ thanh trượt
def draw_paddles():
    pygame.draw.rect(screen, white, (0, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, white, (screen_width - paddle_width, paddle2_y, paddle_width, paddle_height))



# Bóng (Trường)
ball_radius = 17
balls = [{"x": screen_width / 2, "y": screen_height / 2, "speed_x": 5, "speed_y": 5, "color": (255, 0, 0)}]

def move_balls():
    global balls
    for ball in balls:
        ball["x"] += ball["speed_x"]
        ball["y"] += ball["speed_y"]

        if ball["y"] - ball_radius < 0 or ball["y"] + ball_radius > screen_height:
            ball["speed_y"] = -ball["speed_y"]

        if (ball["x"] - ball_radius < paddle_width and paddle1_y < ball["y"] < paddle1_y + paddle_height) or \
           (ball["x"] + ball_radius > screen_width - paddle_width and paddle2_y < ball["y"] < paddle2_y + paddle_height):
            ball["speed_x"] = -ball["speed_x"]

def draw_balls():
    for ball in balls:
        pygame.draw.circle(screen, ball["color"], (int(ball["x"]), int(ball["y"])), ball_radius)

def reset_ball():
    global balls
    balls = [{"x": screen_width / 2, "y": screen_height / 2, "speed_x": 5, "speed_y": 5, "color": (255, 0, 0)}]  # Đặt lại danh sách bóng

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

last_ball_added = 0


#Tuyên
score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)


def update_score():
    global balls, score1, score2
    for ball in balls[:]:
        if ball["x"] < 0:
            score2 += 1
            balls.remove(ball)
        elif ball["x"] > screen_width:
            score1 += 1
            balls.remove(ball)


def draw_score():
    player1_text = font.render(f"{player1_name}: {score1}", True, white)
    player2_text = font.render(f"{player2_name}: {score2}", True, white)
    screen.blit(player1_text, (screen_width / 4 - player1_text.get_width() / 2, 20))
    screen.blit(player2_text, (screen_width * 3 / 4 - player2_text.get_width() / 2, 20))

# Thời gian
start_time = pygame.time.get_ticks()
time_font = pygame.font.Font(None, 50)

clock = pygame.time.Clock()

def draw_time():
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    time_text = f"Time: {minutes:02}:{seconds:02}"
    time_surface = time_font.render(time_text, True, white)
    screen.blit(time_surface, (screen_width / 2 - 60, 20))


#CẬP NHẬT MỚI
    player1_name = ""
    player2_name = ""

# Thêm biến xác định chế độ chơi
   # Hàm nhập tên người chơi
def enter_player_names():
    global player1_name, player2_name

    player1_name = ""
    player2_name = ""
    active_player = 1  # Bắt đầu với Player 1

    while True:
        screen.fill((0, 0, 0))  # Làm sạch màn hình
        font = pygame.font.Font(None, 74)

        # Hiển thị hướng dẫn nhập tên
        if active_player == 1:
            instruction = font.render("Enter Player 1 Name:", True, (255, 255, 255))
        else:
            instruction = font.render("Enter Player 2 Name:", True, (255, 255, 255))
        screen.blit(instruction, (screen_width / 2 - instruction.get_width() / 2, 200))

        # Hiển thị tên đã nhập
        if active_player == 1:
            name_surface = font.render(player1_name, True, (255, 255, 255))
        else:
            name_surface = font.render(player2_name, True, (255, 255, 255))
        screen.blit(name_surface, (screen_width / 2 - name_surface.get_width() / 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Nhấn Enter để chuyển sang người chơi tiếp theo
                    if active_player == 1:
                        active_player = 2
                    else:
                        return  # Kết thúc nhập tên
                elif event.key == pygame.K_BACKSPACE:  # Xóa ký tự cuối
                    if active_player == 1:
                        player1_name = player1_name[:-1]
                    else:
                        player2_name = player2_name[:-1]
                else:  # Thêm ký tự vào tên
                    if active_player == 1:
                        player1_name += event.unicode
                    else:
                        player2_name += event.unicode


play_with_ai = True  # True: chơi với máy, False: chơi 2 người
ai_speed = 5  # Tốc độ di chuyển của AI

def display_mode_selection():
    global play_with_ai
    while True:
        screen.blit(menu_background, (0, 0))
        title_font = pygame.font.Font(None, 80) #font chữ lớn
        option_font = pygame.font.Font(None, 50) #font chữ nhỏ
        white = (255, 255, 255)

        title = title_font.render("PING PONG PLUS", True, white)
        screen.blit(title, (screen_width / 2 - title.get_width() / 2, 150))

        single_player = option_font.render("1: PLAY WITH MACHINE", True, white)
        multiplayer = option_font.render("2: 2-PLAYERS", True, white)
        screen.blit(single_player, (screen_width / 2 - single_player.get_width() / 2, 300))
        screen.blit(multiplayer, (screen_width / 2 - multiplayer.get_width() / 2, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Nhấn phím 1
                    play_with_ai = True
                    return
                elif event.key == pygame.K_2:  # Nhấn phím 2
                    play_with_ai = False
                    enter_player_names()  # Gọi hàm nhập tên
                    return



#Viet Anh

def handle_ai_movement():
    global paddle2_y
    if balls[0]["y"] > paddle2_y + paddle_height / 2 and paddle2_y < screen_height - paddle_height:
        paddle2_y += ai_speed

    elif balls[0]["y"] < paddle2_y + paddle_height / 2 and paddle2_y > 0:
        paddle2_y -= ai_speed

# Cập nhật hàm điều khiển thanh trượt
def handle_paddle_movement(keys):
    global paddle1_y, paddle2_y
    # Điều khiển người chơi 1
    if keys[pygame.K_w] and paddle1_y > 0:
        paddle1_y -= paddle_speed
    if keys[pygame.K_s] and paddle1_y < screen_height - paddle_height:
        paddle1_y += paddle_speed

    # Điều khiển người chơi 2 hoặc AI
    if not play_with_ai:  # Nếu chơi 2 người
        if keys[pygame.K_UP] and paddle2_y > 0:
            paddle2_y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2_y < screen_height - paddle_height:
            paddle2_y += paddle_speed
    else:  # Nếu chơi với AI
        handle_ai_movement()


#WINNER (Trang)
game_over = False

player1_name = ""
player2_name = ""

def check_winner():
    global game_over
    if score1 == 10:
        display_winner(player1_name)
        game_over = True
    elif score2 == 10:
        display_winner(player2_name if not play_with_ai else "AI")
        game_over = True


def display_winner(winner):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render(f"WINNER: {winner}!", True, (255, 255, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))
    pygame.display.flip()
    pygame.time.wait(3000)



display_mode_selection() # Hiển thị menu lựa chọn chế độ chơi trước khi vào trò chơi chính.

# Vòng lặp chính (Kiên)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score1, score2 = 0, 0
            reset_ball()
            game_over = False
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        continue

    keys = pygame.key.get_pressed()
    handle_paddle_movement(keys)
    move_balls()
    update_score()
    check_winner()

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    if elapsed_time // 30 > last_ball_added:
        balls.append({
            "x": screen_width / 2,
            "y": screen_height / 2,
            "speed_x": 5,
            "speed_y": 5,
            "color": random_color()
        })
        last_ball_added = elapsed_time // 30

    if not balls:
        reset_ball()

    screen.blit(background_image, (0, 0))
    draw_paddles()
    draw_balls()
    draw_score()
    draw_time()

    pygame.display.flip()
    clock.tick(60)


