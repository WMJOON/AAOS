# deliberation/

Deliberation Chamber의 합의 산출물(특히 플래그십 합의)을 **sealed 패키지**로 보존한다.

- 규칙: append-only (sealed 패키지는 수정하지 않는다)
- 입력: `03_AAOS-Deliberation_Chamber/sessions/**`
- 출력(패키지): `_archive/deliberation/<timestamp>__deliberation-consensus__<slug>/`

