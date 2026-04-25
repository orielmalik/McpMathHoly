# McpMathHoly

> Modular MCP + FastAPI system with Analytics SDK for execution tracking and data-driven evaluation.

---

## 📌 Overview

This project is a **tool-based MCP architecture** that separates:

- Execution Layer (LLM + Math Engines)
- Tool Layer (Strategies / MCP tools)
- Observability Layer (Logging + Analytics)
- Data Science Layer (Pandas SDK)

The goal is not only to solve problems, but to **analyze how they are solved**.

---

## 🧠 Core Idea

Instead of treating AI as a black box, this system:

- Executes structured actions (solve, matrix, expression, motion)
- Logs every event as a structured JSON record
- Builds a dataset of system behavior
- Uses Pandas to analyze performance, accuracy, and stability

---

## 🏗 Architecture

### 1. Execution Layer
- LLM Router
- MCP Tool Dispatcher
- Strategy Pattern (SymPy / NumPy / custom logic)

### 2. Logging Layer
- Singleton Logger (Execution logs)
- Analytics Logger (JSONL event store)

### 3. Data Science Layer
- PandasSDK
- ReportEngine
- Plot generation (matplotlib)

---

## 📊 Analytics Capabilities

The system generates:

- Operation distribution (usage frequency)
- Latency analysis per operation
- Success / failure rate
- Stability metrics (output consistency)
- Visual plots (PNG reports)

---

## 📈 Example Output Metrics

- Success Rate per operation
- Average Latency per strategy
- Most used mathematical operations
- System performance bottlenecks

---

## 🧩 Tech Stack

- Python 3.11+
- FastAPI
- FastMCP
- SymPy (symbolic math)
- NumPy (numerical math)
- Pandas (data analysis)
- Matplotlib (visualization)

---

## 🚀 Design Patterns Used

- Strategy Pattern (math engines)
- Factory Pattern (tool selection)
- Singleton Pattern (logging system)
- Command Pattern (MCP execution layer)
- Event Sourcing (analytics logging)

---

## 📥 How It Works

1. Input action (e.g. "solve: 2x + 1 = 10")
2. Router decides execution path
3. Strategy or LLM executes logic
4. Result is logged as JSON event
5. Pandas SDK reads logs
6. Reports + graphs are generated

---

## 📊 Data Science Role

This project treats execution logs as a dataset:

- Each request = one data point
- System behavior = analyzable dataset
- Pandas transforms runtime → insights

This enables:
- Debugging via statistics
- Performance evaluation
- System reliability tracking

---

## ❓ Interview Q&A (20 Questions)

### Architecture

**1. What is the core idea of this system?**  
A modular MCP execution system with analytics-driven observability.

**2. Why use Strategy Pattern?**  
To separate math logic per operation type.

**3. Why Event Sourcing?**  
To store every execution as immutable data for analysis.

**4. Why separate execution and analytics?**  
To avoid coupling runtime logic with reporting logic.

**5. What is MCP in your system?**  
A tool dispatch layer between LLM and execution engines.

---

### Data Science

**6. What data do you collect?**  
Operation, input, output, latency, success flag.

**7. What is the dataset used for?**  
System performance analysis and debugging.

**8. Why Pandas?**  
Fast aggregation, grouping, and statistical analysis.

**9. What metrics do you compute?**  
Accuracy, latency, stability, usage frequency.

**10. What is stability?**  
Consistency of outputs for repeated inputs.

---

### Analytics

**11. What is the most important metric?**  
Success rate per operation.

**12. Why track latency?**  
To detect performance bottlenecks.

**13. Why visualize operations?**  
To understand system usage distribution.

**14. What does failure rate show?**  
Weak areas in math strategies or LLM routing.

**15. Can this detect bugs?**  
Yes, via anomaly patterns in logs.

---

### System Design

**16. Why use JSONL logs?**  
Efficient append-only event storage.

**17. Why not store everything in DB?**  
Simplicity + easy Pandas ingestion.

**18. Why Singleton logger?**  
Global consistent logging instance.

**19. What makes this scalable?**  
Separation of execution and analytics layers.

**20. Can this evolve into production system?**  
Yes, it mirrors observability systems like Datadog.

---

## 📦 Output Files

- analytics_logs.jsonl
- operations.png
- latency.png
- system_report.json