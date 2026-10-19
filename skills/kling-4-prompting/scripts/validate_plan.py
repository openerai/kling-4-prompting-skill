#!/usr/bin/env python3
"""Check an INTERNAL Kling 4 writing plan, not a Kling/API request or media output.

Usage: python3 validate_plan.py plan.json
Read stdin with '-'. Exit 0 = no detected errors, 1 = constraint violations,
2 = invalid JSON/root. Unknown fields are not validated. MB means supplied MB;
missing file metadata and token counts remain unchecked, not assumed valid.

Minimal example:
{
  "model": "4.0", "entry": "omni", "operation": "generate",
  "duration": 30, "resolution": "1080p", "aspect_ratio": "16:9",
  "references": [
    {"id": "@Image1", "type": "image", "role": "identity"},
    {"id": "@Video1", "type": "video", "role": "action", "duration": 12}
  ],
  "keyframes": [],
  "shots": [{"start": 0, "end": 10}, {"start": 10, "end": 30}],
  "one_take": false
}
Reference types: image, video, voice, element, video_element. Put an edit
source in references with type=video and main=true; count each uploaded slot
once. video_element.duration is the contributing source clip duration (3-8s).
Keyframe ids must point to image references. 'beats' may describe contiguous
intervals inside a single continuous take without treating them as cuts.
Optional measured fields: size_mb, reference.aspect_ratio, prompt_tokens.
"""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path

TYPES = {"image", "video", "voice", "element", "video_element"}
VIDEO_TYPES = {"video", "video_element"}
OUTPUT_RATIOS = {"21:9", "16:9", "1:1", "9:16", "Auto"}


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def ratio(value):
    if not isinstance(value, str):
        return None
    try:
        a, b = value.split(":")
        a, b = float(a), float(b)
        return a / b if a > 0 and b > 0 and math.isfinite(a / b) else None
    except (ValueError, ZeroDivisionError):
        return None


def validate(plan):
    errors, warnings = [], []
    model, entry = plan.get("model"), plan.get("entry")
    duration = plan.get("duration")
    for flag in ("one_take", "hdr_requested", "hdr_available_verified", "extension_requested", "bgm_or_sfx_audio_upload"):
        if flag in plan and not isinstance(plan[flag], bool):
            errors.append(f"{flag} must be a JSON boolean")
    if not isinstance(model, str) or model not in {"4.0", "4.0-flash"}:
        errors.append("model must be 4.0 or 4.0-flash (internal labels only)")
    if not isinstance(entry, str) or entry not in {"omni", "keyframes"}:
        errors.append("entry must be omni or keyframes")
    op = plan.get("operation", "generate")
    if not isinstance(op, str) or op not in {"generate", "edit", "recreate"}:
        errors.append("operation must be generate, edit or recreate")
    limit = 20 if model == "4.0-flash" else 30
    duration_ok = number(duration) and float(duration).is_integer() and 3 <= duration <= limit
    if not duration_ok:
        errors.append(f"duration must be a whole number from 3 to {limit} seconds")
    resolutions = {"720p"} if model == "4.0-flash" else {"720p", "1080p", "4K"}
    if not isinstance(plan.get("resolution"), str) or plan["resolution"] not in resolutions:
        errors.append("unsupported resolution for selected model")
    if plan.get("hdr_requested") and not plan.get("hdr_available_verified"):
        warnings.append("HDR marked coming soon in overview; actual route availability unverified")
    if plan.get("hdr_requested") and plan.get("resolution") == "720p":
        errors.append("guide only lists HDR for 1080p/4K")
    if plan.get("extension_requested"):
        warnings.append("2-minute extension is coming soon; do not assume availability")
    if plan.get("bgm_or_sfx_audio_upload"):
        errors.append("audio uploads are voice-profile sources, not BGM/SFX inputs")
    tokens = plan.get("prompt_tokens")
    if tokens is None:
        warnings.append("prompt token count not measured; 8000-token limit unchecked")
    elif not isinstance(tokens, int) or isinstance(tokens, bool) or not 0 <= tokens <= 8000:
        errors.append("prompt_tokens must be a measured integer between 0 and 8000")

    refs = plan.get("references", [])
    if not isinstance(refs, list):
        errors.append("references must be a list")
        refs = []
    if len(refs) > 15:
        errors.append("combined reference limit exceeded: 15")
    counts, by_id = Counter(), {}
    total_video_seconds = 0
    unknown_video_time = False
    missing_metadata = False
    main_count = 0
    for i, ref in enumerate(refs):
        tag = f"references[{i}]"
        if not isinstance(ref, dict):
            errors.append(f"{tag} must be an object")
            continue
        kind, rid = ref.get("type"), ref.get("id")
        if not isinstance(kind, str) or kind not in TYPES:
            errors.append(f"{tag}: unsupported reference type")
            continue
        counts[kind] += 1
        if not isinstance(rid, str) or not rid.strip():
            errors.append(f"{tag}: nonempty id required")
        elif rid in by_id:
            errors.append(f"{tag}: duplicate id; represent each uploaded slot once")
        else:
            by_id[rid] = ref
        if not isinstance(ref.get("role"), str) or not ref["role"].strip():
            errors.append(f"{tag}: explicit role required")
        if entry == "keyframes" and kind != "image":
            errors.append(f"{tag}: Keyframes entry accepts image inputs only")
        if "main" in ref and not isinstance(ref["main"], bool):
            errors.append(f"{tag}: main must be a JSON boolean")
        if ref.get("main"):
            main_count += 1
            if kind != "video":
                errors.append(f"{tag}: edit primary must be a video")
        if kind in VIDEO_TYPES | {"voice"}:
            seconds = ref.get("duration")
            lo, hi = (3, 8) if kind == "video_element" else (5, 30) if kind == "voice" else (3, 30)
            if not number(seconds) or not lo <= seconds <= hi:
                errors.append(f"{tag}: source duration must be {lo}-{hi}s")
                if kind in VIDEO_TYPES:
                    unknown_video_time = True
            if kind in VIDEO_TYPES and number(seconds):
                total_video_seconds += seconds
        mb = ref.get("size_mb")
        max_mb = {"image": 30, "video": 300, "voice": 50}.get(kind)
        if max_mb is not None:
            if mb is None:
                missing_metadata = True
            elif not number(mb) or not 0 < mb <= max_mb:
                errors.append(f"{tag}: size_mb must be positive and <= {max_mb}")
        if kind in {"image", "video"}:
            ar = ref.get("aspect_ratio")
            if ar is None:
                missing_metadata = True
            elif ratio(ar) is None or not 0.4 <= ratio(ar) <= 2.5:
                errors.append(f"{tag}: input aspect_ratio outside 2:5-5:2")
    caps = {"image": 10, "video": 5, "voice": 3, "video_element": 3}
    for kind, cap in caps.items():
        if counts[kind] > cap:
            errors.append(f"{kind} reference count exceeds {cap}")
    if counts["element"] + counts["video_element"] > 7:
        errors.append("combined element count exceeds 7")
    video_count = counts["video"] + counts["video_element"]
    if video_count > 5:
        errors.append("shared video quota exceeds 5 clips")
    if total_video_seconds > 30:
        errors.append("shared video duration exceeds 30 seconds")
    if unknown_video_time:
        warnings.append("shared duration incomplete because a video source duration is invalid/missing")
    if missing_metadata:
        warnings.append("some source file size/aspect metadata absent; those limits unchecked")
    if op == "edit" and (entry != "omni" or main_count != 1):
        errors.append("edit requires Omni and exactly one primary video")
    elif op != "edit" and main_count:
        errors.append("main=true is reserved for an edit source")
    if op == "recreate" and (entry != "omni" or not counts["video"]):
        errors.append("video recreation requires Omni and a video reference")

    frames = plan.get("keyframes", [])
    if not isinstance(frames, list):
        errors.append("keyframes must be a list")
        frames = []
    if len(frames) > 10:
        errors.append("keyframe count exceeds 10")
    if model == "4.0-flash" and len(frames) > 1:
        errors.append("Flash does not support start-and-last or multiple keyframes")
    previous = -1
    mapped_image_ids = set()
    for i, frame in enumerate(frames):
        if not isinstance(frame, dict):
            errors.append(f"keyframes[{i}] must be an object")
            continue
        rid, t = frame.get("id"), frame.get("time")
        if not isinstance(rid, str) or by_id.get(rid, {}).get("type") != "image":
            errors.append(f"keyframes[{i}] must refer to an uploaded image id")
        else:
            mapped_image_ids.add(rid)
        if not number(t) or t < 0 or t <= previous or (number(duration) and t > duration):
            errors.append(f"keyframes[{i}] timestamp must increase and lie within the clip")
        if number(t):
            previous = t
    if model == "4.0-flash" and len(frames) == 1 and isinstance(frames[0], dict) and frames[0].get("time") != 0:
        warnings.append("Flash non-initial single keyframe support not established; verify actual route")
    if entry == "keyframes":
        image_ids = {rid for rid, ref in by_id.items() if ref.get("type") == "image"}
        if image_ids != mapped_image_ids:
            errors.append("every Keyframes image id must be mapped to a keyframe timestamp")
        if not frames:
            warnings.append("no keyframe anchors; verify current UI behavior, prefer Omni for text-only generation")
    first = frames[0] if frames and isinstance(frames[0], dict) else {}
    first_id = first.get("id")
    first_ratio = by_id.get(first_id, {}).get("aspect_ratio") if isinstance(first_id, str) else None
    output_ratio = plan.get("aspect_ratio", "Auto")
    if entry == "keyframes" and frames:
        if output_ratio != "Auto" and (ratio(output_ratio) is None or not 0.4 <= ratio(output_ratio) <= 2.5):
            errors.append("keyframe output aspect_ratio must be image-driven and within input limits")
        if first_ratio and output_ratio != "Auto" and ratio(first_ratio) and ratio(output_ratio):
            if not math.isclose(ratio(first_ratio), ratio(output_ratio), abs_tol=1e-6):
                errors.append("output aspect ratio conflicts with first keyframe")
        if not first_ratio:
            warnings.append("first-keyframe aspect ratio missing; output ratio conflict unchecked")
    elif entry == "keyframes" and (not isinstance(output_ratio, str) or output_ratio not in OUTPUT_RATIOS - {"Auto"}):
        errors.append("Keyframes without images lists 21:9, 16:9, 1:1 or 9:16, not Auto")
    elif not isinstance(output_ratio, str) or output_ratio not in OUTPUT_RATIOS:
        errors.append("output aspect ratio is not listed for this entry")

    for field in ("shots", "beats"):
        intervals = plan.get(field, [])
        if not isinstance(intervals, list):
            errors.append(f"{field} must be a list")
            continue
        if field == "shots" and plan.get("one_take") and len(intervals) > 1:
            errors.append("one_take conflicts with multiple shots; use beats for continuous action")
        cursor = 0.0
        for i, interval in enumerate(intervals):
            if not isinstance(interval, dict):
                errors.append(f"{field}[{i}] must be an object")
                continue
            start, end = interval.get("start"), interval.get("end")
            if not number(start) or not number(end) or start < 0 or end <= start:
                errors.append(f"{field}[{i}]: invalid interval")
                continue
            if not math.isclose(start, cursor, abs_tol=1e-6):
                errors.append(f"{field}[{i}]: timeline gap/overlap")
            cursor = end
        if intervals and number(duration) and not math.isclose(cursor, duration, abs_tol=1e-6):
            errors.append(f"{field} do not cover the requested duration")
    return {"valid": not errors, "errors": errors, "warnings": warnings,
            "scope": "plan constraints only; no media, semantics, API compatibility or availability verification"}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("plan", help="internal JSON plan path, or - for stdin")
    args = parser.parse_args()
    try:
        raw = sys.stdin.read() if args.plan == "-" else Path(args.plan).read_text(encoding="utf-8")
        plan = json.loads(raw)
        if not isinstance(plan, dict):
            raise ValueError("root must be a JSON object")
    except (OSError, ValueError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    result = validate(plan)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
