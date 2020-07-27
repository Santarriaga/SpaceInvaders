import pygame
pygame.init()


win = pygame.display.set_mode((800, 900))

pygame.display.set_caption("Project")

background = pygame.image.load('bg.jpg')
spaceship = pygame.image.load('ship.png')
laser = pygame.image.load('laser.png')
enemy1 = pygame.image.load('enemy.png')
explosion = pygame.image.load('explosionpurple.png')

hitsound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load('Waves.mp3')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

score = 0


class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.hitbox = (self.x, self.y - 5, 50, 55)
        self.health = 2
        self.dead = False

    def draw(self, win):
        win.blit(spaceship, (self.x, self.y))

        self.hitbox = (self.x, self.y - 5, 50, 55)
#       pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

    def hit(self):
        if self.health > 0:
            self.x = 400
            self.y = 825
            self.health -= 1
        else:
            self.dead = True


class Projectile(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

    def draw(self, win):
        win.blit(laser, (self.x, self.y) )


class Enemy(object):
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.vel = 15
        self.path = [self.x, self.end]
        self.hitbox = (self.x , self.y, self.width, self.height)
        self.health = 1
        self.visible = True
        self.explosion = 3

    def draw(self, win):
        self.move()
        if self.visible:
            win.blit(enemy1, (self.x, self.y))

            self.hitbox = (self.x, self.y, self.width, self.height)
#           pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        else:
            win.blit(explosion, (self.x, self.y))
            self.explosion -= 1

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.y += 70
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.y += 70

    def hit(self):
        if self.health > 0:
            self.health -= 1
#            hitsound.play()
        else:
            self.visible = False

        print("hit")


screenWidth = 800
screenHeight = 900


def redrawGameWindow():
    win.blit(background, (0,0))
    ship.draw(win)

    for i in aliens:
        if i.explosion > 0:
            i.draw(win)
        else:
            aliens.pop(aliens.index(i))
            aliens.append(Enemy(0,0, 75, 75, 735))

    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (625, 25))

    for i in bullets:
        i.draw(win)

    pygame.display.update()


# Main Loop
font = pygame.font.SysFont('comicsans', 30)
ship = Character(400, 800, 50, 48)
alien = Enemy(0, 0, 75, 75, 735)


run = True
bullets = []
bulletCount = 0

aliens = []
enemyCount = 25

for i in range(enemyCount):
    aliens.append(Enemy(i * -100, 0, 75, 75, 735))

while run:
    clock.tick(30)

    if ship.dead:
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('Game Over!', 1, (255, 255, 255))
        win.blit(text, (200, 100))
        pygame.display.update()
        run = False


#    check spaceship collision
    for alien in aliens:
        if alien.visible == True:
            if ship.hitbox[1] < alien.hitbox[1] + alien.hitbox[3] and ship.hitbox[1] + ship.hitbox[3] > alien.hitbox[1]:
                if ship.hitbox[0] + ship.hitbox[2] > alien.hitbox[0] and ship.hitbox[0] < alien.hitbox[0] + alien.hitbox[2]:
                    ship.hit()

#    makes sure only one but is being shot at time
    if bulletCount > 0:
        bulletCount += 1
    if bulletCount < 10:
        bulletCount = 0

#    checks if game is still running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#    checks for bullet collision
    for alien in aliens:
        for i in bullets:
            if i.y < alien.hitbox[1] + alien.hitbox[3] and i.y > alien.hitbox[1]:
                if i.x > alien.hitbox[0] and i.x < alien.hitbox[0] + alien.hitbox[2]:
                    alien.hit()
                    score += 25
                    bullets.pop(bullets.index(i) )

#           makes bullets move
            if i.y < screenHeight and i.y > 0:
                i.y -= i.vel
            else:
                bullets.pop(bullets.index(i))

#   gets user input
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ship.x > ship.vel:
        ship.x -= ship.vel
    if keys[pygame.K_RIGHT] and ship.x < screenWidth - ship.width - ship.vel:
        ship.x += ship.vel
    if keys[pygame.K_UP] and ship.y > ship.vel:
        ship.y -= ship.vel
    if keys[pygame.K_DOWN] and ship.y < screenHeight - ship.height - ship.vel:
        ship.y += ship.vel
    if keys[pygame.K_SPACE] and bulletCount == 0:
        if len(bullets) < 10:
            bullets.append(Projectile(ship.x + 23, ship.y - 24, 5, 15))
            bulletCount = 1



    redrawGameWindow()

pygame.quit()


