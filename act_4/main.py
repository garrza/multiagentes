import agentpy as ap
from src.agentes.deductive_agent import SavingAgent
import numpy as np

class WealthModel(ap.Model):

    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, SavingAgent)

    def step(self):
        self.agents.step()

    def update(self):
        wealth_values = [agent.wealth for agent in self.agents]
        self.record('Gini Coefficient', self.gini(wealth_values))

    def gini(self, x):
        """Calcula el coeficiente de Gini."""
        x = np.array(x)
        mad = np.abs(np.subtract.outer(x, x)).mean()
        rmad = mad / np.mean(x)
        return 0.5 * rmad

    def end(self):
        self.agents.record('wealth')
        
        
# Parámetros del modelo
parameters = {
    'agents': 50,
    'steps': 50,
}

# Ejecutar el modelo
model = WealthModel(parameters)
results = model.run()