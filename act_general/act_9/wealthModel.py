from wealthAgent import WealthAgent
import agentpy as ap
import numpy as np


class WealthModel(ap.Model):
    """
    Modelo para simular agentes WealthAgent utilizando el protocolo CNET.
    """

    def setup(self):
        # Crear agentes y asignar roles
        self.agents = ap.AgentList(self, self.p.num_agents, WealthAgent)
        self.manager = self.agents.random()  # Seleccionar un manager aleatorio
        self.manager.role = "manager"  # Asignar el rol de manager

    def step(self):
        self.agents.step()  # Ejecutar un paso para todos los agentes

    def end(self):
        # Mostrar estado final de los agentes
        for agent in self.agents:
            print(f"[FINAL STATE] Agent {agent.id}: Role: {agent.role}, Final Wealth: {agent.wealth}")
