from message import Message
import agentpy as ap
import numpy as np


class WealthAgent(ap.Agent):
    """
    Wealth agent que utiliza el protocolo CNET para negociar y ejecutar tareas.
    """

    def setup(self):
        self.wealth = np.random.randint(1, 10)  # Riqueza inicial asegurada
        self.role = "worker"  # Todos los agentes son workers por defecto
        self.tasks = []  # Tareas asignadas
        print(f"[SETUP] Agent {self.id} initialized with wealth {self.wealth} and role {self.role}")

    def call_for_proposals(self, task):
        """
        Envia un mensaje call-for-proposal a otros agentes.
        """
        print(f"[CALL-FOR-PROPOSALS] Manager {self.id} announces task: {task}")
        for agent in self.model.agents:
            if agent != self:  # Excluirse a sí mismo
                Message(sender=self, receiver=agent, performative="call-for-proposal", content=task).send()

    def evaluate_task(self, task):
        """
        Evalúa el costo de realizar una tarea.
        """
        cost = abs(task["amount"] - self.wealth)
        print(f"[EVALUATE] Agent {self.id} evaluated task {task} with cost {cost}")
        return cost

    def send_proposal(self, task, sender):
        """
        Envia una propuesta al manager para realizar la tarea.
        """
        cost = self.evaluate_task(task)
        Message(sender=self, receiver=sender, performative="propose", content={"cost": cost}).send()
        print(f"[PROPOSE] Worker {self.id} proposes to Manager {sender.id} with cost {cost}")

    def perform_task(self, task):
        """
        Realiza la tarea asignada (transferir riqueza).
        """
        if self.wealth >= task["amount"]:  # Verificar si tiene suficiente riqueza
            self.wealth -= task["amount"]
            task["receiver"].wealth += task["amount"]
            print(f"[PERFORM-TASK] Worker {self.id} transferred {task['amount']} to Agent {task['receiver'].id}")
        else:
            print(f"[PERFORM-TASK FAILED] Worker {self.id} could not perform task due to insufficient wealth")

    def step(self):
        """
        Procesa los mensajes y toma acciones basadas en el rol.
        """
        if self.role == "manager":
            # Como manager, crear y anunciar una tarea
            if not self.tasks:  # Si no hay tareas pendientes
                # Filtrar agentes que no sean el manager (self)
                potential_receivers = [agent for agent in self.model.agents if agent != self]
                receiver = self.model.random.choice(potential_receivers)  # Seleccionar un receptor aleatorio
                task = {
                    "amount": np.random.randint(1, 5),  # Cantidad de riqueza a transferir
                    "receiver": receiver
                }
                self.tasks.append(task)
                self.call_for_proposals(task)  # Anunciar la tarea
            else:
                # Evaluar propuestas en el buffer de mensajes
                proposals = [msg for msg in Message.environment_buffer if msg.receiver == self and msg.performative == "propose"]
                if proposals:
                    best_proposal = min(proposals, key=lambda x: x.content["cost"])
                    Message.environment_buffer.remove(best_proposal)  # Eliminar propuesta seleccionada
                    Message(
                        sender=self,
                        receiver=best_proposal.sender,
                        performative="accept-proposal",
                        content=self.tasks.pop(0)
                    ).send()
                    print(f"[ACCEPT-PROPOSAL] Manager {self.id} accepted proposal from Worker {best_proposal.sender.id}")

        elif self.role == "worker":
            # Como worker, responder a solicitudes de tareas
            for msg in Message.environment_buffer:
                if msg.receiver == self and msg.performative == "call-for-proposal":
                    self.send_proposal(msg.content, msg.sender)
                elif msg.receiver == self and msg.performative == "accept-proposal":
                    self.perform_task(msg.content)
                    Message(
                        sender=self,
                        receiver=msg.sender,
                        performative="inform",
                        content="Task completed"
                    ).send()
