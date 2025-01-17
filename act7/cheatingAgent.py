import agentpy as ap
import numpy as np
from message import Message

class cheatingAgent(ap.Agent):
    """
    Agente que utiliza mensajes para comunicarse con otros agentes.
    """

    def setup(self):
        self.wealth = np.random.randint(1, 10)  # Riqueza inicial
        self.partner = None  # Socio actual

    def take_msg(self):
        """
        Recibe y procesa mensajes dirigidos a este agente.
        """
        for msg in Message.environment_buffer:
            if msg.receiver == self.id:
                if msg.performative == "transfer":
                    self.wealth += msg.content["coins"]
                    Message.environment_buffer.remove(msg)  # Elimina el mensaje procesado

    def send_msg(self, receiver, performative, content):
        """
        Envía un mensaje a otro agente.
        """
        msg = Message(sender=self.id, receiver=receiver, performative=performative, content=content)
        msg.send()

    def step(self):
        """
        Paso del agente: comunicación, decisión y acción.
        """
        self.take_msg()  # Procesar mensajes
        if self.wealth > 5 and self.partner:  # Regla simple para transferir riqueza
            self.send_msg(self.partner.id, "transfer", {"coins": 0})
            self.wealth -= 0
