# -*- coding:utf-8 -*-
# This file holds various game objects like the player, obstacles, and items.
import random
# Standard library imports.
from typing import Sequence

# Third-party library imports.
import pygame as pg


# Constants
PLAYER_ROTATE_SPEED = 300  # The speed the keyboard can rotate the player angle.
PLAYER_PUSH_ACC = 300  # The acceleration that is applied to the player when the extinguisher is active.
PLAYER_CIRCLE_RADIUS = 30  # The radius of the collision circle for the player.
TANK_DECREASE = 5  # The speed the tank should decrease at per second.
TANK_MAX = 100  # The maximum value of the tank.
MAX_ASTEROID_ROT_SPEED = 50  # The maximum speed an asteroid can rotate at.


class Player:
    def __init__(self, pos: Sequence[float], image: pg.Surface):
        # I'm not using type hints for some variables here because their type is obvious.
        self.pos = pg.Vector2(pos)  # The position of the player, in pixels.
        self.vel = pg.Vector2(0, 0)  # The velocity of the player.
        self.acc = pg.Vector2(0, 0)  # The acceleration of the player.
        self.angle = 0.0  # The angle of the fire extinguisher, in degrees.
        self.pushing = False  # Whether the extinguisher is active and pushing.
        self.radius = PLAYER_CIRCLE_RADIUS  # The radius of the collision circle.
        self.base_image = image  # Store a copy of the original image to avoid rotation corruption.
        self.image = pg.transform.rotate(self.base_image, -self.angle)  # This image is used for drawing.
        self.rect = self.image.get_rect(center=self.pos)  # This is used only for drawing.

        # Create the player mask.
        self.mask = pg.mask.from_surface(self.image)

    def update(self, dt: float, game_bounds: pg.Vector2, obstacles: list["Obstacle"]):
        """Update the player.

        This function handles movement, collision detection, etc.
        """
        # Update the acceleration if the extinguisher is active.
        if self.pushing:
            self.acc.from_polar((-PLAYER_PUSH_ACC, self.angle))
        else:
            self.acc = pg.Vector2(0, 0)
        # Update the velocity and position based on acceleration and delta-time.
        self.vel += self.acc * dt
        self.pos += self.vel * dt

        # Collision detection with the game boundaries.
        # The player bounces off the game edges.
        if self.pos.x - self.radius < 0:
            self.vel.x *= -1
            self.pos.x = self.radius
        if self.pos.x + self.radius > game_bounds.x:
            self.vel.x *= -1
            self.pos.x = game_bounds.x - self.radius
        if self.pos.y - self.radius < 0:
            self.vel.y *= -1
            self.pos.y = self.radius
        if self.pos.y + self.radius > game_bounds.y:
            self.vel.y *= -1
            self.pos.y = game_bounds.y - self.radius

        # Update the image and rect.
        self.image = pg.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center=self.pos)

        

        for obstacle in obstacles:
            if self.mask.overlap(obstacle.mask, (pg.Vector2(obstacle.rect.topleft) - self.rect.topleft)):
                # bounce off obstacle
                self.vel = -self.vel


        self.mask = pg.mask.from_surface(self.image)

    def draw(self, screen: pg.Surface, camera: pg.Vector2):
        """Draw the player to the screen."""
        screen.blit(self.image, self.rect.topleft + camera)
        # screen.blit(self.mask.to_surface(), (0, 0))


class Obstacle:
    def __init__(self, pos: Sequence[float], image: pg.Surface):
        self.pos = pg.Vector2(pos)
        self.rot_speed = random.randint(-MAX_ASTEROID_ROT_SPEED, MAX_ASTEROID_ROT_SPEED)
        self.base_image = image
        self.radius = self.base_image.get_width() // 2

        self.angle = random.randrange(360)
        self.image = pg.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)  # Used only for drawing.
        self.mask = pg.mask.from_surface(self.image)

    def update(self, dt: float):
        """Update the obstacle.

        Rotate the image, etc.
        """
        self.angle += self.rot_speed * dt
        self.angle %= 360
        self.image = pg.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, screen: pg.Surface, camera: pg.Vector2):
        """Draw the obstacle to the screen."""
        screen.blit(self.image, self.rect.topleft + camera)
