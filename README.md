*This project has been created as part of the 42 curriculum by okruhlia.*

# FLY-IN: Autonomous Fleet Router

```text
> SYSTEM OVERRIDE INITIATED...
> LOADING AERIAL DAEMONS: [PYTHON_3.10+]... [OK]
> INITIALIZING GRAPHICAL UI: [PYGAME-CE]... [DONE]
> CHECKING TYPE SAFETY ICE: [MYPY --STRICT]... 100% SECURE
> PROBING ZONE NETWORK: START_HUB DETECTED
> BYPASSING COLLISION PROTOCOLS: ENGAGED
> STATUS: ALL FLEET DRONES STANDING BY.
> WELCOME, OPERATOR. THE SKY IS YOURS.
```

* [01] DESCRIPTION: MISSION BRIEFING
* [02] INSTRUCTIONS: DEPLOYMENT PROCEDURES
* [03] ALGORITHM: LOGIC_CORE & PATHFINDING
* [04] VISUAL REPRESENTATION: TACTICAL OVERLAY
* [05] RESOURCES: INFORMATION ASSETS

## [01] DESCRIPTION: MISSION BRIEFING
**Fly-in** is a highly optimized routing and simulation engine designed to navigate a fleet of autonomous drones through a complex, dynamic network of connected zones. 

* **Objective:** Route all drones from a central starting hub to a final destination in the absolute minimum number of simulation turns.
* **Tech Stack:** Pure Python (Object-Oriented), strict type hinting (`mypy`), Pygame for rendering.
* **Constraints:** The system rigorously enforces zone capacities, multi-turn travel times for restricted areas, and simultaneous movement limits to prevent mid-air collisions.

## [02] INSTRUCTIONS: DEPLOYMENT PROCEDURES
To initialize the simulation and take control of the fleet, execute the following commands in your terminal:

| Routine | Action | System Feedback |
| :--- | :--- | :--- |
| `make install` | Install dependencies | Bootstraps `uv`/`pip` requirements. |
| `make run` | Launch the simulation | Opens the graphical interface. |
| `make debug` | Tactical debugging | Drops into `pdb` for step-by-step memory inspection. |
| `make lint` | Code structure scan | Runs `flake8` and `mypy` type checks. |
| `make lint-strict`| Deep ICE penetration | Enforces ultimate type safety (`mypy --strict`). |
| `make clean` | Cache wipe | Purges `__pycache__` and residual metadata. |

**Interface Usage:** Once launched, use the `UP`/`DOWN` arrows to select a map in the main menu and press `ENTER`. In the simulation, use `SPACE` to advance the simulation by one turn, and the `LEFT`/`RIGHT` arrows to pan the camera across large network graphs.

## [03] ALGORITHM: LOGIC_CORE & PATHFINDING
The breach of the optimal pathing problem is handled by a custom-built, dependency-free graph traversal engine.

* **Dynamic Heatmap Generation:** The `Navigator` module scans the network backward from the `end_hub` to the `start_hub`, generating a topological heatmap (distance dictionary). It dynamically adjusts the weight of nodes based on their type (e.g., `priority` zones reduce costs, `restricted` zones increase them).
* **Turn-Based Collision Avoidance:** During each tick, the `Simulator` sorts active drones based on their proximity to the goal. Drones query their adjacent connections and "book" departures.
* **Capacity Locking:** Before a drone moves, the algorithm checks `max_drones` constraints of the target zone and `max_link_capacity` of the connection. If the path is heavily congested, the drone will hold its position, acting as a tactical delay to maintain flow stability.

## [04] VISUAL REPRESENTATION: TACTICAL OVERLAY
The simulation abandons basic terminal output in favor of a full graphical tactical overlay powered by Pygame.

* **Responsive Viewport:** The `Camera` module dynamically calculates the maximum bounds of the loaded map and automatically scales (zooms) the network to fit vertically on the user's monitor.
* **Horizontal Panning:** For extreme-scale networks, the viewport restricts vertical overflow but allows smooth horizontal panning with constrained padding boundaries.
* **State Visualization:** Nodes and links are rendered dynamically. Drone movements are animated as discrete, frame-independent spatial translations, instantly updating their graphical positions upon resolving the logic matrix for the current turn.

## [05] RESOURCES: INFORMATION ASSETS
The routing matrix was stabilized utilizing the following data havens:

* **Pygame CE Documentation:** Exploited for surface rendering, event loop management, and dynamic resolution scaling.
* **Python Typing Vault:** Deep-level integration of `typing` (`NoReturn`, `Any`, Forward References) to survive the `mypy --strict` execution.
* **AI Collaboration (Gemini):** Utilized for structural logic optimization, resolving complex circular import deadlocks, enforcing strict type-hinting compliance across the OOP architecture, and generating docstrings. AI was employed as a tactical peer-reviewer to refine mathematical logic (like viewport scaling) while the core engine logic was manually forged.