# Evaluation Metrics

## Enterprise RAG System

## 1. Overview

This document defines the evaluation metrics used to measure the quality, safety, performance, and reliability of the Enterprise Retrieval-Augmented Generation (RAG) System.

The purpose of the evaluation framework is not simply to determine whether the system produces an answer.

Instead, it must answer:

> **Did the system retrieve the right evidence, provide sufficient context, generate a correct and grounded answer, handle uncertainty safely, enforce access control, and operate within acceptable performance and reliability constraints?**

The evaluation framework therefore separates the RAG pipeline into measurable layers.

```text
User Query
    ↓
Query Processing
    ↓
Retrieval
    ↓
Context Construction
    ↓
Generation
    ↓
Final Answer
    ↓
Evaluation
```

---

# 2. Evaluation Philosophy

The system will follow an evidence-based evaluation process.

```text
Baseline
   ↓
Measure
   ↓
Identify Failure
   ↓
Change Component
   ↓
Measure Again
   ↓
Compare
   ↓
Accept / Reject
```

No optimization should be considered successful based solely on subjective inspection.

A change should demonstrate measurable improvement while considering potential trade-offs in:

* Quality
* Grounding
* Latency
* Reliability
* Security
* Computational cost

---

# 3. Evaluation Layers

The evaluation framework is divided into the following layers:

| Layer       | Primary Question                                     |
| ----------- | ---------------------------------------------------- |
| Retrieval   | Did we retrieve the correct evidence?                |
| Context     | Did sufficient relevant evidence reach the LLM?      |
| Generation  | Is the final answer correct and relevant?            |
| Grounding   | Are answer claims supported by evidence?             |
| Abstention  | Does the system safely handle insufficient evidence? |
| Security    | Was only authorized evidence used?                   |
| Performance | How efficiently does the system respond?             |
| Reliability | Does the system behave safely under failures?        |

---

# 4. Retrieval Metrics

Retrieval metrics evaluate the quality of the evidence returned by the retrieval system.

```text
Query
  ↓
Retriever
  ↓
Ranked Results
  ↓
Retrieval Evaluation
```

---

## 4.1 Recall@K

### What

Recall@K measures how much of the known relevant evidence is retrieved within the top K results.

### Formula

```text
Recall@K =
Number of relevant items retrieved in Top-K
--------------------------------------------
Total number of relevant items
```

### Example

Suppose the ground-truth relevant chunks are:

```text
Chunk A
Chunk B
```

The retriever returns:

```text
Chunk X
Chunk A
Chunk Y
Chunk B
Chunk Z
```

For K = 5:

```text
Relevant retrieved = 2
Total relevant      = 2

Recall@5 = 2 / 2 = 1.0
```

### Why It Matters

A RAG system cannot generate a grounded answer if the necessary evidence is never retrieved.

### Interpretation

Higher Recall@K generally indicates better coverage of relevant evidence.

### Limitation

High recall does not guarantee good ranking or low retrieval noise.

A system could retrieve all relevant evidence while also returning many irrelevant documents.

### RAG Usage

Recall@K will be used to evaluate whether the retrieval layer successfully finds the evidence required to answer known questions.

---

# 5. Precision@K

## What

Precision@K measures the proportion of retrieved Top-K results that are relevant.

### Formula

```text
Precision@K =
Number of relevant items retrieved in Top-K
--------------------------------------------
K
```

### Example

If 3 of the Top-5 retrieved chunks are relevant:

```text
Precision@5 = 3 / 5 = 0.60
```

### Why It Matters

Low precision means the context may contain unnecessary or distracting information.

### Interpretation

Higher Precision@K indicates that retrieved results contain less irrelevant content.

### Limitation

Precision@K can be low even when all required evidence is successfully retrieved.

### RAG Usage

Used to evaluate retrieval noise and compare retrieval strategies.

---

# 6. Hit Rate@K

## What

Hit Rate@K measures whether at least one relevant result appears within the Top-K retrieved results.

### Definition

```text
Hit@K =
1 → At least one relevant result is retrieved
0 → No relevant result is retrieved
```

### Example

```text
Top-5:
Chunk X
Chunk Y
Chunk A  ← Relevant
Chunk Z
Chunk Q
```

Therefore:

```text
Hit@5 = 1
```

### Why It Matters

It provides a simple measure of whether retrieval found at least some useful evidence.

### Limitation

It does not measure how many relevant items were retrieved or how well they were ranked.

### RAG Usage

Useful for quickly identifying queries where the retriever completely failed to find relevant evidence.

---

# 7. Mean Reciprocal Rank (MRR)

## What

MRR evaluates how highly the first relevant result appears in the ranking.

### Formula

For a single query:

```text
Reciprocal Rank = 1 / rank of first relevant result
```

Across multiple queries:

```text
MRR = Average Reciprocal Rank
```

### Example

If the first relevant result appears at rank 2:

```text
Reciprocal Rank = 1 / 2 = 0.5
```

If it appears at rank 1:

```text
Reciprocal Rank = 1
```

### Why It Matters

In RAG, highly relevant evidence appearing near the top can improve context selection and reduce unnecessary retrieval noise.

### Interpretation

Higher MRR indicates that relevant evidence tends to appear earlier in the ranking.

### Limitation

MRR focuses primarily on the first relevant result and does not fully capture multiple relevant documents.

### RAG Usage

Useful when ranking quality is important, especially when only a limited number of retrieved chunks are passed downstream.

---

# 8. Context Quality Metrics

Retrieval quality alone does not guarantee high-quality generation.

The retrieved evidence must be transformed into useful final context.

```text
Retrieved Candidates
        ↓
Context Selection
        ↓
Final Context
        ↓
LLM
```

Context evaluation will focus on:

* Context relevance
* Context precision
* Context recall
* Context completeness

These metrics help identify failures between retrieval and generation.

---

# 9. Context Relevance

## What

Context relevance measures whether the supplied context is relevant to the user's question.

### Example

Question:

> "What is the remote-work policy?"

Context:

```text
Remote Work Policy
Employees may work remotely up to three days per week.
```

High relevance.

If the context instead contains:

```text
Shipping Policy
Refund Policy
Product Pricing
```

context relevance is low.

### Why It Matters

Irrelevant context can distract the LLM and increase the risk of incorrect answers.

### Limitation

Context relevance does not necessarily mean the context contains enough information to answer the question.

---

# 10. Context Recall

## What

Context recall measures whether the context contains the information required to answer the question.

### Core Question

> Did the final context preserve the necessary evidence?

### Example

Ground-truth evidence:

```text
Employees may work remotely up to three days per week.
Managers may approve additional exceptions.
```

Final context contains only:

```text
Employees may work remotely up to three days per week.
```

The context may have partial recall.

### Why It Matters

Important evidence can be lost during:

* Retrieval
* Filtering
* Reranking
* Context selection
* Context truncation

---

# 11. Context Precision

## What

Context precision measures how much of the selected context is relevant to the question.

### Why It Matters

Large amounts of irrelevant context can:

* Increase token usage
* Increase latency
* Distract the model
* Increase the probability of unsupported generation

### RAG Usage

Context precision will be evaluated when comparing:

```text
Top-K Retrieval
        VS
Reranked Top-K
```

---

# 12. Answer Correctness

## What

Answer correctness measures whether the generated answer accurately answers the question according to the expected answer or ground truth.

### Example

**Question:**

> "How many remote-work days are allowed?"

**Ground Truth:**

> "Up to three days per week."

**Generated Answer:**

> "Employees can work remotely up to three days per week."

Correct.

### Why It Matters

The ultimate purpose of the RAG pipeline is to produce useful and accurate answers.

### Limitation

Correctness alone cannot determine whether the answer was actually grounded in retrieved evidence.

A model could produce the correct answer using unsupported prior knowledge.

---

# 13. Answer Relevance

## What

Answer relevance measures whether the generated response directly addresses the user's question.

### Example

Question:

> "What is the annual leave allowance?"

A response discussing remote work policy is irrelevant even if the information is factually correct.

### Why It Matters

A response can be factually correct but still fail to answer the user's actual question.

### RAG Usage

Used to identify query-understanding and generation failures.

---

# 14. Answer Completeness

## What

Answer completeness measures whether the response includes the necessary information required by the question.

### Example

Question:

> "What is the remote-work limit and who can approve exceptions?"

If the answer only states the remote-work limit but omits the approval rule, the answer is incomplete.

### Why It Matters

Retrieval may succeed while generation still omits important evidence.

---

# 15. Grounding / Faithfulness

## What

Grounding measures whether claims made by the generated answer are supported by the provided context.

### Core Principle

```text
Generated Claim
      ↓
Supporting Evidence
      ↓
Retrieved Source
```

### Example

Context:

> Employees may work remotely up to three days per week.

Answer:

> Employees may work remotely up to three days per week.

Grounded.

If the answer says:

> Employees may work remotely seven days per week.

without supporting evidence:

Not grounded.

### Why It Matters

Grounding is one of the most important quality dimensions of an enterprise RAG system.

### Evaluation Focus

We will investigate:

* Unsupported claims
* Contradictions with context
* Claims not traceable to evidence
* Evidence-supported claims

### Limitation

Automated grounding evaluation may itself require careful validation, particularly for complex or ambiguous answers.

---

# 16. Hallucination / Unsupported Claim Rate

## What

This measures how frequently the system produces unsupported claims.

### Conceptual Formula

```text
Unsupported Claim Rate =
Unsupported factual claims
--------------------------
Total factual claims
```

### Desired Direction

```text
Lower is better
```

### Why It Matters

The system must not confidently invent enterprise policies, procedures, or facts.

### RAG Usage

Particularly important for:

* Unanswerable questions
* Incomplete context
* Conflicting documents
* Ambiguous queries

---

# 17. Abstention Metrics

The system must distinguish between:

```text
Answerable Question
        ↓
Should Answer
```

and:

```text
Unanswerable Question
        ↓
Should Abstain
```

We will evaluate:

* Correct answer rate on answerable questions
* Correct abstention rate on unanswerable questions
* False-answer rate on unanswerable questions
* Over-abstention rate on answerable questions

---

## 17.1 False Answer Rate

Measures how often the system provides an unsupported answer when it should have abstained.

### Desired Direction

```text
Lower is better
```

---

## 17.2 Over-Abstention Rate

Measures how often the system refuses to answer questions for which sufficient evidence actually exists.

### Desired Direction

```text
Lower is better
```

### Trade-off

The system should avoid both:

```text
Too Much Answering → Hallucination
Too Much Abstaining → Poor Utility
```

The goal is a balanced behavior.

---

# 18. Security Evaluation Metrics

Security failures are treated separately from normal quality failures.

## Unauthorized Retrieval Rate

Measures how frequently unauthorized evidence is retrieved for a user.

### Target

```text
Unauthorized Retrieval Rate = 0
```

## Unauthorized Context Exposure

Measures whether restricted evidence reaches the generation layer.

### Target

```text
Unauthorized Context Exposure = 0
```

## Cross-User / Cross-Domain Leakage

Tests whether information belonging to one authorization scope can appear in another user's retrieval or answer.

### Target

```text
No unauthorized information leakage
```

Security failures are considered **critical failures**, regardless of overall RAG quality.

---

# 19. Performance Metrics

Performance metrics measure system efficiency.

## 19.1 End-to-End Latency

Measures the total time from receiving a query to returning the final response.

```text
Request
   ↓
Processing
   ↓
Retrieval
   ↓
Reranking
   ↓
Context Construction
   ↓
LLM
   ↓
Response
```

---

## 19.2 Stage-Level Latency

Latency should also be measured independently for:

* Query processing
* Retrieval
* Reranking
* Context construction
* LLM generation

This allows engineers to identify performance bottlenecks.

---

## 19.3 Latency Percentiles

The system will track:

```text
p50
p95
p99
```

### Why

Average latency can hide slow requests.

Percentiles provide a better representation of user experience and tail latency.

---

# 20. Reliability Metrics

Reliability evaluation will cover:

* Request success rate
* Error rate
* Timeout rate
* Retry rate
* Dependency failure rate
* Recovery success rate

### Example

```text
Total Requests = 1000
Successful     = 970
Failed         = 20
Timeout        = 10
```

The system can then calculate operational reliability indicators from observed behavior.

---

# 21. Evaluation Metric Direction

The general interpretation of metrics is:

| Metric                        | Desired Direction                 |
| ----------------------------- | --------------------------------- |
| Recall@K                      | Higher                            |
| Precision@K                   | Higher                            |
| Hit Rate@K                    | Higher                            |
| MRR                           | Higher                            |
| Context Relevance             | Higher                            |
| Context Recall                | Higher                            |
| Context Precision             | Higher                            |
| Answer Correctness            | Higher                            |
| Answer Relevance              | Higher                            |
| Answer Completeness           | Higher                            |
| Faithfulness / Groundedness   | Higher                            |
| Unsupported Claim Rate        | Lower                             |
| False Answer Rate             | Lower                             |
| Over-Abstention Rate          | Lower                             |
| Unauthorized Retrieval Rate   | **Zero**                          |
| Unauthorized Context Exposure | **Zero**                          |
| Latency                       | Lower, within quality constraints |
| Error Rate                    | Lower                             |
| Timeout Rate                  | Lower                             |

---

# 22. Metric Trade-offs

No single metric represents overall RAG quality.

For example:

```text
Configuration A
Recall@5       = High
Faithfulness   = Medium
Latency        = Low
```

versus:

```text
Configuration B
Recall@5       = Slightly Lower
Faithfulness   = High
Latency        = Higher
```

Configuration B may be preferable depending on the production requirements.

Therefore, optimization decisions must consider multiple dimensions simultaneously.

---

# 23. Baseline Evaluation

Before optimization, the system must establish a baseline.

Example structure:

| Metric             |       Baseline |
| ------------------ | -------------: |
| Recall@5           | Measured Value |
| Precision@5        | Measured Value |
| MRR                | Measured Value |
| Hit Rate@5         | Measured Value |
| Context Relevance  | Measured Value |
| Answer Correctness | Measured Value |
| Faithfulness       | Measured Value |
| Abstention Rate    | Measured Value |
| p50 Latency        | Measured Value |
| p95 Latency        | Measured Value |
| Error Rate         | Measured Value |

Actual values will be populated after the baseline system is implemented and evaluated.

---

# 24. Evaluation Record

Every major experiment should record enough information to reproduce the result.

```text
Experiment ID
Dataset Version
Corpus Version
Chunking Configuration
Embedding Model
Retrieval Strategy
Top-K
Reranker
Context Configuration
LLM
Prompt Version
Evaluation Version
Results
Observations
Decision
```

This creates a traceable relationship between:

```text
Configuration
     ↓
Experiment
     ↓
Metrics
     ↓
Result
     ↓
Engineering Decision
```

---

# 25. Root-Cause Evaluation

Metrics should not only tell us **that** the system failed.

They should help us investigate **where the failure occurred**.

```text
Wrong Answer
     ↓
Retrieval Metrics
     ↓
Context Metrics
     ↓
Generation Metrics
     ↓
Grounding Metrics
     ↓
Root Cause
```

Example:

### Case 1

```text
Recall@5 = Low
```

Likely investigation:

* Chunking
* Embedding
* Retrieval
* Indexing

### Case 2

```text
Recall@5 = High
Context Quality = Low
```

Likely investigation:

* Context selection
* Reranking
* Context construction

### Case 3

```text
Retrieval = Good
Context = Good
Faithfulness = Low
```

Likely investigation:

* Prompting
* Generation
* Model behavior
* Grounding controls

This separation is critical for systematic debugging.

---

# 26. Evaluation Principles

## Principle 1 — Measure Before Optimizing

Establish a baseline before modifying the system.

## Principle 2 — Change One Major Variable at a Time

When practical, isolate the effect of a major change.

## Principle 3 — Use the Same Evaluation Dataset

Comparisons should use consistent evaluation data whenever possible.

## Principle 4 — Evaluate Trade-offs

A quality improvement that causes unacceptable latency or cost may not be a production improvement.

## Principle 5 — Security Is Non-Negotiable

A high-quality answer does not compensate for unauthorized information exposure.

## Principle 6 — Track Regression

An optimization should not improve one metric while silently degrading critical system behavior.

---

# 27. Evaluation Workflow

The complete evaluation workflow is:

```text
              Build Baseline
                    ↓
              Run Evaluation
                    ↓
             Analyze Metrics
                    ↓
             Identify Failure
                    ↓
             Root-Cause Analysis
                    ↓
              Modify Component
                    ↓
             Run Evaluation Again
                    ↓
              Compare Results
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
      Improvement          Regression
          ↓                   ↓
        Keep                Reject
          │                   │
          └─────────┬─────────┘
                    ↓
             Document Result
```

---

# 28. Future Evaluation Extensions

The evaluation framework may later be extended to include:

* Cost per query
* Token efficiency
* Throughput
* Concurrent-user performance
* Time-to-first-token
* Streaming performance
* Model-specific evaluation
* Multi-turn conversational evaluation
* Multilingual evaluation
* Robustness testing
* Adversarial retrieval testing
* Prompt-injection resistance

These are not required for the initial evaluation implementation and will be introduced when justified by system requirements.

---

# 29. Definition of Completion

The Evaluation Metrics phase is considered complete when:

* Retrieval metrics are defined.
* Context metrics are defined.
* Generation metrics are defined.
* Grounding metrics are defined.
* Abstention metrics are defined.
* Security metrics are defined.
* Performance metrics are defined.
* Reliability metrics are defined.
* Metric direction is documented.
* Baseline comparison methodology is defined.
* Root-cause evaluation methodology is defined.
* Experiment reproducibility requirements are documented.

> **Evaluation Metrics Status: Defined**
