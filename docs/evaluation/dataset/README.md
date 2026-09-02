# Evaluation Dataset

## 1. Overview

The Evaluation Dataset defines the structured set of questions, expected behaviors, ground-truth references, and access-control scenarios used to evaluate the Enterprise RAG Platform.

The purpose of this dataset is not simply to verify whether the system can answer questions. It is designed to determine whether the complete RAG pipeline can:

* Retrieve the correct information
* Use relevant evidence
* Generate accurate and grounded answers
* Abstain when sufficient evidence is unavailable
* Handle ambiguous or conflicting information
* Respect document-level and user-level access control
* Remain reliable across different question types and difficulty levels
* Provide reproducible evidence for evaluation and debugging

The evaluation dataset serves as the foundation for measuring the system against the success criteria and evaluation metrics defined in this project.

---

## 2. Evaluation Philosophy

The evaluation dataset follows a **failure-oriented and evidence-driven approach**.

A successful RAG system should not only answer correctly when everything goes well. It should also behave safely and predictably when:

* Relevant information is difficult to retrieve
* The knowledge base does not contain the answer
* Multiple documents contain similar information
* Documents contain conflicting information
* The user asks an ambiguous question
* Retrieved context is incomplete
* The requested information is outside the user's authorization scope
* The system encounters noisy or irrelevant retrieval results

Therefore, the dataset intentionally contains both **normal cases and challenging failure cases**.

The goal is to answer:

> **Can the system retrieve, reason over, and respond from authorized enterprise knowledge reliably?**

---

# 3. Dataset Objectives

The evaluation dataset is designed to support the following objectives:

### 3.1 Retrieval Evaluation

Determine whether the system retrieves the correct documents or chunks required to answer a question.

### 3.2 Generation Evaluation

Determine whether the generated response is accurate, relevant, complete, and consistent with the retrieved evidence.

### 3.3 Grounding Evaluation

Determine whether claims made by the LLM are supported by retrieved enterprise evidence.

### 3.4 Abstention Evaluation

Determine whether the system refuses to fabricate an answer when sufficient evidence is unavailable.

### 3.5 Security Evaluation

Determine whether the system prevents unauthorized information from being retrieved, exposed, or used in generated responses.

### 3.6 Robustness Evaluation

Determine how the system behaves across different question types, ambiguity levels, retrieval difficulties, and knowledge-base conditions.

### 3.7 Regression Evaluation

Provide a stable evaluation set that can be executed repeatedly after changes to:

* Chunking
* Embedding models
* Retrieval strategies
* Reranking
* Prompting
* LLMs
* Access-control logic
* Context construction
* Infrastructure

---

# 4. Evaluation Dataset Structure

Each evaluation case represents one independently testable scenario.

A conceptual evaluation record follows this structure:

```text
Evaluation Case
│
├── Case ID
├── Question
├── Category
├── Difficulty
├── Expected Answer
├── Relevant Documents
├── Relevant Chunks
├── Authorization Scope
├── Expected Behavior
└── Evaluation Notes
```

The exact storage format may evolve as the evaluation framework becomes automated.

---

# 5. Evaluation Case Schema

Each evaluation case should contain enough information to support both automated evaluation and human analysis.

| Field                 | Description                                                 |
| --------------------- | ----------------------------------------------------------- |
| `case_id`             | Unique identifier for the evaluation case                   |
| `question`            | User question submitted to the RAG system                   |
| `category`            | Type of question or evaluation scenario                     |
| `difficulty`          | Relative difficulty of the case                             |
| `expected_answer`     | Ground-truth answer or expected response                    |
| `relevant_documents`  | Documents containing supporting information                 |
| `relevant_chunks`     | Specific chunks expected to support the answer              |
| `authorization_scope` | User or role permissions required to access the information |
| `expected_behavior`   | Expected system behavior                                    |
| `evaluation_notes`    | Additional information useful for analysis                  |

Example:

```text
Case ID:
EVAL-001

Question:
What is the company's annual leave policy?

Category:
Factual

Difficulty:
Easy

Expected Answer:
Employees are entitled to the annual leave allowance defined in the current HR policy.

Relevant Documents:
hr/leave-policy.pdf

Relevant Chunks:
chunk_014
chunk_015

Authorization Scope:
employee

Expected Behavior:
Answer using the current authorized HR policy and provide supporting evidence.
```

---

# 6. Question Categories

The dataset should contain multiple categories to evaluate different capabilities of the RAG system.

## 6.1 Factual Questions

Questions whose answers can be directly found in a document.

Example:

```text
What is the company's annual leave policy?
```

Purpose:

* Validate basic retrieval
* Validate straightforward answer generation
* Establish baseline system performance

---

## 6.2 Exact Lookup Questions

Questions requiring precise retrieval of specific information.

Examples:

```text
What is the maximum reimbursement amount?

What is the support escalation window?

What is the policy effective date?
```

Purpose:

* Test precision
* Detect small retrieval or generation errors
* Evaluate handling of numbers, dates, identifiers, and thresholds

---

## 6.3 Paraphrased Questions

Questions that express information differently from the source document.

Example:

Document:

```text
Employees may work remotely up to three days per week.
```

Question:

```text
How many days each week can an employee work from home?
```

Purpose:

* Evaluate semantic retrieval
* Test embedding quality
* Ensure the system does not depend on exact keyword matching

---

## 6.4 Multi-Hop Questions

Questions requiring information from multiple pieces of evidence.

Example:

```text
Which employees are eligible for the travel allowance, and what is the maximum amount they can claim?
```

Purpose:

* Test multi-document retrieval
* Test context construction
* Test reasoning over multiple evidence sources

---

## 6.5 Unanswerable Questions

Questions for which the knowledge base does not contain sufficient information.

Example:

```text
What will the company's revenue be next year?
```

when no relevant forecasting information exists in the knowledge base.

Expected behavior:

```text
The system should clearly state that sufficient information is not available.
```

Purpose:

* Evaluate safe abstention
* Detect hallucination
* Measure unsupported-answer behavior

---

## 6.6 Ambiguous Questions

Questions where the intended meaning is unclear.

Example:

```text
What is the policy for leave?
```

Possible interpretations may include:

* Annual leave
* Sick leave
* Parental leave
* Unpaid leave

Expected behavior may be:

* Ask a clarification question, or
* Provide a clearly scoped answer if the system can safely infer the intent

Purpose:

* Evaluate ambiguity handling
* Prevent unjustified assumptions

---

## 6.7 Conflicting Information

Questions where multiple documents contain inconsistent information.

Example:

```text
What is the current remote-work policy?
```

where an older document says three days per week and a newer policy says two days.

Expected behavior:

* Prefer the authoritative/current document
* Avoid combining conflicting information
* Identify the applicable source when necessary

Purpose:

* Evaluate document authority
* Test freshness/version handling
* Detect contradictory-context failures

---

## 6.8 Permission-Restricted Questions

Questions where the information exists but the requesting user is not authorized to access it.

Example:

```text
What is the executive compensation structure?
```

when the user's authorization scope does not permit access.

Expected behavior:

```text
Do not retrieve or expose unauthorized information.
```

Purpose:

* Evaluate retrieval-time access control
* Evaluate context isolation
* Evaluate response-level security

---

## 6.9 Noisy Retrieval Cases

Cases designed to contain multiple semantically similar but irrelevant documents.

Example:

```text
What is the employee travel reimbursement policy?
```

with documents about:

* Travel policy
* Customer travel
* Vendor travel
* Conference travel
* Employee reimbursement

Purpose:

* Test retrieval precision
* Test reranking
* Detect irrelevant context contamination

---

## 6.10 Long-Context Questions

Questions where relevant evidence appears inside a large set of retrieved context.

Purpose:

* Test context construction
* Evaluate relevant evidence selection
* Detect lost-in-the-middle or context dilution problems

---

# 7. Difficulty Levels

Each evaluation case should have a defined difficulty level.

### Easy

Characteristics:

* Direct answer
* Single relevant document
* Clear wording
* Strong retrieval signal

### Medium

Characteristics:

* Paraphrased question
* Multiple candidate documents
* More complex wording
* Requires combining nearby evidence

### Hard

Characteristics:

* Multi-hop reasoning
* Conflicting documents
* Ambiguous wording
* Weak retrieval signals
* Long context
* Multiple possible interpretations

Difficulty should be based on **system complexity**, not merely question length.

---

# 8. Ground Truth

Ground truth defines what the system is expected to retrieve or answer.

Ground truth may contain:

### Expected Answer

The correct response or acceptable answer characteristics.

### Relevant Documents

Documents that contain authoritative evidence.

### Relevant Chunks

Specific chunks that provide the supporting evidence.

### Expected Behavior

The expected system action when a direct answer is not appropriate.

For example:

```text
Expected Behavior:
Abstain because the knowledge base does not contain sufficient evidence.
```

Ground truth should be explicit enough to support reproducible evaluation.

---

# 9. Evidence Mapping

Each answerable evaluation case should ideally map the expected answer to supporting evidence.

Conceptually:

```text
Question
   ↓
Expected Answer
   ↓
Relevant Document
   ↓
Relevant Chunk
   ↓
Supporting Evidence
```

This mapping enables root-cause analysis.

For example:

```text
Question: What is the remote-work allowance?

Expected Answer: 2 days per week

Relevant Chunk: policy_chunk_027
```

If the system returns an incorrect answer, we can determine whether:

```text
1. Correct chunk was not retrieved
2. Correct chunk was retrieved but ranked too low
3. Correct evidence was retrieved but context construction failed
4. LLM misinterpreted the evidence
5. LLM generated an unsupported claim
```

This makes the evaluation dataset useful for **diagnosis**, not only scoring.

---

# 10. Authorization Scope

Security-sensitive evaluation cases must define the authorization context under which the question is evaluated.

Examples:

```text
employee
manager
hr
finance
admin
```

The exact role model may evolve with the implementation.

The evaluation framework should test both:

### Authorized Access

The user is permitted to access the information.

Expected behavior:

```text
Retrieve → Generate → Answer
```

### Unauthorized Access

The user is not permitted to access the information.

Expected behavior:

```text
Block → Do Not Retrieve → Do Not Expose
```

The evaluation must verify that unauthorized information does not leak through:

* Retrieved documents
* Retrieved chunks
* Context passed to the LLM
* Generated responses
* Citations or evidence references

---

# 11. Expected Behavior

Not every evaluation case should have a traditional answer.

The `expected_behavior` field defines what the system should do.

Possible behaviors include:

```text
answer
answer_with_evidence
ask_clarification
abstain
deny_access
identify_conflict
```

This distinction is important because a system that correctly refuses to answer an unsupported question should not be considered a failure.

---

# 12. Dataset Distribution

The evaluation dataset should contain a balanced mixture of question types.

A conceptual distribution may include:

| Category              | Purpose                           |
| --------------------- | --------------------------------- |
| Factual               | Baseline retrieval and generation |
| Exact Lookup          | Precision                         |
| Paraphrased           | Semantic retrieval                |
| Multi-Hop             | Multi-step reasoning              |
| Unanswerable          | Abstention                        |
| Ambiguous             | Clarification                     |
| Conflicting           | Authority and freshness           |
| Permission Restricted | Security                          |
| Noisy Retrieval       | Retrieval robustness              |
| Long Context          | Context robustness                |

The exact percentages should be determined after the initial dataset is created and analyzed.

The dataset should avoid over-representing easy factual questions because doing so can create misleadingly high overall performance.

---

# 13. Dataset Versioning

Evaluation datasets should be versioned.

Example:

```text
v0.1
v0.2
v1.0
```

A dataset version should change when:

* New evaluation cases are added
* Ground truth is corrected
* Relevant documents change
* Expected behavior changes
* Authorization scenarios are updated
* Evaluation methodology changes

Each experiment should record the dataset version used.

Example:

```text
Experiment:
RAG-baseline-001

Dataset:
v0.1
```

This ensures that historical evaluation results remain reproducible.

---

# 14. Dataset Quality Requirements

The evaluation dataset itself must be validated.

A high-quality evaluation case should have:

* A clearly defined question
* A verified expected answer or behavior
* Correct evidence mapping
* Correct authorization scope
* Unambiguous evaluation criteria
* A known category
* A defined difficulty level
* No accidental dependency on undocumented assumptions

Poorly defined evaluation cases can produce misleading system metrics.

Therefore:

> **Evaluation quality is a prerequisite for trustworthy system evaluation.**

---

# 15. Dataset Contamination and Leakage

The evaluation dataset should be protected from accidental contamination.

Evaluation questions and expected answers should not be used as hidden prompt examples or hard-coded system rules.

The system should solve evaluation cases using the same pipeline and knowledge sources available during normal operation.

The goal is to measure generalization rather than memorization.

---

# 16. Train / Development / Evaluation Separation

Where applicable, datasets should be separated into:

```text
Development Dataset
Evaluation Dataset
Regression Dataset
```

### Development Dataset

Used during active development and debugging.

### Evaluation Dataset

Used to measure system performance against standardized cases.

### Regression Dataset

Contains previously failed or historically important cases that must continue to pass after system changes.

This separation helps reduce overfitting to the evaluation set.

---

# 17. Regression Cases

Whenever the system experiences a meaningful failure, the case should be considered for inclusion in the regression dataset.

Example:

```text
Failure:
The correct document was retrieved but the wrong policy version was selected.

Action:
Add the question to the regression dataset.

Future requirement:
The system must correctly select the authoritative policy.
```

This creates a continuous feedback loop:

```text
Production / Testing Failure
          ↓
Root Cause Analysis
          ↓
Evaluation Case
          ↓
Regression Dataset
          ↓
Future Evaluation
```

---

# 18. Evaluation Workflow

The evaluation dataset participates in the following workflow:

```text
Evaluation Case
       ↓
Submit Question
       ↓
Apply User Authorization
       ↓
Retrieve Documents
       ↓
Retrieve / Rank Chunks
       ↓
Construct Context
       ↓
Generate Response
       ↓
Collect Evidence
       ↓
Compare Against Ground Truth
       ↓
Calculate Metrics
       ↓
Analyze Failures
       ↓
Improve System
       ↓
Run Regression Evaluation
```

This creates a repeatable evaluation lifecycle.

---

# 19. Root-Cause Analysis

A failed evaluation case should not simply be recorded as:

```text
FAILED
```

The evaluation process should identify the failure stage.

Possible root causes include:

```text
Ingestion Failure
        ↓
Parsing Failure
        ↓
Cleaning Failure
        ↓
Chunking Failure
        ↓
Embedding Failure
        ↓
Retrieval Failure
        ↓
Reranking Failure
        ↓
Context Construction Failure
        ↓
Generation Failure
        ↓
Grounding Failure
        ↓
Authorization Failure
```

This classification allows engineering improvements to target the actual bottleneck.

---

# 20. Evaluation Record

Each evaluation run should eventually produce a structured record containing information such as:

```text
case_id
dataset_version
question
user_role
retrieved_documents
retrieved_chunks
generated_answer
expected_answer
expected_behavior
latency
evaluation_metrics
pass/fail
failure_type
notes
```

This information enables reproducibility and post-evaluation analysis.

---

# 21. Success Conditions

The evaluation dataset is considered effective when it can reliably distinguish between:

### Strong System Behavior

```text
Correct evidence retrieved
        ↓
Relevant context constructed
        ↓
Grounded answer generated
        ↓
Evidence provided
        ↓
No unauthorized information exposed
```

### Weak System Behavior

```text
Wrong evidence
     OR
Missing evidence
     OR
Irrelevant context
     OR
Unsupported answer
     OR
Unauthorized information exposure
```

The dataset should make these differences measurable.

---

# 22. Future Extensions

Future versions of the evaluation dataset may include:

* Multilingual questions
* Temporal reasoning
* Table and structured-data questions
* Document comparison
* Cross-document contradiction detection
* Complex multi-hop reasoning
* Adversarial questions
* Prompt-injection evaluation cases
* Citation correctness evaluation
* Human preference evaluation
* Production-derived anonymized evaluation cases
* Automated dataset generation with human validation

These extensions will be introduced only when required by the system's evaluation needs.

---

# 23. Definition of Completion

The Evaluation Dataset phase is considered complete when:

* A standardized evaluation case schema is defined
* Multiple question categories are represented
* Ground truth is defined
* Relevant evidence can be identified
* Authorization scope can be represented
* Expected behavior is defined
* Difficulty levels are defined
* Unanswerable and abstention cases are included
* Security-sensitive cases are included
* Dataset versioning is established
* Regression cases can be incorporated
* Evaluation cases can be mapped to the project's metrics

At that point, the dataset can serve as the foundation for systematic RAG evaluation.

---

## 24. Key Principle

> **A RAG system should not be evaluated only by whether it produces an answer. It should be evaluated by whether it retrieves the right evidence, uses authorized information, produces a grounded response, and behaves safely when the evidence is insufficient.**

The Evaluation Dataset exists to make that behavior measurable, reproducible, and continuously improvable.
