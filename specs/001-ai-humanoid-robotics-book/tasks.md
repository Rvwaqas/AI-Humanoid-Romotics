# Development Tasks: AI-Humanoid-Robotics Book

**Feature Branch**: `001-ai-humanoid-robotics-book` | **Date**: 2025-12-06 | **Spec**: specs/001-ai-humanoid-robotics-book/spec.md

## Summary

This document outlines the detailed development tasks for the AI-Humanoid Robotics Book project, organized by user stories and phases. The project involves creating a Docusaurus-based online textbook, a FastAPI backend with RAG, personalization, and translation features, and a React frontend to integrate these functionalities. Deployment will leverage GitHub Actions for GitHub Pages and Render.

## Implementation Strategy

Development will follow an incremental delivery approach, prioritizing core user stories first. Each user story phase is designed to be independently testable and potentially deployable as a minimal viable increment. Parallelization opportunities are identified for tasks that do not have direct dependencies on other in-progress tasks.

## Phase 1: Setup (Project Initialization)

- [ ] T001 Initialize Docusaurus project in `web/` directory.  
- [ ] T002 Initialize Python FastAPI project in `backend/` directory.  
- [ ] T003 Create `requirements.txt` for backend with initial dependencies: `fastapi`, `uvicorn`, `openai`, `qdrant-client`, `sqlalchemy`, `psycopg2-binary` in `backend/requirements.txt`.  
- [ ] T004 Create `backend/.env` template file in `backend/.env.example`.
- [ ] T005 Configure `mcp-server-git` for version control in `.git/config`.

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T006 Setup Neon DB connection string configuration in `backend/src/config.py` (or similar for environment variables).
- [ ] T007 Implement the core `User` model with `email`, `hardware_specs`, and `coding_background` fields using SQLAlchemy in `backend/src/models/user.py`.
- [ ] T008 Implement Better-Auth integration for user registration and authentication in `backend/src/services/auth_service.py` and `backend/src/api/auth.py`.

## Phase 3: User Story 1 - Access Comprehensive AI-Humanoid Robotics Guide (Priority: P1)

**Story Goal**: Users can access and read the full content of the AI-Humanoid Robotics textbook through the Docusaurus site.

**Independent Test**: Navigate to the Docusaurus site (once deployed or served locally) and verify that all four modules and their respective content (once written) are accessible and readable. This delivers the core educational content.

- [ ] T009 [P] [US1] Create `sidebars.ts` to reflect Modules 1-4 structure in `web/sidebars.ts`.
- [ ] T010 [P] [US1] Write Module 1 content: ROS 2, Nodes, URDF in `web/docs/module-1-ros2/intro.md`.
- [ ] T011 [P] [US1] Write Module 2 content: Gazebo, Physics, Unity, Sensors in `web/docs/module-2-gazebo/sim.md`.
- [ ] T012 [P] [US1] Write Module 3 content: NVIDIA Isaac Sim, Synthetic data, Isaac ROS, Hardware Requirements (RTX 4070 Ti+) in `web/docs/module-3-isaac/brain.md` and `web/docs/module-3-isaac/hardware.md`.
- [ ] T013 [P] [US1] Write Module 4 content: VLA, Whisper, Cognitive Planning, Capstone in `web/docs/module-4-vla/capstone.md`.

## Phase 4: User Story 2 - Personalized Learning Experience (Priority: P1)

**Story Goal**: Users can receive personalized content and translations based on their profile.

**Independent Test**: Sign up with different hardware/coding profiles. Navigate to a chapter and use the "Personalize" button to observe content changes. Use the "Translate" button to verify Urdu translation.

- [ ] T014 [US2] Create a Signup Modal (React component) that collects `hardware_specs` and `coding_background` during user registration in `web/src/components/SignupModal.tsx`.
- [ ] T015 [US2] Implement the `User` service in the backend to handle user profile updates including `hardware_specs` and `coding_background` in `backend/src/services/user_profile_service.py`.
- [ ] T016 [US2] Implement the `/personalize` API endpoint in `backend/src/api/features.py` that rewrites chapter content based on user's `coding_background` using OpenAI.
- [ ] T017 [US2] Implement the `/translate` API endpoint in `backend/src/api/features.py` that translates chapter content to Urdu using OpenAI.
- [ ] T018 [US2] Create `SmartComponents.tsx` for the interactive toolbar with "Personalize for [User Role]" and "Translate to Urdu" buttons in `web/src/components/SmartComponents.tsx`.
- [ ] T019 [US2] Integrate the interactive toolbar (`SmartComponents`) into the Docusaurus layout (e.g., in `web/src/theme/Layout.tsx` or similar).

## Phase 5: User Story 3 - Interactive Q&A with Chatbot (Priority: P2)

**Story Goal**: Users can ask questions about the book's content through a floating chatbot and get accurate answers.

**Independent Test**: Open the floating chat widget. Ask questions directly related to the book's content and verify accurate, book-sourced responses. Ask irrelevant questions and confirm appropriate handling.

- [ ] T020 [US3] Create an ingestion script (`backend/ingestion_script.py`) to read markdown files from `web/docs/*.md`, generate embeddings, and upload to Qdrant.
- [ ] T021 [US3] Implement the `/chat` API endpoint in `backend/src/api/chat.py` utilizing Qdrant for RAG and OpenAI for response generation.
- [ ] T022 [US3] Embed a floating chat window component (`ChatWidget.tsx`) in the frontend that interacts with the `/chat` endpoint in `web/src/components/ChatWidget.tsx`.

## Phase 6: Reusable Skills & Deployment

- [ ] T023 Create the `validate_content` agent skill script in `scripts/validate_content.py`.
- [ ] T024 Configure GitHub Actions for deploying the Docusaurus frontend to GitHub Pages in `.github/workflows/deploy-frontend.yml`.
- [ ] T025 Configure `render.yaml` for deploying the FastAPI backend to Render.com.

## Dependencies

User Story 1 (Content Access) is a foundational dependency for User Stories 2 (Personalization/Translation) and 3 (Chatbot), as their functionality relies on the existence of book content. User Stories 2 and 3 can be developed in parallel after User Story 1 is substantially complete.

- US1: No direct story dependencies.
- US2: Depends on US1 (content for personalization/translation).
- US3: Depends on US1 (content for RAG).

## Parallel Execution Examples

- **After Phase 2 completion**: Development of Module 1 (`web/docs/module-1-ros2/intro.md`) and Module 2 (`web/docs/module-2-gazebo/sim.md`) can proceed in parallel (T010, T011).
- **After US1 completion**: Frontend Auth UI (T014) and Backend Ingestion Script (T020) can proceed in parallel.

## Suggested MVP Scope

The Minimum Viable Product (MVP) for this project would encompass the completion of **Phase 1 (Setup)**, **Phase 2 (Foundational)**, and **Phase 3 (User Story 1 - Access Comprehensive AI-Humanoid Robotics Guide)**. This would deliver the core textbook content accessible via the Docusaurus site, providing immediate educational value to users. Subsequent user stories can be iteratively added upon this foundation.