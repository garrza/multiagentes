from wealthModel import WealthModel

# Parámetros para la simulación
parameters = {
    'num_agents': 3,  # Número de agentes
    'steps': 2,       # Número de pasos
}

# Crear y ejecutar el modelo
model = WealthModel(parameters)
results = model.run()
