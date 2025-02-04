class Vehiculo:
    def __init__(self, tipo, max_speed, acceleration):
        self.tipo = tipo  # Nombre del tipo de vehículo
        self.max_speed = max_speed  # Velocidad máxima (m/s)
        self.acceleration = acceleration  # Aceleración (m/s²)
    
    def __repr__(self):
        return f"{self.tipo}(width {self.width}m, length {self.length}m, max {self.max_speed}m/s)"
    
# Tipos de vehículos predefinidos
AUTO = Vehiculo("Auto", 0.5, 0.01)
# CAMION = Vehiculo("Camion", 2, 5, 20, 1.5)
# MOTO = Vehiculo("Moto", 2, 5, 35, 3.0)
