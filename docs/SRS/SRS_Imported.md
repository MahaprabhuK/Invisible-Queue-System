# Invisible Queue: A Real-Time Animated Queue Simulation and Wait-Time Prediction System

## Introduction

### Purpose
This document outlines the functional and non-functional requirements for the software system titled “Invisible Queue: A Real-Time Animated Queue Simulation and Wait-Time Prediction System.”

The purpose of this system is to model service-counter queue dynamics, predict waiting times based on mathematical queue theories, and provide a decision-support tool that suggests whether it is worth waiting in the queue.

### Scope
The Invisible Queue system is a web-based application that:
*   Simulates customer arrivals and service processes.
*   Displays an animated representation of a service counter.
*   Maintains real-time queue length.
*   Predicts expected waiting time using M/M/1 queue modeling.
*   Computes a wait-worthiness decision score.
*   Synchronizes simulation with system clock.
*   Uses synthetic dataset for simulation control.

The system does not:
*   Use real CCTV input.
*   Perform face recognition.
*   Integrate real payment systems.
*   Connect to live physical sensors (future extension).

### Definitions, Acronyms, Abbreviations
*   **Queue Length (Q)** – Number of customers currently waiting.
*   **Arrival Rate (λ)** – Average number of customers arriving per unit time.
*   **Service Rate (μ)** – Average number of customers served per unit time.
*   **Utilization Factor (ρ)** – Ratio λ / μ.
*   **Wq** – Expected waiting time in queue.
*   **W** – Expected total time in system.
*   **Wait-Worthiness Score (S)** – Decision metric indicating whether waiting is advisable.
*   **Simulation Tick** – One-second update cycle.

## Overall Description

### Product Perspective
The system consists of five major modules:
1.  **User Interface Layer** (Streamlit-based web UI).
2.  **Animation Engine**.
3.  **Simulation Engine**.
4.  **Prediction Engine**.
5.  **Decision Logic Module**.

### Product Functions (High-Level)
The system shall:
1.  Simulate queue arrivals using probabilistic modelling.
2.  Simulate service completion process.
3.  Maintain queue state dynamically.
4.  Display animated service counter.
5.  Compute expected waiting time.
6.  Compute wait-worthiness score.
7.  Synchronize updates with real-time clock.
8.  Limit maximum queue size to realistic constraints (<100).
9.  Allow configurable parameters (λ and μ).

### User Characteristics
*   Service counter manager
*   Administrative user
*   Academic evaluator
*   Users are assumed to have basic familiarity with web applications.

### Constraints
*   Developed using Python 3.13.
*   Web interface built using Streamlit.
*   Runs on Windows operating system.
*   Uses synthetic data for simulation.
*   System assumes stable internet connection for initial deployment.

### Assumptions and Dependencies
*   Customer arrivals follow Poisson distribution.
*   Service time follows exponential distribution.
*   System clock is accurate.
*   Synthetic data approximates real-world behaviour.

## Functional Requirements

### FR-1: Queue Simulation
The system shall simulate customer arrivals based on arrival rate (λ).
Arrival probability follows Poisson distribution.

### FR-2: Service Process
Service completion shall follow exponential distribution with rate (μ).

### FR-3: Utilization Calculation
The system shall compute utilization factor:
ρ = λ / μ
Condition for stability: λ < μ

### FR-4: Waiting Time Estimation (M/M/1 Model)
The system shall estimate queue performance using the M/M/1 queuing model.
*   Expected number of customers in system formula provided.
*   Expected number of customers in queue formula provided.
*   Expected waiting time in queue formula provided.

### FR-5: Wait-Worthiness Score
The system shall compute decision score S:
S = α(T_threshold - W)
Decision Rule:
*   If S > 0 → Worth Waiting
*   If S ≤ 0 → Not Worth Waiting

### FR-6: Real-Time Synchronization
The system shall update simulation at 1-second intervals synchronized with system clock.

### FR-7: Animation Rendering
The system shall visually render:
*   Service counter
*   Clerk
*   Customers in non-linear queue arrangement
*   Real-time clock display

## External Interface Requirements
*   **User Interface**: Web-based interactive UI using Streamlit.
*   **Software Interface**: Python 3.x, Streamlit, NumPy, Pandas.

## Non-Functional Requirements
*   **NFR-1 Performance**: System shall update within 1-second latency.
*   **NFR-2 Usability**: User interface shall be intuitive and visually understandable.
*   **NFR-3 Reliability**: System shall operate continuously for at least 1 hour without failure.
*   **NFR-4 Maintainability**: Modular architecture.
*   **NFR-5 Scalability**: Allow integration of ML-based predictive modeling.

## Software Process Model
Agile Scrum model with 5 planned sprints.

## Requirements Traceability Matrix
(As provided in the source text)
