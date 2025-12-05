# Implementation Plan: AI-Humanoid-Robotics Book

**Branch**: `001-ai-humanoid-robotics-book` | **Date**: 2025-12-06 | **Spec**: specs/001-ai-humanoid-robotics-book/spec.md
**Input**: Feature specification from `/specs/001-ai-humanoid-robotics-book/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This project aims to deliver a comprehensive guide and development environment for AI-Humanoid Robotics. It involves creating an interactive Docusaurus-based online textbook, a FastAPI backend providing RAG-powered chatbot, personalization, and translation features, and a React frontend to integrate these functionalities. The deployment will be managed via GitHub Actions to GitHub Pages for the frontend and Render for the backend.

## Technical Context

**Language/Version**: Python 3.11 (for backend), TypeScript/JavaScript (for frontend)  
**Primary Dependencies**: FastAPI, Uvicorn, OpenAI SDK, Qdrant client, SQLAlchemy, Neon Postgres, Better-Auth, Docusaurus, React, `mcp-server-git`.  
**Storage**: Neon (Serverless Postgres) for user profiles and authentication data; Qdrant Cloud for vector embeddings of book content.  
**Testing**: NEEDS CLARIFICATION (No specific testing frameworks or strategies were defined in the user's plan)  
**Target Platform**: Web (Docusaurus/React frontend), Linux server (FastAPI backend).  
**Project Type**: Web application (frontend + backend).  
**Performance Goals**: Chatbot response time under 3 seconds (SC-005), Ingestion script processes 1MB markdown within 60 seconds (SC-006).  
**Constraints**: RAG chatbot must answer questions based *only* on the book's content (FR-004).  
**Scale/Scope**: Comprehensive guide and development environment for AI-Humanoid Robotics, covering Docusaurus documentation, FastAPI backend with RAG, and React frontend.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-Driven Development**: The plan aligns with the feature specification.
- [x] **Syllabus Adherence**: The content generation phase explicitly covers the required syllabus modules.
- [x] **Interactive Features Integration**: The plan incorporates Smart Auth, RAG Chatbot, Personalization, and Translation features.
- [x] **Deployment Readiness**: The plan includes GitHub Actions for GitHub Pages and Render for backend deployment.
- [ ] **Technology Stack (Immutable)**: (No new technologies introduced outside the specified stack, existing stack is respected).

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-humanoid-robotics-book/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/             # For User profile, etc.
│   ├── services/           # Authentication, RAG, Personalization, Translation logic
│   └── api/                # FastAPI endpoints
├── ingestion_script.py     # Script for reading docs and uploading embeddings
└── tests/

web/
├── src/
│   ├── components/         # React components (e.g., SignupModal, SmartComponents, ChatWidget)
│   ├── pages/
│   └── docs/               # Docusaurus markdown content for the book modules
├── sidebars.ts             # Docusaurus sidebar configuration
└── tests/

scripts/validate_content.py # Agent skill script
.github/workflows/          # GitHub Actions for CI/CD
render.yaml                 # Render.com deployment configuration
requirements.txt            # Backend Python dependencies
```

**Structure Decision**: The project will adopt a monorepo structure with a `backend/` directory for the FastAPI application and a `web/` directory for the Docusaurus/React frontend, alongside shared `scripts/` and deployment configuration files.

## Phases

### Phase 1: Infrastructure & Scaffolding
1. Initialize Docusaurus project in `/web`.
2. Initialize FastAPI project in `/backend`.
3. Configure `mcp-server-git` for version control.
4. Create `requirements.txt` for backend (fastapi, uvicorn, openai, qdrant-client, sqlalchemy, database drivers).

### Phase 2: Content Generation (The Book)
1. Create `sidebars.ts` to reflect Modules 1-4.
2. Write Module 1: Focus on ROS 2, Nodes, and URDF (`web/docs/module-1-ros2/*.md`).
3. Write Module 2: Focus on Gazebo, Physics, and Unity (`web/docs/module-2-gazebo/*.md`).
4. Write Module 3: Focus on NVIDIA Isaac Sim and Hardware Specs (RTX requirement) (`web/docs/module-3-isaac/*.md`).
5. Write Module 4: Focus on VLA, Whisper, and the Capstone (`web/docs/module-4-vla/*.md`).

### Phase 3: The Backend Brain (FastAPI)
1. Auth System: Implement Better-Auth with the custom schema (`hardware_specs`, `coding_background`) using Neon Postgres.
2. RAG System: Implement `/chat` endpoint using Qdrant and OpenAI.
3. Features API: Implement `/personalize` and `/translate` endpoints.
4. Ingestion: Create a script to read `web/docs/*.md` and upload embeddings to Qdrant.

### Phase 4: Frontend Intelligence (React)
1. Auth UI: Create a Signup Modal that collects hardware/coding details.
2. Interactive Toolbar: Create `SmartComponents.tsx` containing:
   - Button: "Personalize for [User Role]"
   - Button: "Translate to Urdu"
3. Chat Widget: Embed a floating chat window that calls the `/chat` endpoint.

### Phase 5: Reusable Skills & Deployment
1. Skill: Create the `validate_content` agent skill (`scripts/validate_content.py`).
2. Deploy: Configure GitHub Actions for Pages and `render.yaml` for Backend.
