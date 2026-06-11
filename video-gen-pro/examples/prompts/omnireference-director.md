# Omnireference Director Prompt Example

## User Intent

Generate a 9:16 voiced short video using:

- one character image as appearance reference
- one motion video as action reference
- one audio clip as rhythm reference

## Director Prompt

```text
成片目标：做一条 8 秒电影感角色奔跑短片，观众记住的是主角在霓虹雨夜中突然加速冲向远处光源的紧张感。

参考关系：参考图1用于主角外观和服装，保持发型、外套主色和脸部轮廓一致；参考视频1用于跑步动作节奏和侧后方跟拍方式，不复制原视频背景；参考音频1用于鼓点节奏和紧张情绪，画面动作随鼓点逐步加速。

画面与风格：雨夜城市街道，地面积水反射红蓝霓虹，电影感写实，浅景深，轻微胶片颗粒。

镜头设计：低角度侧后方跟拍，开场中景，2 秒后镜头轻微推近，最后 2 秒加速并出现轻微手持晃动。

动作节奏：0-2 秒主角调整呼吸开始奔跑；2-5 秒脚步踩过积水，水花随鼓点溅起；5-8 秒主角突然加速冲向远处白色光源。

声音设计：使用参考音频1的鼓点节奏，加入低频环境氛围和雨声，不生成对白。

限制：保持主角身份一致，不添加无关文字、logo 或多余角色。
```

## CLI Shape

```bash
videogen omni \
  --prompt "<director prompt>" \
  --reference-image character.png \
  --reference-video motion.mp4 \
  --reference-audio beat.mp3 \
  --generate-audio true \
  --duration 8 \
  --ratio 9:16 \
  --wait
```
