# Kling 4 Prompting Skill

Kling 4 공식 가이드를 바탕으로 영상 프롬프트를 설계하는 **Kling 4 프롬프트 디렉터**입니다.

An unofficial Agent Skill for writing and refining Kling 4 prompts, with explicit reference roles, continuity planning, scoped video edits, keyframes, and version-aware constraints.

## 할 수 있는 일

- 텍스트·이미지·영상 참조로 장면과 시간별 액션 구성
- Omni Reference / Keyframes 선택 및 일반 4.0 / Flash 제한 구분
- 인물·의상·제품·카메라·공간 연속성 유지 지침 작성
- 한국어를 포함한 다국어 대사의 화자·연기·음향 설계
- 배경·인물·스타일·카메라 등 지정 부분만 수정하는 편집 프롬프트 작성
- 전체 자산 수와 공유 영상 한도, 타임라인을 내부 계획 검사기로 점검

프롬프트 작성 도구입니다. Kling에 직접 연결하거나 영상을 자동 생성하는 프로그램은 아닙니다. 생성 실행은 별도로 연결한 도구와 그 도구의 실제 지원 범위를 확인해야 합니다.

## 등록과 사용

Agent Skills를 지원하는 환경에 [`skills/kling-4-prompting`](skills/kling-4-prompting) 폴더 전체를 등록하세요. `SKILL.md`만 복사하면 연결된 레퍼런스와 검사기를 사용할 수 없습니다.

- Codex 로컬 환경: 폴더를 사용자 스킬 디렉터리의 `kling-4-prompting`으로 복사합니다.
- Claude 등 다른 에이전트: 해당 환경의 스킬 등록 기능으로 같은 폴더를 등록합니다. 제품별 등록 방식과 스크립트 실행 지원 여부는 현재 환경에서 확인하세요.
- 스크립트를 실행하지 못하는 환경에서도 프롬프트 지침과 레퍼런스를 읽고 수동으로 조건을 점검할 수 있습니다.

요청 예시:

```text
Kling 4 프롬프트 디렉터로 30초, 16:9 영상 프롬프트를 작성해줘.
@Image1은 동일 인물과 의상, @Image2는 배경, @Video1은 액션 타이밍만 참조해.
빠른 6샷으로 구성하고 한국어 대사와 환경음을 넣어줘. 자막은 제외해줘.
```

```text
Edit @Video1 방식으로 배경만 화산 지대로 바꾸는 프롬프트를 써줘.
인물의 정체성·동작·카메라·컷·길이는 유지하고 새 환경에 맞춰 재조명해줘.
```

실제 업로드 순서와 참조 태그를 확인하세요. 예시의 @번호는 실제 첨부물을 뜻하지 않습니다.

## 구성

| 파일 | 용도 |
|---|---|
| [SKILL.md](skills/kling-4-prompting/SKILL.md) | 핵심 작업 지침 |
| [capabilities.md](skills/kling-4-prompting/references/capabilities.md) | 공식 사양·버전 차이·문서 충돌 처리 |
| [continuity-and-editing.md](skills/kling-4-prompting/references/continuity-and-editing.md) | 공간·물리·부분 편집 지침 |
| [examples.md](skills/kling-4-prompting/references/examples.md) | 9개 작성 예시·대응 패턴 |
| [migration-and-evidence.md](skills/kling-4-prompting/references/migration-and-evidence.md) | Kling 3 → 4 변경 근거와 검증 경계 |
| [validate_plan.py](skills/kling-4-prompting/scripts/validate_plan.py) | 내부 JSON 계획의 한도·시간 검사 |

## 내부 계획 검사기

Python 3 표준 라이브러리만 사용합니다. Python 3.10 이상을 권장합니다.

```bash
python3 skills/kling-4-prompting/scripts/validate_plan.py --help
python3 skills/kling-4-prompting/scripts/validate_plan.py /path/to/plan.json
```

입력 예시와 필드 설명은 `--help`에 있습니다. **검사기 JSON은 Kling API 요청 스키마가 아닙니다.** 오류가 없더라도 화질·프롬프트 의미·립싱크·정확한 토큰 수·계정별 기능 제공·API 호환성은 검증하지 않습니다. 측정하지 않은 파일 크기나 비율은 임의 값으로 채우지 말고 누락 경고를 확인하세요.

## 근거와 검증 범위

- 공식 기능 근거: [Kling 4.0 User Guide](https://kling.ai/quickstart/kling-4-model-user-guide)
- 문서 표기일: 2026-10-14 / 마지막 확인일: 2026-10-18 (Asia/Seoul)
- 개정 기반: [aedev-tools/kling-3-prompting-skill](https://github.com/aedev-tools/kling-3-prompting-skill)
- 기반 커밋: `3beb4cbb2c5cd7580d9b5f945238074514e8b5a3`

Gravitas의 근거 중심 검증 절차에 따라 원본 스킬·공식 문서·라이선스를 대조하고 독립 검토와 사용 시나리오 점검을 수행했습니다. 실제 Kling 영상의 품질·생성 속도·성공률을 벤치마크한 결과는 아닙니다.

HDR와 최대 2분 확장 등 문서상 출시 예정 표기는 현재 UI에서 확인하기 전 제공 기능으로 확정하지 않습니다. 모델과 플랫폼의 사양이 변경될 수 있으므로 실행 시 현재 UI 및 연결 도구가 우선합니다.

Kling 공식 제작물이나 공식 인증 스킬이 아닙니다. 예시의 세부 시간·카메라·동작 지시는 창작 목표이며 결과 보장이 아닙니다.

## 라이선스

[MIT License](LICENSE). 원본 저작권 및 MIT 고지를 보존했습니다. 원본 README의 Apache 표기와 실제 LICENSE의 MIT 고지가 달라 LICENSE 원문을 기준으로 처리했습니다. 상세 출처와 변경 범위는 [UPSTREAM.md](skills/kling-4-prompting/assets/UPSTREAM.md)를 확인하세요.

공식 가이드 전문, 생성 영상, 사용자 레퍼런스 파일은 포함하지 않습니다.
