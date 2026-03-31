# Implementation Plan: HU05 - Rendir Examen Diagnóstico

## Phase 1: Infrastructure and Question Management [checkpoint: manual]
- [x] Task: Create Models for Exams and Questions (manual)
    - [x] Create `ExamenDiagnostico` model to represent the overall assessment.
    - [x] Create `Pregunta` model with fields for text, type (Choice/Text), and category/topic.
    - [x] Create `Opcion` model for Multiple Choice questions.
    - [x] Create `RespuestaUsuario` model to store student attempts and answers.
- [x] Task: Configure Django Admin for Question Management (manual)
    - [x] Register `ExamenDiagnostico`, `Pregunta`, and `Opcion` in `admin.py`.
    - [x] Ensure nested inline editing for options within questions.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Infrastructure and Question Management' (Protocol in workflow.md) (manual)

## Phase 2: Exam Interface and Submission Logic [checkpoint: manual]
- [x] Task: Implement Exam View and Template (manual)
    - [x] Create a URL for `rendir_examen`.
    - [x] Write tests for the exam view (restricted to students).
    - [x] Implement the view to fetch questions and render the HTML form.
- [x] Task: Implement Submission and Score Logic (manual)
    - [x] Write tests for the exam submission logic.
    - [x] Implement the logic to process POST data and save `RespuestaUsuario`.
    - [x] Calculate the total score and score per topic.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Exam Interface and Submission Logic' (Protocol in workflow.md) (manual)

## Phase 3: Results and UI Polish [checkpoint: manual]
- [x] Task: Implement Results View (manual)
    - [x] Write tests for the results view.
    - [x] Create a view to display the feedback (Score, Success message, Topic summary).
- [x] Task: Implement Global Timer (manual)
    - [x] Add `tiempo_limite` field to `ExamenDiagnostico`.
    - [x] Implement JavaScript countdown on the exam template.
    - [x] Add backend validation to reject submissions after the time limit.
- [x] Task: Final UI/UX Adjustments (manual)
    - [x] Apply CSS styles consistent with the project's gamified theme.
    - [x] Ensure responsive design for mobile.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Results and UI Polish' (Protocol in workflow.md) (manual)
