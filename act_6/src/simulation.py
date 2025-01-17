from typing import List, Dict
from .environment import Environment
from .agents.base import Agent
from .agents.basic_agent import BasicAgent
from .agents.smart_agent import SmartAgent
from .agents.efficient_agent import EfficientAgent
from .agents.collaborative_agent import CollaborativeAgent
from .ontology import (
    create_vacuum_ontology,
    initialize_environment,
    get_cell_at_position,
)


class Simulation:
    def __init__(
        self,
        width: int,
        height: int,
        num_agents: int,
        dirty_percentage: float,
        max_time: int,
        agent_type: str = "mixed",
    ):
        # Create and initialize ontology
        self.onto = create_vacuum_ontology()
        self.environment = Environment(width, height, dirty_percentage)
        self.cells = initialize_environment(self.onto, width, height, dirty_percentage)
        self.agents = self._initialize_agents(num_agents, agent_type)
        self.max_time = max_time
        self.current_time = 0
        self.initial_dirty = self.environment.get_dirty_count()
        self.agent_type = agent_type

    def _initialize_agents(self, num_agents: int, agent_type: str) -> List[Agent]:
        agents = []

        for i in range(num_agents):
            # Create ontology agent instance
            if agent_type == "mixed":
                agent_class = (
                    self.onto.BasicAgent
                    if i % 4 == 0
                    else (
                        self.onto.SmartAgent
                        if i % 4 == 1
                        else (
                            self.onto.EfficientAgent
                            if i % 4 == 2
                            else self.onto.CollaborativeAgent
                        )
                    )
                )
            elif agent_type == "collaborative":
                agent_class = self.onto.CollaborativeAgent
            else:
                agent_class = (
                    self.onto.BasicAgent
                    if i % 3 == 0
                    else (
                        self.onto.SmartAgent if i % 3 == 1 else self.onto.EfficientAgent
                    )
                )

            onto_agent = agent_class(f"agent_{i}")

            # Initialize agent position
            initial_pos = (0, 0)  # You might want to randomize this
            onto_agent.has_position = [get_cell_at_position(self.onto, *initial_pos)]

            # Create corresponding Python agent
            if isinstance(onto_agent, self.onto.BasicAgent):
                agent = BasicAgent(initial_pos, onto_agent)
            elif isinstance(onto_agent, self.onto.SmartAgent):
                agent = SmartAgent(initial_pos, onto_agent)
            elif isinstance(onto_agent, self.onto.EfficientAgent):
                agent = EfficientAgent(initial_pos, onto_agent)
            else:
                agent = CollaborativeAgent(initial_pos, onto_agent)

            agents.append(agent)

        return agents

    def run(self) -> Dict:
        while (
            self.current_time < self.max_time and self.environment.get_dirty_count() > 0
        ):
            for agent in self.agents:
                perception = agent.see(self.environment)
                action = agent.next(perception)
                agent.action(action, self.environment)
                agent.update_ontology()  # Update ontology after each action

            self.current_time += 1

        # Calculate statistics
        total_moves = sum(agent.moves_count for agent in self.agents)
        total_cleaned = sum(agent.cells_cleaned for agent in self.agents)
        remaining_dirty = self.environment.get_dirty_count()
        cleaning_efficiency = (
            (total_cleaned / total_moves * 100) if total_moves > 0 else 0
        )

        return {
            "initial_dirty": self.initial_dirty,
            "remaining_dirty": remaining_dirty,
            "cleaned_cells": total_cleaned,
            "total_moves": total_moves,
            "time_steps": self.current_time,
            "cleaning_efficiency": cleaning_efficiency,
        }

    def _get_statistics(self) -> Dict:
        total_moves = sum(agent.moves_count for agent in self.agents)
        total_cleaned = sum(agent.cells_cleaned for agent in self.agents)
        remaining_dirty = self.environment.get_dirty_count()
        cleaning_efficiency = (
            (total_cleaned / total_moves * 100) if total_moves > 0 else 0
        )

        return {
            "initial_dirty": self.initial_dirty,
            "remaining_dirty": remaining_dirty,
            "cleaned_cells": total_cleaned,
            "total_moves": total_moves,
            "time_steps": self.current_time,
            "cleaning_efficiency": cleaning_efficiency,
        }
