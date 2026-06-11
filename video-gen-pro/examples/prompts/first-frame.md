# First-Frame Director Prompt Example

## User Intent

用户提供一张人物站立的开场图，要求让画面动起来，做一个 6 秒、9:16、无声的氛围片。

## Director Prompt

```text
成片目标：以首帧为开场，让画面在 6 秒内出现一个克制但可见的变化，氛围片，不要广告感。

参考关系：首帧用于场景与人物外观，保持人物身份、服装主色和发型不变；不替换背景。

画面与风格：写实电影感，自然冷暖光，浅景深，画面噪点克制。

镜头设计：单个连续镜头，从首帧的中近景开始缓慢推进，最后停在人物上半身。

动作节奏：0-2 秒人物呼吸，发丝轻动；2-4 秒微微转头看向镜头外；4-6 秒目光收回到镜头方向，画面随之轻微推近。

声音设计：无声，不生成对白和音乐。

限制：不改变首帧布局；不加入文字、字幕、logo 或新角色。
```

## CLI Shape

```bash
videogen first-frame \
  --prompt "<director prompt>" \
  --first-frame frame.png \
  --ratio 9:16 \
  --duration 6 \
  --generate-audio false \
  --wait
```

## Self Check

- 是否保留了首帧的人物身份、布局、色调。
- 是否只描述了一个核心变化（呼吸 → 转头 → 推近）。
- 是否禁用了与无声场景冲突的"音乐 / 对白"指令。
- 是否没有混入 `reference_image` / `reference_video` / `reference_audio` 参数。
