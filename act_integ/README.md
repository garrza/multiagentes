# Traffic Intersection Game Theory Analysis

This project implements game theory analysis for various traffic intersection scenarios, modeling the interactions between vehicles, pedestrians, and traffic lights.

## Game Scenarios

1. **Vehicle Intersection Game**

   - Models interaction between two vehicles at an intersection without traffic lights
   - Actions: proceed/yield
   - Nash Equilibrium: (yield, proceed) and (proceed, yield)
   - Pareto Optimal: (yield, proceed) and (proceed, yield)

2. **Pedestrian Vehicle Game**

   - Models interaction between a pedestrian and vehicle at a crossing
   - Actions: cross/stop for pedestrian, proceed/brake for vehicle
   - Nash Equilibrium: (stop, proceed)
   - Pareto Optimal: (stop, proceed) and (cross, brake)

3. **Emergency Red Light Game**

   - Models interaction between a vehicle and traffic light during urgency
   - Actions: wait/run_light for vehicle, stay_red/change_green for light
   - Nash Equilibrium: (wait, change_green)
   - Pareto Optimal: (wait, change_green)

4. **Pedestrian Light Request Game**
   - Models interaction between pedestrians and traffic light system
   - Actions: request/jaywalk for pedestrian, respond/ignore for light
   - Nash Equilibrium: (request, respond)
   - Pareto Optimal: (request, respond)

## Interaction Protocols

The project implements three types of interaction protocols:

1. **Negotiation Protocol**

   - Used for vehicle-to-vehicle intersection negotiations
   - Sequence: Request → Propose → Accept → Confirm

2. **Voting Protocol**

   - Used for pedestrian light change requests
   - Multiple pedestrians can vote for light changes
   - Sequence: Request → Support → Acknowledge → Confirm

3. **Auction Protocol**
   - Used for emergency vehicle priority
   - Sequence: Announce → Query → Report → Grant

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run game theory analysis:

```bash
python -m models.game_analysis
```

This will generate payoff matrix visualizations for each game scenario.

2. Generate interaction protocol diagrams:

```bash
python -m models.interaction_protocols
```

This will create sequence diagrams for each interaction protocol.

## Files Structure

- `models/`
  - `game_theory.py` - Core game theory implementations
  - `game_analysis.py` - Analysis and visualization tools
  - `interaction_protocols.py` - Protocol implementations
  - `agents.py` - Agent implementations
  - `traffic_model.py` - Traffic simulation model

## Analysis Results

The analysis generates:

- Payoff matrices for each game
- Nash equilibria identification
- Pareto optimal outcomes
- Maximum social welfare calculations
- Sequence diagrams for interaction protocols

## Conclusions

1. **Most Conflicting Scenarios**:

   - Vehicle intersection without traffic lights
   - Pedestrian crossing without light control

2. **Best Solution Approaches**:

   - Nash Equilibrium works well for clear priority situations
   - Pareto efficiency is crucial for emergency scenarios
   - Maximum social welfare guides traffic light timing

3. **Protocol Effectiveness**:
   - Negotiation works best for vehicle-vehicle interactions
   - Voting is effective for pedestrian-light interactions
   - Auction protocol efficiently handles emergency priorities
