---

description: "Actionable, dependency-ordered tasks for Physical AI & Humanoid Robotics – A Technical Book"
---

# Tasks: Physical AI & Humanoid Robotics – A Technical Book

**Input**: Design documents from `specs/001-physical-ai-book/`
**Prerequisites**: `plan.md`, `spec.md` (required)

**Organization**: Tasks are grouped by the project's defined phases and within those, by user story or chapter to facilitate independent implementation and testing of each increment.

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All book content will be under the `book/` directory.
- `book/docs/` for chapters.
- `book/src/` for Docusaurus components.
- `book/static/` for images, diagrams, code snippets.

---

## Phase 1: Setup & Foundation (Weeks 1–6) 🎯 Foundational Infrastructure

**Purpose**: Project initialization, Docusaurus setup, templating, and initial foundational chapters.

### Setup (Shared Infrastructure)

- [X] T001 Create root project directory: `book/`
- [X] T002 Initialize Docusaurus project within `book/` directory
- [X] T003 [P] Configure `book/docusaurus.config.js` for project title, sidebar, and theme
- [X] T004 [P] Create `book/sidebar.js` (initially empty)
- [X] T005 [P] Create `.github/workflows/deploy.yml` for GitHub Actions CI/CD to GitHub Pages
- [X] T006 Create `LICENSE` file at project root (MIT license) `LICENSE`
- [X] T007 Create `CONTRIBUTING.md` file at project root `CONTRIBUTING.md`
- [X] T008 [P] Set up Zotero for reference management (Manual task)
- [X] T009 [P] Configure Zotero to export BibTeX (master bibliography skeleton) `bib.tex` (Manual task)
- [X] T010 Create reusable Markdown chapter template `book/docs/chapter-template.md`
- [X] T011 Create reusable Mermaid diagram template `book/static/diagram-template.md`
- [X] T012 Create reusable LaTeX equation template `book/docs/latex-template.md`

### Foundational Chapters (US1, US2, US3)

**Goal**: Complete foundational chapters, establishing core content and citation practices.

#### Chapter 1: Introduction to Physical AI and Embodied Intelligence (US1, P1)
- [X] T013 [US1] Outline Chapter 1 (H1->H3 structure) `book/docs/chapter-1.md`
- [X] T014 [US1] Research primary sources for Chapter 1, ensure APA 7th citation readiness `book/docs/chapter-1.md` (Manual task)
- [X] T015 [US1] Draft Chapter 1 content, integrating citations for all technical claims `book/docs/chapter-1.md` (Manual task)
- [X] T016 [US1] Review Chapter 1 against quality gates (content, citation, source quality, plagiarism) `book/docs/chapter-1.md` (Manual task)

#### Chapter 2: A Brief History of Humanoid Robotics (1950–2025) (US1, P1)
- [X] T017 [US1] Outline Chapter 2 (H1->H3 structure) `book/docs/chapter-2.md`
- [X] T018 [US1] Research primary sources for Chapter 2, ensure APA 7th citation readiness `book/docs/chapter-2.md` (Manual task)
- [X] T019 [US1] Draft Chapter 2 content, integrating citations for all technical claims `book/docs/chapter-2.md` (Manual task)
- [X] T020 [US1] Review Chapter 2 against quality gates (content, citation, source quality, plagiarism) `book/docs/chapter-2.md` (Manual task)

#### Chapter 3: Kinematics, Dynamics, and Control of Bipedal Humanoids (US1, US2, P1)
- [X] T021 [US1,US2] Outline Chapter 3 (H1->H3 structure) `book/docs/chapter-3.md`
- [X] T022 [US1,US2] Research primary sources for Chapter 3, ensure APA 7th citation readiness `book/docs/chapter-3.md` (Manual task)
- [X] T023 [US1,US2] Draft Chapter 3 content, integrating citations and LaTeX for math `book/docs/chapter-3.md` (Manual task)
- [X] T024 [US1,US2] Create Mermaid/SVG diagrams for kinematics/dynamics, add to `book/static/img/` `book/static/img/ch3_diagrams.svg` (Manual task)
- [X] T025 [US1,US2] Review Chapter 3 against quality gates `book/docs/chapter-3.md` (Manual task)

**Checkpoint**: Foundational setup complete. Initial chapters drafted and reviewed.

---

## Phase 2: Core Systems & State-of-the-Art (Weeks 7–14) 🎯 Core Content

**Purpose**: Develop core technical chapters, integrating bleeding-edge research and practical examples.

#### Chapter 4: Sensing the Physical World (US2, P2)
- [X] T026 [US2] Outline Chapter 4 `book/docs/chapter-4.md`
- [X] T027 [US2] Research primary sources for Chapter 4 (2023-2025 papers) `book/docs/chapter-4.md` (Manual task)
- [X] T028 [US2] Draft Chapter 4 content, integrating citations `book/docs/chapter-4.md` (Manual task)
- [X] T029 [US2] Create Mermaid/SVG diagrams for sensing modalities, add to `book/static/img/` `book/static/img/ch4_diagrams.svg` (Manual task)
- [X] T030 [US2] Review Chapter 4 quality gates `book/docs/chapter-4.md` (Manual task)

#### Chapter 5: ROS 2 as the Robotic Nervous System (US2, P2)
- [X] T031 [US2] Outline Chapter 5 `book/docs/chapter-5.md`
- [X] T032 [US2] Research primary sources for ROS 2 applications `book/docs/chapter-5.md` (Manual task)
- [X] T033 [US2] Draft Chapter 5 content, integrating citations `book/docs/chapter-5.md` (Manual task)
- [X] T034 [US2] Develop and test ROS 2 code snippets, add to `book/static/code/` `book/static/code/ch5_ros2_snippets.py` (Manual task)
- [X] T035 [US2] Review Chapter 5 quality gates `book/docs/chapter-5.md` (Manual task)

#### Chapter 6: High-Fidelity Simulation (US2, P2)
- [X] T036 [US2] Outline Chapter 6 `book/docs/chapter-6.md`
- [X] T037 [US2] Research primary sources for Gazebo, Isaac Sim, Digital Twins `book/docs/chapter-6.md` (Manual task)
- [X] T038 [US2] Draft Chapter 6 content, integrating citations `book/docs/chapter-6.md` (Manual task)
- [X] T039 [US2] Create diagrams for simulation architectures `book/static/img/ch6_diagrams.svg` (Manual task)
- [X] T040 [US2] Review Chapter 6 quality gates `book/docs/chapter-6.md` (Manual task)

#### Chapter 7: Perception for Humanoids (US2, P2)
- [X] T041 [US2] Outline Chapter 7 `book/docs/chapter-7.md`
- [X] T042 [US2] Research primary sources for Visual SLAM, Scene Understanding `book/docs/chapter-7.md` (Manual task)
- [X] T043 [US2] Draft Chapter 7 content, integrating citations `book/docs/chapter-7.md` (Manual task)
- [X] T044 [US2] Develop and test Visual SLAM code snippets (ROS 2/Isaac Sim) `book/static/code/ch7_perception_snippets.py` (Manual task)
- [X] T045 [US2] Review Chapter 7 quality gates `book/docs/chapter-7.md` (Manual task)

#### Chapter 8: Locomotion and Balance (US1, US2, P2)
- [X] T046 [US1,US2] Outline Chapter 8 `book/docs/chapter-8.md`
- [X] T047 [US1,US2] Research primary sources (ZMP, RL-based locomotion) `book/docs/chapter-8.md` (Manual task)
- [X] T048 [US1,US2] Draft Chapter 8 content, integrating citations and math `book/docs/chapter-8.md` (Manual task)
- [X] T049 [US1,US2] Create diagrams for locomotion principles `book/static/img/ch8_diagrams.svg` (Manual task)
- [X] T050 [US1,US2] Review Chapter 8 quality gates `book/docs/chapter-8.md` (Manual task)

#### Chapter 9: Manipulation and Dexterous Hands (US2, P2)
- [X] T051 [US2] Outline Chapter 9 `book/docs/chapter-9.md`
- [X] T052 [US2] Research primary sources for manipulation and dexterous hands `book/docs/chapter-9.md` (Manual task)
- [X] T053 [US2] Draft Chapter 9 content, integrating citations `book/docs/chapter-9.md` (Manual task)
- [X] T054 [US2] Create diagrams for robotic hands/manipulators `book/static/img/ch9_diagrams.svg` (Manual task)
- [X] T055 [US2] Review Chapter 9 quality gates `book/docs/chapter-9.md` (Manual task)

**Checkpoint**: Core technical content and examples developed.

---

## Phase 3: Advanced Topics & Integration (Weeks 15–20) 🎯 Advanced Concepts

**Purpose**: Cover advanced topics, integrate concepts, and compare platforms.

#### Chapter 10: Vision-Language-Action Models and Cognitive Architectures for Robots (US1, P3)
- [X] T056 [US1] Outline Chapter 10 `book/docs/chapter-10.md`
- [X] T057 [US1] Research primary sources for VLA models and cognitive architectures `book/docs/chapter-10.md` (Manual task)
- [X] T058 [US1] Draft Chapter 10 content, integrating citations `book/docs/chapter-10.md` (Manual task)
- [X] T059 [US1] Create diagrams for VLA model architectures `book/static/img/ch10_diagrams.svg` (Manual task)
- [X] T060 [US1] Review Chapter 10 quality gates `book/docs/chapter-10.md` (Manual task)

#### Chapter 11: Sim-to-Real Transfer Techniques (US1, P3)
- [X] T061 [US1] Outline Chapter 11 `book/docs/chapter-11.md`
- [X] T062 [US1] Research primary sources for Sim-to-Real techniques `book/docs/chapter-11.md` (Manual task)
- [X] T063 [US1] Draft Chapter 11 content, integrating citations `book/docs/chapter-11.md` (Manual task)
- [X] T064 [US1] Create diagrams illustrating Sim-to-Real methods `book/static/img/ch11_diagrams.svg` (Manual task)
- [X] T065 [US1] Review Chapter 11 quality gates `book/docs/chapter-11.md` (Manual task)

#### Chapter 12: Current Humanoid Platforms: Technical Comparison (2025 Landscape) (US3, P3)
- [X] T066 [US3] Outline Chapter 12 `book/docs/chapter-12.md`
- [X] T067 [US3] Research publicly available specs for humanoid platforms (Atlas, Figure 02, Unitree G1, Tesla Optimus, Apptronik Apollo) `book/docs/chapter-12.md` (Manual task)
- [X] T068 [US3] Draft Chapter 12 content, integrating citations and comparison tables `book/docs/chapter-12.md` (Manual task)
- [X] T069 [US3] Create comparison table diagrams `book/static/img/ch12_table.svg` (Manual task)
- [X] T070 [US3] Review Chapter 12 quality gates `book/docs/chapter-12.md` (Manual task)

**Checkpoint**: Advanced topics covered and platform comparisons complete.

---

## Phase 4: Synthesis & Futures (Weeks 21–24) 🎯 Final Content Synthesis

**Purpose**: Synthesize all content, address ethical considerations, and look to the future.

#### Chapter 13: Safety, Ethics, and Societal Impact of Human-Scale Robots (P3)
- [X] T071 Outline Chapter 13 `book/docs/chapter-13.md`
- [X] T072 Research primary sources for safety and ethical considerations in robotics `book/docs/chapter-13.md` (Manual task)
- [X] T073 Draft Chapter 13 content, integrating citations `book/docs/chapter-13.md` (Manual task)
- [X] T074 Review Chapter 13 quality gates `book/docs/chapter-13.md` (Manual task)

#### Chapter 14: The Road Ahead: Research Frontiers and Open Problems (P3)
- [X] T075 Outline Chapter 14 `book/docs/chapter-14.md`
- [X] T076 Research cutting-edge research frontiers and open problems `book/docs/chapter-14.md` (Manual task)
- [X] T077 Draft Chapter 14 content, integrating citations `book/docs/chapter-14.md` (Manual task)
- [X] T078 Review Chapter 14 quality gates `book/docs/chapter-14.md` (Manual task)

#### Chapter 15: Conclusion and Future Directions (P3)
- [X] T079 Outline Chapter 15 `book/docs/chapter-15.md`
- [X] T080 Synthesize key takeaways from the entire book `book/docs/chapter-15.md` (Manual task)
- [X] T081 Draft Chapter 15 content `book/docs/chapter-15.md` (Manual task)
- [X] T082 Review Chapter 15 quality gates `book/docs/chapter-15.md` (Manual task)

### Cross-Chapter Consistency & Bibliography

- [X] T083 Perform final cross-chapter consistency pass (terminology, style, formatting) (Manual task)
- [X] T084 Complete master bibliography (`bib.tex` + Markdown version), ensuring ≥50 unique sources and ≥50% peer-reviewed `bib.tex`, `book/docs/bibliography.md` (Manual task)
- [X] T085 Update `book/sidebar.js` with final chapter titles and structure `book/sidebar.js`

**Checkpoint**: All content drafted and consistent.

---

## Phase 5: Validation & Deployment (Weeks 25–26) 🎯 Final Review & Launch

**Purpose**: Comprehensive quality assurance and official publication.

### Quality Assurance

- [X] T086 Run full plagiarism scan (Turnitin + GPTZero) on all book content (Manual task)
- [X] T087 Coordinate external technical review by a PhD-level expert (Manual task)
- [X] T088 Incorporate feedback from external technical review (Manual task)
- [X] T089 Perform final proofreading and copyediting (Manual task)
- [X] T090 Validate Flesch-Kincaid readability (grade 10–12 target) (Manual task)

### Deployment

- [ ] T091 Build Docusaurus site locally, verify zero errors
- [ ] T092 Deploy Docusaurus site to GitHub Pages via CI/CD
- [ ] T093 Verify live GitHub Pages deployment functionality
- [ ] T094 Generate PDF version of the book via Docusaurus/WeasyPrint

**Checkpoint**: Book published and validated.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup & Foundation)**: No dependencies - can start immediately.
- **Phase 2 (Core Systems & State-of-the-Art)**: Depends on Phase 1 completion.
- **Phase 3 (Advanced Topics & Integration)**: Depends on Phase 2 completion.
- **Phase 4 (Synthesis & Futures)**: Depends on Phase 3 completion.
- **Phase 5 (Validation & Deployment)**: Depends on Phase 4 completion.

### Within Each Chapter

- Outlining → Research → Drafting → Diagram/Code Integration → Review.
- Tests for code snippets MUST be written and FAIL before implementation.

### Parallel Opportunities

- Tasks marked with `[P]` within a phase can run in parallel.
- Research for different chapters in the same phase can run in parallel.
- Diagram creation and code snippet development for different chapters can run in parallel.

---

## Implementation Strategy

### Incremental Delivery (Chapter by Chapter)

1.  Complete Phase 1 (Setup & Foundation).
2.  For each subsequent phase, complete one chapter and its associated tasks (outline, research, draft, diagrams, code, review) fully before moving to the next chapter within that phase. This allows for continuous quality checks and feedback integration.
3.  Utilize checkpoints to validate progress after each major phase.

### Parallel Team Strategy (if applicable)

With multiple contributors:

1.  Team completes Phase 1 (Setup & Foundation) together.
2.  Once Phase 1 is done, different team members can tackle different chapters within a phase in parallel (e.g., one person drafts Chapter 4, another researches Chapter 5).
3.  Cross-chapter consistency and master bibliography tasks (Phase 4) will require coordination.

---

## Notes

- All code snippets must be testable and pass in the specified environments.
- Every technical claim must be backed by a verifiable source.
- Maintain a consistent writing style and tone throughout the book.
- Proactively track progress against the timeline and adjust as needed.
