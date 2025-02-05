from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class GameOutcome:
    description: str
    utility_player1: int
    utility_player2: int

@dataclass
class GameScenario:
    name: str
    description: str
    player1_type: str
    player2_type: str
    actions_player1: List[str]
    actions_player2: List[str]
    payoff_matrix: Dict[Tuple[str, str], GameOutcome]
    
    def get_nash_equilibria(self) -> List[Tuple[str, str]]:
        """Find Nash equilibria in the game"""
        equilibria = []
        for action1 in self.actions_player1:
            for action2 in self.actions_player2:
                if self._is_nash_equilibrium(action1, action2):
                    equilibria.append((action1, action2))
        return equilibria
    
    def _is_nash_equilibrium(self, action1: str, action2: str) -> bool:
        """Check if given action pair is a Nash equilibrium"""
        # Check if player 1 can improve by changing strategy
        current_outcome = self.payoff_matrix[(action1, action2)]
        for alt_action in self.actions_player1:
            if alt_action != action1:
                alt_outcome = self.payoff_matrix[(alt_action, action2)]
                if alt_outcome.utility_player1 > current_outcome.utility_player1:
                    return False
                    
        # Check if player 2 can improve by changing strategy
        for alt_action in self.actions_player2:
            if alt_action != action2:
                alt_outcome = self.payoff_matrix[(action1, alt_action)]
                if alt_outcome.utility_player2 > current_outcome.utility_player2:
                    return False
                    
        return True

# Define game scenarios
GAME_SCENARIOS = [
    GameScenario(
        name="Vehicle-Vehicle Intersection",
        description="Two vehicles approach intersection without traffic light",
        player1_type="Vehicle",
        player2_type="Vehicle",
        actions_player1=["stop", "proceed"],
        actions_player2=["stop", "proceed"],
        payoff_matrix={
            ("stop", "stop"): GameOutcome("Both wait", -1, -1),
            ("stop", "proceed"): GameOutcome("P1 waits, P2 goes", -2, 2),
            ("proceed", "stop"): GameOutcome("P1 goes, P2 waits", 2, -2),
            ("proceed", "proceed"): GameOutcome("Collision risk", -10, -10)
        }
    ),
    GameScenario(
        name="Pedestrian-Vehicle Crossing",
        description="Pedestrian wants to cross while vehicle approaches",
        player1_type="Pedestrian",
        player2_type="Vehicle",
        actions_player1=["wait", "cross"],
        actions_player2=["stop", "continue"],
        payoff_matrix={
            ("wait", "stop"): GameOutcome("Safe crossing opportunity", 1, -1),
            ("wait", "continue"): GameOutcome("Vehicle passes first", 0, 2),
            ("cross", "stop"): GameOutcome("Safe crossing", 2, -2),
            ("cross", "continue"): GameOutcome("Dangerous situation", -20, -15)
        }
    ),
    # Add more scenarios...
] 