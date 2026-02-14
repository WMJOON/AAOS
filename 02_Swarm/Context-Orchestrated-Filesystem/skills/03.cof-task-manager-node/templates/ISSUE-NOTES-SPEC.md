# issue_notes/ Specification

작업 중 발생한 이슈, 의사결정, 논의 사항 기록 노드.

## Structure

```
NN.agents-task-context/
└── issue_notes/
    ├── RULE.md
    └── {parentName}-issue_note-{timestamp}.md
```

## Creation Command

```bash
mkdir -p {targetPath}/01.agents-task-context/issue_notes
```

## Rules

1. 이슈는 발생 즉시 기록
2. 해결된 이슈는 해결 방법과 영향 범위 명시
3. 반복 이슈는 상위 troubleshooting.md로 승격

## File Naming

`{parentName}-issue_note-{YYYYMMDD-HHMM}.md`

## RULE.md Template

```markdown
# issue_notes/ Rule

## Purpose
작업 수행 중 발생한 이슈·의사결정·논의 사항 기록.

## Rules
1. 발생 즉시 기록
2. 해결 시 방법 및 영향 범위 명시
3. 반복 이슈는 troubleshooting.md로 승격
```
