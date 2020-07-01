# Andrew Quigley (ajq2vb) and Kevin Kern (kjk9cd)

import gamebox, pygame, random

"""
Our game is similar to the game play of the google no internet connection game, obstacles move towards a player and the
player must jump to avoid them while collecting as many bananas as they can. Our game includes a title screen that 
prompts th user to press r, to reveal the rules, or to press space (that flashes because why not) to begin the game. 
Once space is press the text moves off the screen and the grass begins to move once the text is full of the screen the 
obstacles begin to move towards the player and the up arrow must be pressed to jump over them. Bananas will appear to 
be collected and your total will be displayed on the right side of the screen and the time you lasted with be displayed 
on the left hand side of the screen. If a spear is touched the game will end 

"""

camera = gamebox.Camera(800, 600)
# creates the jungle background
background = gamebox.from_image(400, 300, "back1.jpg")
background.size = [1000, 600]
# this blue bar is what sits at the bottom of the screen that is not seen but acts as the boarder for the player when it
# jumps
ground = gamebox.from_color(400, 602, "blue", 1000, 4)
# the monkey player that is controlled by the up arrow
player = gamebox.from_image(180, 592, "monkey.png")
player.size = [60, 40]
# list of the banana image sot be collected
bananas = [
    gamebox.from_image(900, 500, "banana.png")
]
# Color of most of the text
color = "dark green"

title = gamebox.from_text(400, 250, "Jungle Jump", 60, color, True)
# Rules is in a list so we can show the rules if requested or keep the screen less cluttered by the long rules
# well they aren't long but I thought it was a nicer touch to be able to click something and have the rules appear
rules = [
    gamebox.from_text(400, 300, "Press r for Rules", 30, color),
    gamebox.from_text(400, 275, "Use the UP Arrow to avoid the incoming Spears", 30, color),
    gamebox.from_text(400, 250, "Be sure to collect those delicious Bananas for our monkey friend!", 30, "brown")
    ]
start = gamebox.from_text(400, 350, "PRESS SPACE TO START", 30, color)
names = gamebox.from_text(400, 30, "Kevin Kern (kjk9cd)", 40, "black", True, True)
# A list of the grass images to be added and removed as the grass scrolls across the screen to give the
# apearnace of movement
grasses = [
    gamebox.from_image(400, 400, "http://www.textures4photoshop.com/tex/thumbs/free-transparent-grass-texture-seamless-PNG-thumb43.png"),
    gamebox.from_image(1200, 400, "http://www.textures4photoshop.com/tex/thumbs/free-transparent-grass-texture-seamless-PNG-thumb43.png")
    ]
# list of spear images because these will also be scrolling
obstacles = [
    gamebox.from_image(900, 600, "spear.png")
]
# this is a boolean list that will run in parallel with the obstacles list so it know when to move up and down
# im realising I could have just made a 2d list to attach a boolean value to each obstacle but well too late works the
# same
ob_bool = [
    True
]

player.speedy = 0

press = True
# Create a list of various images that are different heights that we can have different heights so like maybe six of
# seven different sized images that we acn just iterate too
height = list(range(100, 200))
# Controls the distance between each obstacle at various different distances but the smallest value is large enough it
# it won't be a problem of being to close
dist = list(range(1100, 1200, 5))
# again controls the distance at which they appear same for the banana height only its height
banana_dist = list(range(900, 1000))
banana_height = list(range(120, 50))
# if space is pressed this is what turn the game on
pygame_on = False
# if r is pressed this controls the game
rule_bol = True
banana_count = 0


def exit_title_screen():
    """
    This removes the title screen text from the game so the game can begin, really its just moving it out of the window
    :return: void
    """
    global pygame_on
    if title.y > -200 or names.y > -200:
        # moves stuff off the screen so the game can begin
        title.y -= 10
        start.y -= 10
        names.y -= 10
    for rule in rules:
        if rule.y > -100:
            rule.y -= 10


def grass_move():
    """
    Moves the grass across the screen to make the gamebox look more likes it moving and allows for a continious loop
    of grass by removing an appending the grass as one moves completely off the screen it is removed an added to the end
    :return: void
    """
    for grass in grasses:
        grass.size = [800, 400]
        grass.x -= 10
        if grass.x == -400:
            grasses.append(gamebox.from_image(1200, 400,"http://www.textures4photoshop.com/tex/thumbs/free-transparent-grass-texture-seamless-PNG-thumb43.png"))
        if grass.x == -1300:
            grasses.pop(0)


def banana_move():
    """
    This function handles all of the abilities of our collectable bananas whihc appends a banana if one is touched or
    if there are not touched and move off the screen the banana is removed in both of these cases, this function also
    creates a running counter of the bananas collected
    :return:
    """
    global bananas, banana_count
    b_d = random.randint(850, 1000)
    banana_counter = gamebox.from_text(690, 340, "Bananas: " + str(banana_count), 35, "yellow")
    camera.draw(banana_counter)
    for banana in bananas:
        banana.x -= 10
        if player.touches(banana):
            banana_count += 1
            bananas.pop(0)
            bananas.append(gamebox.from_image(b_d, 500, "banana.png"))
        if banana.x < 0:
            bananas.append(gamebox.from_image(b_d, 500, "banana.png"))
            bananas.pop(0)


def obstacle_move():
    """
    These pipes will be replaced some kind of graphic images that will serve as the pipes but those images should have
    the url placed in the obstacles method, and one time in the append statement hopefully this change should alter how
    the function operates and no further changes will be needed, yes this was fixed
    :return: void
    """
    global dist, height

    # d is getting a random index for the dist list so that way we can in the append statement access different heights
    d = random.randint(0, len(dist)-1)
    # h is getting a random index for the height list so we can add a random height to the append statement
    h = random.randint(0, len(height)-1)
    for obstacle in obstacles:
        obstacle.x -= 10

        if obstacle.y >= 550 and ob_bool[obstacles.index(obstacle)]:
            obstacle.y -= 4.9
            if obstacle.y <= 550:
                ob_bool[obstacles.index(obstacle)] = False

        if not ob_bool[obstacles.index(obstacle)]:
            obstacle.y += 1.70
            if obstacle.y >= 650:
                ob_bool[obstacles.index(obstacle)] = True

        if player.right_touches(obstacle):
            player.move_to_stop_overlapping(obstacle)
            gamebox.pause()
            end = gamebox.from_text(400, 300, "GAME OVER :`(", 50, color)
            camera.draw(end)
            camera.display()

        # The below if statement is meant to create a new obstacle every time one passes the between 750 and 800
        if 795 <= obstacle.x <= 800:
            # for the height part the images in the obstacle function should have varying heights or we are going to
            # have figure out how to change the heights of an imported image but for now h represents the height
            obstacles.append(gamebox.from_image(dist[d], 600, "spear.png"))
            ob_bool.append(True)
            obstacle.size = [20, height[h]]
        if obstacle.x < -400:
            obstacles.pop(0)
            ob_bool.pop(0)


count = 0
timer = 0
flash = 0
jump = True


def tick(keys):
    global pygame_on, press, rule_bol, count, timer, flash, jump
    flash += 1
    camera.clear("blue")
    # ground is drawn first because gamebox displays things in layers so the ground needs to be displayed first so
    #  it will be covered, more compactly what ever you display last will overlap and cover what you displayed first
    camera.draw(ground)
    camera.draw(background)
    for grass in grasses:
        grass.size = [800, 400]
        camera.draw(grass)
    for obstacle in obstacles:
        camera.draw(obstacle)
    for banana in bananas:
        banana.size = [35, 35]
        camera.draw(banana)
    # this statement says if r is not pushed display the first rule in the rules list but if r is pushed then rules[0]
    # will stop displaying and rule[1]\rule[2] will begin to display
    if rule_bol:
        camera.draw(rules[0])
        camera.draw(names)
        camera.draw(title)
    else:
        camera.draw(rules[1])
        camera.draw(rules[2])
    # below if statement flashes the press start command
    if 0 < flash % 50 < 25:
        camera.draw(start)

    camera.draw(player)

    if pygame.K_r in keys:
        rule_bol = False

    # the boolean pygame_on is to see whether the game can begin so pressing enter turns pygame_on to true
    if pygame.K_SPACE in keys:
        pygame_on = True
    # if pygame_on is true once space is pressed and will stay true so this will conitnuely run without having to press
    # space every time because once space is pressed it stays at true
    if pygame_on:
        grass_move()
        exit_title_screen()
        # the below if statement means once the names and rules are moved off the screen the game can begin and because
        # the exit_title_screen function just moves them off the screen and then they stop this if statement will always
        # be true
        if names.y < 0:
            count += 1
            obstacle_move()
            banana_move()
            scoring = gamebox.from_text(75, 340, "Time: " + str(timer) + ' secs', 35, "brown")
            if count % 30 == 0:
                timer += 1
            camera.draw(scoring)
    if not jump:
        # gravity that is only acting when the player is off the ground
        player.speedy += 1
        player.y = player.y + player.speedy
    if player.bottom_touches(ground):
        jump = True
        # for some reason without this the ground is pushed down on impact
        player.move_to_stop_overlapping(ground)
        # setting the speed to zero once it touches the ground so it doesnt move through it
        player.speedy = 0
    if pygame.K_UP in keys and jump:
        # gives the player a burst of speed so it launches up
        # the reason for this being under the if player touches bottom statement is because the player is
        # only allow to jump once it has touched the ground again
        player.speedy = -12
        jump = False
    player.move_speed()
    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)
