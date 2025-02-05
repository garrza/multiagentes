from enum import Enum
from typing import List, Optional, Dict
from dataclasses import dataclass
import graphviz


class MessageType(Enum):
    REQUEST = "request"
    PROPOSE = "propose"
    ACCEPT = "accept"
    REJECT = "reject"
    INFORM = "inform"
    QUERY = "query"
    CONFIRM = "confirm"


@dataclass
class Message:
    sender: str
    receiver: str
    msg_type: MessageType
    content: str
    timestamp: float


class InteractionProtocol:
    def __init__(self, name: str):
        self.name = name
        self.participants: List[str] = []
        self.messages: List[Message] = []
        self.states: Dict[str, str] = {}  # participant -> current state

    def add_participant(self, participant: str):
        if participant not in self.participants:
            self.participants.append(participant)
            self.states[participant] = "initial"

    def add_message(self, message: Message):
        self.messages.append(message)

    def generate_sequence_diagram(self, filename: str):
        """Generate a sequence diagram using Graphviz"""
        dot = graphviz.Digraph(comment=f"Sequence Diagram: {self.name}")
        dot.attr(rankdir="LR")

        # Add participants
        for participant in self.participants:
            dot.node(participant, participant)

        # Add message flows
        for msg in self.messages:
            dot.edge(
                msg.sender,
                msg.receiver,
                f"{msg.msg_type.value}: {msg.content}",
                dir="forward",
            )

        # Save the diagram
        dot.render(filename, view=False, format="png")


class IntersectionNegotiationProtocol(InteractionProtocol):
    """Protocol for negotiating intersection crossing between two vehicles"""

    def __init__(self):
        super().__init__("Intersection Negotiation")
        self.add_participant("Vehicle1")
        self.add_participant("Vehicle2")

        # Define the negotiation sequence
        self.add_message(
            Message(
                "Vehicle1",
                "Vehicle2",
                MessageType.REQUEST,
                "Request to cross intersection",
                0.0,
            )
        )
        self.add_message(
            Message(
                "Vehicle2",
                "Vehicle1",
                MessageType.PROPOSE,
                "Propose yield/proceed strategy",
                1.0,
            )
        )
        self.add_message(
            Message(
                "Vehicle1",
                "Vehicle2",
                MessageType.ACCEPT,
                "Accept proposed strategy",
                2.0,
            )
        )
        self.add_message(
            Message(
                "Vehicle2", "Vehicle1", MessageType.CONFIRM, "Confirm agreement", 3.0
            )
        )


class PedestrianLightVotingProtocol(InteractionProtocol):
    """Protocol for pedestrians voting on traffic light changes"""

    def __init__(self):
        super().__init__("Pedestrian Light Voting")
        self.add_participant("Pedestrian1")
        self.add_participant("Pedestrian2")
        self.add_participant("TrafficLight")

        # Define the voting sequence
        self.add_message(
            Message(
                "Pedestrian1",
                "TrafficLight",
                MessageType.REQUEST,
                "Request light change",
                0.0,
            )
        )
        self.add_message(
            Message(
                "Pedestrian2",
                "TrafficLight",
                MessageType.REQUEST,
                "Support light change request",
                1.0,
            )
        )
        self.add_message(
            Message(
                "TrafficLight",
                "Pedestrian1",
                MessageType.INFORM,
                "Acknowledge vote received",
                2.0,
            )
        )
        self.add_message(
            Message(
                "TrafficLight",
                "Pedestrian2",
                MessageType.INFORM,
                "Acknowledge vote received",
                2.1,
            )
        )
        self.add_message(
            Message(
                "TrafficLight",
                "Pedestrian1",
                MessageType.CONFIRM,
                "Confirm light change scheduled",
                3.0,
            )
        )
        self.add_message(
            Message(
                "TrafficLight",
                "Pedestrian2",
                MessageType.CONFIRM,
                "Confirm light change scheduled",
                3.1,
            )
        )


class EmergencyVehicleAuctionProtocol(InteractionProtocol):
    """Protocol for auctioning priority passage for emergency vehicles"""

    def __init__(self):
        super().__init__("Emergency Vehicle Auction")
        self.add_participant("EmergencyVehicle")
        self.add_participant("RegularVehicle1")
        self.add_participant("RegularVehicle2")
        self.add_participant("TrafficLight")

        # Define the auction sequence
        self.add_message(
            Message(
                "EmergencyVehicle",
                "TrafficLight",
                MessageType.REQUEST,
                "Announce emergency priority need",
                0.0,
            )
        )
        self.add_message(
            Message(
                "TrafficLight",
                "RegularVehicle1",
                MessageType.QUERY,
                "Query current priority level",
                1.0,
            )
        )
        self.add_message(
            Message(
                "TrafficLight",
                "RegularVehicle2",
                MessageType.QUERY,
                "Query current priority level",
                1.1,
            )
        )
        self.add_message(
            Message(
                "RegularVehicle1",
                "TrafficLight",
                MessageType.INFORM,
                "Report normal priority",
                2.0,
            )
        )
        self.add_message(
            Message(
                "RegularVehicle2",
                "TrafficLight",
                MessageType.INFORM,
                "Report normal priority",
                2.1,
            )
        )
        self.add_message(
            Message(
                "TrafficLight",
                "EmergencyVehicle",
                MessageType.CONFIRM,
                "Grant highest priority",
                3.0,
            )
        )


def generate_all_protocol_diagrams():
    """Generate sequence diagrams for all interaction protocols"""
    protocols = [
        IntersectionNegotiationProtocol(),
        PedestrianLightVotingProtocol(),
        EmergencyVehicleAuctionProtocol(),
    ]

    for protocol in protocols:
        filename = f"protocol_{protocol.name.lower().replace(' ', '_')}"
        protocol.generate_sequence_diagram(filename)
        print(f"Generated sequence diagram for {protocol.name}")


if __name__ == "__main__":
    generate_all_protocol_diagrams()
