[README.md](https://github.com/user-attachments/files/32696085/README.md)
# Employee Performance & Attrition Prediction Using Deep Learning

An AI-powered HR decision-support system that combines employee attrition prediction, performance prediction, SHAP explainability, HR recommendations, information retrieval, and risk simulation in one integrated platform.

> **Project type:** Academic HR decision-support prototype  
> **Primary stack:** Python, Flask, TensorFlow, Scikit-learn, SHAP, HTML, CSS, JavaScript

---

## Overview

The system is designed to help HR teams analyze employee data and support evidence-based workforce decisions.

The platform combines:

- Employee attrition prediction
- Employee performance prediction
- SHAP-based explainability
- HR recommendation generation
- HR policy/document retrieval
- Risk scenario simulation
- Model evaluation and evidence
- Employee-level assessment

The application is intended to **support human review**, not to make autonomous employment decisions.

---

## Main Modules

### 1. Attrition Prediction

Predicts the probability that an employee may leave the organization.

The deployed assessment uses a Deep Neural Network and classifies risk using the current project threshold:

```text
HIGH   >= 0.64
MEDIUM >= 0.40
LOW    < 0.40
```

The workflow includes:

```text
Employee Data
    ↓
Preprocessing
    ↓
Deep Neural Network
    ↓
Attrition Probability
    ↓
Risk Level
```

---

### 2. Performance Prediction

Predicts employee performance across four ratings:

```text
2
3
4
5
```

The performance model uses a Deep Neural Network with dense layers, batch normalization, dropout, and softmax output.

The system returns:

- Predicted performance rating
- Performance label
- Confidence
- Class probabilities

---

### 3. SHAP Explainability

The system provides employee-level explanations using SHAP KernelExplainer.

The explanation identifies features that contributed to the model's predicted attrition risk.

Example output fields:

```text
Feature
Impact
Importance
Direction
```

> SHAP contributions explain model behavior and should not be interpreted as causal evidence.

---

### 4. HR Recommendation Engine

The system generates HR-focused recommendations using employee attributes and prediction results.

The recommendation workflow can consider:

- Attrition risk
- Burnout
- Engagement
- Manager support
- Overtime
- Work-life balance
- Years since promotion
- Training
- Performance
- Perceived AI job risk

The generated actions are intended to support HR review and intervention planning.

---

### 5. HR Knowledge Search

The HR Knowledge module is an Information Retrieval system for searching the internal HR document collection.

Current retrieval methods:

```text
BM25
TF-IDF
Language Model
```

The knowledge base contains 20 HR documents covering:

- Leave
- Performance
- Benefits
- Training
- Compensation

Search results include:

- Document name
- Document ID
- Relevance score
- Matched terms
- View Document action

The **View Document** feature opens the actual retrieved HR policy/document so HR can read the source content.

---

### 6. HR Action Center

The HR Action Center generates an employee-specific HR retrieval query from the employee's model assessment and workplace factors.

The query is searched using:

```text
BM25
TF-IDF
Language Model
```

The retrieved results are combined into policy evidence that can support an employee-level HR assessment.

---

### 7. Risk Simulator

The Risk Simulator allows HR users to change selected employee factors and compare the current prediction with a simulated scenario.

Simulation factors include:

- Burnout
- Engagement
- Manager support
- Work-life balance
- Overtime
- Training
- Salary hike
- Years since promotion

The simulator compares:

```text
Current State
      vs
Simulated State
```

and reports:

- Attrition probability
- Risk level
- Performance rating
- Performance confidence
- Risk change
- Performance change
- Recommendations

Scenario history is stored locally in the browser.

---

### 8. Model Evidence

The Model Evidence page presents recorded evaluation evidence for the tested attrition and performance models.

It includes:

- Model comparison
- Confusion matrices
- DNN architecture
- Evaluation notes
- Global SHAP feature importance when a saved artifact is available

#### Recorded Attrition Evaluation

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7260 | 0.3631 | 0.7039 | 0.4791 | 0.8071 |
| Random Forest | 0.8240 | 0.5118 | 0.3631 | 0.4248 | 0.7925 |
| Deep Neural Network | 0.6730 | 0.3263 | 0.7765 | 0.4595 | 0.7890 |

#### Recorded Performance Evaluation

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 |
|---|---:|---:|---:|---:|---:|
| Deep Neural Network | 0.4200 | 0.3281 | 0.3842 | 0.3275 | 0.4392 |
| Logistic Regression | 0.3620 | 0.3529 | 0.4904 | 0.3163 | 0.4026 |
| Random Forest | 0.5530 | 0.3039 | 0.3076 | 0.2958 | 0.5270 |

These values are the recorded test-set evaluation results from the project's model training/evaluation workflow.

---

# System Architecture

```text
                    HR INTELLIGENCE PLATFORM
                             │
              ┌──────────────┴──────────────┐
              │                             │
        Employee Data                  HR Documents
              │                             │
              ▼                             ▼
       Prediction Engine              IR Engine
              │                     ┌───────┼───────┐
              ▼                     │       │       │
       Attrition Risk              TF-IDF  BM25   LM
       Performance                    │       │       │
              │                       └───────┼───────┘
              ▼                               │
        SHAP Explanation                      │
              │                               │
              └──────────────┬────────────────┘
                             ▼
                    HR Decision Support
                             │
                             ▼
                    Recommended Actions
                             │
                             ▼
                     Relevant HR Policies
```

---

# Information Retrieval Workflow

```text
HR Query
   ↓
Text Preprocessing
   ↓
BM25 / TF-IDF / Language Model
   ↓
Ranked HR Documents
   ↓
Relevance Score + Matched Terms
   ↓
View Actual HR Document
```

---

# Dataset

The project uses the employee dataset:

```text
data/employee_attrition_hr_2026.csv
```

Dataset characteristics used by the project:

- 5,000 employee records
- 29 columns
- Unique employee IDs
- Attrition target: Yes / No
- Performance ratings: 2, 3, 4, 5
- No missing values in the prepared dataset
- Employee ID is excluded from predictive features

---

# Information Retrieval Collection

The HR knowledge base contains 20 internal HR documents across:

```text
hr_documents/
├── leave/
├── performance/
├── benefits/
├── training/
└── compensation/
```

Examples include:

```text
annual_leave.txt
performance_review.txt
promotion_guidelines.txt
overtime_policy.txt
technical_training.txt
employee_benefits.txt
salary_policy.txt
bonus_policy.txt
```

The indexed collection contains:

```text
20 documents
234 unique terms
597 indexed postings
```

---

# Technology Stack

## Backend

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- TensorFlow
- SHAP
- Joblib

## Frontend

- HTML5
- CSS3
- JavaScript
- Chart.js
- Lucide Icons

## Information Retrieval

- Inverted Index
- BM25
- TF-IDF
- Language Model
- Jelinek-Mercer smoothing

## Machine Learning

- Logistic Regression
- Random Forest
- Deep Neural Network

---

# Project Structure

```text
employee-attrition-performance-ai/
│
├── app.py
├── prediction_service.py
│
├── bm25_search.py
├── ir_search_service.py
├── language_model_search.py
├── search_hr_documents.py
│
├── add_hr_documents.py
├── ingest_hr_documents.py
├── build_inverted_index.py
│
├── preprocess.py
├── preprocess_attrition.py
├── preprocess_performance.py
│
├── train_attrition.py
├── train_performance.py
├── train_hr_classifier.py
│
├── explain_attrition.py
├── explain_performance.py
├── optimize_attrition_threshold.py
├── hr_recommendation.py
├── eda.py
│
├── data/
├── artifacts/
├── models/
├── processed_data/
├── ir_artifacts/
├── extracted_documents/
├── hr_documents/
├── results/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── prediction.html
│   ├── employees.html
│   ├── knowledge_search.html
│   ├── simulator.html
│   └── model_evidence.html
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/shivamlendghar/employee-attrition-performance-ai.git
```

Enter the project directory:

```bash
cd employee-attrition-performance-ai
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the Flask application:

```bash
python app.py
```

Open the application in a browser:

```text
http://127.0.0.1:5000
```

---

# Application Routes

| Page | Route |
|---|---|
| Dashboard | `/` |
| Prediction Lab | `/prediction` |
| Employee Roster | `/employees` |
| HR Knowledge | `/knowledge-search` |
| Risk Simulator | `/simulator` |
| Model Evidence | `/model-evidence` |

---

# API Endpoints

```text
GET  /api/health

GET  /api/employees

GET  /api/employees/<employee_id>

POST /api/predict

POST /api/employees/<employee_id>/action-center

POST /api/employees/<employee_id>/explain

POST /api/search

GET  /api/document/<document_id>

POST /api/simulate

GET  /api/dashboard

GET  /api/model-evidence
```

---

# Example HR Knowledge Search

A user can search:

```text
promotion policy
```

The selected IR method returns ranked results containing:

```text
Document
Document ID
Relevance Score
Matched Terms
```

The user can then select:

```text
View Document
```

to read the actual HR policy/document content.

---

# Important Notes

This project is an **academic HR decision-support prototype**.

Predictions and recommendations are intended to support human review and should not be used as autonomous employment decisions.

SHAP explanations represent model contributions and should not be treated as proof of causation.

The recorded evaluation metrics represent the project's model evaluation runs and should be interpreted in the context of the dataset and test split used during development.

---

# Current Limitations

The prototype does not implement production-grade:

- Authentication
- Role-based authorization
- Audit logging
- Enterprise employee-data access controls
- Encryption and secure deployment
- Formal fairness/bias assessment
- Continuous model monitoring

Additional governance, privacy, security, and fairness review would be required before real-world HR deployment.

---

# End-to-End Workflow

```text
Employee Roster
      ↓
Select Employee
      ↓
AI Assessment
      ↓
Attrition Risk + Performance
      ↓
SHAP Explanation
      ↓
HR Recommendations
      ↓
Relevant HR Policies
      ↓
BM25 / TF-IDF / Language Model
      ↓
HR Decision Support
```

---

# Project Objective

The objective of the project is to demonstrate how deep learning, machine learning, explainability, information retrieval, and recommendation techniques can be integrated into a unified HR intelligence platform.

The system brings together:

```text
Prediction
+
Explainability
+
Information Retrieval
+
Recommendations
+
Simulation
+
Model Evidence
```

to create a single academic HR decision-support workflow.

---

# Author

**Employee Performance & Attrition Prediction Using Deep Learning**

Academic Project
