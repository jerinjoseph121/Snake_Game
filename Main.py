import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

snake_size = 25
snake_pos = [(WIDTH/2)-(snake_size/2), (HEIGHT/2)-(snake_size/2)]
snake_body = [snake_pos]

food_size = 25
food_pos = [random.randint(0, WIDTH-food_size), random.randint(0, HEIGHT-food_size)]

SPEED = 5

score = 0

myFont = pygame.font.SysFont('Comic Sans MS', 40)
newFont = pygame.font.SysFont('Comic Sans MS', 20)

directions = ['UP']
turns = []

BACKGROUND_COLOR = (0, 0, 0)

clock = pygame.time.Clock()

game_over = False

def snake_collision(snake_body, directions):
    for snake_pos in snake_body:
        s_x = snake_pos[0]
        s_y = snake_pos[1]
        if snake_pos != snake_body[0]:
            if directions[0] == 'UP':
                if ((snake_body[0][0]>=s_x) and (snake_body[0][0]<(s_x+snake_size))) or ((s_x>=snake_body[0][0]) and (s_x<(snake_body[0][0]+snake_size))):
                    if ((snake_body[0][1]>=s_y) and (snake_body[0][1]<(s_y+snake_size))):
                        return True
            elif directions[0] == 'DOWN':
                if ((snake_body[0][0]>=s_x) and (snake_body[0][0]<(s_x+snake_size))) or ((s_x>=snake_body[0][0]) and (s_x<(snake_body[0][0]+snake_size))):
                    if (((snake_body[0][1]+snake_size)>=s_y) and ((snake_body[0][1]+snake_size)<(s_y+snake_size))):
                        return True
            elif directions[0] == 'LEFT':
                if ((snake_body[0][0]>=s_x) and (snake_body[0][0]<(s_x+snake_size))):
                    if ((snake_body[0][1]>=s_y) and (snake_body[0][1]<(s_y+snake_size))) or ((s_y>=snake_body[0][1]) and (s_y<(snake_body[0][1]+snake_size))):
                        return True
            elif directions[0] == 'RIGHT':
                if (((snake_body[0][0]+snake_size)>=s_x) and ((snake_body[0][0]+snake_size)<(s_x+snake_size))):
                    if ((snake_body[0][1]>=s_y) and (snake_body[0][1]<(s_y+snake_size))) or ((s_y>=snake_body[0][1]) and (s_y<(snake_body[0][1]+snake_size))):
                        return True
    return False

def snake_turn(turns, snake_body, directions):
    for idx, snake_pos in enumerate(snake_body):
        for index, turn in enumerate(turns):
            if snake_pos == turn[0]:
                directions[idx] = turn[1]
    if turns and (snake_body[len(snake_body) - 1] == turns[0][0]):
        del turns[0]

def body_increase(snake_body, directions):
    for idx, snake_pos in enumerate(snake_body):
        last_pos = snake_pos
        index = idx
    s_x = last_pos[0]
    s_y = last_pos[1]
    if directions[index] == 'UP':
        snake_body.append([s_x, s_y + snake_size])
        directions.append('UP')
    elif directions[index] == 'DOWN':
        snake_body.append([s_x, s_y - snake_size])
        directions.append('DOWN')
    elif directions[index] == 'LEFT':
        snake_body.append([s_x + snake_size, s_y])
        directions.append('LEFT')
    elif directions[index] == 'RIGHT':
        snake_body.append([s_x - snake_size, s_y])
        directions.append('RIGHT')

def snake_movement(snake_body, directions, SPEED):
    for idx, snake_pos in enumerate(snake_body):
        s_x = snake_pos[0]
        s_y = snake_pos[1]
        if directions[idx] == 'UP':
            s_y -= SPEED
        elif directions[idx] == 'DOWN':
            s_y += SPEED
        elif directions[idx] == 'LEFT':
            s_x -= SPEED
        elif directions[idx] == 'RIGHT':
            s_x += SPEED
        snake_body[idx] = [s_x, s_y]

def food_collision(snake_pos, food_pos):
    s_x = snake_pos[0]
    s_y = snake_pos[1]
    f_x = food_pos[0]
    f_y = food_pos[1]
    if (s_x >= f_x and s_x < (f_x + food_size)) or (f_x >= s_x and f_x < (s_x + snake_size)):
        if (s_y >= f_y and s_y < (f_y + food_size)) or (f_y >= s_y and f_y < (s_y + snake_size)):
            return True
    return False

while True:

    if not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and (directions[0] == 'LEFT' or directions[0] == 'RIGHT'):
                    directions[0] = 'UP'
                elif event.key == pygame.K_s and (directions[0] == 'LEFT' or directions[0] == 'RIGHT'):
                    directions[0] = 'DOWN'
                elif event.key == pygame.K_a and (directions[0] == 'UP' or directions[0] == 'DOWN'):
                    directions[0] = 'LEFT'
                elif event.key == pygame.K_d and (directions[0] == 'UP' or directions[0] == 'DOWN'):
                    directions[0] = 'RIGHT'
                if len(snake_body) > 1:
                    turns.append([snake_body[0], directions[0]])

        snake_movement(snake_body, directions, SPEED)
        snake_turn(turns, snake_body, directions)

        screen.fill(BACKGROUND_COLOR)

        for snake_pos in snake_body:
            pygame.draw.rect(screen, RED, (snake_pos[0], snake_pos[1], snake_size, snake_size))

        pygame.draw.rect(screen, YELLOW, (food_pos[0], food_pos[1], food_size, food_size))

        if snake_collision(snake_body, directions):
            game_over = True

        if food_collision(snake_body[0], food_pos):
            score += 1
            food_pos[0] = random.randint(0, WIDTH-food_size)
            food_pos[1] = random.randint(0, HEIGHT-food_size)
            body_increase(snake_body, directions)

        score_text = 'Score:' + str(score)
        score_label = myFont.render(score_text, 1, BLUE)

        screen.blit(score_label, (10, 10))

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    del snake_body[0:len(snake_body)]
                    del directions[0:len(directions)]
                    del turns[0:len(turns)]
                    food_pos = [random.randint(0, WIDTH-food_size), random.randint(0, HEIGHT-food_size)]
                    snake_pos = [(WIDTH/2)-(snake_size/2), (HEIGHT/2)-(snake_size/2)]
                    snake_body = [snake_pos]
                    directions = ['UP']
                    score = 0
                    game_over = False
        end_text = 'Game Over'
        end_label = myFont.render(end_text, 1, ORANGE)

        end_score_text = 'Score:' + str(score)
        end_score_label = myFont.render(end_score_text, 1, ORANGE)

        continue_text = 'Press enter key to continue'
        continue_label = newFont.render(continue_text, 1, (124, 105, 45))

        screen.blit(end_label, (200, 200))
        screen.blit(end_score_label, (225, 250))
        screen.blit(continue_label, (175, 300))

    pygame.display.update()

    clock.tick(30)