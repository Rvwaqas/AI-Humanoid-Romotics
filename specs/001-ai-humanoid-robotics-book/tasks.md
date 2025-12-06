# Development Tasks: AI-Humanoid-Robotics Book

**Feature Branch**: `001-ai-humanoid-robotics-book` | **Date**: 2025-12-06 | **Spec**: specs/001-ai-humanoid-robotics-book/spec.md

## Summary

This document outlines the detailed development tasks for the AI-Humanoid Robotics Book project, organized by user stories and phases. The project involves creating a custom book-like UI, a FastAPI backend with RAG, personalization, and translation features, and a React frontend to integrate these functionalities. Deployment will leverage GitHub Actions for GitHub Pages and Render.

## Implementation Strategy

Development will follow an incremental delivery approach, prioritizing core user stories first. Each user story phase is designed to be independently testable. Parallelization opportunities are identified for tasks that do not have direct dependencies on other in-progress tasks.

## Phase 1: Setup (Project Initialization)

- [x] T001 Initialize Docusaurus project in `web/` directory.
- [x] T002 Initialize Python FastAPI project in `backend/` directory.
- [x] T003 Create `requirements.txt` for backend with initial dependencies: `fastapi`, `uvicorn`, `openai`, `qdrant-client`, `sqlalchemy`, `psycopg2-binary`, `better-auth`, `asyncpg` in `backend/requirements.txt`.
- [x] T004 Create `backend/.env.example` template file.
- [x] T005 Configure `mcp-server-git` for version control.

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T006 Setup Neon DB connection string configuration in `backend/src/config.py`.
- [x] T007 Implement the core `User` model with `email`, `hardware_specs`, and `coding_background` fields using SQLAlchemy in `backend/src/models/user.py`.
- [x] T008 Implement Better-Auth integration for user registration and authentication in `backend/src/services/auth_service.py` and `backend/src/api/auth.py`.

## Phase 3: User Story 1 - Access Comprehensive AI-Humanoid Robotics Guide (Priority: P1)

**Story Goal**: Users can access and read the full content of the AI-Humanoid Robotics textbook through a custom book-like UI.

**Independent Test**: Navigate to the site and verify that all four modules and their respective content are accessible and readable within the book UI.

- [x] T009 [P] [US1] Write Module 1 content: ROS 2, Nodes, URDF in `web/docs/module-1-ros2/intro.md`.
- [x] T010 [P] [US1] Write Module 2 content: Gazebo, Physics, Unity, Sensors in `web/docs/module-2-gazebo/sim.md`.
- [x] T011 [P] [US1] Write Module 3 content: NVIDIA Isaac Sim, Synthetic data, Isaac ROS, Hardware Requirements (RTX 4070 Ti+) in `web/docs/module-3-isaac/brain.md` and `web/docs/module-3-isaac/hardware.md`.
- [x] T012 [P] [US1] Write Module 4 content: VLA, Whisper, Cognitive Planning, Capstone in `web/docs/module-4-vla/capstone.md`.
- [x] T013 [US1] Create the main `Book` component to manage page state and animations in `web/src/components/Book/Book.tsx`.
- [x] T014 [US1] Create the `Page` component to render markdown content in `web/src/components/Book/Page.tsx`.
- [x] T015 [US1] Create the CSS for the book UI in `web/src/components/Book/styles.module.css`.
- [x] T016 [US1] Integrate the `Book` component into the main page and fetch/render markdown content in `web/src/pages/index.tsx`.

## Phase 4: User Story 2 - Personalized Learning Experience (Priority: P1)

**Story Goal**: Users can receive personalized content and translations based on their profile.

**Independent Test**: Sign up with different hardware/coding profiles. Navigate to a chapter and use the "Personalize" button to observe content changes. Use the "Translate" button to verify Urdu translation.

- [x] T017 [US2] Create a Signup Modal (React component) that collects `hardware_specs` and `coding_background` in `web/src/components/SignupModal.tsx`.
- [x] T018 [US2] Implement the `User` service in the backend to handle user profile updates in `backend/src/services/user_profile_service.py`.
- [x] T019 [US2] Implement the `/personalize` API endpoint in `backend/src/api/features.py`.
- [x] T020 [US2] Implement the `/translate` API endpoint in `backend/src/api/features.py`.
- [x] T021 [US2] Create `ChapterToolbar.tsx` with "Personalize" and "Translate" buttons in `web/src/components/ChapterToolbar.tsx`.
- [x] T022 [US2] Integrate the `ChapterToolbar` into the `Book` component in `web/src/components/Book/Book.tsx`.

## Phase 5: User Story 3 - Interactive Q&A with Chatbot (Priority: P2)

**Story Goal**: Users can ask questions about the book's content through a floating chatbot and get accurate answers.

**Independent Test**: Open the floating chat widget. Ask questions directly related to the book's content and verify accurate, book-sourced responses.

- [x] T023 [US3] Create an ingestion script (`backend/ingestion_script.py`) to read markdown files and upload to Qdrant.
- [x] T024 [US3] Implement the `/chat` API endpoint in `backend/src/api/chat.py`.
- [x] T025 [US3] Create a floating chat window component (`FloatingChat.tsx`) in `web/src/components/FloatingChat.tsx`.
- [x] T026 [US3] Integrate the `FloatingChat` component into the main page (`web/src/pages/index.tsx`) to overlay the `Book` component.

## Phase 6: Reusable Skills & Deployment

- [x] T027 Create the `validate_content` agent skill script in `scripts/validate_content.py`.
- [x] T028 Configure GitHub Actions for deploying the Docusaurus frontend to GitHub Pages in `.github/workflows/deploy-frontend.yml`.
- [x] T029 Configure `render.yaml` for deploying the FastAPI backend to Render.com.

## Dependencies

- **US1**: No direct story dependencies.
- **US2**: Depends on US1 (content and UI for personalization/translation).
- **US3**: Depends on US1 (content for RAG).

## Parallel Execution Examples

- **After Phase 2 completion**: Development of Module 1 (T009) and Module 2 (T010) can proceed in parallel.
- **After US1 completion**: Frontend Auth UI (T017) and Backend Ingestion Script (T023) can proceed in parallel.

## Suggested MVP Scope

The Minimum Viable Product (MVP) would encompass Phase 1, Phase 2, and Phase 3 (User Story 1). This delivers the core textbook content accessible via the custom book UI.
