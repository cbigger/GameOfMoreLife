import pygame
import random
pygame.init()

def makeGrid(rows, columns):
    return [[0 for _ in range(rows)] for _ in range(columns)]

def updateWin():
    global Size, Matrix, window, width, height
    pixel_size = width / Size
    for i in range(Size):
        for j in range(Size):
            color = (255, 255, 255) if Matrix[i][j] == 0 else (0, 0, 0)
            pygame.draw.rect(window, color, pygame.Rect(pixel_size*i, pixel_size*j, pixel_size, pixel_size))
    for line in range(Size):
        pygame.draw.line(window, (116, 116, 116), (0, line * width/Size), (width, line * width/Size))
        pygame.draw.line(window, (116, 116, 116), (line * height/Size, 0), (line * height/Size, height))
    pygame.display.update()

def moveCells():
    global Matrix, Size
    MatrixNewGen = makeGrid(Size, Size)
    for i in range(Size):
        for j in range(Size):
            try:
                surroundingCells = [
                    Matrix[i-1][j-1], Matrix[i-1][j], Matrix[i-1][j+1],
                    Matrix[i][j-1],                  Matrix[i][j+1],
                    Matrix[i+1][j-1], Matrix[i+1][j], Matrix[i+1][j+1]
                ]
            except IndexError:
                surroundingCells = []

            surroundingCount = sum(surroundingCells)

            if Matrix[i][j] == 1 and surroundingCount in (2, 3):
                MatrixNewGen[i][j] = 1
            elif Matrix[i][j] == 0 and surroundingCount == 3:
                MatrixNewGen[i][j] = 1

    Matrix = MatrixNewGen

def randomize():
    global Matrix
    for row in Matrix:
        for i in range(len(row)):
            row[i] = random.randint(0, 1)

def clear():
    global Matrix
    for row in Matrix:
        for i in range(len(row)):
            row[i] = 0

def MouseSetting(button):
    global Matrix, width, height, Size
    MouseCords = pygame.mouse.get_pos()
    MouseX = int(MouseCords[0] // (width/Size))
    MouseY = int(MouseCords[1] // (height/Size))
    if button in (1, 3):  # Handles both left and right clicks
        Matrix[MouseX][MouseY] = 1 - Matrix[MouseX][MouseY]

def stepForward():
    moveCells()
    updateWin()

width, height = 1400, 1400
Size = 150   #
Matrix = makeGrid(Size, Size)
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")
FPS = 20
def main():
    clock = pygame.time.Clock()
    move = False
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                MouseSetting(event.button)
            elif event.type == pygame.KEYDOWN:  # Checks if any key is pressed down
                if event.key == pygame.K_DOWN:
                    move = False
                elif event.key == pygame.K_UP:
                    move = True
                elif event.key == pygame.K_LEFT:
                    randomize()
                elif event.key == pygame.K_RIGHT:
                    clear()
                elif event.key == pygame.K_s and not move:
                    stepForward()  # Steps forward when 's' is pressed and the game is paused

        if move:
            moveCells()
        updateWin()

    pygame.quit()


if __name__ == "__main__":
    main()
