import pygame
import sys
import math
from car import Car
from genetic_algorithm import next_generation

# Standard screen setup constants
WIDTH = 1280
HEIGHT = 720
GENERATION = 0 # Track which generation we are on

def draw_map(screen):
    # This prepares the collision map.
    # We clear the screen with White, which our cars treat as "Lava"/Walls.
    screen.fill((255, 255, 255))
    
    # Draw the Track! 
    # Black pixels (0,0,0) are safe road.
    
    # Draw a big black oval first (The outer edge of the track)
    pygame.draw.ellipse(screen, (0, 0, 0), [100, 100, 1080, 520]) 
    
    # Draw a smaller white oval inside (The inner island)
    # This leaves a black ring which is our racetrack.
    pygame.draw.ellipse(screen, (255, 255, 255), [250, 200, 780, 320])

def main():
    global GENERATION
    
    # Initialize the Pygame engine
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Self Driving Car Logic - Generation: 0")
    clock = pygame.time.Clock()
    
    # Create a separate invisible surface for collision detection
    # We draw the clean track map on it once, so we don't have to check pixel colors on the main decorated screen
    map_surface = pygame.Surface((WIDTH, HEIGHT))
    draw_map(map_surface)
    
    # Start Line coordinates (Bottom center of the track loop)
    start_pos = [640, 650] 
    
    # Create the startup crew!
    # Spawning 30 dumb cars that don't know how to drive yet.
    cars = []
    for _ in range(30): 
        cars.append(Car(start_pos, map_surface))

    # The Game Loop
    while True:
        # Standard exit check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update all cars
        alive_cars = 0
        for car in cars:
            # Only process cars that haven't crashed
            if car.alive:
                alive_cars += 1
                
                # 1. Look around: Get data from sensors
                inputs = car.get_data()
                
                # 2. Think: Ask the brain what to do
                output = car.brain.feed_forward(inputs)
                
                # 3. Act: Interpret the brain's output
                # Output 0 governs speed.
                if output[0] > 0:
                    car.speed = 2 # Gas pedal pressed!
                else:
                    car.speed = 0 # Brakes!
                    
                # Output 1 governs steering
                # Result is between -1 and 1, so we multiply by 5 to get a decent turn speed.
                car.angle += output[1] * 5 
                
                # Apply physics
                car.update()
        
        # If everyone crashed, it's time for the next generation!
        if alive_cars == 0:
            GENERATION += 1
            # Evolve the population!
            cars = next_generation(cars, map_surface, start_pos)
            print(f"Generation {GENERATION} Complete - Starting new batch.")

        # Render everything to the screen
        screen.blit(map_surface, (0, 0)) # Draw the track background
        
        for car in cars:
            if car.alive:
                car.draw(screen)
        
        # Draw some stats so we know what's happening
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Generation: {GENERATION}", True, (0, 0, 0))
        text_alive = font.render(f"Still Alive: {alive_cars}", True, (0, 0, 0))
        screen.blit(text, (10, 10))
        screen.blit(text_alive, (10, 50))

        # Flip the display buffer to show the new frame
        pygame.display.flip()
        
        # Cap logic to 60 FPS
        clock.tick(60)

if __name__ == "__main__":
    main()
