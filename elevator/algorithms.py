"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithsm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    num_people: Optional[int]
    max_floor: int

    def __init(self, max_floor: int, num_people: Optional[int]) -> None:
        """
        initialize a RandomArrivals

        Precondition:
            max_floor>=2
            num_people is None or num_people>=0
        """
        ArrivalGenerator.__init__(self, max_floor, num_people)

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """
        create a dict and stores person given by
        pairs of random start and target
        """
        if self.num_people is None:
            self.num_people = 0

        generated = {}
        for i in range(1, self.max_floor + 1):
            generated[i] = []

        for i in range(0, self.num_people):
            start = random.randint(1, self.max_floor)
            target = random.randint(1, self.max_floor)
            while target == start:
                target = random.randint(1, self.max_floor)
            generated[start].append(Person(start, target))

        return generated


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    filename: the name of sample_arrivals we want to import

    generate_list: The dict where read data from filename is written to

    === Representation Invariants ===
    max_floor >= 2
    filename should not be change
    """
    filename: str
    max_floor: int
    generate_list: Dict[int, Dict[int, List[Person]]]

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
        """
        ArrivalGenerator.__init__(self, max_floor, None)
        self.generate_list = {}

        # We've provided some of the "reading from csv files" boilerplate code
        # for you to help you get started.
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                data = list(map(int, line))
                round_ = data[0]
                self.generate_list[round_] = {}

                for i in range(1, self.max_floor + 1):
                    self.generate_list[round_][i] = []

                person_index = 1
                while person_index < len(data):
                    start = data[person_index]
                    target = data[person_index + 1]
                    self.generate_list[round_][start].append(
                        Person(start, target))
                    person_index += 2

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """
        take in a round_num and if it's key in generate_list
        then return the value it matches
        """
        if round_num in self.generate_list:
            return self.generate_list[round_num]
        else:
            return {}


###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """

    @staticmethod
    def get_motion_direction(elevator_floor: int,
                             target_floor: Optional[int]) -> int:
        """
        a static method determines whether elevator should
        go upwards or downwards or stay
        according to its relative position to target
        """
        if target_floor is None:
            return 0
        elif elevator_floor - target_floor < 0:
            return 1
        else:
            return -1

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that picks a random direction for each elevator.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]], max_floor: int) -> \
            List[Direction]:
        """
        move each elevator randomly, which may go up, down, or stay
        using random int generator
        move elevators with these values
        records the directions and return a collective list of them
        """
        directions = []

        for elevator in elevators:
            direction = random.randint(-1, 1)
            while not 1 <= elevator.floor + direction <= max_floor:
                direction = random.randint(-1, 1)

            elevator.move(direction)
            directions.append(Direction(direction))

        return directions


class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]], max_floor: int) -> \
            List[Direction]:
        """
        for each elevator:
        if it's empty, loop through(low to high) waiting to find
        the first lowest floor having someone waiting,
        and move towards that floor by 1
        if no one waiting, moves default direction which is 0, means stay
        if not empty, just move towards first passenger's target by 1
        return the records of movement
        """
        directions = []
        for elevator in elevators:
            direction = 0
            if elevator.fullness() == 0.0:
                for floor in waiting:
                    if len(waiting[floor]) > 0:
                        direction = MovingAlgorithm.get_motion_direction(
                            elevator.floor, floor)
                        break
            else:
                direction = MovingAlgorithm.get_motion_direction(
                    elevator.floor, elevator.passengers[0].target)

            elevator.move(direction)
            directions.append(Direction(direction))

        return directions


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """

    def move_elevators(self, elevators: List[Elevator],
                       waiting: Dict[int, List[Person]], max_floor: int) -> \
            List[Direction]:

        """
        for each elevator:
        if it's empty, move towards the closest floor that has someone waiting,
        by looping through waiting to find the floor with minimum difference and
        having waiting person
        if not empty, moves towards the closest target floor of
        all passengers who are on the elevator
        by calculating each passenger's target's distance to current floor and
        select the closest to go
        return the records of movement
        """
        directions = []
        for elevator in elevators:
            if elevator.fullness() == 0.0:
                min_distance = 2147483647
                target_floor = None

                for floor in waiting:
                    if len(waiting[floor]) == 0:
                        continue

                    difference = floor - elevator.floor

                    if abs(difference) < abs(
                            min_distance):
                        min_distance = difference
                        target_floor = floor

                    # to break the tie, we will choose the floor which has
                    # a negative difference(below elevator.floor)
                    elif abs(difference) == abs(
                            min_distance) and difference < min_distance:
                        min_distance = difference
                        target_floor = floor

                direction = MovingAlgorithm.get_motion_direction(
                    elevator.floor, target_floor)
            else:
                min_distance = 2147483647
                target_floor = None

                for passenger in elevator.passengers:
                    difference = passenger.target - elevator.floor

                    if abs(difference) < abs(min_distance):
                        min_distance = difference
                        target_floor = passenger.target

                    # to break the tie, we will choose the floor which has
                    # a negative difference(below elevator.floor)
                    elif abs(difference) == abs(
                            min_distance) and difference < min_distance:
                        min_distance = difference
                        target_floor = passenger.target

                direction = MovingAlgorithm.get_motion_direction(
                    elevator.floor, target_floor)

            elevator.move(direction)
            directions.append(Direction(direction))

        return directions


if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'disable': ['R0201']
    })
