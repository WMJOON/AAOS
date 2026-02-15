#!/usr/bin/env python3
"""
awt-topology-design cone module scaffold script.
Convergence Cone 프레임워크 기반 워크플로우 디렉토리와 workflow.md를 생성한다.

v1.0 → v1.1 변경:
  - 비선형 DAG 토폴로지 지원 (--edges)
  - θ_GT regime별 종료 전략 분리
  - termination/ 디렉토리 신설 (1급 산출물)
  - 에러 핸들링 강화

Usage:
    # 선형 체인 (기본)
    python3 scaffold_workflow.py \\
        --name my-etl-pipeline \\
        --nodes "classify:converge:L1,extract:converge:L1,reason:diverge:L3,validate:validate:L0" \\
        --output /path/to/output

    # 비선형 토폴로지
    python3 scaffold_workflow.py \\
        --name market-analysis \\
        --nodes "scan:converge:L1,analyze:diverge:L3,synthesize:converge:L1" \\
        --edges "scan->analyze,analyze->analyze:loop,analyze->synthesize" \\
        --d-min 5 \\
        --cooldown 2 \\
        --output /path/to/output
"""

import argparse
import os
import sys
from datetime import datetime, timezone

# ── θ_GT 레벨 → 기본값 매핑 ──

VALID_MODES = {"converge", "diverge", "validate"}
VALID_THETA_LEVELS = {"L0", "L1", "L2", "L3", "L4"}
VALID_EDGE_TYPES = {"sequential", "loop", "conditional", "fan_out"}

THETA_DEFAULTS = {
    "L0": {"mode": "validate",  "regime": "convergent",   "model": "Haiku",        "temp": "0",        "d_min": 0, "termination_type": "answer_convergence"},
    "L1": {"mode": "converge",  "regime": "convergent",   "model": "Haiku/Sonnet", "temp": "0~0.3",    "d_min": 0, "termination_type": "answer_convergence"},
    "L2": {"mode": "diverge→converge", "regime": "verificatory", "model": "Sonnet", "temp": "0.5→0.2", "d_min": 4, "termination_type": "verification_pass"},
    "L3": {"mode": "diverge",   "regime": "deliberative", "model": "Sonnet/Opus",  "temp": "0.7~1.0",  "d_min": 6, "termination_type": "decision_sufficiency"},
    "L4": {"mode": "diverge",   "regime": "deliberative", "model": "Opus",         "temp": "0.7~1.0",  "d_min": 8, "termination_type": "decision_sufficiency"},
}

# 하위 호환: 기존 라벨 → 레벨 매핑
LEGACY_THETA_MAP = {
    "very_narrow": "L0", "narrow": "L1", "medium": "L2", "wide": "L3",
}


def error_exit(msg):
    print(f"❌ Error: {msg}", file=sys.stderr)
    sys.exit(1)


def resolve_theta(raw):
    """θ_GT 라벨을 정규화. 레거시 라벨도 지원."""
    if raw in VALID_THETA_LEVELS:
        return raw
    if raw in LEGACY_THETA_MAP:
        return LEGACY_THETA_MAP[raw]
    error_exit(
        f"Unknown θ_GT level: '{raw}'. "
        f"Valid: {sorted(VALID_THETA_LEVELS)} or legacy: {sorted(LEGACY_THETA_MAP.keys())}"
    )


def parse_nodes(nodes_str):
    """Parse node string: 'name:mode[:theta],…'"""
    nodes = []
    for i, part in enumerate(nodes_str.split(","), 1):
        tokens = [t.strip() for t in part.strip().split(":")]
        if not tokens or not tokens[0]:
            error_exit(f"Empty node definition at position {i}")

        name = tokens[0]
        mode = tokens[1] if len(tokens) > 1 else None
        theta_raw = tokens[2] if len(tokens) > 2 else None

        # mode 검증
        if mode and mode not in VALID_MODES:
            error_exit(
                f"Node '{name}': Invalid mode '{mode}'. Valid: {sorted(VALID_MODES)}"
            )

        # θ 미지정 시 mode에서 추론, mode도 없으면 기본값
        if theta_raw:
            theta = resolve_theta(theta_raw)
        elif mode:
            theta = {"converge": "L1", "diverge": "L3", "validate": "L0"}.get(mode, "L1")
        else:
            theta = "L1"

        defaults = THETA_DEFAULTS.get(theta, THETA_DEFAULTS["L1"])

        # mode 미지정 시 θ에서 추론
        if not mode:
            mode = defaults["mode"].split("→")[0]  # "diverge→converge" → "diverge"

        node = {
            "index": i,
            "id": f"n{i}",
            "name": name,
            "mode": mode,
            "theta": theta,
            "regime": defaults["regime"],
            "model": defaults["model"],
            "temp": defaults["temp"],
            "d_min": defaults["d_min"],
            "termination_type": defaults["termination_type"],
        }
        nodes.append(node)
    return nodes


def parse_edges(edges_str, nodes):
    """Parse edge string: 'a->b,a->c:loop,…'"""
    node_ids = {n["name"] for n in nodes}
    edges = []

    for part in edges_str.split(","):
        part = part.strip()
        if not part:
            continue

        # 'from->to:type' 또는 'from->to'
        if "->" not in part:
            error_exit(f"Invalid edge format: '{part}'. Expected 'from->to[:type]'")

        arrow_parts = part.split("->")
        src = arrow_parts[0].strip()
        dst_and_type = arrow_parts[1].strip().split(":")
        dst = dst_and_type[0].strip()
        etype = dst_and_type[1].strip() if len(dst_and_type) > 1 else "sequential"

        if src not in node_ids:
            error_exit(f"Edge source '{src}' not found in nodes: {sorted(node_ids)}")
        if dst not in node_ids:
            error_exit(f"Edge target '{dst}' not found in nodes: {sorted(node_ids)}")
        if etype not in VALID_EDGE_TYPES:
            error_exit(f"Invalid edge type '{etype}'. Valid: {sorted(VALID_EDGE_TYPES)}")

        edges.append({"from": src, "to": dst, "type": etype})

    return edges


def infer_linear_edges(nodes):
    """노드 순서대로 선형 엣지 생성."""
    return [
        {"from": nodes[i]["name"], "to": nodes[i + 1]["name"], "type": "sequential"}
        for i in range(len(nodes) - 1)
    ]


def detect_topology(edges):
    """엣지 패턴으로 토폴로지 유형 추론."""
    types = {e["type"] for e in edges}
    if "loop" in types:
        return "loop"
    src_counts = {}
    for e in edges:
        src_counts[e["from"]] = src_counts.get(e["from"], 0) + 1
    if any(c > 1 for c in src_counts.values()):
        if "conditional" in types:
            return "conditional"
        return "fan_out"
    return "linear"


def iso_now_z() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def is_strategy_or_high_risk(workflow_class, risk_tolerance):
    cls = (workflow_class or "").strip().lower()
    risk = (risk_tolerance or "").strip().lower()
    return cls in {"strategy", "high_risk"} or risk == "high"


def make_gate_node(name, index):
    defaults = THETA_DEFAULTS["L0"]
    return {
        "index": index,
        "id": f"n{index}",
        "name": name,
        "mode": "validate",
        "theta": "L0",
        "regime": defaults["regime"],
        "model": defaults["model"],
        "temp": defaults["temp"],
        "d_min": defaults["d_min"],
        "termination_type": defaults["termination_type"],
    }


def ensure_strategy_gate(nodes, edges):
    node_names = [n["name"] for n in nodes]
    next_index = len(nodes) + 1
    for gate in ("C1", "H1", "H2"):
        if gate not in node_names:
            nodes.append(make_gate_node(gate, next_index))
            node_names.append(gate)
            next_index += 1

    edge_keys = {(e["from"], e["to"]) for e in edges}
    required = [("T4", "C1"), ("C1", "H1"), ("H1", "H2")]
    for src, dst in required:
        if src in node_names and dst in node_names and (src, dst) not in edge_keys:
            edges.append({"from": src, "to": dst, "type": "sequential"})
            edge_keys.add((src, dst))

    # 가능한 경우 H2 뒤를 기존 합성 노드로 연결한다.
    if "H2" in node_names:
        downstream = None
        for candidate in ("T5", "T8"):
            if candidate in node_names:
                downstream = candidate
                break
        if downstream and ("H2", downstream) not in edge_keys:
            edges.append({"from": "H2", "to": downstream, "type": "sequential"})


# ── 문서 생성 ──

def gen_mermaid(nodes, edges):
    """Mermaid DAG 생성."""
    node_map = {n["name"]: n for n in nodes}
    lines = ["```mermaid", "graph TD"]

    for n in nodes:
        label = f'{n["name"]}\\n[{n["mode"]}|{n["theta"]}|{n["regime"]}]'
        lines.append(f'    {n["id"]}["{label}"]')

    for e in edges:
        src_id = node_map[e["from"]]["id"]
        dst_id = node_map[e["to"]]["id"]
        if e["type"] == "loop":
            lines.append(f'    {src_id} -->|loop: termination_check| {dst_id}')
        elif e["type"] == "conditional":
            lines.append(f'    {src_id} -.->|conditional| {dst_id}')
        else:
            lines.append(f'    {src_id} --> {dst_id}')

    lines.append("```")
    return "\n".join(lines)


def gen_workflow_md(
    wf_name,
    nodes,
    edges,
    d_min_override,
    cooldown,
    strategy_gate_enabled,
    proposal_id,
    visibility_tier,
):
    """workflow.md 생성."""
    today = datetime.now().strftime("%Y.%m.%d")
    topology = detect_topology(edges)
    mermaid = gen_mermaid(nodes, edges)

    # 노드 속성 테이블
    table_rows = []
    for n in nodes:
        d = d_min_override if d_min_override and n["regime"] == "deliberative" else n["d_min"]
        table_rows.append(
            f'| {n["id"]} | {n["name"]} | `{n["mode"]}` | {n["theta"]} '
            f'| {n["regime"]} | {n["model"]} | {n["temp"]} | {d or "-"} '
            f'| `{n["termination_type"]}` |'
        )

    # Deliberative 노드 종료 상세
    delib_sections = []
    for n in nodes:
        if n["regime"] == "deliberative":
            d = d_min_override or n["d_min"]
            delib_sections.append(f"""### {n["id"]}: {n["name"]} — Deliberative 종료 규칙

- **θ_GT**: {n["theta"]} ({n["regime"]} regime)
- **종료 타입**: `decision_sufficiency`
- **D_min**: {d}
- **쿨다운 윈도우(w)**: {cooldown}
- **종료 공식**:
  ```
  Terminate_deliberative(k) =
    D(k) ≥ {d}
    AND orthogonality(n_k, {{n_1..n_{{k-1}}}}) < ε  (연속 {cooldown}회)
    AND (ΔC(k) < δ  OR  Δsem(k) < τ)
  ```
- **D_min 미달 시**: perspective forcing → `termination/perspective_forcing.md`
- **종료 선언 형식**: → `termination/strategy.md` 참조
- **종료의 의미**: "충분히 탐색하여 판단할 수 있다" (NOT "최선의 답을 찾았다")""")

    delib_detail = "\n\n".join(delib_sections) if delib_sections else "_deliberative 노드 없음_"

    pf1_block = ""
    if strategy_gate_enabled:
        pf1_block = """## Mandatory Preflight

- PF1: 멘탈모델 먼저 세팅할까요?

## Strategy/High-Risk Gate

- 필수 노드: C1, H1, H2
- 필수 엣지: T4 -> C1 -> H1
- H1 finalization 전 web evidence + COWI artifacts 검증 필요
"""

    return f"""---
artifact_type: workflow_topology_spec
owner_swarm: agentic-workflow-topology
proposal_id: "{proposal_id}"
visibility_tier: "{visibility_tier}"
generated_at: "{iso_now_z()}"
workflow_name: "{wf_name}"
---

# {wf_name}

> Convergence Cone v1.1 기반 워크플로우 정의서
> Generated: {today}

---

## Overview

- **워크플로우**: {wf_name}
- **노드 수**: {len(nodes)}
- **토폴로지**: {topology}
- **설계 기준**: Cone Boundary Principle + Orthogonality Principle

---

## θ_GT Profile

| 노드 | 이름 | Mode | θ_GT | Regime | 모델 | Temp | D_min | 종료 타입 |
|------|------|------|------|--------|------|------|-------|----------|
{chr(10).join(table_rows)}

---

## Node Graph

{mermaid}

---

{pf1_block}
---

## Termination Strategy ⭐

종료는 regime에 따라 다른 철학을 따른다:

| Regime | 해당 노드 | 종료 = | 종료 타입 |
|--------|----------|--------|----------|
| Convergent | {', '.join(n['name'] for n in nodes if n['regime']=='convergent') or '-'} | 정답 도달 | `answer_convergence` |
| Verificatory | {', '.join(n['name'] for n in nodes if n['regime']=='verificatory') or '-'} | 기준 통과 | `verification_pass` |
| Deliberative | {', '.join(n['name'] for n in nodes if n['regime']=='deliberative') or '-'} | 충분한 근거 확보 | `decision_sufficiency` |

{delib_detail}

상세 규칙: → `termination/strategy.md`

---

## Cost Simulation

| 지표 | 기존(단일) | 분할 후 | 변화 |
|------|-----------|--------|------|
| 종합 F1 | _측정 필요_ | _측정 필요_ | |
| 평균 토큰/건 | _측정 필요_ | _측정 필요_ | |
| 예상 월비용 | _측정 필요_ | _측정 필요_ | |
| 종료까지 평균 반복 | N/A | _측정 필요_ | |
| 조율 오버헤드 | 0 | _측정 필요_ | |

채택 기준: `split_quality / split_cost > baseline × 1.1`

---

## Decision Log

- 분할 판단 근거: θ_GT 불연속 변화 지점 {len(nodes)-1}개 식별
- 토폴로지 선택 근거: {topology}
- 분할 채택 조건: → _검증 필요_
"""


def gen_node_md(node, cooldown):
    """노드별 상세 파일 생성."""
    return f"""# Node {node["index"]}: {node["name"]}

## 속성

- **Mode**: `{node["mode"]}`
- **θ_GT**: {node["theta"]}
- **Regime**: {node["regime"]}
- **종료 타입**: `{node["termination_type"]}`
- **권장 모델**: {node["model"]}
- **Temperature**: {node["temp"]}
- **D_min**: {node["d_min"] or "N/A"}

## Logical Axes

_Phase 1에서 식별된 이 노드의 판단 축을 기록:_

```json
{{
  "logical_axes": [],
  "orthogonality_tracking": true
}}
```

## 입력

_정의 필요_

## 출력

_정의 필요_

## 프롬프트

→ `prompts/node_{node["index"]:02d}_{node["name"]}.prompt` 참조

## Termination Declaration 형식

이 노드는 종료 시 반드시 다음을 출력해야 한다:

```json
{{
  "termination_status": "terminate | continue",
  "termination_type": "{node["termination_type"]}",
  "termination_rationale": {{
    "orthogonality_score": "<float>",
    "semantic_expansion_delta": "<float>",
    "decision_sensitivity": "<low | medium | high>",
    "axes_explored": [],
    "axes_remaining_estimate": 0
  }},
  "justification": "<자연어 종료 근거>"
}}
```
"""


def gen_termination_strategy(nodes, d_min_override, cooldown):
    """regime별 종료 전략 문서 생성."""
    regimes = {}
    for n in nodes:
        regimes.setdefault(n["regime"], []).append(n)

    sections = []

    if "convergent" in regimes:
        names = ", ".join(n["name"] for n in regimes["convergent"])
        sections.append(f"""## Convergent Regime — `answer_convergence`

해당 노드: {names}

종료 조건:
- validate (L0): 즉시 종료 (1회 판정)
- converge (L1): Δsem(k) < δ AND k ≥ 2 AND confidence > τ

종료의 의미: **정답에 도달했다.**""")

    if "verificatory" in regimes:
        names = ", ".join(n["name"] for n in regimes["verificatory"])
        sections.append(f"""## Verificatory Regime — `verification_pass`

해당 노드: {names}

종료 조건:
- candidates ≥ N_min AND best > τ AND margin(best, second) > δ

종료의 의미: **검증 기준을 통과했다.**""")

    if "deliberative" in regimes:
        names = ", ".join(n["name"] for n in regimes["deliberative"])
        d = d_min_override or max(n["d_min"] for n in regimes["deliberative"])
        sections.append(f"""## Deliberative Regime — `decision_sufficiency` ⭐

해당 노드: {names}

종료 조건:
```
Terminate_deliberative(k) =
  D(k) ≥ {d}
  AND orthogonality < ε  (연속 {cooldown}회)
  AND (ΔC < δ  OR  Δsem < τ)
  AND decision_sensitivity = low
```

종료의 의미: **의사결정에 충분한 근거를 확보했다.**
⚠️ "최선의 답을 찾았다"가 아님. "수렴 실패"로 해석하지 말 것.""")

    return "# Termination Strategy\n\n" + "\n\n---\n\n".join(sections)


def gen_terminate_check():
    """종료 판정 프롬프트 템플릿."""
    return """# 종료 판정 프롬프트 (v1.1)

## 1. 직교성 체크 (모든 반복 노드 공통)

```
이전 반복들에서 사용된 판단 축: {cumulative_axes}

이번 반복에서 사용된 판단 축을 식별하라.

판정 기준:
- 기존 축과 독립적인 새로운 판단 기준인가?
- 기존 축의 선형결합(단순 조합)이 아닌가?
- 기존 축으로는 도달할 수 없는 결론을 가능하게 하는가?

출력:
- 새 축이 있다면: 축 이름, 기존 축과의 차이, orthogonality_score (0~1)
- 새 축이 없다면: 'SATURATED', orthogonality_score = 0

주의: 같은 축의 다른 값은 새 축이 아니다.
```

## 2. 결정 민감도 체크 (Deliberative regime 전용)

```
현재까지의 잠정 결론: {현재_결론}
탐색되지 않은 잠재 축: {미탐색_축_후보}

질문: 위 잠재 축 중 하나가 탐색되었을 때,
현재 결론이 뒤집히거나 크게 변할 가능성이 있는가?

- HIGH: 탐색 계속. SATURATED 무시.
- LOW: 종료 정당.
```

## 3. 결정 안정성 체크

```
이전 반복의 잠정 결론: {이전_결론}
이번 반복의 잠정 결론: {현재_결론}

핵심 차이가 있는가?
- 있다면: 변경된 부분과 이유를 명시
- 없다면: 'STABLE'
```
"""


def gen_perspective_forcing():
    """Perspective forcing 프롬프트 템플릿."""
    return """# Perspective Forcing 프롬프트

D(k) < D_min인데 직교성이 0에 수렴할 때 사용한다.

```
현재까지 탐색된 판단 축: {cumulative_axes}
현재 D(k) = {현재_차원수}, D_min = {최소_차원수}

아직 탐색되지 않았을 수 있는 관점:
- 이해관계자를 바꿔보라 (고객→공급자→규제자→사회)
- 시간축을 바꿔보라 (단기→중기→장기)
- 추상화 수준을 바꿔보라 (전술→전략→비전)
- 반대 입장에서 보라 (찬성→반대→제3자)
- 도메인을 바꿔보라 (기술→경제→법률→윤리)

위 중 기존 축과 독립적인 새로운 판단 축을 식별하라.
식별 불가하면 'TRULY_SATURATED'를 반환하라.
```

TRULY_SATURATED 반환 시:
- D_min을 현재 D(k)로 하향 조정
- Termination Declaration에 D_min 하향 사실을 명시
- 이후 정상 종료 판정 진행
"""


def gen_quality_criteria():
    """품질 기준 템플릿."""
    return """# 품질 기준 정의

## 노드별 품질 메트릭

| 노드 | Mode | Regime | 핵심 메트릭 | 목표 |
|------|------|--------|-----------|------|
| _노드명_ | converge | convergent | Precision | ≥ 0.90 |
| _노드명_ | diverge | deliberative | Coverage (D/D_min) | ≥ 1.0 |
| _노드명_ | diverge | deliberative | Orthogonality at termination | < ε |
| _노드명_ | validate | convergent | Accuracy | ≥ 0.95 |

## 전체 워크플로우 품질

- **종합 F1**: _목표 설정 필요_
- **분할 효율**: split_quality / split_cost > baseline × 1.1
- **종료 정당성**: 모든 노드의 Termination Declaration이 정상 출력되는가?
"""


# ── 메인 스캐폴드 ──

def scaffold(args):
    """디렉토리 + 파일 생성."""
    nodes = parse_nodes(args.nodes)

    # 엣지 파싱 또는 추론
    if args.edges:
        edges = parse_edges(args.edges, nodes)
    else:
        edges = infer_linear_edges(nodes)

    strategy_gate_enabled = is_strategy_or_high_risk(args.workflow_class, args.risk_tolerance)
    if strategy_gate_enabled:
        ensure_strategy_gate(nodes, edges)

    topology = detect_topology(edges)
    base = os.path.join(args.output, args.name)

    # 디렉토리 생성
    for d in ["nodes", "prompts", "termination", "validation", "analysis"]:
        os.makedirs(os.path.join(base, d), exist_ok=True)

    # workflow.md
    with open(os.path.join(base, "workflow.md"), "w") as f:
        f.write(
            gen_workflow_md(
                args.name,
                nodes,
                edges,
                args.d_min,
                args.cooldown,
                strategy_gate_enabled,
                args.proposal_id,
                args.visibility_tier,
            )
        )

    # 노드 상세
    for n in nodes:
        with open(os.path.join(base, "nodes", f"node_{n['index']:02d}_{n['name']}.md"), "w") as f:
            f.write(gen_node_md(n, args.cooldown))

    # 프롬프트 템플릿
    for n in nodes:
        with open(os.path.join(base, "prompts", f"node_{n['index']:02d}_{n['name']}.prompt"), "w") as f:
            f.write(f"# Prompt: {n['name']}\n\n## Mode: {n['mode']}\n## Regime: {n['regime']}\n\n_프롬프트 작성 필요_\n")

    # termination/ (v1.1 신규)
    with open(os.path.join(base, "termination", "strategy.md"), "w") as f:
        f.write(gen_termination_strategy(nodes, args.d_min, args.cooldown))

    with open(os.path.join(base, "termination", "terminate_check.md"), "w") as f:
        f.write(gen_terminate_check())

    with open(os.path.join(base, "termination", "perspective_forcing.md"), "w") as f:
        f.write(gen_perspective_forcing())

    # validation/
    with open(os.path.join(base, "validation", "quality_criteria.md"), "w") as f:
        f.write(gen_quality_criteria())

    # analysis/ (placeholder)
    with open(os.path.join(base, "analysis", "cone_profile.md"), "w") as f:
        f.write("# θ_GT 프로파일링 결과\n\n_Phase 1 완료 후 기록_\n")

    with open(os.path.join(base, "analysis", "cost_simulation.md"), "w") as f:
        f.write("# 비용-품질 시뮬레이션\n\n_Phase 5 완료 후 기록_\n")

    # 결과 출력
    print(f"✅ Scaffolded: {base}/")
    print(f"   topology: {topology}")
    print(f"   strategy_gate_enabled: {strategy_gate_enabled}")
    print(f"   {len(nodes)} nodes + {len(edges)} edges")
    print(f"   termination/ + validation/ + analysis/")
    print()
    for n in nodes:
        icon = {"deliberative": "⚡", "verificatory": "🔍", "convergent": "→"}.get(n["regime"], "?")
        print(f"   {icon} {n['id']}: {n['name']} [{n['mode']}|{n['theta']}|{n['regime']}] → {n['termination_type']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convergence Cone v1.1 워크플로우 스캐폴더",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 선형 체인
  %(prog)s --name etl --nodes "extract:converge:L1,transform:diverge:L3,load:validate:L0"

  # 비선형 (루프)
  %(prog)s --name analysis \\
    --nodes "scan:converge:L1,analyze:diverge:L3,report:converge:L1" \\
    --edges "scan->analyze,analyze->analyze:loop,analyze->report"

  # 레거시 라벨 호환
  %(prog)s --name legacy --nodes "a:converge:narrow,b:diverge:wide"
        """,
    )
    parser.add_argument("--name", required=True, help="워크플로우 이름")
    parser.add_argument(
        "--nodes", required=True,
        help="노드 정의. 형식: 'name:mode[:theta],…' "
             "theta는 L0~L4 또는 레거시(very_narrow,narrow,medium,wide)")
    parser.add_argument(
        "--edges", default=None,
        help="엣지 정의 (선택). 형식: 'from->to[:type],…' "
             "type: sequential(기본), loop, conditional, fan_out. "
             "미지정 시 선형 체인으로 자동 생성.")
    parser.add_argument("--output", default=".", help="출력 경로 (기본: 현재 디렉토리)")
    parser.add_argument("--d-min", type=int, default=None, help="deliberative 노드의 D_min 오버라이드")
    parser.add_argument("--cooldown", type=int, default=2, help="쿨다운 윈도우 w (기본: 2)")
    parser.add_argument(
        "--workflow-class",
        choices=["strategy", "high_risk", "general"],
        default="general",
        help="워크플로우 분류 (기본: general)",
    )
    parser.add_argument(
        "--risk-tolerance",
        choices=["low", "medium", "high"],
        default="medium",
        help="리스크 허용도 (기본: medium)",
    )
    parser.add_argument(
        "--proposal-id",
        default="UNASSIGNED",
        help="proposal identifier for workflow artifacts",
    )
    parser.add_argument(
        "--visibility-tier",
        choices=["must_show", "optional", "internal"],
        default="internal",
        help="visibility tier metadata for workflow artifacts",
    )

    args = parser.parse_args()
    scaffold(args)
