import pygame_menu
import pygame
import connect4 as c4P
import connect4AI as c4AI
import connect6 as c6P
import connect6AI as c6AI

pygame.init()
surface = pygame.display.set_mode((700, 700))
mainMenu = pygame_menu.Menu('Welcome', 600, 500,
                            theme=pygame_menu.themes.THEME_DARK)
connect4Menu = pygame_menu.Menu('Connect 4', 600, 500,
                                theme=pygame_menu.themes.THEME_DARK)

connect4Difficulty = pygame_menu.Menu('Connect 4', 600, 500,
                                      theme=pygame_menu.themes.THEME_DARK)

connect6Menu = pygame_menu.Menu('Connect 6', 600, 500,
                                theme=pygame_menu.themes.THEME_DARK)

connect6Difficulty = pygame_menu.Menu('Connect 6', 600, 550,
                                      theme=pygame_menu.themes.THEME_DARK)

currDifficulty = 1


def show_mainMenu():
    mainMenu.mainloop(surface)


def show_connect4Menu():
    connect4Menu.mainloop(surface)


def show_connect6Menu():
    connect6Menu.mainloop(surface)


def showConnect4Difficulty():
    connect4Difficulty.mainloop(surface)


def showConnect6Difficulty():
    connect6Difficulty.mainloop(surface)


def set_difficulty(value, difficulty):
    global currDifficulty
    currDifficulty = difficulty
    print(currDifficulty)


def startC4Player():
    c4P.run()
    # surface = pygame.display.set_mode((700, 700))


def startC4AI():
    c4AI.run(currDifficulty)
    # surface = pygame.display.set_mode((700, 700))


def startC6Player():
    c6P.run()
    surface = pygame.display.set_mode((900, 900))
    connect6Menu.set_relative_position(position_x=50, position_y=50)
    connect6Difficulty.set_relative_position(position_x=50, position_y=50)


def startC6AI():
    c6AI.run(currDifficulty)
    surface = pygame.display.set_mode((900, 900))
    connect6Menu.set_relative_position(position_x=50, position_y=50)
    connect6Difficulty.set_relative_position(position_x=50, position_y=50)


def init():
    # menuBar = pygame_menu.widgets.MENUBAR_STYLE_NONE
    mainMenu.add.label("Connect X", font_size=70)
    mainMenu.add.button('Connect 4', show_connect4Menu)
    mainMenu.add.button('Connect 6', show_connect6Menu)
    mainMenu.add.button("Exit", pygame_menu.events.EXIT)

    connect4Menu.add.label("Vs Whom", font_size=70)
    connect4Menu.add.button('VS Player', startC4Player)
    connect4Menu.add.button('VS AI', showConnect4Difficulty)
    connect4Menu.add.button("Go Back", show_mainMenu)
    connect4Menu.add.button("Exit", pygame_menu.events.EXIT)

    connect4Difficulty.add.label("Select Difficulty", font_size=60)
    connect4Difficulty.add.selector('Difficulty: ', [('Very Easy', 1), ('Normal', 2), ('Hard', 4)],
                                    onchange=set_difficulty)
    connect4Difficulty.add.button("Start", startC4AI)
    connect4Difficulty.add.button("Go Back", show_connect4Menu)
    connect4Difficulty.add.button("Exit", pygame_menu.events.EXIT)

    connect6Menu.add.label("Vs Whom", font_size=70)
    connect6Menu.add.button('VS Player', startC6Player)
    connect6Menu.add.button('VS AI', showConnect6Difficulty)
    connect6Menu.add.button("Go Back", show_mainMenu)
    connect6Menu.add.button("Exit", pygame_menu.events.EXIT)

    connect6Difficulty.add.label("Select Difficulty", font_size=70)
    connect6Difficulty.add.selector('Difficulty: ', [('Very Easy', 1), ('Normal', 2), ('Hard', 4)],
                                    onchange=set_difficulty)
    connect6Difficulty.add.button("Start", startC6AI)
    connect6Difficulty.add.button("Go Back", show_connect6Menu)
    connect6Difficulty.add.button("Exit", pygame_menu.events.EXIT)

    mainMenu.mainloop(surface)


init()
