"""CSC148 Assignment 1 - People and Elevators

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains classes for the two "basic" entities in this simulation:
people and elevators. We have provided basic outlines of these two classes
for you; you are responsible for implementing these two classes so that they
work with the rest of the simulation.

You may NOT change any existing attributes, or the interface for any public
methods we have provided. However, you can (and should) add new attributes,
and of course you'll have to implement the methods we've provided, as well
as add your own methods to complete this assignment.

Finally, note that Person and Elevator each inherit from a kind of sprite found
in sprites.py; this is to enable their instances to be visualized properly.
You may not change sprites.py, but are responsible for reading the documentation
to understand these classes, as well as the abstract methods your classes must
implement.
"""
from __future__ import annotations
from typing import List
from sprites import PersonSprite, ElevatorSprite


class Elevator(ElevatorSprite):
    """An elevator in the elevator simulation.

    Remember to add additional documentation to this class docstring
    as you add new attributes (and representation invariants).

    === Attributes ===
    passengers: A list of the people currently on this elevator
    floor: An int indicating the current floor elevator locates
    capacity: An int restricts the maximum passengers elevator can hold

    === Representation invariants ===
     - capacity should not change
     - 1 <= floor <= 6
    """

    passengers: List[Person]
    floor: int
    capacity: int

    def __init__(self, capacity: int) -> None:
        """
        initialize a new elevator

        Preconditions:
            capacity>=1
        """
        ElevatorSprite.__init__(self)
        self.capacity = capacity
        self.passengers = []
        self.floor = 1

    def disembark(self) -> List[Person]:
        """
        disembark passengers when they arrive at target floor
        make a list of passengers disembarked each round
        and displays leaving effect and do calculations by reference to it
        in Simulation._handle_leaving
        """
        exit_list = []
        for passenger in self.passengers:
            if self.floor == passenger.target:
                exit_list.append(passenger)

        for passenger in exit_list:
            self.passengers.remove(passenger)
        return exit_list

    def board(self, passenger: Person) -> bool:
        """
        board passengers when elevator arrives at their start floor
        if elevator is not full, return successful boolean
        and append the passenger to elevator.passenger
        if full, return failure boolean and do nothing
        """
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            return True
        else:
            return False

    def move(self, direction: int) -> None:
        """
        update the elevator's floor position by adding movement
        direction > 0 means go upwards
        direction < 0 means go downwards
        direction = 0 means stay
        """
        self.floor += direction

    def fullness(self) -> float:
        """
        return a float indicating the fullness of elevator
        used to display effect of elevator sprite
        """
        return len(self.passengers) / self.capacity


class Person(PersonSprite):
    """A person in the elevator simulation.

    === Attributes ===
    start: the floor this person started on
    target: the floor this person wants to go to
    wait_time: the number of rounds this person has been waiting

    === Representation invariants ===
     - 1 <= start <= 6
     - 1<= target <= 6
     - wait_time >= 0
    """
    start: int
    target: int
    wait_time: int = 0

    def __init__(self, start: int, target: int) -> None:
        """
        initialize a new passenger
        """
        PersonSprite.__init__(self)
        self.start = start
        self.target = target

    def record_wait(self) -> None:
        """
        increment wait_time each round
        """
        self.wait_time += 1

    def get_anger_level(self) -> int:
        """Return this person's anger level.

        A person's anger level is based on how long they have been waiting
        before reaching their target floor.
            - Level 0: waiting 0-2 rounds
            - Level 1: waiting 3-4 rounds
            - Level 2: waiting 5-6 rounds
            - Level 3: waiting 7-8 rounds
            - Level 4: waiting >= 9 rounds
        """
        anger_level = None

        if self.wait_time <= 2:
            anger_level = 0
        elif 3 <= self.wait_time <= 4:
            anger_level = 1
        elif 5 <= self.wait_time <= 6:
            anger_level = 2
        elif 7 <= self.wait_time <= 8:
            anger_level = 3
        elif self.wait_time >= 9:
            anger_level = 4

        return anger_level


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['sprites'],
        'max-nested-blocks': 4,
        'max-attributes': 12,
        'disable': ['R0201']
    })
