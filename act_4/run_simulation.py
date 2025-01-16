import matplotlib.pyplot as plt
from src.wealth_simulation import WealthSimulation


def run_wealth_simulation():
    """Ejecuta la simulación y visualiza los resultados."""
    # Parámetros de la simulación
    parameters = {
        "n_deductive": 3,  # Número de agentes deductivos
        "n_bdi": 3,  # Número de agentes BDI
        "steps": 20,  # Número de pasos de simulación
    }

    # Ejecutar simulación
    model = WealthSimulation(parameters)
    results = model.run()

    # Graficar resultados
    data = results.variables.WealthSimulation
    plt.figure(figsize=(10, 6))
    plt.plot(data["Riqueza_promedio_Deductivos"], label="Agentes Deductivos")
    plt.plot(data["Riqueza_promedio_BDI"], label="Agentes BDI")
    plt.xlabel("Pasos de simulación")
    plt.ylabel("Riqueza promedio")
    plt.title("Evolución de la riqueza por tipo de agente")
    plt.legend()
    plt.grid(True)
    plt.savefig("resultados_simulacion.png")
    plt.close()


if __name__ == "__main__":
    run_wealth_simulation()
