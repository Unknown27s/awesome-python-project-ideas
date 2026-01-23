import pygame
import math
import numpy as np
from neural_network import NeuralNetwork

# Some constants to keep things consistent
CAR_SIZE_X = 20
CAR_SIZE_Y = 10
COLOR_CAR = (0, 0, 255)     # Blue cars!
COLOR_SENSOR = (0, 255, 0)  # Green sensor beams
COLOR_CRASHED = (255, 0, 0) # Red for crash

class Car:
    def __init__(self, position, map_surface):
        # Where are we starting?
        self.position = np.array(position, dtype=float)
        self.map_surface = map_surface
        
        # Physics stuff
        self.angle = 0  # Which way are we facing?
        self.speed = 0  # How fast are we going?
        
        self.alive = True # Is the car still running?
        self.distance = 0  # Fitness score: how far did we make it?
        self.time_alive = 0 # How long did we survive?
        
        # The Brain! 
        # 5 inputs (sensors) -> 6 hidden neurons -> 2 outputs (speed and steering)
        self.brain = NeuralNetwork(5, 6, 2)
        
        # Radar sensors to "see" walls
        self.radars = []
        
        # Center point for rotation math
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]

    def draw(self, screen):
        # Time to render the car.
        # We draw it on a temporary surface so we can rotate it without distorting the original shape.
        car_surface = pygame.Surface((CAR_SIZE_X, CAR_SIZE_Y), pygame.SRCALPHA)
        
        # If it crashed, paint it red like a disaster scene.
        color = COLOR_CRASHED if not self.alive else COLOR_CAR
        pygame.draw.rect(car_surface, color, (0, 0, CAR_SIZE_X, CAR_SIZE_Y))
        
        # Pygame rotation goes counter-clockwise, so we negate our angle.
        rotated_car = pygame.transform.rotate(car_surface, -self.angle)
        rect = rotated_car.get_rect(center=self.center)
        screen.blit(rotated_car, rect.topleft)
        
        # Draw the laser beams (sensors) so we can see what the car sees.
        if self.alive:
            for radar in self.radars:
                position = radar[0]
                pygame.draw.line(screen, COLOR_SENSOR, self.center, position, 1)
                pygame.draw.circle(screen, COLOR_SENSOR, position, 2)

    def check_collision(self):
        # Am I dead? Let's check.
        self.alive = True
        
        for point in self.corners:
            # First, check if we literally drove off the monitor.
            if point[0] < 0 or point[0] >= self.map_surface.get_width() or \
               point[1] < 0 or point[1] >= self.map_surface.get_height():
                self.alive = False
                break
            
            # Now check the map. We assume white pixels are walls (lava!).
            try:
                if self.map_surface.get_at((int(point[0]), int(point[1]))) == (255, 255, 255, 255): 
                     self.alive = False
                     break
            except:
                self.alive = False # Just in case we go out of bounds
                break

    def check_radar(self, degree):
        # This is the "eye" of the car. It casts a ray in a specific direction.
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Keep extending the ray until we hit a wall or reach max vision range
        while length < 100: # We can see up to 100 pixels ahead
            length += 5 # Optimize by checking every 5 pixels instead of 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
            
            # Stop if we hit the edge of the screen
            if x < 0 or x >= self.map_surface.get_width() or \
               y < 0 or y >= self.map_surface.get_height():
                break
            
            # Stop if we hit a wall
            if self.map_surface.get_at((x, y)) == (255, 255, 255, 255):
                break
        
        # Calculate the actual distance to the obstacle
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self):
        # If we crashed, stop processing physics.
        if not self.alive:
            return

        # Simple trigonometry to move in the direction we are facing
        self.center[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = self.center[0] - CAR_SIZE_X / 2 
        self.center[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = self.center[1] - CAR_SIZE_Y / 2
        
        # Give ourselves points for staying alive and moving!
        self.distance += self.speed
        self.time_alive += 1
        
        # Calculate the 4 corners of the car for accurate collision detection.
        # This prevents the car from clipping through walls with its edges.
        length = CAR_SIZE_X / 2
        
        # Calculating corners based on rotation... Math warning!
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, 
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, 
                     self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, 
                       self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, 
                        self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        
        self.corners = [left_top, right_top, left_bottom, right_bottom]
        
        # Check if we hit anything
        self.check_collision()
        
        # Clear old sensor data and scan again
        self.radars.clear()
        # Scan at 5 angles: -90 (left), -45, 0 (straight), 45, 90 (right)
        for d in [-90, -45, 0, 45, 90]:
            self.check_radar(d)

    def get_data(self):
        # Prepare data for the brain.
        # We normalize distance so inputs are roughly between 0 and 1.
        # This helps the Neural Network learn faster.
        inputs = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            inputs[i] = int(radar[1] / 10) # Crude normalization
        return inputs
