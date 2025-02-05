from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple


class AgentType(Enum):
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"
    TRAFFIC_LIGHT = "traffic_light"


class AgentPersonality(Enum):
    AGGRESSIVE = "aggressive"
    PATIENT = "patient"
    IMPULSIVE = "impulsive"
    CAUTIOUS = "cautious"


@dataclass
class GameOutcome:
    description: str
    utility_player1: float
    utility_player2: float

    @property
    def social_welfare(self) -> float:
        return self.utility_player1 + self.utility_player2


class TrafficGame:
    def __init__(self, name: str, player1_type: AgentType, player2_type: AgentType):
        self.name = name
        self.player1_type = player1_type
        self.player2_type = player2_type
        self.payoff_matrix: Dict[Tuple[str, str], GameOutcome] = {}
        self.preference_chain: List[Tuple[str, str]] = []

    def add_outcome(self, action1: str, action2: str, outcome: GameOutcome):
        self.payoff_matrix[(action1, action2)] = outcome

    def get_outcome(self, action1: str, action2: str) -> GameOutcome:
        return self.payoff_matrix.get((action1, action2))

    def set_preference_chain(self, chain: List[Tuple[str, str]]):
        self.preference_chain = chain

    def find_nash_equilibrium(self) -> List[Tuple[str, str]]:
        nash_equilibria = []
        actions1 = set(a1 for a1, _ in self.payoff_matrix.keys())
        actions2 = set(a2 for _, a2 in self.payoff_matrix.keys())

        for a1 in actions1:
            for a2 in actions2:
                # Check if this strategy pair is a Nash equilibrium
                current_outcome = self.get_outcome(a1, a2)
                if not current_outcome:
                    continue

                # Check if player 1 can improve by deviating
                can_improve1 = any(
                    self.get_outcome(other_a1, a2).utility_player1
                    > current_outcome.utility_player1
                    for other_a1 in actions1
                    if other_a1 != a1
                )

                # Check if player 2 can improve by deviating
                can_improve2 = any(
                    self.get_outcome(a1, other_a2).utility_player2
                    > current_outcome.utility_player2
                    for other_a2 in actions2
                    if other_a2 != a2
                )

                if not can_improve1 and not can_improve2:
                    nash_equilibria.append((a1, a2))

        return nash_equilibria

    def find_pareto_optimal(self) -> List[Tuple[str, str]]:
        pareto_optimal = []
        strategy_pairs = list(self.payoff_matrix.keys())

        for s1 in strategy_pairs:
            outcome1 = self.get_outcome(*s1)
            is_pareto_optimal = True

            for s2 in strategy_pairs:
                if s1 == s2:
                    continue

                outcome2 = self.get_outcome(*s2)
                # Check if outcome2 dominates outcome1
                if (
                    outcome2.utility_player1 >= outcome1.utility_player1
                    and outcome2.utility_player2 >= outcome1.utility_player2
                    and (
                        outcome2.utility_player1 > outcome1.utility_player1
                        or outcome2.utility_player2 > outcome1.utility_player2
                    )
                ):
                    is_pareto_optimal = False
                    break

            if is_pareto_optimal:
                pareto_optimal.append(s1)

        return pareto_optimal

    def find_maximum_social_welfare(self) -> Tuple[Tuple[str, str], float]:
        max_welfare = float("-inf")
        best_strategy = None

        for strategy, outcome in self.payoff_matrix.items():
            welfare = outcome.social_welfare
            if welfare > max_welfare:
                max_welfare = welfare
                best_strategy = strategy

        return best_strategy, max_welfare


# Define the four game scenarios
def create_vehicle_intersection_game() -> TrafficGame:
    """Game 1: Two vehicles at intersection without traffic light"""
    game = TrafficGame("Vehicle Intersection", AgentType.VEHICLE, AgentType.VEHICLE)

    # Actions: "proceed" or "yield"
    game.add_outcome(
        "proceed", "proceed", GameOutcome("Collision", -10, -10)
    )  # Both lose severely
    game.add_outcome(
        "proceed", "yield", GameOutcome("First vehicle passes", 5, 2)
    )  # First gains more, second loses less
    game.add_outcome(
        "yield", "proceed", GameOutcome("Second vehicle passes", 2, 5)
    )  # Vice versa
    game.add_outcome(
        "yield", "yield", GameOutcome("Deadlock", 0, 0)
    )  # Neutral but inefficient

    game.set_preference_chain(
        [
            ("yield", "proceed"),  # Most preferred - safe passage
            ("proceed", "yield"),  # Also good - safe passage
            ("yield", "yield"),  # Suboptimal but safe
            ("proceed", "proceed"),  # Worst - collision
        ]
    )

    return game


def create_pedestrian_vehicle_game() -> TrafficGame:
    """Game 2: Pedestrian crossing while vehicle approaches"""
    game = TrafficGame("Pedestrian Crossing", AgentType.PEDESTRIAN, AgentType.VEHICLE)

    # Actions: "cross"/"stop" for pedestrian, "proceed"/"brake" for vehicle
    game.add_outcome(
        "cross", "proceed", GameOutcome("Collision risk", -15, -10)
    )  # Both lose severely, pedestrian more
    game.add_outcome(
        "cross", "brake", GameOutcome("Safe pedestrian crossing", 5, -1)
    )  # Pedestrian wins, vehicle minor inconvenience
    game.add_outcome(
        "stop", "proceed", GameOutcome("Vehicle passes first", 2, 5)
    )  # Vehicle wins, pedestrian waits
    game.add_outcome(
        "stop", "brake", GameOutcome("Unnecessary stop", 0, -2)
    )  # Inefficient outcome

    game.set_preference_chain(
        [
            ("stop", "proceed"),  # Most preferred - clear priority
            ("cross", "brake"),  # Also good - safe crossing
            ("stop", "brake"),  # Inefficient but safe
            ("cross", "proceed"),  # Worst - danger
        ]
    )

    return game


def create_emergency_red_light_game() -> TrafficGame:
    """Game 3: Vehicle at prolonged red light with urgency"""
    game = TrafficGame(
        "Emergency at Red Light", AgentType.VEHICLE, AgentType.TRAFFIC_LIGHT
    )

    # Actions: "wait"/"run_light" for vehicle, "stay_red"/"change_green" for light
    game.add_outcome(
        "run_light", "stay_red", GameOutcome("Running red light", -5, -8)
    )  # Both lose - safety risk and rule violation
    game.add_outcome(
        "run_light", "change_green", GameOutcome("Light changes just in time", 5, 5)
    )  # Win-win
    game.add_outcome(
        "wait", "stay_red", GameOutcome("Continued waiting", -3, 2)
    )  # Vehicle loses time, light maintains order
    game.add_outcome(
        "wait", "change_green", GameOutcome("Normal operation", 3, 3)
    )  # Satisfactory for both

    game.set_preference_chain(
        [
            ("wait", "change_green"),  # Most preferred - orderly
            ("run_light", "change_green"),  # Good timing
            ("wait", "stay_red"),  # Frustrating but safe
            ("run_light", "stay_red"),  # Worst - dangerous
        ]
    )

    return game


def create_pedestrian_light_request_game() -> TrafficGame:
    """Game 4: Pedestrian requesting light change"""
    game = TrafficGame(
        "Pedestrian Light Request", AgentType.PEDESTRIAN, AgentType.TRAFFIC_LIGHT
    )

    # Actions: "request"/"jaywalk" for pedestrian, "respond"/"ignore" for light
    game.add_outcome(
        "request", "respond", GameOutcome("Proper crossing", 5, 5)
    )  # Win-win
    game.add_outcome(
        "request", "ignore", GameOutcome("Frustrated waiting", -2, 2)
    )  # Pedestrian loses, light maintains schedule
    game.add_outcome(
        "jaywalk", "respond", GameOutcome("Unnecessary light change", 2, -1)
    )  # Inefficient
    game.add_outcome(
        "jaywalk", "ignore", GameOutcome("Unsafe crossing", -5, -5)
    )  # Lose-lose

    game.set_preference_chain(
        [
            ("request", "respond"),  # Most preferred - proper operation
            ("request", "ignore"),  # Maintaining order
            ("jaywalk", "respond"),  # Inefficient
            ("jaywalk", "ignore"),  # Worst - unsafe
        ]
    )

    return game
