import random
import pygame
import sys
import math
import time

pygame.init()

target_fps = 60

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial",18)


class Particle():
    instances = []

    def __init__(self, x, y):
        print("create")
        self.position = pygame.Vector2(x, y)
        self.radius = 8
        self.colour = (255, 255, 255)

        self.speed = 1
        self.angle = random.random() * math.pi * 2

        self.makeup = ["H"]

        Particle.instances.append(self)

    def update(self):
        for circle in Particle.instances:
            if circle == self:
                continue
            if self.position.distance_to(circle.position) < self.radius + circle.radius:
                if self.makeup.count("H") == 1 and len(self.makeup) == 1 and circle.makeup.count("H") == 1 and len(circle.makeup) == 1:
                    self.makeup.extend(circle.makeup)
                    Particle.instances.remove(circle)
                else:
                    # get angle of line between 2 points
                    normal = math.atan2(circle.position.y - self.position.y, circle.position.x - self.position.x)
                    # Set angles appropriately
                    self.angle = normal + math.pi
                    circle.angle = normal
                l = self.makeup
                # Single H
                if len(l) == 1 and l[0] == "H":
                    self.colour = "blue"
                    self.radius = 8
                # Double H
                if len(l) == 2 and l[0] == "H" and l[1] == "H":
                    self.colour = "green"
                    self.radius = 10

        # Collide with walls of screen
        if self.position.x - self.radius < 0:
            self.position.x = 0 + self.radius
            self.angle = math.pi - self.angle
        if self.position.x + self.radius > screen.get_width():
            self.position.x = screen.get_width() - self.radius
            self.angle = math.pi - self.angle
        if self.position.y - self.radius < 0:
            self.position.y = 0 + self.radius
            self.angle = math.pi * 2 - self.angle
        if self.position.y + self.radius > screen.get_height():
            self.position.y = screen.get_height() - self.radius
            self.angle = math.pi * 2 - self.angle

        self.position.x += self.speed * math.cos(self.angle)
        self.position.y += self.speed * math.sin(self.angle)


    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.position.x), int(self.position.y)), self.radius)


def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))


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
                Particle(event.pos[0], event.pos[1])

    for particle in Particle.instances:
        particle.update()
        particle.draw(screen)

    # Final Render
    pygame.display.update()
    screen.fill((100, 100, 100))

    # Limit Fps & Display real FPS in the caption
    clock.tick(60)
    fps_counter()

pygame.quit()
sys.exit()