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

    def __str__(self):
        return f"Sender: {self.sender}, Receiver: {self.receiver}, Performative: {self.performative}, Content: {self.content}"

    def send(self):
        """Envía el mensaje al buffer del entorno."""
        Message.environment_buffer.append(self)
