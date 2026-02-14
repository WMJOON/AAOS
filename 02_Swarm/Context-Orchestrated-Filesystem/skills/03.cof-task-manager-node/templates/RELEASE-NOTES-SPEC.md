# release_notes/ Specification

티켓 또는 작업 단위 완료 결과 요약 기록 노드.

## Structure

```
NN.agents-task-context/
└── release_notes/
    ├── RULE.md
    └── {parentName}-release_note-{timestamp}.md
```

## Creation Command

```bash
mkdir -p {targetPath}/01.agents-task-context/release_notes
```

## Rules

1. 주요 변경 사항과 산출물 간결히 정리
2. 후속 작업 또는 의존 티켓에 영향 주는 사항 반드시 명시

## File Naming

`{parentName}-release_note-{YYYYMMDD-HHMM}.md`

## RULE.md Template

```markdown
# release_notes/ Rule

## Purpose
작업 단위 완료 결과 요약 기록.

## Rules
1. 주요 변경 사항·산출물 간결히 정리
2. 후속 작업·의존 티켓 영향 사항 명시
```
