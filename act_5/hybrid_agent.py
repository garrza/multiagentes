import agentpy as ap
import numpy as np

class HybridAgent(ap.Agent):
    """Agente híbrido con razonamiento reactivo y deliberativo."""

    def setup(self):
        self.wealth = np.random.randint(1, 10)  # Asigna riqueza inicial al azar
        self.beliefs = {'partner': None}  # Creencias del agente
        self.actions = [self.transfer_wealth, self.save_wealth]  # Acciones posibles

    def see(self, agents):
        """Percibe el entorno y actualiza sus creencias."""
        partner = self.model.random.choice(agents)
        self.beliefs['partner'] = partner

    def react(self):
        """Capa reactiva: toma decisiones rápidas."""
        if self.wealth < 3:
            return self.save_wealth  # Prioriza ahorrar si la riqueza es baja

    def deliberate(self):
        """Capa deliberativa: toma decisiones planeadas."""
        if self.beliefs['partner'] is not None and self.wealth > 5:
            return self.transfer_wealth  # Planea transferir si tiene suficiente riqueza

    def integrate(self):
        """Integra las capas reactiva y deliberativa."""
        reactive_action = self.react()
        if reactive_action:
            return reactive_action  # La capa reactiva tiene prioridad
        return self.deliberate()  # Si no hay urgencia, usa la capa deliberativa

    def transfer_wealth(self):
        """Acción: Transferir riqueza."""
        partner = self.beliefs['partner']
        if partner is not None:
            partner.wealth += 1
            self.wealth -= 1

    def save_wealth(self):
        """Acción: Ahorrar riqueza."""
        pass

    def step(self):
        """Ciclo del agente."""
        self.see(self.model.agents)  # Percepción
        action = self.integrate()  # Decisión híbrida
        if action:
            action()  # Ejecuta la acción seleccionada
