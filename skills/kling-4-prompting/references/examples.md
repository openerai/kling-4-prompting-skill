# 예시 프롬프트

예시는 작성 패턴이며 생성 성공 사례나 벤치마크가 아니다. @태그는 해당 자산이 실제
업로드되어 동일 번호를 받은 경우에만 사용하라. 아래에서 제공됐다고 가정한 자료가
없으면 제거하거나 실제 첨부에 맞춰라. UI 설정과 프롬프트의 숫자를 일치시켜라.

목차: 1. 30초 액션 / 2. 한국 가족 대화 / 3. 첫 프레임 원테이크 /
4. 중간 키프레임 / 5. 배경 교체 / 6. 카메라만 이동 / 7. 광고 재구성 /
8. 요청한 자막·음악 / 9. Flash 충돌 대응.

## 1. 30초 액션 — Omni, 이미지 2장, 6샷

가정: @Image1 인물 시트, @Image2 수상 도시 환경. 일반 4.0 / 30초 / 16:9.
렌즈 숫자보다 화면에 보이는 경로·행동의 연결을 우선하는 예시다.

```text
@Image1 defines the courier's identity, hair, body proportions, ivory coat and red document case. @Image2 defines the canal city, bridges and late-afternoon lighting. Keep these designs consistent across six shots.
A courier races to deliver one red case aboard a departing river tram. Warm sunlight grazes wet stone and pale canal walls. The tram travels screen-left to screen-right in every shot. Thirty seconds, six hard-cut shots, real-time action.
Shot 1, 0–4s: Full-body side tracking. Already running, she grips the case in her right hand and sprints toward a rising pedestrian bridge as the tram bell rings.
Shot 2, 4–9s: Low wide shot. Her left foot drives off the near bank; she clears the narrow opening and lands on the descending bridge deck. Her coat tails lag behind her landing, then swing forward.
Shot 3, 9–14s: A side tracking shot follows her across the bridge. She ducks beneath a swinging rope while keeping the case close to her right hip; her momentum carries her toward the far stairs.
Shot 4, 14–20s: Wide view from the same side of the travel axis. She takes three fast steps down, plants her left foot on the last step and jumps toward the rear platform of the moving tram. Both hands catch the rail while the case's wrist strap remains on her right wrist.
Shot 5, 20–26s: Medium side view. Her boots find the platform, her knees absorb the landing and she pulls herself upright. She opens her right hand, slides the strap free and hands the case to the conductor's waiting left hand.
Shot 6, 26–30s: Pull back from the moving tram as the conductor holds the case and she exhales with relief. The cleared bridge recedes behind them.
Synchronized footsteps, cloth, tram bell, rail contact and river ambience. The tram sound moves left to right in stereo. No dialogue, no subtitles, no background music.
```

## 2. 20초 한국 가족 대화 — Omni, 텍스트만

가정: 일반 4.0 / 20초 / 16:9. 발화 시간은 작성용 배분이며 실제 음성 길이 측정값이 아니다.

```text
A mother in her late forties and her teenage son sit at a small Korean apartment kitchen table after dinner. The mother remains frame-left; her son remains frame-right. Warm ceiling light falls on a half-peeled tangerine and two water glasses. Twenty seconds, three shots, restrained live-action performances.
Shot 1, 0–7s: A steady medium two-shot. The son lowers his eyes to the tangerine. In a quiet, hesitant Korean teenage voice, he says, “엄마, 나 오늘 발표하다가 말이 하나도 안 나왔어.” The mother stops peeling and listens until he finishes.
Shot 2, 7–14s: Medium close-up of the mother from the same side of the table axis. She places one tangerine segment beside his glass. In a warm, unhurried Korean voice, she says, “그래도 끝까지 앞에 서 있었잖아. 그거면 오늘은 잘한 거야.”
Shot 3, 14–20s: Return to the two-shot. He picks up the segment, glances at her and asks, “다음엔 좀 나아질까?” She meets his eyes and answers gently, “응. 엄마도 아직 연습 중이야.” They share a small, relieved smile.
Each line belongs only to its named speaker. Allow brief listening pauses between lines. Keep the two voices distinct and lip movements synchronized to the Korean words. Quiet refrigerator hum, soft plate contact and natural room tone sit below the dialogue. No subtitles. No background music.
```

## 3. 이미지 첫 프레임, 10초 원테이크 — Keyframes

가정: @Image1은 향수 이미지이자 9:16 첫 프레임. 별도 참조 자산 없음.

```text
Use @Image1 as the first frame. Preserve the exact amber glass bottle, ivory label, cap geometry, stone plinth and opening composition. Ten seconds, vertical 9:16, one continuous take, no cuts.
0–3s: A narrow band of warm window light travels across the bottle's left edge while a single droplet slides down the glass.
3–7s: The camera makes a slow, shallow arc toward the bottle's right side. The bottle and plinth remain fixed in world space; their parallax against the distant curtain changes naturally.
7–10s: The camera settles with the existing label readable and the droplet reaching the base. The glass retains its thickness, amber color and reflections throughout.
Quiet room tone and a delicate glass contact sound. No subtitles. No background music.
```

## 4. 중간 키프레임 — Keyframes, 4장

가정: 같은 16:9 비율로 준비한 4장, 0/8/18/30초에 대응. 각 이미지 내용이 아래와
맞는 경우에만 사용하라. Keyframes의 시점 설정은 현재 UI에서 별도로 매핑하라.

```text
Thirty seconds, 16:9. Map @Image1 to 0s, @Image2 to 8s, @Image3 to 18s and @Image4 to 30s. These four images are timeline anchors, not a displayed collage. One continuous camera move follows the same origami crane across the same studio table.
0–8s: Begin with the folded paper shape in @Image1. Its two wings unfold along visible existing creases as the camera approaches the side-on position in @Image2. The paper retains its fibers, printed pattern and physical thickness.
8–18s: The crane rises with two deliberate wing strokes. The camera lifts with it and reaches the hovering composition of @Image3. Its moving shadow remains attached to the table plane below.
18–30s: The crane glides toward the open window, descends to the sill and folds its wings. The camera follows one continuous arc and settles into the framing of @Image4. Hold the final composition briefly as the paper stops moving.
Soft paper creaks, wing rustle and distant outdoor birds. No subtitles. No background music. No cuts.
```

## 5. 배경과 재조명만 변경 — Omni edit

가정: @Video1 원본이 업로드됨. 원본을 보지 않고 새 액션을 만들어 넣지 않는 예시다.

```text
Edit @Video1. Replace only the background with an active volcanic landscape of dark basalt, distant lava flows and drifting ash. Relight the existing subject with warm lava bounce from below and cool overcast light from above; update the subject's shadows and reflections to match. Preserve the original subject's identity, outfit, body movements, trajectory, screen size, camera path, framing, cuts, timing, duration and audio. Keep everything else unchanged.
```

## 6. 카메라만 왼쪽 1m 이동 — Omni edit

가정: 원본이 정지 카메라이고 남성·화병·받침대·액자가 있는 경우.

```text
Edit @Video1. Replace the stationary viewpoint with one continuous camera truck exactly one meter to the camera's left over the original clip duration. Keep the same focal length and camera height; allow only a small pan to maintain the man in the composition. Preserve the man's identity, outfit and original actions, and keep the vase, pedestal and framed picture fixed in world space. Reveal previously occluded surfaces through depth-dependent parallax. Preserve the location, lighting, duration and audio. Keep everything else unchanged.
```

1m는 목표 지시다. 실제 이동 거리를 확인한 측정값이라고 말하지 말라.

## 7. 참조 영상의 구조로 새 광고 제작 — Omni recreation

가정: @Video1 15초 광고, @Image1 제품, @Image2 새 세트. 원본 픽셀 보존 편집이
아니라 새 촬영의 구조 참조다. 원본을 열람하지 않았다면 구체적인 컷 설명을 추가하지 말라.

```text
Use @Video1 only as the reference for its 15-second shot structure, camera movement, reveal timing and closing product hold. @Image1 defines the exact ceramic speaker design, proportions, surface texture and existing wordmark. @Image2 defines the new pale-blue studio set and soft side lighting. Recreate the same visual progression using this speaker and this set throughout. The original video's products, people and environment are not appearance references. Preserve the speaker's geometry and readable existing wordmark through every camera move. Use synchronized ceramic taps, a soft power-on tone and quiet studio ambience. No subtitles. No background music.
```

## 8. 요청한 자막·음악을 보존 — Omni, 10초

```text
A tiny felt fox crosses a moss-covered tree root at sunrise, carrying one red felt lantern. Ten seconds, 16:9, one continuous low tracking shot. Rounded stitched shapes, visible wool fibers and soft stop-motion movement throughout; no photorealistic surfaces.
0–6s: The fox takes four careful steps while the lantern swings with a small delay. Warm light shines through its thin red fabric.
6–10s: It reaches the far end, raises the lantern and looks toward the rising sun. Display the exact Korean subtitle “천천히 가도 괜찮아” at bottom-center from 6s to 10s in large ivory lettering with a thin dark outline. Keep the lantern and fox's face unobstructed.
Gentle original acoustic music with soft plucked strings continues throughout, beneath felt footsteps and morning birds. No dialogue.
```

## 9. Flash 충돌 대응 문구

“Flash 기준으로는 최대 20초·720p이며 첫+끝 프레임/다중 키프레임을 지원하지 않습니다.
요청하신 30초·4K·키프레임 구성은 일반 Kling 4.0 기준으로 작성하겠습니다.”

사용자가 Flash 고정을 명시했다면 변경을 확정하지 말고 지원 범위의 분할 대안과
그에 따른 키프레임 제어 차이를 설명하라. 버전·길이·해상도를 몰래 변경하지 말라.
