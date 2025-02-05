from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import numpy as np
from models.game_theory import (
    TrafficGame,
    create_vehicle_intersection_game,
    create_pedestrian_vehicle_game,
    create_emergency_red_light_game,
    create_pedestrian_light_request_game,
)


def analyze_game(game: TrafficGame) -> Dict:
    """Analyze a traffic game and return its key properties"""
    nash_equilibria = game.find_nash_equilibrium()
    pareto_optimal = game.find_pareto_optimal()
    max_welfare_strategy, max_welfare = game.find_maximum_social_welfare()

    return {
        "name": game.name,
        "nash_equilibria": nash_equilibria,
        "pareto_optimal": pareto_optimal,
        "max_welfare_strategy": max_welfare_strategy,
        "max_welfare": max_welfare,
        "preference_chain": game.preference_chain,
    }


def plot_payoff_matrix(game: TrafficGame, filename: str = None):
    """Visualize the payoff matrix of a game"""
    actions1 = sorted(set(a1 for a1, _ in game.payoff_matrix.keys()))
    actions2 = sorted(set(a2 for _, a2 in game.payoff_matrix.keys()))

    n_actions1 = len(actions1)
    n_actions2 = len(actions2)

    # Create matrices for player 1 and 2 payoffs
    payoff1 = np.zeros((n_actions1, n_actions2))
    payoff2 = np.zeros((n_actions1, n_actions2))

    for i, a1 in enumerate(actions1):
        for j, a2 in enumerate(actions2):
            outcome = game.get_outcome(a1, a2)
            if outcome:
                payoff1[i, j] = outcome.utility_player1
                payoff2[i, j] = outcome.utility_player2

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot player 1's payoffs
    im1 = ax1.imshow(payoff1, cmap="RdYlGn")
    ax1.set_title(f"{game.player1_type.value.title()}'s Payoffs")
    ax1.set_xticks(np.arange(n_actions2))
    ax1.set_yticks(np.arange(n_actions1))
    ax1.set_xticklabels(actions2)
    ax1.set_yticklabels(actions1)
    plt.colorbar(im1, ax=ax1)

    # Plot player 2's payoffs
    im2 = ax2.imshow(payoff2, cmap="RdYlGn")
    ax2.set_title(f"{game.player2_type.value.title()}'s Payoffs")
    ax2.set_xticks(np.arange(n_actions2))
    ax2.set_yticks(np.arange(n_actions1))
    ax2.set_xticklabels(actions2)
    ax2.set_yticklabels(actions1)
    plt.colorbar(im2, ax=ax2)

    # Add text annotations
    for i in range(n_actions1):
        for j in range(n_actions2):
            ax1.text(j, i, f"{payoff1[i, j]:.1f}", ha="center", va="center")
            ax2.text(j, i, f"{payoff2[i, j]:.1f}", ha="center", va="center")

    plt.suptitle(f"Payoff Matrix: {game.name}")
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
    plt.close()


def analyze_all_games():
    """Analyze all traffic game scenarios and print results"""
    games = [
        create_vehicle_intersection_game(),
        create_pedestrian_vehicle_game(),
        create_emergency_red_light_game(),
        create_pedestrian_light_request_game(),
    ]

    results = []
    for game in games:
        analysis = analyze_game(game)
        results.append(analysis)

        print(f"\nAnalysis for: {game.name}")
        print("=" * 50)
        print(f"Nash Equilibria: {analysis['nash_equilibria']}")
        print(f"Pareto Optimal Outcomes: {analysis['pareto_optimal']}")
        print(f"Maximum Social Welfare Strategy: {analysis['max_welfare_strategy']}")
        print(f"Maximum Social Welfare Value: {analysis['max_welfare']}")
        print("\nPreference Chain:")
        for strategy in analysis["preference_chain"]:
            outcome = game.get_outcome(*strategy)
            print(
                f"  {strategy}: {outcome.description} (Utilities: {outcome.utility_player1}, {outcome.utility_player2})"
            )

        # Generate visualization
        plot_payoff_matrix(
            game, f"game_analysis_{game.name.lower().replace(' ', '_')}.png"
        )

    return results


if __name__ == "__main__":
    analyze_all_games()
