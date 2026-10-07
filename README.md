                         ┌──────────────────────┐
                         │      User Query      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     React Frontend   │
                         │                      │
                         │ Query Input          │
                         │ Result Table         │
                         │ Charts               │
                         │ Confidence           │
                         │ Explanation          │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP POST
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI Backend  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      AI Planner      │
                         │                      │
                         │ Gemini / Local       │
                         │ Fallback Planner     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Structured Query   │
                         │        Plan          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Validator      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Deterministic       │
                         │      Executor        │
                         │                      │
                         │ Pandas Analytics     │
                         │ Aggregation           │
                         │ Ranking              │
                         │ Grouping             │
                         │ Comparison           │
                         │ Time Analysis        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Confidence +         │
                         │ Explanation          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Result         │
                         └──────────────────────┘