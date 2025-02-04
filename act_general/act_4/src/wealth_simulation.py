import agentpy as ap
import numpy as np

from act_4.src.agentes.saving_agent import SavingAgent
from act_4.src.agentes.wealth_bdi_agent import WealthBDIAgent


class WealthSimulation(ap.Model):
    """Modelo de simulación que combina agentes deductivos y BDI."""
    
    def setup(self):
        """Inicializa el modelo de simulación."""
        self.n_deductive = self.p.get('n_deductive', 2)
        self.n_bdi = self.p.get('n_bdi', 2)
        
        deductive_agents = [SavingAgent(self) for _ in range(self.n_deductive)]
        bdi_agents = [WealthBDIAgent(self) for _ in range(self.n_bdi)]
        
        self.agents = ap.AgentList(self, deductive_agents + bdi_agents)

    def step(self):
        """Ejecuta un paso de la simulación."""
        self.agents.step()
        
        deductive_wealth = [a.wealth for a in self.agents if a.type == 'deductive']
        bdi_wealth = [a.wealth for a in self.agents if a.type == 'bdi']
        
        avg_deductive = np.mean(deductive_wealth) if deductive_wealth else 0
        avg_bdi = np.mean(bdi_wealth) if bdi_wealth else 0
        
        self.record('Riqueza_promedio_Deductivos', avg_deductive)
        self.record('Riqueza_promedio_BDI', avg_bdi)
        
    def end(self):
        """Finaliza la simulación y reporta resultados."""
        print("\nResultados finales:")
        for agent in self.agents:
            print(f"Agente {agent.type} {agent.id}: Riqueza final = {agent.wealth}")