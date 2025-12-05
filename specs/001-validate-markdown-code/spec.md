# Feature Specification: Agent Skill: Validate Markdown Code

**Feature Branch**: `001-validate-markdown-code`  
**Created**: 2025-12-06  
**Status**: Draft  
**Input**: User description: "Agent Skill: A custom script (scripts/validate_content.py) that Claude can use to check if a markdown file contains valid Python/ROS 2 code blocks before committing."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Validate Markdown Code Before Commit (Priority: P1)

As an agent, I want to automatically validate Python/ROS 2 code blocks within markdown files before committing changes, so that I can ensure code quality and prevent broken examples or incorrect syntax from being committed.

**Why this priority**: This is the core functionality of the request and directly addresses the user's need for automated code validation within markdown.

**Independent Test**: This can be fully tested by modifying a markdown file with valid/invalid code blocks and attempting a commit. The pre-commit hook should either pass or fail based on the code block validity.

**Acceptance Scenarios**:

1. **Given** a markdown file with valid Python code blocks, **When** the agent attempts to commit, **Then** the validation script runs and the commit proceeds successfully.
2. **Given** a markdown file with invalid Python code blocks, **When** the agent attempts to commit, **Then** the validation script fails, preventing the commit and providing informative error messages.
3. **Given** a markdown file with valid ROS 2 code blocks (e.g., `ros2 run <package> <node>`), **When** the agent attempts to commit, **Then** the validation script runs and the commit proceeds successfully.
4. **Given** a markdown file with invalid ROS 2 code blocks, **When** the agent attempts to commit, **Then** the validation script fails, preventing the commit and providing informative error messages.
5. **Given** a markdown file with no code blocks or only non-Python/non-ROS 2 code blocks, **When** the agent attempts to commit, **Then** the validation script runs and the commit proceeds successfully (no errors due to irrelevant content).

### Edge Cases

- What happens when a markdown file contains mixed code blocks (Python, ROS 2, and others)?
- How does the script handle very large markdown files with many code blocks?
- What if the Python/ROS 2 code blocks rely on external dependencies not available in the validation environment?
- How does the script provide actionable feedback when validation fails?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a custom script (`scripts/validate_content.py`) accessible to the agent.
- **FR-002**: The script MUST be capable of identifying code blocks within markdown files.
- **FR-003**: The script MUST validate Python code blocks for syntactical correctness.
- **FR-004**: The script MUST validate ROS 2 specific commands (e.g., `ros2 run`, `ros2 topic`) for basic structural correctness.
- **FR-005**: The script MUST return a non-zero exit code if any Python or ROS 2 code block is invalid, preventing the commit.
- **FR-006**: The script MUST return a zero exit code if all Python and ROS 2 code blocks are valid or if no such blocks are found.
- **FR-007**: The script MUST provide clear, actionable error messages indicating the file, line number, and nature of the validation failure.
- **FR-008**: The agent MUST automatically configure the pre-commit hook for automated execution of the validation script (e.g., by modifying `.git/hooks/pre-commit`).

### Key Entities

- **Markdown File**: A text file with `.md` extension containing code blocks.
- **Code Block**: A section within a markdown file delineated by triple backticks, potentially with a language specifier (e.g., ````python`, ````bash`).
- **Python Code**: Snippets of code written in the Python programming language.
- **ROS 2 Command**: Shell commands specific to the Robot Operating System 2 framework.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The validation script correctly identifies valid Python/ROS 2 code blocks with 99% accuracy.
- **SC-002**: The validation script correctly identifies invalid Python/ROS 2 code blocks with 99% accuracy.
- **SC-003**: The pre-commit validation process completes within 5 seconds for markdown files up to 1MB in size.
- **SC-004**: The error messages provided by the script enable an agent to quickly identify and fix issues in markdown code blocks within 2 minutes.