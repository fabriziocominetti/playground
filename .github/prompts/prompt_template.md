---
name: 'prompt_name'
agent: 'agent'
model: GPT-5
description: 'Concise purpose statement (what this prompt achieves).'
---
## 1. High-Level Goal
Clearly state the objective in one sentence.
Goal: "Generate {{ project_name }} design answering: {{ user_query }}".

## 2. Context
Provide domain/background context.
Domain Context:
"{{ domain_context }}"

## 3. Task Breakdown
List explicit subtasks or phases the model must address.
Subtasks:
1. Clarify assumptions.
2. Provide structured solution/design.
3. Highlight trade-offs.
4. List next actionable steps.

## 4. Constraints & Guardrails
"{{ constraints }}"  (e.g. latency < 2s, use only Python stdlib, avoid external APIs, keep memory under 512MB).
Hard requirements must be satisfied or explicitly flagged if impossible.

## 5. Required Output Format
Produce output using this structure:
```
Title: <short descriptive title>
Summary: <2-3 sentences>
Detailed Steps:
	- Step 1: ...
	- Step 2: ...
Architecture (if applicable):
	Components:
		- Name: Purpose
Data Structures:
	- <Name>: <Fields>
Code Snippets:
	```python
	# minimal, runnable, focused
	```
Validation Checklist:
	- [ ] Requirement A
	- [ ] Requirement B
Risks & Mitigations:
	- Risk: <description> -> Mitigation: <strategy>
Next Actions (chronological):
	1. ...
	2. ...
```

## 6. Style & Tone
Tone: concise, actionable, technically precise, no fluff.
Avoid: repetition, unsupported claims, verbose marketing language.

## 7. Reasoning Instructions
Use explicit chain-of-thought internally; return only the structured final answer (no raw reasoning). If trade-offs are unclear, list information needed.

## 8. Embedded Examples (Few-Shot)
{{ examples }}
Example Pattern:
Input: "Design ingestion for weather API"
Output (excerpt):
```
Title: Weather API Ingestion Pipeline
Summary: Provides hourly normalized weather records.
Detailed Steps:
	- Step 1: Pull JSON from provider every hour using Airflow DAG.
	- Step 2: Validate schema (temp, humidity, wind) with Pydantic.
	- Step 3: Store raw in DuckDB staging, then transform to curated parquet.
Architecture:
	Components:
		- FetchOperator: requests + retry
		- Validator: pydantic models
		- StorageLayer: duckdb tables (raw/weather_raw, curated/weather_hourly)
```

## 9. Evaluation Criteria (for self-check)
The answer must:
- Satisfy all listed constraints.
- Provide runnable or near-runnable code where requested.
- Include at least one risk & mitigation.
- Use the specified output structure exactly.
- Explicitly mark unmet constraints.

## 10. Variable Reference
Placeholder catalog:
| Variable | Meaning |
|----------|---------|
| {{ project_name }} | Project or pipeline name |
| {{ user_query }} | User's current question or need |
| {{ domain_context }} | Background info/domain specifics |
| {{ constraints }} | Hard limits/resources/policies |
| {{ examples }} | Few-shot guidance block |

## 11. Invocation Guidance
Fill variables programmatically or manually.
Pseudo-code (Python):
```python
from pathlib import Path
template = Path('.github/prompts/prompt_template.md').read_text()
filled = (template
	.replace('{{ project_name }}', 'Weather Pipeline')
	.replace('{{ user_query }}', 'Design a daily aggregation DAG')
	.replace('{{ domain_context }}', 'We collect hourly weather readings from API X.')
	.replace('{{ constraints }}', 'Use Airflow, DuckDB, no external paid services.')
	.replace('{{ examples }}', 'Input: ...\nOutput: ...'))
print(filled)
```

## 12. Adaptation Patterns
- Data Engineering: emphasize schema, storage layers, scheduling.
- RAG / LLM: add sections for embedding strategy, chunking, retrieval eval metrics.
- Orchestration: include DAG/task dependencies diagram in Architecture.
- Chatbot: include user intent classification + fallback strategy.

## 13. Extension Hooks
Add optional sections if needed:
- Security Considerations
- Performance Targets
- Monitoring & Observability
- Cost Estimate

<!-- End of template. Replace placeholders above this line for each new prompt instance. -->