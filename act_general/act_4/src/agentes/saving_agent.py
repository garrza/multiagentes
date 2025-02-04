import agentpy as ap
import numpy as np

class SavingAgent(ap.Agent):
    """Agente con razonamiento deductivo para ahorro y transferencia de riqueza."""

    def setup(self):
        """Inicialización del agente."""
        self.wealth = np.random.randint(1, 10)  # Asigna riqueza inicial al azar
        self.beliefs = {'partner': None}  # Creencia sobre si hay un socio
        self.actions = [self.transfer_wealth, self.save_wealth]  # Posibles acciones
        self.rules = [self.rule_transfer, self.rule_save]  # Reglas de inferencia
        self.type = 'deductive'  # Identificador del tipo de agente

    def see(self, agents):
        """Función de percepción para actualizar creencias."""
        possible_partners = [agent for agent in agents if agent.id != self.id]
        if possible_partners:
            partner = self.model.random.choice(possible_partners)
            self.beliefs['partner'] = partner

    def next(self):
        """Procesa las reglas para decidir la próxima acción."""
        for action in self.actions:
            for rule in self.rules:
                if rule(action):
                    return action
        return None

    def action(self, act):
        """Ejecuta la acción seleccionada."""
        if act is not None:
            act()

    def rule_transfer(self, act):
        """Regla: Si tengo riqueza suficiente y un socio, transfiero."""
        return (
            self.wealth > 5
            and self.beliefs['partner'] is not None
            and act == self.transfer_wealth
        )

    def rule_save(self, act):
        """Regla: Si tengo poca riqueza, ahorro."""
        return self.wealth <= 5 and act == self.save_wealth

    def transfer_wealth(self):
        """Acción: Transferir riqueza al socio."""
        partner = self.beliefs['partner']
        if partner is not None and self.wealth > 0:
            transfer_amount = 1
            partner.wealth += transfer_amount
            self.wealth -= transfer_amount
            print(f"Agente Deductivo {self.id} transfirió {transfer_amount} a Agente {partner.id}")

    def save_wealth(self):
        """Acción: Ahorrar riqueza (no hacer nada)."""
        print(f"Agente Deductivo {self.id} decide ahorrar. Riqueza actual: {self.wealth}")

    def step(self):
        """Ciclo del agente."""
        self.see(self.model.agents)
        action = self.next()
        self.action(action)