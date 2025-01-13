# agente de albert

import agentpy as ap

class WealthBDIAgent(ap.Agent):
    """ A BDI agent with wealth """

    def setup(self):
        """ Initialize beliefs, desires, intentions, and plans. """
        self.beliefs = {
            'wealth': 1,  # Agent's current wealth
            'partner': None  # The agent believes a partner exists
        }
        self.desires = []  # List of goals to achieve
        self.intentions = []  # Committed actions or plans
        self.plan = []  # Steps to execute

    def perceive(self):
        """ Update beliefs based on the environment. """
        partner = self.model.agents.random()
        self.beliefs['partner'] = partner

    def deliberate(self):
        """ Update desires based on beliefs. """
        self.desires = []
        if self.beliefs['wealth'] > 0 and self.beliefs['partner'] is not None:
            self.desires.append('transfer_wealth')

    def filter_intentions(self):
        """ Generate intentions from desires. """
        self.intentions = []
        if 'transfer_wealth' in self.desires:
            self.intentions.append(self.transfer_wealth)

    def execute(self):
        """ Execute the current plan or generate a new one. """
        if not self.plan and self.intentions:
            # Generate a plan for the first intention
            self.plan = [self.intentions.pop()]
        
        if self.plan:
            action = self.plan.pop(0)
            action()  # Execute the action

    def step(self):
        """ Perception, deliberation, intention formation, and execution. """
        self.perceive()  # Update beliefs
        self.deliberate()  # Formulate desires
        self.filter_intentions()  # Create intentions
        self.execute()  # Execute actions

    def transfer_wealth(self):
        """ Action to transfer wealth to a partner. """
        partner = self.beliefs['partner']
        if partner:
            partner.beliefs['wealth'] += 1
            self.beliefs['wealth'] -= 1
