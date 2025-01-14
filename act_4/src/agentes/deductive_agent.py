# agente de dan

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

    def see(self, agents):
        """Función de percepción para actualizar creencias."""
        partner = self.model.random.choice(agents)
        self.beliefs['partner'] = partner  # Actualiza creencia del socio

    def next(self):
        """Procesa las reglas para decidir la próxima acción."""
        for action in self.actions:
            for rule in self.rules:
                if rule(action):
                    return action  # Devuelve la acción validada por la regla
        return None  # No se toma acción si ninguna regla aplica

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
        if partner is not None:
            partner.wealth += 1
            self.wealth -= 1

    def save_wealth(self):
        """Acción: Ahorrar riqueza (no hacer nada)."""
        pass

    def step(self):
        """Ciclo del agente."""
        self.see(self.model.agents)  # Percepción
        action = self.next()  # Decisión
        self.action(action)  # Ejecución