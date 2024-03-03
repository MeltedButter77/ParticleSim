import random
import pygame
import sys
import math
import time

pygame.init()

target_fps = 60

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)


class Ball:
    instances = []

    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.radius = 15
        self.colour = (255, 255, 255)

        self.speed = 1
        self.angle = random.random() * math.pi * 2

        self.velocity = pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * self.speed

        self.gravity = 0.1
        self.collision_dampening = 0.8

        Ball.instances.append(self)

    def update(self):
        ### Collisions ###
        # Collide other balls
        for circle in Ball.instances:
            if circle == self:
                continue
            if self.position.distance_to(circle.position) < self.radius + circle.radius:
                # get angle of line between 2 points
                normal = math.atan2(circle.position.y - self.position.y, circle.position.x - self.position.x)

                pygame.draw.line(screen, (0, 255, 0), (int(self.position.x), int(self.position.y)), (int(circle.position.x), int(circle.position.y)), 2)

                # Set angles appropriately
                self.angle = normal + math.pi
                circle.angle = normal

        # Collide with walls of screen
        if self.position.x - self.radius < 0:
            self.position.x = 0 + self.radius
            self.angle = math.pi - self.angle
            self.speed = self.speed * self.collision_dampening
        if self.position.x + self.radius > screen.get_width():
            self.position.x = screen.get_width() - self.radius
            self.angle = math.pi - self.angle
            self.speed = self.speed * self.collision_dampening
        if self.position.y - self.radius < 0:
            self.position.y = 0 + self.radius
            self.angle = math.pi * 2 - self.angle
            self.speed = self.speed * self.collision_dampening
        if self.position.y + self.radius > screen.get_height():
            self.position.y = screen.get_height() - self.radius
            self.angle = math.pi * 2 - self.angle
            self.speed = self.speed * self.collision_dampening

        ### Gravity effects ###
        # get velocity from angle and speed
        self.velocity = pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * self.speed

        # add gravity to the velocity
        self.velocity.y += self.gravity

        # convert velocity back to self.angle and self.speed
        self.angle = math.atan2(self.velocity.y, self.velocity.x)
        self.speed = math.sqrt(self.velocity.x ** 2 + self.velocity.y ** 2)

        ### Position updates ###
        self.position.x += self.speed * math.cos(self.angle)
        self.position.y += self.speed * math.sin(self.angle)

    def draw(self, surface):
        pygame.draw.circle(surface, self.colour, (int(self.position.x), int(self.position.y)), self.radius)
        pygame.draw.line(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), (int(self.position.x + self.radius * math.cos(self.angle)), int(self.position.y + self.radius * math.sin(self.angle))), 2)


def fps_counter():
    fps = str(int(clock.get_fps()))
    fps_t = font.render(fps, 1, pygame.Color("RED"))
    screen.blit(fps_t, (0, 0))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Ball(event.pos[0], event.pos[1])

    for particle in Ball.instances:
        particle.draw(screen)
        particle.update()

    # Final Render
    pygame.display.update()
    screen.fill((100, 100, 100))

    # Limit Fps & Display real FPS in the caption
    clock.tick(60)
    fps_counter()

pygame.quit()
sys.exit()
