import sys
import pygame


pygame.init()
pygame.mixer.init()


# defining variables

width = 1366
height = 768
cell_width = 120
cell_height = 153
top_offset = 194
left_offset = 505
clicked = False
mouse_pos = []
player = 1
sound_playing = True


# defining boards

board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

graphical_board = [[[None, None], [None, None], [None, None]], 
  [[None, None], [None, None], [None, None]], 
  [[None, None], [None, None], [None, None]]]

# defining the images

background = pygame.image.load("game_files/bg.png")
choice_screen = pygame.image.load("game_files/choice_screen.png")
circle_choice = pygame.image.load("game_files/circle_choice.png")
cross_choice = pygame.image.load("game_files/cross_choice.png")
x_img = pygame.image.load("game_files/cross.png")
o_img = pygame.image.load("game_files/circle.png")
horizontal = pygame.image.load("game_files/horizontal.png")
vertical = pygame.image.load("game_files/vertical.png")
ldiag = pygame.image.load("game_files/ldiag.png")
rdiag = pygame.image.load("game_files/rdiag.png")
player_1_won = pygame.image.load("game_files/player 1 won1.png")
player_2_won = pygame.image.load("game_files/player 2 won1.png")
draw = pygame.image.load("game_files/draw1.png")
play_again = pygame.image.load("game_files/play again button.png")
pause_button = pygame.image.load("game_files/pause_button.png")
pause_screen = pygame.image.load("game_files/pause_screen.png")
quit_button = pygame.image.load("game_files/quit_button.png")
quit_button_2 = pygame.image.load("game_files/quit button.png")
sound_on = pygame.image.load("game_files/sound_on.png")
sound_off = pygame.image.load("game_files/sound_off.png")


# defining required rects 
choice_screen_rect = choice_screen.get_rect(center=(684,415))
circle_choice_rect = circle_choice.get_rect(center=(520,455))
cross_choice_rect = cross_choice.get_rect(center=(865,455))
pause_rect = pause_button.get_rect(center=(1280,50))
pause_screen_rect = pause_screen.get_rect(center=(684,415))
quit_rect = quit_button.get_rect(center=(1280,100))
ldiag_rect = ldiag.get_rect(center=(684,420))
rdiag_rect = rdiag.get_rect(center=(684,420))
player_1_won_rect = player_1_won.get_rect(center=(684,415))
player_2_won_rect = player_2_won.get_rect(center=(684,415))
play_again_rect = play_again.get_rect(center=(565,455))
quit_button_rect = quit_button_2.get_rect(center=(880,455))
draw_rect = draw.get_rect(center=(684,415))
sound_off_rect = sound_off.get_rect(topleft=(1266,668))
sound_on_rect = sound_on.get_rect(topleft=(1266,668))


# loading up the BGM
pygame.mixer.music.load("game_files/abcdefg.mp3")
if sound_playing:
  pygame.mixer.music.play(-1)  # playing the music in an infinite loop (unless stopped later)


# display the background
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("TicTacToe_00X_1")

def background_displaying():        # making it a function for convenience (will come in handy later on)
  screen.fill((255,0,0))
  screen.blit(background,(0,0))

  # displaying everything else
  screen.blit(pause_button,pause_rect)
  screen.blit(quit_button,quit_rect)
  if sound_playing:
    screen.blit(sound_on,sound_on_rect)
  else:
    screen.blit(sound_off,sound_off_rect)
  pygame.display.update()

background_displaying()     # calling it once to initially get everything on screen


# defining functions

def choice():
  global player

  while True:           # looping the entire thing until a valid choice is made
    screen.blit(choice_screen,choice_screen_rect)
    screen.blit(circle_choice,circle_choice_rect)
    screen.blit(cross_choice,cross_choice_rect)
    pygame.display.update()             

    for events in pygame.event.get():
      if events.type == pygame.QUIT:
        sys.exit()
      if events.type == pygame.MOUSEBUTTONDOWN:
        if quit_rect.collidepoint(pygame.mouse.get_pos()):
          sys.exit()
        if circle_choice_rect.collidepoint(pygame.mouse.get_pos()):
          player = -1                     # if circle chosen, then setting -1 to player
          background_displaying()         # re-drawing the initial background (essentially removing the choice dialogbox)
          return
        if cross_choice_rect.collidepoint(pygame.mouse.get_pos()):
          player = 1
          background_displaying()         # if cross chosen, no changes made to player, just re-drawing the background
          return


def draw_board(board,x_img,o_img):

  'this function draws the board'
  
  global graphical_board
  for i in range(3):
    for j in range(3):
      # creating X image in the graphical board
      if board[i][j] == 1:
        graphical_board[i][j][0] = x_img
        graphical_board[i][j][1] = x_img.get_rect(center=(j*120 + 564, i*151 + 269))
      # creating O image in the graphical board
      elif board[i][j] == -1:
        graphical_board[i][j][0] = o_img
        graphical_board[i][j][1] = o_img.get_rect(center=(j*120 + 564, i*151 + 269))

  for i in range(3):
    for j in range(3):
        if graphical_board[i][j][0] is not None:
            screen.blit(graphical_board[i][j][0], graphical_board[i][j][1])
    
def add_XO(board,mouse_pos,player):

  'this function adds X or O to the board'
  
  x_pos = mouse_pos[0]
  y_pos = mouse_pos[1]
    
  adjusted_x_pos = x_pos - left_offset
  adjusted_y_pos = y_pos - top_offset

  row = adjusted_y_pos // cell_height  # Determine the row based on mouse y position
  col = adjusted_x_pos // cell_width    # Determine the column based on mouse x position
  
  if adjusted_x_pos < 0 or adjusted_y_pos < 0 or row >= 3 or col >= 3:
    return  # Ignore clicks outside the grid
  
  if 0 <= row < 3 and 0 <= col < 3:
    if board[row][col] == 0:  # Only place X or O if the cell is empty
        board[row][col] = player
        # calling the draw_board function every time an X or O is added
        draw_board(board,x_img,o_img)
        return player * -1      # after a successful placing, the turn is changed to the other player
  
    return player


def checkWinner(board):
    # Checking rows
    for i in range(3):
      if 0 not in [board[i][0], board[i][1], board[i][2]]:  # All cells in the row are not empty
        if board[i][0] == board[i][1] == board[i][2]:       # If they're not empty, checking if they're equal
          return board[i][0], 'row', i                      # Return the winner, type of line to draw, and the number of row

    # Checking columns
    for i in range(3):
      if 0 not in [board[0][i], board[1][i], board[2][i]]:  # All cells in the column are not empty
        if board[0][i] == board[1][i] == board[2][i]:       # If they're not empty, checking if they're equal
          return board[0][i], 'column', i  # Return the winner, type of line, and the number of column

    # Checking diagonals
    if 0 not in [board[0][0], board[1][1], board[2][2]]:  # Checking the left-to-right diagonal [checking that they're not empty]
      if board[0][0] == board[1][1] == board[2][2]:       # If they're not empty, checking if they're equal
        return board[0][0], 'ldiag', None                 # Return the winner, type of line, and None (for the sake of no. of returns)
    if board[0][2] == board[1][1] == board[2][0] != 0:    # Checking the right-to-left diagonal [checking that they're not empty]
        return board[0][2], 'rdiag', None                 # Return the winner, type of line, and None (for the sake of no. of returns)

    # If no winner, then return nothing
    return 0, None, None


def drawWinningLine(typeofline,no):
  if typeofline == 'row':
    horizontal_rect = horizontal.get_rect(center=(684,(no*153)+267))
    screen.blit(horizontal,horizontal_rect)
  elif typeofline == 'column':
    vertical_rect = vertical.get_rect(center=((no*121)+563,420))
    screen.blit(vertical,vertical_rect)
  elif typeofline == 'ldiag':
    screen.blit(ldiag,ldiag_rect)
  elif typeofline == 'rdiag':
    screen.blit(rdiag,rdiag_rect)
  pygame.display.update()


def checkDraw(board):
  for row in board:
    if 0 in row:
      return False
  return True

def reset_game():
  global board, graphical_board, player, clicked
  board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Reset board
  graphical_board = [[[None, None], [None, None], [None, None]],
                      [[None, None], [None, None], [None, None]],
                      [[None, None], [None, None], [None, None]]]  # Reset graphical board
  player = 1  # Reset to player 1
  clicked = False
  background_displaying()  # Re-display the background
  draw_board(board, x_img, o_img)  # Re-draw the board


# the main game loop
running = True
paused = False 
waiting_for_click = False

choice()    # calling the choice to set the player 1

while running:
  
  # game events loop

  for events in pygame.event.get():

    if events.type == pygame.QUIT:
      running = False       # if the user quits the game the loop is terminated
      sys.exit()

    if events.type == pygame.MOUSEBUTTONDOWN and not clicked:
      clicked = True
    if events.type == pygame.MOUSEBUTTONUP and clicked:
      clicked = False       # this is to ensure that a full click cycle has been completed
      mouse_pos = pygame.mouse.get_pos()
      
      if quit_rect.collidepoint(mouse_pos):
        running = False
        sys.exit()

      if paused:            # checking if paused
        paused = False      # if yes, then setting it back to unpaused
        background_displaying()             # re-drawing the background
        draw_board(board,x_img,o_img)       # re-drawing the last state of the board
        pygame.display.update()             
        continue                            # skipping the rest of the loop

      if pause_rect.collidepoint(mouse_pos):      # checking if pause button is clicked
        paused = True         # if yes, then setting the game to paused
        screen.blit(pause_screen,pause_screen_rect)         # displaying the pause screen
        pygame.display.update()
        continue           # skipping the rest of the code

      if sound_on_rect.collidepoint(mouse_pos):
        if sound_playing:
          sound_playing = False
          background_displaying()
          pygame.mixer.music.stop()
        else:
          sound_playing = True
          background_displaying()
          pygame.mixer.music.play(-1)  # Loops indefinitely
      
      if mouse_pos[0] >= 505 and mouse_pos[0] <= 860:    # checking if the click was within the board, only then will I call the add_XO() function and change the player turn
        
        player = add_XO(board,mouse_pos,player)          # adding X or O based on whose turn it is
        print(graphical_board,board)                     # printing the state of board and graphical_board onto the console (for seeing)
       
        winner = checkWinner(board)
       
        if winner[0] is not 0:
          drawWinningLine(winner[1],winner[2])
       
          if winner[0] == 1:
            screen.blit(player_1_won,player_1_won_rect)         # display the "player 1 has won" dialog box
       
          elif winner[0] == -1:
            screen.blit(player_2_won,player_2_won_rect)         # display the "player 2 has won" dialog box
          
          screen.blit(play_again,play_again_rect)               # displaying the play again button
          screen.blit(quit_button_2,quit_button_rect)           # displaying the quit button
          pygame.display.update()
        
          waiting_for_click = True             

        elif checkDraw(board):
          screen.blit(draw,draw_rect)
          screen.blit(play_again,play_again_rect)
          screen.blit(quit_button_2,quit_button_rect)
          pygame.display.update()
        
          waiting_for_click = True
          
    while waiting_for_click:
      for events in pygame.event.get():
        if events.type == pygame.QUIT:
          running = False      
          sys.exit()
        if events.type == pygame.MOUSEBUTTONDOWN:
          if play_again_rect.collidepoint(pygame.mouse.get_pos()):
            waiting_for_click = False
            reset_game()
          if quit_button_rect.collidepoint(pygame.mouse.get_pos()):
            running = False
            sys.exit()
                    
      
  pygame.display.update() 