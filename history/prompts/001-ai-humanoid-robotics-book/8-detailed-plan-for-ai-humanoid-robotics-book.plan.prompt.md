---
id: 8
title: Detailed Plan for AI Humanoid Robotics Book
stage: plan
date: 2025-12-06
surface: agent
model: gemini-pro
feature: 001-ai-humanoid-robotics-book
branch: 001-ai-humanoid-robotics-book
user: {{USER}}
command: /sp.plan
labels: ["planning", "architecture"]
links:
  spec: specs/001-ai-humanoid-robotics-book/spec.md
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - specs/001-ai-humanoid-robotics-book/plan.md
tests:
  []
---

## Prompt

/sp.plan # 02_plan.md
## Phase 1: Environment & Scaffolding
1.  Initialize Docusaurus in `/web`.
2.  Initialize FastAPI in `/backend`.
3.  Configure `mcp-server-git`.
4.  Create `requirements.txt` (fastapi, uvicorn, openai, qdrant-client, sqlalchemy, asyncpg, better-auth).
## Phase 2: Content Generation (The Book)
1.  **Sidebar:** Create `sidebars.ts` mapping Modules 1-4.
2.  **Writing:** Generate content for all 4
2.  **Writing:** Generate content for all 4 modules.
 -   *Constraint:* Ensure Module 3 explicitly covers the "Sim Rig" vs "Edge Brain" architecture defined in the prompt.
3.  **Auditing:** Use the "Agent Skill" to verify hardware mentions in the text.
## Phase 3: The "Brain" (Backend API)
1.  **Database:** Setup Neon Postgres connection.
2.  **Auth:** Implement Better-Auth routes (`/api/auth/*`).
3.  **RAG Pipeline:**
 -   Script: `scripts/ingest.py` to read Docs -> Qdrant. -   Script: `scripts/ingest.py` to read Docs -> Qdrant.
 -   Endpoint: `POST /chat` (Retrieves context -> OpenAI Answer).
4.  **Transformation API:**
-   Endpoint: `POST /personalize` (Input: Text + User Profile -> Output: Rewritten Text).
 -   Endpoint: `POST /translate` (Input: Text -> Output: Urdu Text).
## Phase 4: The "Face" (Frontend Integration)
1.  **Auth UI:** Create `SignupModal.tsx`. Fields: Email, Password, Hardware, Background.
2.  **Smart Toolbar:** Create `ChapterToolbar.tsx`.
 -   Connect "Personalize" button to `/personalize`.
  -   Connect "Translate" button to `/translate`.
3.  **Chat Widget:** Create `FloatingChat.tsx`.
4.  **Swizzle:** Inject `ChapterToolbar` into the Docusaurus `DocItem` layout.
## Phase 5: Deployment
1.  **Backend:** Create `render.yaml`.
2.  **Frontend:** Configure `docusaurus.config.ts` for GitHub Pages.
dont use UI of docusures make your own book like UI

## Response snapshot

I have updated the implementation plan for the AI Humanoid Robotics Book. The plan now includes a custom book-like UI for the frontend, as you requested.

The updated plan is located at: `G:\Hackathon_Qtr_04\AI-Humanoid-Robotics\specs\001-ai-humanoid-robotics-book\plan.md`

I have also created a Prompt History Record for this interaction.

## Outcome

- ✅ Impact: Created a detailed implementation plan for the AI Humanoid Robotics Book feature.
- 🧪 Tests: No tests were run.
- 📁 Files: Updated the implementation plan with a custom book-like UI.
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: The user's request to create a custom book-like UI instead of using the default Docusaurus UI is a significant change that will require careful implementation in the frontend.

## Evaluation notes (flywheel)

- Failure modes observed: The bash script for creating PHR failed on Windows.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
