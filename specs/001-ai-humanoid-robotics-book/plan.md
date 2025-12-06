# Implementation Plan: AI Humanoid Robotics Book

**Branch**: `001-ai-humanoid-robotics-book`
**Date**: 2025-12-06
**Spec**: [G:\Hackathon_Qtr_04\AI-Humanoid-Robotics\specs\001-ai-humanoid-robotics-book\spec.md](G:\Hackathon_Qtr_04\AI-Humanoid-Robotics\specs\001-ai-humanoid-robotics-book\spec.md)

## Summary

This project will create a comprehensive guide to AI-Humanoid Robotics, delivered as an interactive online book. The project includes a Docusaurus-based frontend (with a custom book-like UI), a FastAPI backend with a RAG pipeline for interactive Q&A, and features for content personalization and translation.

## Technical Context

**Language/Version**: Python 3.11, TypeScript (ES2022)
**Primary Dependencies**: FastAPI, Docusaurus 3.x, React, OpenAI SDK, Qdrant, SQLAlchemy, Better-Auth
**Storage**: Neon (Serverless Postgres)
**Testing**: pytest, Vitest
**Target Platform**: Web (GitHub Pages for frontend, Render.com for backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <3s response time for chat and personalization APIs.
**Constraints**: All AI-generated content must be based solely on the book's content.
**Scale/Scope**: 10k users, ~100 pages of book content.

## Constitution Check

*   **Spec-Driven Development**: Adherence to `spec.md` and `plan.md` is mandatory.
*   **Syllabus Adherence**: Content must align with the defined syllabus.
*   **Interactive Features Integration**: "Magic Buttons" and RAG Chatbot are core features.
*   **Deployment Readiness**: Target platforms are GitHub Pages and Render.
*   **Technology Stack**: The tech stack is immutable and must be followed.
*   **Development Workflow**: Code reviews, automated testing, CI/CD, and semantic versioning are required.

## Project Structure

### Documentation

```text
specs/001-ai-humanoid-robotics-book/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code

```text
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

web/
├── src/
│   ├── components/
│   │   ├── Book/
│   │   │   ├── Book.tsx
│   │   │   ├── Page.tsx
│   │   │   └── styles.module.css
│   │   ├── ChapterToolbar.tsx
│   │   ├── FloatingChat.tsx
│   │   └── SignupModal.tsx
│   ├── pages/
│   └── theme/
└── tests/
```

**Structure Decision**: A standard web application structure with a separate `frontend` and `backend` directory is chosen to maintain a clear separation of concerns.

## Phase 1: Environment & Scaffolding

1.  Initialize Docusaurus in `/web`.
2.  Initialize FastAPI in `/backend`.
3.  Configure `mcp-server-git`.
4.  Create `requirements.txt` (fastapi, uvicorn, openai, qdrant-client, sqlalchemy, asyncpg, better-auth).

## Phase 2: Content Generation (The Book)

1.  **Sidebar:** Create `sidebars.ts` mapping Modules 1-4.
2.  **Writing:** Generate content for all 4 modules.
    *   **Constraint:** Ensure Module 3 explicitly covers the "Sim Rig" vs "Edge Brain" architecture defined in the prompt.
3.  **Auditing:** Use the "Agent Skill" to verify hardware mentions in the text.

## Phase 3: The "Brain" (Backend API)

1.  **Database:** Setup Neon Postgres connection.
2.  **Auth:** Implement Better-Auth routes (`/api/auth/*`).
3.  **RAG Pipeline:**
    *   Script: `scripts/ingest.py` to read Docs -> Qdrant.
    *   Endpoint: `POST /chat` (Retrieves context -> OpenAI Answer).
4.  **Transformation API:**
    *   Endpoint: `POST /personalize` (Input: Text + User Profile -> Output: Rewritten Text).
    *   Endpoint: `POST /translate` (Input: Text -> Output: Urdu Text).

## Phase 4: The "Face" (Frontend Integration)

1.  **Custom Book UI:**
    *   Create a main `Book` component in `web/src/components/Book/Book.tsx`.
    *   The `Book` component will manage the state of the current page and page-turning animations.
    *   Create a `Page` component in `web/src/components/Book/Page.tsx` to render the content of a single page.
    *   Style the components to resemble an open book with facing pages.
2.  **Auth UI:** Create `SignupModal.tsx`. Fields: Email, Password, Hardware, Background.
3.  **Smart Toolbar:** Create `ChapterToolbar.tsx` and integrate it into the `Book` component.
    *   Connect "Personalize" button to `/personalize`.
    *   Connect "Translate" button to `/translate`.
4.  **Chat Widget:** Create `FloatingChat.tsx` and overlay it on the `Book` component.
5.  **Content Integration:**
    *   Fetch markdown content from the Docusaurus content pipeline.
    *   Render the markdown content within the `Page` components.

## Phase 5: Deployment

1.  **Backend:** Create `render.yaml`.
2.  **Frontend:** Configure `docusaurus.config.ts` for GitHub Pages.