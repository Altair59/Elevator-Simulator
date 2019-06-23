"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any

import algorithms
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)
    data-record: a dictionary used to represent some statistical data needed
    during runtime of simulation
    """
    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]
    data_record: Any

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration.
        """
        self.data_record = {"total_people_arrived": 0,
                            "total_people_completed": 0, "total_round": 0,
                            "time_record": []}
        self.num_floors = config["num_floors"]
        self.arrival_generator = config["arrival_generator"]
        self.moving_algorithm = config["moving_algorithm"]

        self.elevators = []
        for i in range(0, config["num_elevators"]):
            self.elevators.append(
                Elevator(config["elevator_capacity"]))

        self.waiting = {}
        for i in range(1, self.num_floors + 1):
            self.waiting[i] = []

        # Initialize the visualizer.
        # Note that this should be called *after* the other attributes
        # have been initialized.
        self.visualizer = Visualizer(self.elevators, self.num_floors,
                                     config['visualize'])

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Increment everyone's wait time by 1
            for floor in self.waiting:
                for passenger in self.waiting[floor]:
                    passenger.record_wait()

            for elevator in self.elevators:
                for passenger in elevator.passengers:
                    passenger.record_wait()

            # Record current round
            self.data_record["total_round"] += 1

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """
        generate arrivals by calling arrival_generator class
        create the waiting at first
        display effects
        increment total-people_arrived upon arrival
        """
        generated_list = self.arrival_generator.generate(round_num)

        # record arrival data
        for floor in generated_list:
            self.waiting[floor].extend(generated_list[floor])
            self.data_record["total_people_arrived"] += len(
                generated_list[floor])

        self.visualizer.show_arrivals(generated_list)

    def _handle_leaving(self) -> None:
        """
        Handle people leaving elevators.
        display effects
        increment total_people_completed upon disembarking
        """
        for elevator in self.elevators:
            all_disembark = elevator.disembark()

            # record wait time for each passenger who disembarked
            for passenger in all_disembark:
                self.visualizer.show_disembarking(passenger, elevator)
                self.data_record["time_record"].append(passenger.wait_time)

            self.data_record["total_people_completed"] += len(all_disembark)

    def _handle_boarding(self) -> None:
        """
        Handle boarding of people and visualize.
        board people until elevator is full or all people are boarded
        in order
        update waiting if successfully board a passenger
        display effects
        """
        for elevator in self.elevators:
            pos = 0
            while pos < len(self.waiting[elevator.floor]):
                passenger = self.waiting[elevator.floor][pos]

                if elevator.board(passenger):
                    self.waiting[elevator.floor].remove(passenger)
                    self.visualizer.show_boarding(passenger, elevator)
                    pos -= 1
                else:
                    break
                pos += 1

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.

        Use this simulation's moving algorithm to move the elevators.
        """
        self.visualizer.show_elevator_moves(self.elevators,
                                            self.moving_algorithm.move_elevators
                                            (self.elevators, self.waiting,
                                             self.num_floors))

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """
        # if no time has been recorded, which means zero passenger completed
        # append the empty time_record by -1 as instructed
        if len(self.data_record["time_record"]) == 0:
            self.data_record["time_record"].append(-1)

        return {
            'num_iterations': self.data_record["total_round"],
            'total_people': self.data_record["total_people_arrived"],
            'people_completed': self.data_record["total_people_completed"],
            'max_time': max(self.data_record["time_record"]),
            'min_time': min(self.data_record["time_record"]),
            'avg_time': sum(self.data_record["time_record"]) // len(
                self.data_record["time_record"])
        }


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 5,
        'num_elevators': 1,
        'elevator_capacity': 1,
        # This is likely not used.
        'num_people_per_round': 2,
        'arrival_generator': algorithms.FileArrivals(5, 'sample_arrivals.csv'),
        'moving_algorithm': algorithms.ShortSighted(),
        'visualize': True
    }

    sim = Simulation(config)
    stats = sim.run(20)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    # print(sample_run())

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
        'max-nested-blocks': 4,
        'max-attributes': 12,
        'disable': ['R0201']
    })
