import agentpy as ap
import numpy as np
from communicativeAgent import CommunicativeAgent
from richAgent import RichAgent
from cheatingAgent import cheatingAgent


class CommunicationModel(ap.Model):
    """
    Modelo de simulación con agentes comunicándose mediante mensajes.
    """

    def setup(self):
        # Crear agentes
        self.agents = ap.AgentList(self, self.p.agents, CommunicativeAgent)

        # Asignar socios al azar
        for agent in self.agents:
            agent.partner = self.agents.random()  # Asignar un socio aleatorio

    def step(self):
        """Ejecutar un paso para todos los agentes."""
        self.agents.step()

    def update(self):
        """Registrar estadísticas."""
        wealths = [agent.wealth for agent in self.agents]
        self.record("Average Wealth", np.mean(wealths))

    def end(self):
        """Finalizar y registrar la riqueza."""
        self.agents.record("wealth")


# Configuración del modelo
parameters = {
    'agents': 10,  # Número de agentes
    'steps': 20,   # Número de pasos
}

# Ejecutar el modelo
model = CommunicationModel(parameters)
results = model.run()

# Gráficos
import matplotlib.pyplot as plt
plt.plot(results.variables.CommunicationModel["Average Wealth"])
plt.xlabel("Steps")
plt.ylabel("Average Wealth")
plt.title("Wealth Over Time")
plt.show()
