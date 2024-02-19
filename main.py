import pygame
import sys
import math
import time

pygame.init()

target_fps = 60

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",18)

sprites = pygame.sprite.Group()


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        pygame.sprite.Sprite.__init__(self)

        self.add(sprites)

        self.x = x
        self.y = y
        self.radius = radius
        self.color = (255, 255, 255)
        self.image = pygame.surface.Surface((2 * radius, 2 * radius))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = pygame.Vector2(10, 10)
        self.angle = 0
        self.angle_limit = 2 * math.pi

    def update(self, dt):
        self.x += self.speed.x * math.cos(self.angle) * dt
        self.y += self.speed.y * math.sin(self.angle) * dt
        if self.angle > self.angle_limit:
            self.angle = 0
        # update rect location
        self.rect.topleft = (int(self.x), int(self.y))


def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))

particles = []

start_time = 0
delta_time = 0
end_time = 0

running = True
while running:
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("particle created")
                Particle(event.pos[0], event.pos[1], 10)

    # Render sprites
    sprites.update(delta_time)
    sprites.draw(screen)
    print("one")

    # Final Render
    pygame.display.update()
    screen.fill((0, 0, 0))

    # delta_time update
    end_time = time.time()
    delta_time = end_time - start_time

    # Limit Fps & Display real FPS in the caption
    clock.tick(60)
    fps_counter()

pygame.quit()
sys.exit()