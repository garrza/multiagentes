class Message:
    """
    Clase para manejar los mensajes entre agentes.
    """
    environment_buffer = []  # Buffer compartido para almacenar mensajes

    def __init__(self, sender=None, receiver=None, performative=None, content=None):
        self.sender = sender
        self.receiver = receiver
        self.performative = performative
        self.content = content

    def send(self):
        """
        Envía el mensaje al buffer compartido y lo imprime.
        """
        Message.environment_buffer.append(self)
        print(f"[MESSAGE SENT] From: {self.sender.id}, To: {self.receiver.id if self.receiver else 'Broadcast'}, "
              f"Performative: {self.performative}, Content: {self.content}")
