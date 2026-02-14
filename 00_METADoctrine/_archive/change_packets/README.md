# Change Packet Archive

이 폴더는 **활성 제안 단계가 끝난 변경 패킷의 아카이브**를 보관하는 장소입니다.

## 1) 보관 대상

- 상위기관/스웜 변경 제안에 사용된 모든 Change Packet 모음  
- `METADoctrine`, `Record_Archive`, `Immune_system`, `Deliberation_Chamber`, `02_Swarm`, `03_Manifestation` 관련 승인 제안  
- 승인 거절/보류 패킷(근거와 후속 조치 포함)

## 2) 보관 원칙

- Change Packet은 `_archive/change_packets/`에서 직접 생성/보관하며,  
  **변경이 확정되거나 정식 상위 게이트로 회귀한 항목**은 동일 경로 내에서 상태만 갱신한다.
- 아카이브 폴더는 현재 규범(상위 규범, 템플릿, 절차)보다 낮은 계층으로 간주한다.
- 아카이브 내부 문서는 **참조 정합성만 유지**하고, 규범 해설은 별도 상위 문서에서 갱신한다.

## 3) 정리 규칙 (기본)

- `METADoctrine.md` 또는 `METADoctrine_BLUEPRINT.md`가 새 버전으로 supersede되면, 이전 버전 패킷은 아카이브 보존 대상이 된다.
- 같은 변경 주제의 패킷이 두 개 이상 생긴 경우, 최신 완료본/승인본만 유지하고 중복본은 아카이브 폴더 내에서 `superseded-by` 관계로 표시.
- 아카이브 정합성 점검은 분기 단위로 시행하고, 깨진 링크는 즉시 정리한다.

## 4) 현재 경로 안내

- 모든 과거 Change Packet: `00_METADoctrine/_archive/change_packets/`
- 현행 안내(단일 경로): `00_METADoctrine/_archive/change_packets/README.md`
