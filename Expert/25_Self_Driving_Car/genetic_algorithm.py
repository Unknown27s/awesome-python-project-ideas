import random
import numpy as np
from car import Car

def next_generation(cars, map_surface, start_pos):
    # It's Evolution Baby!
    # This function decides who survives and who gets replaced by a better version.
    
    # First, let's rank everyone. The one who drove the furthest wins.
    cars.sort(key=lambda x: x.distance, reverse=True)
    
    # We keep the top 2 performers unchanged. They are the "Kings" of this generation.
    # This strategy is called "Elitism". If we lose our best genes, we might regress.
    best_cars = cars[:2]
    
    new_cars = []
    
    # Clone the champions directly into the new generation.
    for saved_car in best_cars:
        new_car = Car(start_pos, map_surface)
        new_car.brain = saved_car.brain.copy()
        new_cars.append(new_car)
        
    # Now fill the rest of the slots with mutated versions of the champion.
    # We pick the absolute best car and create "children" that are slightly different.
    parent = best_cars[0]
    
    while len(new_cars) < len(cars):
        child = Car(start_pos, map_surface)
        child.brain = parent.brain.copy()
        
        # Mutate the child! 
        # This adds random changes to the brain, hoping one of them is a beneficial mutation.
        child.brain.mutate(rate=0.1) # 10% chance to change any given weight
        
        new_cars.append(child)
        
    return new_cars
