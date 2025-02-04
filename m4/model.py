import agentpy as ap
import random
from agentes import VehicleAgent

class TrafficModel(ap.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup()

    def setup(self):
        """ Configura el modelo con parámetros iniciales """
        self.vehicles = ap.AgentList(self, 0, VehicleAgent)  # Lista vacía al inicio
        self.step_count = 0  

    def step(self):
        """ Ejecuta un paso en la simulación """
        self.step_count += 1

        # Cada 2-5 segundos (~60 steps por segundo, dependiendo del framerate)
        if self.step_count % random.randint(120, 300) == 0:
            new_vehicle = VehicleAgent(self)
            self.vehicles.append(new_vehicle)

        # Actualizar todos los vehículos
        self.vehicles.step()

    def draw(self):
        """ Dibuja los vehículos en la escena """
        for vehicle in self.vehicles:
            vehicle.draw()
