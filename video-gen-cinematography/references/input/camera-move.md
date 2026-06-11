# Camera Move 运镜填法

> Load when: 要填导演法【画面内容】的运镜手法子字段（镜头自身怎么移动/转动），或故事板法每格的运动目标，需要知道各运镜的画面语言效果、什么剧情该选哪个、怎么写进 prompt，以及五类镜头词库速查。
> Avoid: 要定取景远近与景深（去 `shot-scale.md`）、主体放哪与机位方位（去 `composition.md`）、或整片风格基调（去 `style-core.md`）。
> Pairs with: `../../../video-gen-director/references/director-method.md` 定义【画面内容】有哪些槽位，本文件管运镜怎么填；`shot-scale.md` 管景别与焦点、`composition.md` 管构图与机位角度，三者正交叠加；`../../../video-gen-storyboard/references/storyboard-board.md` 画母图每格也用本文件定运动目标。

运镜是镜头自身的移动或转动，给静止画面注入情绪与节奏。它是 AI 视频最需要明写的控制点——不写运镜，模型会自由发挥。本文件按「选项 → 画面语言效果 → 选用判据 → prompt 写法」展开各项运镜，速度（缓慢/匀速/快速）单独可叠加；末尾附按拍摄目的分五类的镜头词库速查。

> 写法约定：Seedance 是中国模型，可仅用中文提示词。本文件正文与示例 prompt 一律中文，英文术语仅在少数处作括注（供外部图像/视频工具识别，非必需）。`media/camera-move/` 下配同名 gif 供人工对照镜头效果（参考自 Runway Gen-4.5 镜头库实测）。

## 运镜

运镜是镜头自身的移动或转动，给静止画面注入情绪与节奏。它是 AI 视频最需要明写的控制点——不写运镜，模型会自由发挥。每项按「画面语言效果 → 选用判据 → prompt 写法」展开；速度（缓慢/匀速/快速）单独可叠加。

### 固定 / 静止（static）

<video src="media/camera-move/move_static.mp4" controls loop muted width="480"></video>

- 画面语言效果：机位完全不动，让动作在画框内发生，冷静、克制、observational。
- 选用判据：要稳定观察、留给表演空间、或对照后续运镜制造反差时用。
- prompt 写法：`固定镜头，机位完全不动，<主体在画框内的动作>`。
  - ⚠️ AI 稳定生成静止镜头的技巧（来自 Runway 官方 FAQ）：视频模型天生倾向加运动，想要真静止，**别只写"镜头不动"，而要明确描述画框内该发生什么运动、元素如何进出画**，并补一句`镜头在整段中保持完全静止，运动只来自主体`。

### 推镜（push in / dolly in）

<video src="media/camera-move/move_push-in.mp4" controls loop muted width="480"></video>

- 画面语言效果：镜头向主体推近，聚焦、强调、代入感增强，情绪逐渐压上来。
- 选用判据：情绪升温、揭示、把观众注意力锁向某主体时用。
- prompt 写法：`缓慢推镜，镜头逐渐靠近<主体面部/物件>，背景渐虚化`。

### 拉镜（pull back / dolly out）

<video src="media/camera-move/move_pull-back.mp4" controls loop muted width="480"></video>

- 画面语言效果：镜头后退，environment 逐渐展开，制造释然、孤独、收束或"原来如此"的揭示。
- 选用判据：段落收尾、揭示主体所处更大环境、情绪释放时用。
- prompt 写法：`缓慢拉镜，镜头后退，从<近>拉至<远>，逐渐展开<环境>`。

### 摇镜（pan，水平）

<video src="media/camera-move/move_pan.mp4" controls loop muted width="480"></video>

- 画面语言效果：机位固定、镜头水平左右转，扫过空间或在两主体间转移。
- 选用判据：横向交代环境、从一主体转到另一主体、定场扫描时用。
- prompt 写法：`水平摇镜，从固定机位<左至右/右至左>扫过<场景>，停在<主体>`。

### 俯仰（tilt，垂直）

<video src="media/camera-move/move_tilt.mp4" controls loop muted width="480"></video>

- 画面语言效果：机位固定、镜头上下转，揭示高度或纵向关系（脚到头、地到天）。
- 选用判据：揭示高大建筑/人物全貌、纵向揭示信息时用。
- prompt 写法：`垂直俯仰，镜头自<下而上/上而下>，从<底部细节>升到<顶部全貌>`。

### 移镜（dolly，前后/轨道）

<video src="media/camera-move/move_dolly.mp4" controls loop muted width="480"></video>

- 画面语言效果：整个机位沿轨道前后移动（区别于变焦），透视自然变化，有真实纵深感。
- 选用判据：跟随主体前进/后退、要真实空间穿越感时用。

### 横移（truck，左右平行）

<video src="media/camera-move/move_truck.mp4" controls loop muted width="480"></video>

- 画面语言效果：机位平行于主体左右移动，跟着横向运动的主体走，保持其在画面位置。
- 选用判据：跟拍横向行走/奔跑的主体、横向展开长卷式场景时用。
- prompt 写法：`镜头向<左/右>横移，平行跟随<主体>行走，背景横向流过`。

### 跟拍（tracking）

<video src="media/camera-move/move_tracking.mp4" controls loop muted width="480"></video>

- 画面语言效果：镜头跟着移动主体走（可在其后/侧/前），强代入、强动势。
- 选用判据：要让观众"跟着"主体行动（奔跑、穿行人群）时用。
- prompt 写法：`跟拍镜头，稳定跟随<主体>奔跑/穿行，背景流动`。

### 升降（pedestal，垂直平移）

<video src="media/camera-move/move_pedestal.mp4" controls loop muted width="480"></video>

- 画面语言效果：整个机位垂直上升/下降（区别于俯仰转动），平移地揭示纵向信息。
- 选用判据：跟随主体起立/坐下、垂直揭示物件时用。

### 摇臂 / 升降臂（crane / jib）

<video src="media/camera-move/move_crane.mp4" controls loop muted width="480"></video>

- 画面语言效果：机位在机械臂上做大幅升降+横移的复合运动，气势大、揭示性强。
- 选用判据：开场或收尾的大气揭示（从特写升到全景、从人群升到天空）时用。
- prompt 写法：`摇臂镜头，平滑<上升/下降>，从<近景主体>揭示到<广阔环境>`。

### 环绕（orbit，360°）

<video src="media/camera-move/move_orbit.mp4" controls loop muted width="480"></video>

- 画面语言效果：镜头绕主体旋转一圈或半圈，全方位展示主体，制造聚焦、华丽或眩晕。
- 选用判据：产品/角色的全方位展示、强调某个高光瞬间时用。
- prompt 写法：`缓慢环绕镜头，360度绕<主体>旋转，逐一展示各角度细节`。

### 弧线（arc）

<video src="media/camera-move/move_arc.mp4" controls loop muted width="480"></video>

- 画面语言效果：镜头沿弧线绕主体局部移动（非整圈），动感优雅，比环绕克制。
- 选用判据：要动势但不必整圈环绕时用。

### 变焦（zoom）

<video src="media/camera-move/move_zoom.mp4" controls loop muted width="480"></video>

- 画面语言效果：镜头焦段变化使主体变大/变小（机位不动，区别于移镜），透视被压缩，略不自然但有特定语感。
- 选用判据：快速拉近注意力、复古/电视感、或与移镜配合做特殊效果时用。

### 急推变焦（crash zoom）

<video src="media/camera-move/move_crash-zoom.mp4" controls loop muted width="480"></video>

- 画面语言效果：极快猛烈变焦推进，制造突发、惊吓、强调的冲击。
- 选用判据：突发事件、惊吓点、漫画式强调时用。
- prompt 写法：`急推变焦，镜头猛然快速推近<主体面部/物件>`。

### 甩镜（whip pan）

<video src="media/camera-move/move_whip-pan.mp4" controls loop muted width="480"></video>

- 画面语言效果：极快水平摇动产生运动模糊，常用作转场或连接两个画面。
- 选用判据：快速转场、连接两个空间/人物、节奏加速时用。
- prompt 写法：`快速甩镜转场，画面模糊横扫，从<画面A>切到<画面B>`。

### 手持（handheld）

<video src="media/camera-move/move_handheld.mp4" controls loop muted width="480"></video>

- 画面语言效果：自然晃动与抖动，纪录片式真实、紧张、临场或混乱。
- 选用判据：要真实粗粝感、紧张临场、纪实风格时用。
- prompt 写法：`手持镜头，自然轻微晃动，纪录片质感，<场景>`（要剧烈则写`剧烈抖动`）。

### 斯坦尼康 / 云台（steadicam / gimbal）

<video src="media/camera-move/move_steadicam.mp4" controls loop muted width="480"></video> <video src="media/camera-move/move_gimbal.mp4" controls loop muted width="480"></video>

- 画面语言效果：稳定器带来"边走边拍却丝滑无抖"的流畅运动，专业、沉浸、连贯。
- 选用判据：要长距离平滑跟随（穿行、长镜头调度）且不要手持的粗粝时用。
- prompt 写法：`斯坦尼康/云台镜头，平滑稳定地跟随<主体>穿行<环境>，无抖动`。

> 速度叠加：以上任意运镜都可叠加速度词——`缓慢`（沉稳/情绪）、`匀速`（中性）、`快速`（紧张/冲击）。AI 视频里还可加 `平滑过渡`、`自然物理运动`、`无突变` 提升流畅度。

## 镜头词库（速查附录）

按拍摄目的分五类的常用镜头词，写 prompt 时按需取用：

- 建立镜头：远景、大全景、俯拍、低角度仰拍。
- 角色镜头：中近景、特写、过肩镜头、侧后方跟拍。
- 运动镜头：缓慢推镜、快速拉远、横向平移、环绕、升降、手持轻微晃动。
- 产品镜头：微距特写、棚拍转台、光线扫过、材质细节拉近。
- 情绪镜头：浅景深、焦点转移、慢动作、逆光轮廓、闪回式过渡。
