# System Design Document
# Invisible Queue: A Real-Time Animated Queue Simulation and Wait-Time Prediction System

## Introduction

### Purpose
This document describes the internal design and architectural structure of the Invisible Queue System. It translates the requirements defined in the Software Requirements Specification (SRS) into a structured implementation blueprint.

### Scope
The design document defines:
*   System architecture
*   Module responsibilities
*   Class structure
*   Data flow
*   Algorithm logic
*   Runtime interaction behaviour

This document focuses on how the system will be built.

## System Architecture Overview

### Architectural Style
The Invisible Queue System follows a layered modular architecture with clear separation of concerns.
The system is divided into five major components:
1.  **Web UI Layer**
2.  **Simulation Engine**
3.  **Prediction Engine**
4.  **Decision Engine**
5.  **Animation Renderer**

### High-Level Architecture Flow
User → Web UI → Simulation Engine → Prediction Engine → Decision Engine → Animation Renderer → Web UI Output

Each module performs a single, well-defined responsibility.

### Design Principles
*   Separation of concerns
*   Mathematical correctness
*   Modularity
*   Real-time responsiveness
*   Extensibility for future ML integration

## Module Design

### Simulation Module
*   **Responsibility**: Simulates queue behaviour using probabilistic arrival and service processes.
*   **Inputs**: Arrival rate (λ), Service rate (μ), Current queue state.
*   **Outputs**: Updated queue length Q(t).
*   **Core Functions**: Generate arrival event (Poisson approximation), Generate service completion event, Update queue length.

### Prediction Module
*   **Responsibility**: Computes queue performance metrics using M/M/1 model.
*   **Inputs**: λ, μ.
*   **Outputs**: Utilization factor (ρ), Waiting time in queue (Wq), Total time in system (W), Expected queue length (L).
*   **Mathematical Models Used**:
    *   ρ = λ / μ
    *   W = 1 / (μ - λ)
    *   Wq = ρ / (μ - λ)
    *   L = λW

### Decision Module
*   **Responsibility**: Evaluates whether waiting in the queue is worthwhile.
*   **Inputs**: Waiting time W, Threshold time T_threshold.
*   **Output**: Decision score S, Recommendation (Worth Waiting / Not Worth Waiting).
*   **Decision Formula**: S = α(T_threshold - W)
*   **Decision rule**:
    *   If S > 0 → Worth Waiting
    *   If S ≤ 0 → Not Worth Waiting

### UI Module
*   **Responsibility**: Accept user inputs, Display queue animation, Display metrics, Display decision result, Update interface every second.

### Animation Module
*   **Responsibility**: Render animated service counter, Render queue of clients, Reflect real-time queue length, Synchronize with simulation tick.

## Class Design

### Class: QueueSimulator
*   **Attributes**: arrival_rate, service_rate, queue_length, current_time.
*   **Methods**: step(), simulate_arrival(), simulate_service(), update_queue().

### Class: PredictionEngine
*   **Methods**: calculate_utilization(), calculate_waiting_time(), calculate_queue_length().

### Class: DecisionEngine
*   **Methods**: compute_score(), evaluate_decision().

### Class: AnimationRenderer
*   **Methods**: render_queue(), render_metrics(), update_display().

## Data Design

### Core Variables
*   λ (arrival rate)
*   μ (service rate)
*   ρ (utilization)
*   Q(t) (queue length)
*   W (total waiting time)
*   Wq (waiting time in queue)
*   S (decision score)

### Data Flow
User inputs λ and μ → Simulation engine updates queue state → Prediction engine computes metrics → Decision engine computes recommendation → UI updates visual display.

## Algorithm Description

### Simulation Cycle
1.  Initialize λ and μ.
2.  At each time tick (1 second):
    *   Generate arrival event.
    *   Generate service completion event.
    *   Update queue length.
3.  Compute utilization and waiting time.
4.  Compute decision score.
5.  Update UI and animation.

## Sequence Flow (Runtime Interaction)
User → Start Simulation → UI triggers Simulation Engine → Simulation Engine updates queue → Prediction Engine computes metrics → Decision Engine evaluates worthiness → Animation Renderer updates display → UI shows updated results.

## Design Constraints
*   Single-server queue (M/M/1 model)
*   Real-time update interval: 1 second
*   λ must be less than μ for stability
*   Queue size limited to realistic bounds (< 100)

## Future Design Extensions
*   Multi-server queue (M/M/c)
*   Machine learning-based λ estimation
*   Real-world sensor integration
*   Cloud deployment
