import agentpy as ap
from hybrid_agent import HybridAgent  # Importa el agente híbrido
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class HybridModel(ap.Model):
    """Modelo para simular agentes híbridos únicamente."""

    def setup(self):
        """Configura los agentes y las condiciones iniciales del modelo."""
        # Crear una lista de agentes híbridos
        self.agents = ap.AgentList(self, self.p.agents, HybridAgent)

    def step(self):
        """Ejecuta un ciclo de vida para todos los agentes."""
        self.agents.step()

    def update(self):
        """Actualiza las estadísticas del modelo."""
        # Registrar riqueza promedio
        wealth_values = [agent.wealth for agent in self.agents]
        self.record("Avg Wealth", np.mean(wealth_values))

    def gini(self, x):
        """Calcula el coeficiente de Gini."""
        x = np.array(x)
        mad = np.abs(np.subtract.outer(x, x)).mean()
        rmad = mad / np.mean(x)
        return 0.5 * rmad

    def end(self):
        """Finaliza la simulación registrando los resultados."""
        self.agents.record("wealth")


# Parámetros del modelo
parameters = {
    'agents': 50,  # Número de agentes híbridos
    'steps': 50,   # Número de pasos
}

# Ejecutar el modelo
model = HybridModel(parameters)
results = model.run()

# Analizar resultados
# Histograma de distribución de riqueza final
final_wealth = [agent.wealth for agent in model.agents]
sns.histplot(final_wealth, color="green", kde=True)
plt.xlabel("Wealth")
plt.ylabel("Frequency")
plt.title("Final Wealth Distribution (Hybrid Agents)")
plt.show()
