import pygame, sys, random, time
#from inspect import stack // was just using for debugging
window_length = 600
window_height = 600

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((window_length,window_height))
logo = pygame.image.load("logo.jpg")

pygame.display.set_caption("Snake")
pygame.display.set_icon(logo)

snakeObj = []
head = pygame.rect
snake_length = 1
apples = []
speed = 15
dirx = 0
diry = 0
score = 0
snakeblock = 10
highscore = score
sfxchannel = pygame.mixer.Channel(1)

def geths():
    with open("hs.txt","r") as reader:
        return int(reader.read().strip())
def seths(score):
    with open("hs.txt","w") as file:
        file.write(str(score))

colours = {
    "white" : (255, 255, 255),
    "black" : (0,0,0),
    "green":(50, 255, 0),
    "red":(255, 0, 0),
    "blue":(0,0,255),
    "yellow":(255,255,0),

}
snakecolor = colours["green"]
def drawtext(surface, text, font, colour, x, y):
    textobj = font.render(text, True, colour)
    rec = surface.blit(textobj, (x,y))
    return rec

def spawnNewSnake():
    global snakeObj, head
    snakeObj.clear()
    head = [250,250]
    snakeObj.append(head)
    return snakeObj


def drawSnake():
    global snakeObj, snake_length, head, snakeblock 

    for i in snakeObj:
        head = pygame.draw.rect(window,snakecolor,[i[0],i[1],snakeblock,snakeblock])
    return head
        

def spawnApple(apple = None):
    global apples, snakeblock, snakecolor
    if apple:
        if snakecolor == colours["red"]:
            return pygame.draw.rect(window, colours["green"],[apple.x,apple.y,apple.w,apple.h])
        else:
            return pygame.draw.rect(window, colours["red"],[apple.x,apple.y,apple.w,apple.h])
    else:
        randx = random.randint(snakeblock, window_length-snakeblock)
        randx = round(randx/snakeblock) * snakeblock
        randy = random.randint(0.1*window_height + snakeblock, window_height-snakeblock) 
        randy = round(randy/snakeblock) * snakeblock

        for i in snakeObj:
            if i[0] == randx and i[1] == randy:
                randx = random.randint(snakeblock, window_length-snakeblock)
                randx = round(randx/snakeblock) * snakeblock
                randy = random.randint(0.1*window_height + snakeblock, window_height-snakeblock) 
                randy = round(randy/snakeblock) * snakeblock
        if snakecolor == colours["red"]:
            newApple = pygame.draw.rect(window,colours["green"],[randx,randy,snakeblock,snakeblock])
        else:
            newApple = pygame.draw.rect(window,colours["red"],[randx,randy,snakeblock,snakeblock])
        apples.append(newApple)
        return newApple
class TextButton():
    def __init__(self, surface, text, textcolour, bgColour, x, y, fontsize):
        self.surface = surface
        self.textcolour = textcolour
        self.bgColour = bgColour
        self.x = x
        self.y = y
        self.fontsize = fontsize
        self.text = text
    def draw(self):
        btnfont = pygame.font.SysFont("Source Code Pro", self.fontsize)
        btntext = btnfont.render(self.text, False,self.textcolour,self.bgColour)
        txtrect = self.surface.blit(btntext,(self.x,self.y))
        self.textrect = txtrect

    def check(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.textrect.collidepoint(event.pos):
                    return True
                else:
                    return False

game_over = False
def loadgame(restart = False):
    global score, game_over, snakeObj, apples, speed
    if restart:
        game_over = False
        
    score = 0
    speed = 15
    while not game_over:
        global dirx, diry,snake_length, head, snakeblock, clickedPlay

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT and dirx == 0:
                    dirx = -snakeblock
                    diry = 0
                    time.sleep(5/1000)

                elif event.key == pygame.K_RIGHT and dirx == 0:
                    dirx = snakeblock
                    diry = 0
                    time.sleep(5/1000) 
                elif event.key == pygame.K_UP and diry == 0:
                    diry = -snakeblock
                    dirx = 0
                    time.sleep(5/1000)
                elif event.key == pygame.K_DOWN and diry == 0:
                    diry = snakeblock
                    dirx = 0
                    time.sleep(5/1000)

        window.fill(colours["black"])
        barrier = pygame.draw.rect(window,colours["green"],[0, 0.1* window_height,window_length,1])
        font = pygame.font.SysFont("Source Code Pro", 25)
        if score > geths():
            seths(score)
        drawtext(window," SCORE: " + str(score),font,colours["white"],0.1 * window_length, 0)
        drawtext(window," HIGH SCORE: " + str(geths()),font,colours["white"],0.5 * window_length, 0)
        if len(snakeObj) == 0:
            spawnNewSnake()
            dirx = snakeblock
            diry = 0
        
        else:
            newx = snakeObj[-1][0]
            newy = snakeObj[-1][1]
            newx += dirx
            newy += diry

            body = [] #New block of body
            body.append(newx)
            body.append(newy)

            snakeObj.append(body) #Stick it on
            drawSnake()
            for part in snakeObj[:-1]:
                if head.collidepoint(part[0],part[1]):
                    game_over = True
                    if score > geths():  
                        seths(score)
                    snakeObj = []
                    apples = []
                    score = 0
                    snake_length = 0           
            if len(snakeObj) > snake_length: #Too long? Cut off 
                del snakeObj[0]


        if len(apples) == 0:
            spawnApple()
        else: 
            apple = spawnApple(apples[0])
            try:
                if apple.colliderect(head):      
                    score += 1
                    apples = []
                    snake_length += 1
                    if score > 0 and score % 5 == 0:
                        speed += 2.5
                    
                    sfxchannel.set_volume(1,0.5)
                    sfxchannel.play(pygame.mixer.Sound("chomp.mp3"))
                                
                if barrier.colliderect(head):
                    game_over = True
                    clickedPlay = False
                    if score > geths():
                        seths(score)
                    snakeObj = []
                    apples = []

                    score = 0
                    snake_length = 0
                elif head.x>= window_length-snake_length or head.x <= 0:
                    game_over = True
                    clickedPlay = False

                    if score > geths():
                        seths(score)
                    snakeObj = []
                    apples = []
                    score = 0
                    snake_length = 0
                elif head.y >= window_height-snake_length:
                    game_over = True
                    clickedPlay = False

                    if score > geths():
                        seths(score)
                    snakeObj = []
                    apples = []
                    score = 0
                    snake_length = 0
                pygame.display.update()
                
            except TypeError as err:
                print(err)


        clock.tick(speed)              

clickedPlay = False
mainmenu = True
customising = False
def customise():
    #print("CALLED BY: {}".format(stack()[1].function)) 
    global customising, snakeObj, dirx, diry, snakeblock, snake_length, window_length, window_height, snakecolor,mainmenu

    while customising:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill(colours["black"])
        dirx = snakeblock
        diry = 0
        if len(snakeObj) == 0:
            spawnNewSnake()
            snakeObj[0][1] = 0.2 * window_height
        snake_length = 10
        newx = snakeObj[-1][0] + dirx
        body = []
        body.append(newx)
        body.append(snakeObj[-1][1])

        snakeObj.append(body)        
        if len(snakeObj) > snake_length:
            del snakeObj[0]
        drawSnake()
        if snakeObj[-1][0] > window_length:
            snakeObj[-1][0] = 0
        img = pygame.image.load("./back_button.png").convert_alpha()
        img = pygame.transform.scale(img,(50,50))
        backbtn = img.get_rect()
        backbtn.topleft = (5,5)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backbtn.collidepoint(event.pos):
                    mainmenu = True
                    customising = False
                    snakeObj = []
                    snake_length = 1
                    window.fill(colours["black"])
                    main_menu()

        window.blit(img,backbtn)
        pygame.draw.rect(window,colours["green"],[0, 0.1* window_height,window_length,1])
        pygame.draw.rect(window,colours["green"],[0, 0.3* window_height,window_length,1])
        green = TextButton(window,"GREEN",colours["black"],colours["green"],0.45 * window_length,0.4 * window_height,26)
        green.draw()
        if green.check(events):
            snakecolor = colours["green"]
        white = TextButton(window,"WHITE",colours["black"],colours["white"],0.45 * window_length,0.46 * window_height,26)
        white.draw()
        if white.check(events):
            snakecolor = colours["white"]    
        red = TextButton(window,"RED",colours["white"],colours["red"],0.45 * window_length,0.52 * window_height,26)
        red.draw()
        if red.check(events):
            snakecolor = colours["red"]       
        blue = TextButton(window,"BLUE",colours["white"],colours["blue"],0.45 * window_length,0.58 * window_height,26)
        blue.draw()
        if blue.check(events):
            snakecolor = colours["blue"]  
        yellow = TextButton(window,"YELLOW",colours["black"],colours["yellow"],0.45 * window_length,0.64 * window_height,26)
        yellow.draw()
        if yellow.check(events):
            snakecolor = colours["yellow"] 
        clock.tick(10)
        pygame.display.update()

playedIntro = False

def main_menu():
    global clickedPlay, game_over, mainmenu, customising, playedIntro
    if not playedIntro:
        sfxchannel.set_volume(0.3)
        sfxchannel.play(pygame.mixer.Sound("intro.mp3"))
        playedIntro = True
    while mainmenu:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill(colours["black"])

        font = pygame.font.SysFont("Source Code Pro",35)
        
        txt = drawtext(window,"SNAKE GAME!",font,colours["green"], (0.325 * window_length), (0.1 * window_height))
        pygame.draw.rect(window,colours["green"],[(0.315 * window_length), (0.1 * window_height),txt.w+10, txt.h],2)

        btn = TextButton(window,"PLAY",colours["black"],colours["green"],(0.2 * window_length),(0.75*window_height),40)
        btn.draw()
        btn2 = TextButton(window,"CUSTOMISE",colours["black"],colours["green"],(0.5 * window_length),(0.75*window_height),40)
        btn2.draw()
        if btn.check(events):
            customising = False
            clickedPlay = True
            game_over = False
            mainmenu = False
            sfxchannel.stop()
            loadgame(True)
        if btn2.check(events):
            sfxchannel.stop()
            mainmenu = False
            customising = True
            customise()
            
        pygame.display.update()
        clock.tick(speed)
        
playingmusic = False

while True: 
    if clickedPlay and not game_over and not mainmenu: 
        loadgame()
    elif game_over and not customising:
        window.fill(colours["black"])
        events = pygame.event.get()
        font = pygame.font.SysFont("Source Code Pro",35)
        font2 = pygame.font.SysFont("Source Code Pro", 25)
        if not playingmusic:
            
            sfxchannel.set_volume(1,0.5)
            sfxchannel.play(pygame.mixer.Sound("death.mp3"))
            playingmusic = True
        
        drawtext(window,"GAME OVER!!", font , colours["green"],(0.325 * window_length), (0.5 * window_height))

        button = TextButton(window,"Try Again?",colours["black"],colours["green"],0.2 * window_length, 0.75 * window_height,30)

        button2 = TextButton(window,"Main Menu",colours["black"],colours["green"],0.6 * window_length, 0.75 * window_height,30)

        barrier = pygame.draw.rect(window,colours["green"],[0, 0.1* window_height,window_length,1])

        if score > geths():
            seths(score)
        drawtext(window," SCORE: " + str(score),font2,colours["white"],0.1 * window_length, 0)
        drawtext(window," HIGH SCORE: " + str(geths()),font2,colours["white"],0.5 * window_length, 0)

        button.draw()
        button2.draw()

        pygame.display.update()
        if button.check(events):
            playingmusic = False
            pygame.mixer.music.stop()
            loadgame(True)
            window.fill(colours["black"])
        if button2.check(events):
            clickedPlay = False
            window.fill(colours["black"])
            game_over = False
            mainmenu = True
            playingmusic = False
            sfxchannel.stop()            
            main_menu()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    elif not clickedPlay and not customising and mainmenu:
        playingmusic = False
        sfxchannel.stop()
        window.fill(colours["black"])
        main_menu()
