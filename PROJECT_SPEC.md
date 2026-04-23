# MathMentor — Gemma 4 Good Hackathon Project Spec

**Author:** Bartek Ogórkiewicz (solo)
**Hackathon:** [Gemma 4 Good Hackathon on Kaggle](https://www.kaggle.com/competitions/gemma-4-good-hackathon)
**Prize Pool:** $200,000
**Deadline:** May 18, 2026 (23:59 UTC)
**Track:** Future of Education
**License:** Apache 2.0

---

## 1. Mission

**Democratize access to personalized math tutoring.** Private tutoring costs $20–50/hour globally — unaffordable for most families. Rural and underserved communities often have limited internet. Students struggle with abstract concepts that benefit from visualization. Gemma 4's on-device capabilities make it possible to deliver a real, personalized, animation-rich math tutor that runs on the hardware families already own: mid-range laptops, old ThinkPads, Chromebooks — even Raspberry Pi 5.

**The philosophy:** AI should reach those who need it most, not only those with fast internet and expensive hardware. Privacy and accessibility are not features — they are the foundation.

---

## 2. Unique Value Proposition

Most hackathon AI apps are generic chatbots. MathMentor is different:

1. **Real visual output, not just text.** Custom [Manim](https://www.manim.community/) animations tailored to the student's specific confusion.
2. **Runs locally on commodity hardware.** No cloud, no API costs, no internet required after setup. Target: 8GB RAM entry-level laptop.
3. **Adaptive model scaling.** Same codebase, three models — pick what your hardware supports.
4. **Closes the learning loop.** Spaced repetition with auto-generated variants + Anki export.
5. **Interactive animations.** Click elements for deeper explanations.

---

## 3. Adaptive Model Selector

The application ships with a model selector that adapts to the user's hardware:

| Tier | Model | RAM | Use case | Multimodal |
|------|-------|-----|----------|------------|
| **Lightweight** | Gemma 4 E2B | 5 GB (4-bit) | Old laptops, Raspberry Pi 5, Chromebooks | Text only |
| **Balanced** (default) | Gemma 4 E4B | 8 GB (4-bit) / 12 GB (8-bit) | Most modern laptops, 8+ GB RAM | Text + image |
| **Premium** | Gemma 4 26B MoE | 18 GB (4-bit) | Workstations, 32+ GB RAM | Text + image |

**Why this matters for judges:** one codebase, three deployment targets. The 2B model serves communities with the least hardware. The 26B model serves users with capable machines. No one is excluded.

**Default behavior:** auto-detect available RAM, pick the best tier that fits. User can override.

---

## 4. Tech Stack

### Runtime
- **Models:** Gemma 4 E2B, E4B, 26B MoE (all quantized)
- **Inference:** Ollama (auto-uses Apple MLX on Silicon Macs)
- **Endpoint:** `http://localhost:11434`

### Backend
- **Language:** Python 3.12
- **Framework:** FastAPI
- **DB:** SQLite + SQLAlchemy
- **Animation:** Manim Community edition, subprocess rendering

### Frontend
- **Framework:** React + TypeScript + Vite
- **Video:** react-player for mp4 scenes
- **Interactive SVG:** custom overlay system (see §8)
- **Styling:** Tailwind + shadcn/ui

### Dev Tools
- **Claude Code** (CLI) for implementation
- **Claude app desktop** with project for architecture and write-up
- **Git/GitHub** — public repo required

---

## 5. Architecture

```
┌──────────────────────────────────────────────┐
│  User input: text + optional photo           │
│  "Explain the derivative of sine"             │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  FastAPI /ask endpoint                        │
│  - Loads conversation history from SQLite     │
│  - Builds system prompt + few-shot examples   │
│  - Sends to Gemma 4 via Ollama                │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  Gemma 4 reasoning (thinking mode visible)    │
│  - Understands concept + student level        │
│  - Decides: explain + animate? just text?     │
│  - Function calls:                            │
│    * generate_manim_scene(concept, params)    │
│    * register_interactive_elements(...)       │
│    * add_to_spaced_repetition(concept)        │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  Manim subprocess                             │
│  - Executes generated Python code             │
│  - Renders SVG frames (key scenes) + mp4      │
│  - Stores in ./videos/session_id/             │
└──────────────┬───────────────────────────────┘
               ↓
┌──────────────────────────────────────────────┐
│  Frontend displays:                           │
│  - Text explanation                           │
│  - Video OR interactive SVG scenes            │
│  - Thinking panel (expandable)                │
│  - "Practice this" button → spaced repetition │
└──────────────────────────────────────────────┘
```

---

## 6. Features by priority

### MUST HAVE (weeks 1–2)
- [ ] Core flow: prompt → Gemma → Manim → video rendered
- [ ] Model selector with auto-detection (E2B/E4B/26B)
- [ ] Multimodal input: upload photograph of handwritten problem
- [ ] Function calling: `generate_manim_scene`, `explain_concept`
- [ ] Visible thinking mode in UI (collapsible panel)
- [ ] Basic conversation history (SQLite)

### SHOULD HAVE (weeks 2–3)
- [ ] Spaced repetition system (SM-2 algorithm)
- [ ] User rates exercise difficulty (1-5) after completion
- [ ] Auto-generated variants of completed exercises
- [ ] Anki export (`.apkg` via genanki) with embedded animations
- [ ] Eval suite: 50 curated Polish math problems with metrics
- [ ] Comparative benchmarks: E2B vs E4B vs 26B on same tasks

### NICE TO HAVE (weeks 3–4 if time)
- [ ] Interactive SVG overlays (click elements for deeper explanation)
- [ ] Concept map — mind map of topics touched in session
- [ ] Demo recorded on low-end hardware (Raspberry Pi 5 / old ThinkPad)
- [ ] Voice input (TTS+STT with on-device model)

---

## 7. Gemma 4 Integration Details

### Function calling schema

```python
tools = [
    {
        "name": "generate_manim_scene",
        "description": "Generates Manim Python code for mathematical animation.",
        "parameters": {
            "concept": "What's being taught (e.g. 'derivative of sin')",
            "approach": "Pedagogical approach (geometric, algebraic, limit-based)",
            "prerequisites": "What student should know first",
            "scene_count": "5-10 typical"
        }
    },
    {
        "name": "register_interactive_elements",
        "description": "Marks animation elements as clickable with explanations.",
        "parameters": {
            "elements": "list[{id, label, explanation, bbox}]"
        }
    },
    {
        "name": "add_to_spaced_repetition",
        "description": "Adds exercise to student's review queue.",
        "parameters": {
            "concept", "difficulty_estimate", "question", "answer"
        }
    }
]
```

### System prompt skeleton

```
You are MathMentor, a patient and pedagogically-sound math tutor.

Rules:
1. Never give the answer immediately. Guide through reasoning.
2. Concrete examples before abstract formalism.
3. Ask if student wants visualization before generating animation.
4. Match student level — detect from vocabulary.
5. Name common misconceptions explicitly.
6. After explaining, suggest adding to spaced repetition.
7. Generate Manim code that is correct and safe — no file I/O, no network.

Available tools: generate_manim_scene, register_interactive_elements,
add_to_spaced_repetition.

Thinking mode: enabled. Show reasoning before answering.
```

---

## 8. Interactive SVG Overlay System

Instead of just mp4, Manim exports key scenes as SVG + metadata JSON. Frontend
overlays invisible clickable regions on top of SVG elements.

### How it works
1. Gemma generates Manim code + calls `register_interactive_elements(...)`
2. Python wrapper runs Manim with `--format=svg`, produces frame SVGs
3. Wrapper parses Manim's Mobject tree, extracts bounding boxes by element ID
4. Frontend renders SVG, places transparent `<div>` overlays at each bbox
5. Click on overlay → fetch deeper explanation from Gemma (scoped to element)

### Fallback
If SVG overlays don't work, mp4 with clickable timeline markers is acceptable.
Don't block MVP on interactivity.

---

## 9. Spaced Repetition Design

### Database

```sql
CREATE TABLE concepts (id TEXT PRIMARY KEY, name TEXT, parent_concept_id TEXT);

CREATE TABLE exercises (
    id TEXT PRIMARY KEY, concept_id TEXT,
    question TEXT, answer TEXT, difficulty INTEGER,
    manim_code TEXT, video_path TEXT, created_at TIMESTAMP
);

CREATE TABLE review_log (
    id TEXT PRIMARY KEY, exercise_id TEXT, rating INTEGER,
    reviewed_at TIMESTAMP, next_review_at TIMESTAMP,
    interval_days INTEGER, ease_factor REAL
);
```

### SM-2 algorithm (simplified)

```python
def update_review(rating, prev_interval_days, prev_ease_factor):
    if rating < 3:
        new_interval = 1
        new_ease = max(1.3, prev_ease_factor - 0.2)
    else:
        new_interval = prev_interval_days * prev_ease_factor
        new_ease = prev_ease_factor + (0.1 - (5 - rating) * 0.08)
    return new_interval, new_ease
```

### Variant generation
When review triggers, Gemma generates structurally similar variant instead of
exact same problem. Prevents rote memory.

---

## 10. Anki Export

Using `genanki` library. Each deck contains:
- Question as front
- Answer + explanation as back
- Manim animation as embedded media

User exports → gets `.apkg` → opens in Anki.

---

## 11. Eval Suite Requirements

50 curated math problems covering:
- **High school (pre-calculus & calculus):** derivatives, limits, integrals, geometry, probability, sequences
- **Undergraduate:** discrete math (combinatorics, graph theory), analysis (series, continuity), linear algebra

For each problem × each model (E2B, E4B, 26B):
- Concept identification correctness (binary)
- Animation code compiles (binary)
- Animation content correctness (human rated 1-5)
- Explanation quality (human rated 1-5)
- Generation time (seconds)
- Peak RAM usage (GB)

Output: CSV + bar charts for write-up. Key story:
*"E2B achieves 71% of E4B quality at 40% RAM. E4B matches 26B on 80% of tasks."*

---

## 12. Submission Deliverables

1. **Working demo** — deployable locally with clear instructions
2. **Public code repository** — this repo, Apache 2.0
3. **Technical write-up** — how Gemma 4 was applied
4. **Video demo** — 2-3 minutes, 3 different problems

### Video demo outline
- 0:00–0:15: Problem (student without tutor access, underserved community)
- 0:15–0:45: Demo 1 — photo → animated explanation
- 0:45–1:15: Demo 2 — interactive click-through
- 1:15–1:45: Demo 3 — spaced repetition + Anki export
- 1:45–2:15: Technical highlights (thinking mode, model scaling)
- 2:15–2:30: Running on cheap hardware

---

## 13. Development Principles (for Claude Code)

1. **Prefer simple over clever.** Hackathon, not research.
2. **Test as you go.** Minimal pytest per endpoint.
3. **Keep prompts in `prompts/` directory** as separate files.
4. **Don't mock Gemma in dev.** Always run real inference.
5. **Log everything.** Model input/output, function calls, render times.
6. **Ask before destroying.** If modifying >50 lines or deleting files, ask.
7. **Small, descriptive commits.** Not `stuff`.
8. **Keep README updated** when architecture changes.

---

## 14. Timeline

**Week 1 (Apr 24 – Apr 30):** PoC
- Ollama + Gemma 4 E4B running locally
- Manim pipeline manual test
- FastAPI + React skeletons
- First end-to-end flow

**Week 2 (May 1 – May 7):** Core features
- Model selector
- Multimodal input
- Function calling
- Thinking mode UI
- Eval suite start (10 problems)

**Week 3 (May 8 – May 14):** Polish + advanced
- Spaced repetition
- Anki export
- Interactive SVG if time
- Full eval suite (50 problems)
- Low-end hardware test

**Week 4 (May 15 – May 18):** Submission
- Write-up (2 days)
- Video recording (1 day)
- Final testing
- Submit before May 18, 23:59 UTC

---

## 15. Known Risks

- **Models may hallucinate Manim API.** Mitigation: RAG over Manim docs,
  retry loop with error feedback, curated few-shot examples.
- **Rendering too slow for live demo.** Mitigation: pre-render cached scenes,
  show loading states clearly.
- **Author's other commitments** (MIMUW coursework, PO exam early May,
  analysis exam mid-May). Mitigation: focus on MUST HAVE until May 1,
  then full sprint.

---

## 16. Author context for Claude

Bartek is a 1st-year CS student at MIMUW with strong math background. Speaks
Polish natively, English fluently. **The entire project — code, UI, submission
write-up, README, video demo — is in English.** Target audience is international
(Kaggle jury is Google DeepMind). Math content is universal; examples should
be language-agnostic where possible.

Bartek prefers casual Polish when chatting, concise explanations, reality
checks over hype. Responds well to direct questions and numerical sanity
checks. Dislikes vibe-coding without understanding what's being built.
