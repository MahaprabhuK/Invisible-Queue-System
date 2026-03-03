# System Analysis Report

## 1. Overview
This report analyzes the alignment between the provided **Software Requirements Specification (SRS)**, **System Design Document (SDD)**, and the current **Codebase Implementation**.

## 2. Structural Alignment

| Component | SDD Specification | Current Implementation | Status |
| :--- | :--- | :--- | :--- |
| **Simulation Engine** | `QueueSimulator` Class | `src/simulation/simulator.py` (Class `QueueSimulator`) | ✅ Aligned |
| **Prediction Engine** | `PredictionEngine` Class | `src/analytics/wait_time.py`<br>`src/analytics/service_status.py` | ⚠️ implemented as functions, not a class |
| **Decision Engine** | `DecisionEngine` Class | `src/analytics/confidence.py` | ⚠️ implemented as functions, not a class |
| **Animation Renderer** | `AnimationRenderer` Class | `src/ui/animation.py` | ⚠️ implemented as functions, not a class |
| **Web UI** | Streamlit-based UI | `src/app.py`, `src/ui/dashboard.py` | ✅ Aligned |

**Observation:** The implementation favors a **functional programming style** for analytics and UI components, whereas the SDD specifies an **object-oriented class structure**. This is a common and acceptable pattern in Python/Streamlit development, though it technically deviates from the design document.

## 3. Functional Requirements Verification

### FR-1 & FR-2: Simulation Logic
*   **Requirement:** Poisson arrivals (λ) and Exponential service times (μ).
*   **Implementation:**
    *   `src/simulation/arrivals.py`: Uses `np.random.poisson` for both arrivals and services.
    *   **Note:** Simulating service *counts* via Poisson distribution per time step is mathematically equivalent to exponential service times for the queue length distribution in a discrete-time simulation.
*   **Status:** ✅ Compliant.

### FR-3: Utilization Calculation
*   **Requirement:** ρ = λ / μ
*   **Implementation:** `calculate_utilization` in `src/analytics/service_status.py` accurately implements this formula.
*   **Status:** ✅ Compliant.

### FR-4: Waiting Time Estimation (M/M/1)
*   **Requirement:** W = 1 / (μ - λ)
*   **Implementation:** `calculate_waiting_time` in `src/analytics/wait_time.py`.
    *   Includes a stability check (`max(μ - λ, ε)`) to prevent division by zero, which is a robust addition not explicitly detailed in the basic formula but implied by "Numerical Stability Constraint" in SRS.
*   **Status:** ✅ Compliant.

### FR-5: Wait-Worthiness Score
*   **Requirement:** S = α(T_threshold - W)
*   **Implementation:** `compute_decision_score` in `src/analytics/confidence.py`.
*   **Status:** ✅ Compliant.

### FR-7: Animation Rendering
*   **Requirement:** Visual rendering of queue and service counter.
*   **Implementation:** `src/ui/animation.py` uses a simple text-based emoji representation (`"🧍 " * queue_length`).
*   **Status:** ⚠️ Partial / Basic. The SDD implies a more graphical "Animation Engine," but the current implementation provides a minimal textual visualization.

## 4. Key Findings

1.  **High Adherence to Core Logic:** The mathematical models for queue theory (M/M/1) and the simulation logic are implemented correctly and match the requirements.
2.  **Architectural Deviation:** The codebase uses a more lightweight, functional approach for `Analytics` and `UI` modules instead of the strict class-based structure defined in the SDD. This reduces boilerplate but diverges from the "Class Design" section.
3.  **UI/Animation Simplicity:** The current animation is very basic (emoji string). The "Animation Engine" described in the SDD suggests a potential for more sophisticated graphics in future sprints.
4.  **Completeness:** The project appears to have completed **Sprint 1 (Basic simulation)** and **Sprint 2 (Waiting time prediction)**, and **Sprint 3 (Decision scoring)**. It is currently working on **Sprint 4 (Animation integration)**.

## 5. Recommendations
*   **Refactor vs. Update Docs:** Decide whether to refactor the functional modules into classes to strictly match the SDD, or update the SDD to reflect the more Pythonic functional design.
*   **Enhance Animation:** Upgrading `src/ui/animation.py` to use Streamlit elements (like progress bars or custom components) or a plotting library (Altair/PyDeck) would better meet the "Animation Engine" expectations.
