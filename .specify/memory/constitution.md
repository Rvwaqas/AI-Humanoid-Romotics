<!-- Sync Impact Report
Version change: 1.0.0 → 1.0.1
List of modified principles:
  - Technology Stack (Immutable): Added OpenAI SDK
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/commands/*.toml: ⚠ pending
  - README.md, docs/quickstart.md: ⚠ pending
Follow-up TODOs: None
-->
# Physical AI & Humanoid Robotics Constitution

## Core Principles

### Spec-Driven Development
All code and content development MUST strictly adhere to the specifications defined in `01_specification.md` and the architectural plan in `02_plan.md`. No implementation shall commence without a clear reference to these documents.

### Syllabus Adherence
The content of the "Physical AI & Humanoid Robotics" textbook MUST precisely align with the provided syllabus, covering topics such as ROS 2, Isaac Sim, and Visual Language and Action (VLA). All generated material must be context-aware and accurate to the syllabus.

### Interactive Features Integration
The textbook MUST incorporate interactive elements, including "Magic Buttons" for personalization and translation, and a RAG (Retrieval Augmented Generation) Chatbot, to enhance the user learning experience. These features are integral to the book's design.

### Deployment Readiness
The final output of the project MUST be deployed on GitHub Pages for the frontend and Render/Vercel for the backend. All development efforts should consider deployment constraints and best practices from the outset to ensure a smooth transition to production.

## Technology Stack (Immutable)
The project's technology stack is strictly defined to ensure consistency, maintainability, and alignment with the required deployment targets.
- **Frontend:** Docusaurus 3.x (TypeScript, React)
- **Backend:** Python FastAPI (Async)
- **AI:** OpenAI SDK (for RAG, Translation, and Personalization)
**Database:** Neon (Serverless Postgres) via SQLAlchemy.
-   **Vector DB:** Qdrant Cloud (Free Tier).
-   **Auth:** Better-Auth (Client & Server).
-   **AI:** OpenAI SDK (for RAG, Translation, and Personalization).
-   **Tools:** Claude Code CLI, Spec-Kit Plus.
## 4. MCP & Tool Usage
-   You have access to `mcp-server-git` to commit changes.
-   You have full internet access to search Google for documentation (e.g., "Better-Auth docs", "NVIDIA Isaac Sim requirements").

## Development Workflow & Quality Gates
This section outlines the standard procedures and quality checkpoints for all development activities.
- **Code Review**: All code changes MUST undergo a peer code review process before merging into the main branch.
- **Automated Testing**: Comprehensive unit, integration, and end-to-end tests (where applicable) are mandatory for all new features and bug fixes.
- **Continuous Integration/Continuous Deployment (CI/CD)**: A robust CI/CD pipeline will automatically build, lint, type-check, and run all tests for every pull request, ensuring code quality and preventing regressions.
- **Semantic Versioning**: All libraries, modules, and public APIs will adhere strictly to Semantic Versioning (MAJOR.MINOR.PATCH) to manage compatibility and breaking changes effectively.

## Governance
This Constitution serves as the foundational governance document for the "Physical AI & Humanoid Robotics" project.
- **Amendment Procedure**: Any proposed amendments to this Constitution require a formal proposal, thorough discussion, and documented consensus among core project stakeholders. All amendments MUST be recorded in an Architectural Decision Record (ADR).
- **Compliance**: All code contributions, architectural decisions, and project activities MUST strictly adhere to the principles and guidelines outlined in this document.
- **Version Control**: This document itself is version-controlled, with version increments reflecting the significance of changes as per semantic versioning rules (MAJOR for backward incompatible changes, MINOR for significant additions, PATCH for clarifications).

**Version**: 1.0.1 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06