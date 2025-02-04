from dataclasses import dataclass
from enum import Enum, auto


class VehicleType(Enum):
    """Enumeration of vehicle types."""
    SEDAN = auto()
    SUV = auto()
    TRUCK = auto()


@dataclass
class Vehicle:
    """Represents a vehicle with its characteristics."""
    type: VehicleType
    max_speed: float
    acceleration: float
    width: float = 2.0
    length: float = 4.5

    def __repr__(self):
        return f"{self.type.name}(width {self.width}m, length {self.length}m, max {self.max_speed}m/s)"

    @classmethod
    def create_auto(cls):
        """Create a default sedan vehicle."""
        return cls(
            type=VehicleType.SEDAN,
            max_speed=20.0,
            acceleration=0.5,
            width=1.8,
            length=4.5
        )

    # Class-level vehicle instances
    AUTO = None

# Initialize the class-level AUTO attribute
Vehicle.AUTO = Vehicle.create_auto()
