import agentpy as ap

class WealthBDIAgent(ap.Agent):
    """Agente BDI para manejo de riqueza."""

    def setup(self):
        """Inicializa creencias, deseos, intenciones y planes."""
        self.wealth = self.model.random.randint(1, 10)  # Riqueza inicial aleatoria
        self.beliefs = {
            'wealth': self.wealth,
            'partner': None,
            'market_condition': 'stable'
        }
        self.desires = []
        self.intentions = []
        self.plan = []
        self.type = 'bdi'  # Identificador del tipo de agente

    def perceive(self):
        """Actualiza creencias basadas en el ambiente."""
        # Filtra para no seleccionarse a sí mismo como socio
        possible_partners = [agent for agent in self.model.agents if agent.id != self.id]
        if possible_partners:
            partner = self.model.random.choice(possible_partners)
            self.beliefs['partner'] = partner
            self.beliefs['wealth'] = self.wealth

    def deliberate(self):
        """Actualiza deseos basados en creencias."""
        self.desires = []
        
        # Deseo de transferir si tiene suficiente riqueza
        if self.beliefs['wealth'] > 3 and self.beliefs['partner'] is not None:
            self.desires.append('transfer_wealth')
        
        # Deseo de ahorrar si tiene poca riqueza
        if self.beliefs['wealth'] <= 3:
            self.desires.append('save_wealth')

    def filter_intentions(self):
        """Genera intenciones a partir de deseos."""
        self.intentions = []
        for desire in self.desires:
            if desire == 'transfer_wealth':
                self.intentions.append(self.transfer_wealth)
            elif desire == 'save_wealth':
                self.intentions.append(self.save_wealth)

    def execute(self):
        """Ejecuta el plan actual o genera uno nuevo."""
        if not self.plan and self.intentions:
            self.plan = [self.intentions.pop(0)]
        
        if self.plan:
            action = self.plan.pop(0)
            action()

    def transfer_wealth(self):
        """Acción para transferir riqueza a un socio."""
        partner = self.beliefs['partner']
        if partner and self.wealth > 0:
            transfer_amount = 1
            partner.wealth += transfer_amount
            self.wealth -= transfer_amount
            self.beliefs['wealth'] = self.wealth
            print(f"Agente BDI {self.id} transfirió {transfer_amount} a Agente {partner.id}")

    def save_wealth(self):
        """Acción para ahorrar riqueza."""
        print(f"Agente BDI {self.id} decide ahorrar. Riqueza actual: {self.wealth}")

    def step(self):
        """Ciclo del agente: percepción, deliberación, formación de intenciones y ejecución."""
        self.perceive()
        self.deliberate()
        self.filter_intentions()
        self.execute()