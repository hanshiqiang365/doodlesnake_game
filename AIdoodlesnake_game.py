#author: hanshiqiang365 （微信公众号）
import random
import pygame
import sys
import time
from pygame.locals import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SIZE = 20
LINE_WIDTH = 1

SCOPE_X = int(SCREEN_WIDTH/SIZE)
SCOPE_Y = int(SCREEN_HEIGHT/SIZE)

FOOD_STYLE_LIST = [(10, (20, 120, 20)), (20, (255, 20, 20)), (30, (20, 20, 120))]
GAME_W = int(SCREEN_WIDTH/SIZE)

FIELD_SIZE = SCOPE_X * SCOPE_Y
BGCOLOR = (20, 120, 20)
BLACK = (0, 0, 0) 
FOOD = 0
FREE_PLACE = (SCOPE_X+1) * (SCOPE_Y+1)
SNAKE_PLACE = 2 * FREE_PLACE

ERR = -404

Display_Clock = 17
Head_index = 0
best_move = ERR
move_directions = {
        'left': -1,
        'right': 1,
        'up': -GAME_W,
        'down': GAME_W
        }

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
        imgText = font.render(text, True, fcolor)
        screen.blit(imgText, (x, y))

def close_game():
        pygame.quit()
        sys.exit()

def check_pressKey():
	if len(pygame.event.get(QUIT)) > 0:
		close_game()
	KeyUp_Events = pygame.event.get(KEYUP)
	if len(KeyUp_Events) == 0:
		return None
	elif KeyUp_Events[0].key == K_ESCAPE:
		close_game()
	return KeyUp_Events[0].key

def get_foodlocation(snake_Coords):
	flag = True
	while flag:
                food_location = {'x': random.randint(0, SCOPE_X-1), 'y': random.randint(2, SCOPE_Y-1)}
                if food_location not in snake_Coords:
                        flag = False
	return food_location

def create_food(coord):
	x = coord['x'] * SIZE
	y = coord['y'] * SIZE
	food_Rect = pygame.Rect(x, y, SIZE, SIZE)
	pygame.draw.rect(screen, FOOD_STYLE_LIST[random.randint(0, 2)][1], food_Rect)

def init_snake(coords):
	x = coords[0]['x'] * SIZE
	y = coords[0]['y'] * SIZE
	Snake_head_Rect = pygame.Rect(x, y, SIZE, SIZE)
	pygame.draw.rect(screen, (0, 80, 255), Snake_head_Rect)
	Snake_head_Inner_Rect = pygame.Rect(x+4, y+4, SIZE-8, SIZE-8)
	pygame.draw.rect(screen, (0, 80, 255), Snake_head_Inner_Rect)
	for coord in coords[1:]:
		x = coord['x'] * SIZE
		y = coord['y'] * SIZE
		Snake_part_Rect = pygame.Rect(x, y, SIZE, SIZE)
		pygame.draw.rect(screen, (0, 155, 0), Snake_part_Rect)
		Snake_part_Inner_Rect = pygame.Rect(x+4, y+4, SIZE-8, SIZE-8)
		pygame.draw.rect(screen, (0, 255, 0), Snake_part_Inner_Rect)

def game_start():
	title_Font = pygame.font.SysFont('SimHei', 120) 
	title_content = title_Font.render('AI贪吃蛇', True, (255, 255, 255), (20, 120, 20))
	angle = 0
	while True:
		screen.fill(BLACK)
		rotated_title = pygame.transform.rotate(title_content, angle)
		rotated_title_Rect = rotated_title.get_rect()
		rotated_title_Rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
		screen.blit(rotated_title, rotated_title_Rect)
		pressKey_content = game_font.render('Press any Key to start the AI Doodle Snake Game!', True, (180, 180, 180))
		pressKey_Rect = pressKey_content.get_rect()
		pressKey_Rect.topleft = (SCREEN_WIDTH-600, SCREEN_HEIGHT-30)
		screen.blit(pressKey_content, pressKey_Rect)
		if check_pressKey():
			pygame.event.get()
			return
		pygame.display.update()
		game_clock.tick(Display_Clock)
		angle -= 5

def game_over():
	title_Font = pygame.font.SysFont('SimHei', 120) 
	title_gameover = title_Font.render('Game Over', True, (255, 0, 0))
	gameover_Rect = title_gameover.get_rect()
	gameover_Rect.midtop = (SCREEN_WIDTH/2, 120)
	screen.blit(title_gameover, gameover_Rect)

	gameauthor_line1 = game_font.render('韩思工作室出品 ', True, (20, 20, 255))
	gameauthor_line1_Rect = gameauthor_line1.get_rect()
	gameauthor_line1_Rect.midtop = (SCREEN_WIDTH/2, 350)
	screen.blit(gameauthor_line1, gameauthor_line1_Rect)
	gameauthor_line2 = game_font.render('（微信公众号：hanshiqiang365）', True, (20, 20, 255))
	gameauthor_line2_Rect = gameauthor_line2.get_rect()
	gameauthor_line2_Rect.midtop = (SCREEN_WIDTH/2, 390)
	screen.blit(gameauthor_line2, gameauthor_line2_Rect)
	
	pygame.display.update()
	pygame.time.wait(500)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				close_game()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					close_game()

def is_freecell(idx, psnake):
	location_x = idx % GAME_W
	location_y = idx // GAME_W
	idx = {'x': location_x, 'y': location_y}
	return (idx not in psnake)

def board_reset(psnake, pboard, pfood):
	temp_board = pboard[:]
	pfood_idx = pfood['x'] + pfood['y'] * GAME_W
	for i in range(FIELD_SIZE):
		if i == pfood_idx:
			temp_board[i] = FOOD
		elif is_freecell(i, psnake):
			temp_board[i] = FREE_PLACE
		else:
			temp_board[i] = SNAKE_PLACE
	return temp_board

def is_movepossible(idx, move_direction):
	flag = False
	if move_direction == 'left':
		if idx%GAME_W > 0:
			flag = True
		else:
			flag = False
	elif move_direction == 'right':
		if idx%GAME_W < (GAME_W-1):
			flag = True
		else:
                        flag = False
	elif move_direction == 'up':
                if idx > (3 * GAME_W - 1):
                        flag = True
                else:
                        flag = False
	elif move_direction == 'down':
		if idx < (FIELD_SIZE - GAME_W):
			flag = True
		else:
			flag = False
	return flag

def board_refresh(psnake, pfood, pboard):
	temp_board = pboard[:]
	pfood_idx = pfood['x'] + pfood['y'] * GAME_W
	queue = []
	queue.append(pfood_idx)
	inqueue = [0] * FIELD_SIZE
	found = False
	while len(queue) != 0:
		idx = queue.pop(0)
		if inqueue[idx] == 1:
			continue
		inqueue[idx] = 1
		for move_direction in ['left', 'right', 'up', 'down']:
			if is_movepossible(idx, move_direction):
				if (idx+move_directions[move_direction]) == (psnake[Head_index]['x'] + psnake[Head_index]['y']*GAME_W):
					found = True
				if temp_board[idx+move_directions[move_direction]] < SNAKE_PLACE:
					if temp_board[idx+move_directions[move_direction]] > temp_board[idx]+1:
						temp_board[idx+move_directions[move_direction]] = temp_board[idx] + 1
					if inqueue[idx+move_directions[move_direction]] == 0:
						queue.append(idx+move_directions[move_direction])
	return (found, temp_board)

def find_snakehead(snake_Coords, direction):
	if direction == 'up':
		newHead = {'x': snake_Coords[Head_index]['x'],
				   'y': snake_Coords[Head_index]['y']-1}
	elif direction == 'down':
		newHead = {'x': snake_Coords[Head_index]['x'],
				   'y': snake_Coords[Head_index]['y']+1}
	elif direction == 'left':
		newHead = {'x': snake_Coords[Head_index]['x']-1,
				   'y': snake_Coords[Head_index]['y']}
	elif direction == 'right':
		newHead = {'x': snake_Coords[Head_index]['x']+1,
				   'y': snake_Coords[Head_index]['y']}
	return newHead

def virtual_move(psnake, pboard, pfood):
	temp_snake = psnake[:]
	temp_board = pboard[:]
	reset_tboard = board_reset(temp_snake, temp_board, pfood)
	temp_board = reset_tboard
	food_eated = False
	while not food_eated:
		refresh_tboard = board_refresh(temp_snake, pfood, temp_board)[1]
		temp_board = refresh_tboard
		move_direction = choose_shortestsafemove(temp_snake, temp_board)
		snake_Coords = temp_snake[:]
		temp_snake.insert(0, find_snakehead(snake_Coords, move_direction))
		if temp_snake[Head_index] == pfood:
			reset_tboard = board_reset(temp_snake, temp_board, pfood)
			temp_board = reset_tboard
			pfood_idx = pfood['x'] + pfood['y'] * GAME_W
			temp_board[pfood_idx] = SNAKE_PLACE
			food_eated = True
		else:
			newHead_idx = temp_snake[0]['x'] + temp_snake[0]['y'] * GAME_W
			temp_board[newHead_idx] = SNAKE_PLACE
			end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y'] * GAME_W
			temp_board[end_idx] = FREE_PLACE
			del temp_snake[-1]
	return temp_snake, temp_board

def is_tailinside(psnake, pboard, pfood):
	temp_board = pboard[:]
	temp_snake = psnake[:]

	end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y'] * GAME_W
	temp_board[end_idx] = FOOD
	v_food = temp_snake[-1]
	
	pfood_idx = pfood['x'] + pfood['y'] * GAME_W
	temp_board[pfood_idx] = SNAKE_PLACE
	
	result, refresh_tboard = board_refresh(temp_snake, v_food, temp_board)
	temp_board = refresh_tboard
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = temp_snake[Head_index]['x'] + temp_snake[Head_index]['y']*GAME_W
		end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y']*GAME_W
		if is_movepossible(idx, move_direction) and (idx+move_directions[move_direction] == end_idx) and (len(temp_snake)>3):
			result = False
	return result

def choose_shortestsafemove(psnake, pboard):
	best_move = ERR
	min_distance = SNAKE_PLACE
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = psnake[Head_index]['x'] + psnake[Head_index]['y']*GAME_W
		if is_movepossible(idx, move_direction) and (pboard[idx+move_directions[move_direction]]<min_distance):
			min_distance = pboard[idx+move_directions[move_direction]]
			best_move = move_direction
	return best_move

def choose_longestsafemove(psnake, pboard):
	best_move = ERR
	max_distance = -1
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = psnake[Head_index]['x'] + psnake[Head_index]['y']*GAME_W
		if is_movepossible(idx, move_direction) and (pboard[idx+move_directions[move_direction]]>max_distance) and (pboard[idx+move_directions[move_direction]]<FREE_PLACE):
			max_distance = pboard[idx+move_directions[move_direction]]
			best_move = move_direction
	return best_move 

def follow_tail(psnake, pboard, pfood):
	temp_snake = psnake[:]
	temp_board = board_reset(temp_snake, pboard, pfood)
	
	end_idx = temp_snake[-1]['x'] + temp_snake[-1]['y'] * GAME_W
	temp_board[end_idx] = FOOD
	v_food = temp_snake[-1]

	pfood_idx = pfood['x'] + pfood['y'] * GAME_W
	temp_board[pfood_idx] = SNAKE_PLACE

	result, refresh_tboard = board_refresh(temp_snake, v_food, temp_board)
	temp_board = refresh_tboard
	
	temp_board[end_idx] = SNAKE_PLACE
	
	return choose_longestsafemove(temp_snake, temp_board)

def find_safeway(psnake, pboard, pfood):
	safe_move = ERR
	real_snake = psnake[:]
	real_board = pboard[:]
	v_psnake, v_pboard = virtual_move(psnake, pboard, pfood)
	if is_tailinside(v_psnake, v_pboard, pfood):
		safe_move = choose_shortestsafemove(real_snake, real_board)
	else:
		safe_move = follow_tail(real_snake, real_board, pfood)
	return safe_move

def anypossible_move(psnake, pboard, pfood):
	best_move = ERR
	reset_board = board_reset(psnake, pboard, pfood)
	pboard = reset_board
	result, refresh_board = board_refresh(psnake, pfood, pboard)
	pboard = refresh_board
	min_distance = SNAKE_PLACE
	for move_direction in ['left', 'right', 'up', 'down']:
		idx = psnake[Head_index]['x'] + psnake[Head_index]['y']*GAME_W
		if is_movepossible(idx, move_direction) and (pboard[idx+move_directions[move_direction]]<min_distance):
			min_distance = pboard[idx+move_directions[move_direction]]
			best_move = move_direction
	return best_move

def game_play():
	board = [0] * FIELD_SIZE
	start_x = random.randint(5, SCOPE_X-6)
	start_y = random.randint(5, SCOPE_Y-6)
	snake_Coords = [{'x': start_x, 'y': start_y},
					{'x': start_x-1, 'y': start_y},
					{'x': start_x-2, 'y': start_y}]
	food_location = get_foodlocation(snake_Coords)
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				close_game()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					close_game()

		screen.fill(BGCOLOR)
		for x in range(SIZE, SCREEN_WIDTH, SIZE):
                        pygame.draw.line(screen, BLACK, (x, 2 * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)
		for y in range(2 * SIZE, SCREEN_HEIGHT, SIZE):
			pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

		init_snake(snake_Coords)
		create_food(food_location)
		score = len(snake_Coords)-3
		game_runtime = round(time.time() - game_starttime)
		print_text(screen, game_font, 30, 7, f'进度: {round(score//9.2)}%')
		print_text(screen, game_font, 330, 7, f'计时: {round(game_runtime // 3600)}:{round((game_runtime % 3600) // 60)}:{round((game_runtime % 3600) % 60)}')
		print_text(screen, game_font, 680, 7, f'得分: {score}')
		
		reset_board = board_reset(snake_Coords, board, food_location)
		board = reset_board
		result, refresh_board = board_refresh(snake_Coords, food_location, board)
		board = refresh_board
		if result:
			best_move = find_safeway(snake_Coords, board, food_location)
		else:
			best_move = follow_tail(snake_Coords, board, food_location)
		if best_move == ERR:
			best_move = anypossible_move(snake_Coords, board, food_location)
		if best_move != ERR:
			newHead = find_snakehead(snake_Coords, best_move)
			snake_Coords.insert(0, newHead)
			head_idx = snake_Coords[Head_index]['x'] + snake_Coords[Head_index]['y']*GAME_W
			end_idx = snake_Coords[-1]['x'] + snake_Coords[-1]['y']*GAME_W
			if (snake_Coords[Head_index]['x'] == food_location['x']) and (snake_Coords[Head_index]['y'] == food_location['y']):
				board[head_idx] = SNAKE_PLACE
				if len(snake_Coords) < FIELD_SIZE:
					food_location = get_foodlocation(snake_Coords)
			else:
				board[head_idx] = SNAKE_PLACE
				board[end_idx] = FREE_PLACE
				del snake_Coords[-1]
		else:
			return

		pygame.display.update()
		game_clock.tick(Display_Clock)

def main():
        global screen, game_font, game_clock, game_starttime
        pygame.init()

        gameIcon = pygame.image.load("snake.png")
        pygame.display.set_icon(gameIcon)

        pygame.mixer.init()
        pygame.mixer.music.load("bgm.wav")
        pygame.mixer.music.play(-1)

        game_font = pygame.font.SysFont('SimHei', 24)
        pygame.display.set_caption('AI Doodle Snake Game - Developed by hanshiqiang365 (wechat public account)')

        game_clock = pygame.time.Clock()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        game_starttime = time.time()

        game_start()
        while True:
                game_play()
                game_over()
		
if __name__ == '__main__':
	main()
