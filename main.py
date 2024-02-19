import pygame
import sys
import math
import time

target_fps = 60

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (255, 255, 255)
        self.speed = pygame.Vector2(10, 10)
        self.angle = 0
        self.angle_limit = 2 * math.pi

    def update(self, dt):
        self.x += self.speed.x * math.cos(self.angle) * dt
        self.y += self.speed.y * math.sin(self.angle) * dt
        if self.angle > self.angle_limit:
            self.angle = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


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
                particles.append(Particle(event.pos[0], event.pos[1], 10))

    for particle in particles:
        particle.update(delta_time)
        particle.draw(screen)

    pygame.display.update()
    screen.fill((0, 0, 0))

    # delta_time update
    end_time = time.time()
    delta_time = end_time - start_time
    start_time = end_time  # Update start_time for the next frame

    # Limit Fps & Display real FPS in the caption
    clock.tick(target_fps)
    if delta_time > 0:
        real_fps = 1 / delta_time
    else:
        real_fps = 0
    pygame.display.set_caption(f'My Game - FPS: {real_fps:.2f}')

pygame.quit()
sys.exit()