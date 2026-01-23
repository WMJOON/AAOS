---
type: "DNA-RULE"
version: "0.1.0"
description: "AAOS-COF v0.1.2의 구조, 규칙, 스킬, 생명주기를 정의하는 통합 DNA"
status: canonical
---

# AAOS-COF DNA (v0.1.2)

본 DNA는 `COF v0.1.2` 군체(Swarm) 구조를 정의하는 핵심 유전체(Genome)이다.
META Doctrine(METADoctrine.md)의 2.1.1-1 조항에 의거하여 작성되었다.

## 1. Rule Genome (규칙 유전체)

- **Source**: `rule/context-orchestrated-filesystem.md`
- **Role**:
  - Context Node의 정의
  - Creation/Modification 권한 제어 (Principle)
  - Ticket Node 구조 정의

## 2. Skill Genome (행동 유전체)

- **Source**: `skills/`
- **Active Skills**:
  - `cof-task-manager-node`: Task Manager 및 Ticket 생성/관리 자동화

## 3. Lifecycle Genome (생명주기 유전체)

- **Source**: `DNA_BLUEPRINT.md`
- **Role**:
  - Natural Dissolution (자연 소멸) 조건 정의
  - Resource Limits (자원 상한) 정의
  - Inquisitor (심판관) 감사 로그 연동

---

> "모든 COF 인스턴스는 본 DNA에 정의된 규칙과 행동 범위를 벗어날 수 없다."
