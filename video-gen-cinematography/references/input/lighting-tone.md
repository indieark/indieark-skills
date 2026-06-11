# Lighting & Tone 光影与调色

> Load when: 要填导演法【氛围与画质】的「色彩与影调」子字段，或给某一段落定具体冷暖/明暗/调色，需要可挑选的影调模板和「抽象词→可见元素」翻译。
> Avoid: 要定整片风格核心/画风（去 `style-core.md`）、视觉基调（去 `visual-tone.md`）、或单镜时间/地点 token（去 `scene-tokens.md`）。
> Pairs with: `style-core.md` 管整片不变的风格核心/画风、`visual-tone.md` 管视觉基调，本文件管在其之下随段落微调的光影调色；`../../../video-gen-director/references/director-method.md`【氛围与画质】定义「色彩与影调」这个槽，本文件管它填什么。

色彩与影调管「画面是暖是冷、对比强弱、明调暗调、有无颗粒滤镜」，是同一题材、同一风格核心下随环境/段落局部微调的一层——风格核心与视觉基调整片锁定不变，靠这一层做出情绪起伏。下列 27 种电影光影按色彩逻辑分七类，每个按「适用情绪 → 可见元素 → prompt 写法」给出成套翻译，挑一个直接粘进【氛围与画质】的「色彩与影调」槽。Seedance 是中国模型用中文即可，影调专名作英文括注以便对齐业界共识。

`media/lighting-tone/` 下配同名实拍短片供人工对照影调效果（参考自 aishotstudio 27 种电影光影）。md 用 `<video>` 引用，VSCode markdown 预览可直接播放；视频不入库（.gitignore），本地存在即可。

---

## 一、暖调

### 黄金时刻（golden hour）

<video src="media/lighting-tone/14_golden-hour.mp4" controls loop muted width="480"></video>

- 适用情绪：温暖、怀旧、希望、收尾的释然；人物高光时刻、回忆段落。
- 可见元素：日落前低角度暖橙阳光、逆光、长投影、空气中暖色薄雾、整体偏暖偏柔。
- prompt 写法：`黄金时刻暖光，低角度落日逆光浸透画面，暖橙薄雾，树木逆光，长投影，电影感风光`。

### 烛光 / 巴洛克（candlelight / baroque）

<video src="media/lighting-tone/19_candlelight.mp4" controls loop muted width="480"></video>

- 适用情绪：私密、危险逼近、宗教/古典庄重、独处沉思。
- 可见元素：单一暖光源（烛/火/油灯）局部照亮，大面积浓重阴影，明暗反差极强，暖光冷影对比。
- prompt 写法：`烛光照明，火光局部照亮主体，大面积深沉阴影，暖色辉光，明暗对照强烈chiaroscuro，亲密氛围`。

### 棕褐西部（sepia / old west）

<video src="media/lighting-tone/13_sepia.mp4" controls loop muted width="480"></video>

- 适用情绪：年代久远、西部荒野、旧照片式的怀旧。
- 可见元素：单色棕褐色染、暖调、做旧质感、西部片美学。
- prompt 写法：`棕褐色调sepia，单色棕褐染色，西部片美学，暖调做旧，老照片质感`。

---

## 二、冷调

### 蓝调时刻（blue hour）

<video src="media/lighting-tone/15_blue-hour.mp4" controls loop muted width="480"></video>

- 适用情绪：忧郁、孤独、临界、夜将至未至的怅惘。
- 可见元素：日落后/日出前的深蓝天光，冷色调，低饱和，柔和无强投影。
- prompt 写法：`蓝调时刻twilight，日落后深蓝天光，冷色调，深蓝，低饱和，忧郁光线`。

### 北欧冷郁（Nordic noir）

<video src="media/lighting-tone/05_nordic-noir.mp4" controls loop muted width="480"></video>

- 适用情绪：压抑、阴沉、犯罪悬疑、北地的疏离冷感。
- 可见元素：去饱和的蓝灰调，阴天散射光，色彩寡淡，整体灰暗无生气。
- prompt 写法：`北欧冷郁风Nordic noir，去饱和蓝灰色调，阴天散射光，色彩寡淡，阴冷压抑氛围`。

### 钠灯工业（sodium vapor）

<video src="media/lighting-tone/17_sodium-vapor.mp4" controls loop muted width="480"></video>

- 适用情绪：都市夜、工业区、孤冷的城市感（其实是暖橙，但情绪偏冷硬，归在城市夜调）。
- 可见元素：钠灯特有的单一橙黄路灯光，城市夜，工业氛围，色彩被压成橙黄单调。
- prompt 写法：`钠灯照明，橙黄路灯单色光，城市夜，工业氛围`。

---

## 三、高低调与对比

### 高调明亮（high key）

<video src="media/lighting-tone/18_high-key.mp4" controls loop muted width="480"></video>

- 适用情绪：明快、干净、商业、轻松无压力；广告、美好日常。
- 可见元素：整体明亮通透，低对比，白净色调，几乎无浓重阴影。
- prompt 写法：`高调照明high key，画面明亮通透，低对比，干净白净色调，商业美学`。

### 黑白明暗对照（film noir）

<video src="media/lighting-tone/04_film-noir.mp4" controls loop muted width="480"></video>

- 适用情绪：宿命、悬疑、硬派、复古黑色电影。
- 可见元素：黑白单色，极高对比，硬光与浓重阴影，戏剧性阴影。
- prompt 写法：`黑色电影film noir，黑白单色，明暗对照chiaroscuro，高对比单色，戏剧性阴影`。

### 剪影（silhouette）

<video src="media/lighting-tone/20_silhouette.mp4" controls loop muted width="480"></video>

- 适用情绪：神秘、孤绝、图形化的张力；隐藏身份、强调轮廓。
- 可见元素：强逆光，主体压成纯黑剪影，高对比，前景漆黑。
- prompt 写法：`剪影风格，强逆光主体，高对比，前景纯黑剪影`。

### 漂白旁路（bleach bypass）

<video src="media/lighting-tone/02_bleach-bypass.mp4" controls loop muted width="480"></video>

- 适用情绪：粗粝、冷酷、战争/末世、纪实硬派。
- 可见元素：保留银盐的去饱和、高对比、颗粒粗粝质感、漂白般的灰冷。
- prompt 写法：`漂白旁路bleach bypass，银盐保留，去饱和，高对比，粗粝颗粒质感`。

---

## 四、商业 / 通用

### 青橙大片调（teal & orange）

<video src="media/lighting-tone/01_teal-orange.mp4" controls loop muted width="480"></video>

- 适用情绪：好莱坞商业大片的"高级感"默认调；动作、科幻、都市。
- 可见元素：肤色/高光偏暖橙，阴影/背景偏青蓝，互补色对比，对比饱和适中。
- prompt 写法：`青橙调色teal and orange，肤色暖橙、阴影青蓝，互补色对比，商业大片美学`。

### 韦斯·安德森粉彩（Wes Anderson pastel）

<video src="media/lighting-tone/07_wes-anderson.mp4" controls loop muted width="480"></video>

- 适用情绪：工整、童趣、复古文艺、刻意的对称仪式感。
- 可见元素：粉彩色板、35mm 胶片感、平光、对称构图。
- prompt 写法：`粉彩色板，韦斯·安德森风格，35mm 胶片质感，平光，对称构图`。

---

## 五、复古胶片

### 柯达克罗姆（Kodachrome）

<video src="media/lighting-tone/11_kodachrome.mp4" controls loop muted width="480"></video>

- 适用情绪：怀旧、年代感、纪实、温暖的旧时光。
- 可见元素：暖色偏移，饱和但不刺眼，轻微胶片颗粒，档案影像质感。
- prompt 写法：`柯达克罗姆Kodachrome胶片，复古摄影，暖色调，档案影像，模拟胶片质感`。

### CineStill 800T 夜景（红光晕）

<video src="media/lighting-tone/12_cinestill-800t.mp4" controls loop muted width="480"></video>

- 适用情绪：都市夜、霓虹、迷离的现代感；区别于干净数字夜景的"胶片夜"。
- 可见元素：钨丝灯白平衡，高光处红色光晕（halation），冷暖混合，35mm 胶片夜景质感。
- prompt 写法：`CineStill 800T 胶片，高光红色光晕halation，钨丝灯白平衡，电影感夜晚，35mm 胶片`。

### 特艺三色（Technicolor）

<video src="media/lighting-tone/03_technicolor.mp4" controls loop muted width="480"></video>

- 适用情绪：浓烈、华丽、黄金时代好莱坞的鲜艳古典。
- 可见元素：三色染印、超饱和、复古影院色彩、艳丽明快。
- prompt 写法：`特艺三色Technicolor，三色染印，超饱和，复古影院，艳丽色彩`。

---

## 六、单色与双色

### 局部留色（selective color）

<video src="media/lighting-tone/24_selective-color.mp4" controls loop muted width="480"></video>

- 适用情绪：强调单一关键元素、风格化表达（《罪恶之城》式）。
- 可见元素：整体黑白/去色，仅保留一种关键色（如红）醒目突出。
- prompt 写法：`局部留色selective color，整体黑白，仅<某物>保留鲜艳<红>色，罪恶之城风格，色彩隔离`。

### 双色调（duotone）

<video src="media/lighting-tone/23_duotone.mp4" controls loop muted width="480"></video>

- 适用情绪：海报感、波普、风格化平面美学。
- 可见元素：仅两种颜色叠印的色板、双色曝光、波普艺术质感。
- prompt 写法：`双色调duotone，双色曝光，<色A>与<色B>双色板，波普艺术`。

### 交叉冲印（cross-processed）

<video src="media/lighting-tone/25_cross-processed.mp4" controls loop muted width="480"></video>

- 适用情绪：失真、迷幻、lomo 复古、不安的化学感。
- 可见元素：色彩偏移、非自然色、lomo 风格、化学冲洗失衡的怪异色调。
- prompt 写法：`交叉冲印cross-processed，色彩偏移，非自然色，lomo 风格，化学失衡色调`。

---

## 七、科幻 / 特殊光

### 赛博朋克霓虹（cyberpunk neon）

<video src="media/lighting-tone/16_cyberpunk.mp4" controls loop muted width="480"></video>

- 适用情绪：科幻、都市夜、迷离高科技（影调层；整片世界观走 style-core 的赛博朋克风格核心）。
- 可见元素：霓虹照明、品红与青对比、反光面、霓虹黑色电影、湿润质感。
- prompt 写法：`赛博朋克霓虹，品红青色霓虹照明，反光面，霓虹黑色电影neon noir，湿润街道`。

### 矩阵绿（Matrix green）

<video src="media/lighting-tone/06_matrix-green.mp4" controls loop muted width="480"></video>

- 适用情绪：数字虚拟、反乌托邦、监控/代码世界。
- 可见元素：整体绿染、荧光绿、矩阵美学、反乌托邦色板。
- prompt 写法：`绿色染调，荧光绿，矩阵Matrix美学，反乌托邦色板`。

### 夜视监控（night vision / CCTV）

<video src="media/lighting-tone/10_night-vision.mp4" controls loop muted width="480"></video>

- 适用情绪：监控、潜入、伪纪录的紧张窥探感。
- 可见元素：单色绿夜视、监控画面、噪点、安防摄像头视角、监控信号质感。
- prompt 写法：`监控录像CCTV，夜视，单色绿，安防摄像头，颗粒噪点，监控信号画面`。

### 生物荧光（bioluminescence）

<video src="media/lighting-tone/21_bioluminescence.mp4" controls loop muted width="480"></video>

- 适用情绪：奇幻、梦境、深海/森林秘境的魔法感。
- 可见元素：发光植物、深蓝夜、有机霓虹、魔幻氛围。
- prompt 写法：`生物荧光bioluminescence，发光植物，深蓝夜，有机霓虹，魔幻氛围`。

### 紫外黑光（ultraviolet / blacklight）

<video src="media/lighting-tone/27_ultraviolet.mp4" controls loop muted width="480"></video>

- 适用情绪：迷幻派对、超现实、荧光夜店。
- 可见元素：紫外黑光、荧光发亮、UV 反应色、深紫调。
- prompt 写法：`紫外黑光blacklight，荧光发亮，UV 反应色，深紫调`。

### 红外航空（infrared / Aerochrome）

<video src="media/lighting-tone/22_infrared.mp4" controls loop muted width="480"></video>

- 适用情绪：超现实、异星、梦境般的颠倒色世界。
- 可见元素：红外摄影、柯达 Aerochrome、粉红色树木、伪色、超现实色彩。
- prompt 写法：`红外摄影infrared，柯达Aerochrome，粉红树木，伪色，超现实色彩`。

### 热成像（thermal imaging）

<video src="media/lighting-tone/26_thermal.mp4" controls loop muted width="480"></video>

- 适用情绪：科技窥视、狩猎/追踪、非人视角。
- 可见元素：热成像热力图、红外相机、铁血战士视角般的温度色谱。
- prompt 写法：`热成像thermal imaging，热力图，红外相机，温度色谱，掠食者视角`。

### 太阳朋克（solarpunk）

<video src="media/lighting-tone/08_solarpunk.mp4" controls loop muted width="480"></video>

- 适用情绪：明亮乐观的生态未来、绿色乌托邦。
- 可见元素：生态未来主义、繁茂绿植、明亮阳光、白绿色板。
- prompt 写法：`太阳朋克solarpunk，生态未来主义，繁茂绿植，明亮阳光，白绿色板`。

### 蒸汽朋克（steampunk）

<video src="media/lighting-tone/09_steampunk.mp4" controls loop muted width="480"></video>

- 适用情绪：维多利亚工业、黄铜机械、复古蒸汽时代。
- 可见元素：黄铜与紫铜、维多利亚工业、暖金氛围、蒸汽。
- prompt 写法：`蒸汽朋克steampunk，黄铜紫铜质感，维多利亚工业，暖金氛围，蒸汽`。

---

> 取用提示：色彩与影调是【氛围与画质】三层里最该随段落微调的一层——同一部戏白天可走「黄金时刻」、入夜切「CineStill 800T」、悬疑高潮压成「北欧冷郁」。风格核心（见 `style-core.md`）与视觉基调（见 `visual-tone.md`）保持不变，只换这一层即可做出情绪起伏。
>
> 七类中「科幻/特殊光」的赛博朋克、太阳朋克、蒸汽朋克、矩阵绿等，既可作纯影调层叠在写实题材上，也对应整片世界观——若要把它定成整片不变的题材基调，请去 `style-core.md` 的风格核心层。本文件只取它们的「光影色彩」面。
