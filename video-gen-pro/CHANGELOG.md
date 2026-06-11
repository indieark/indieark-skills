# Changelog

本文件记录 `video-gen-pro` skill 包内部结构演进。只记录 skill 内部文件，不记录宿主仓库改动。

## 0.5.0 - 2026-06-11

### Changed

- 拆分为 8-skill hub+spoke 技能族（学习 larksuite/cli 模式）：本包收敛为 **hub**（执行器 + 路由枢纽），方法论与编排参考迁出到 7 个同级卫星 skill——`video-gen-script`（generation-workflow.md、multi-segment-continuity.md）、`video-gen-guide`（guide-mode.md）、`video-gen-advisor`（advisor-mode.md）、`video-gen-director`（director-method.md）、`video-gen-storyboard`（visual-storyboard.md + methods/storyboard/ 其余 4 文件与索引）、`video-gen-assets`（assets.md + assets/ 全部，目录拍平为各自 references/ 顶层）、`video-gen-cinematography`（input.md + input/ 整树原样平移，含 gallery.html 与 media/，引用零改动）。`methods/README.md` 留守改写为 `references/methods.md` 方法选择门。根因修复：frontmatter description 从 1102 字符（超过加载器 1024 上限被静默丢弃，导致触发不稳）重写为 434 字符，并附 lark 式「不负责：…（走 …）」负向路由。SKILL.md 重写为路由枢纽（新增 8 行技能族意图路由表、guide/advisor/流程协议改路由卫星、Red Lines 全部原文保留、Route block 增 `Family skill:` 行）；skill.json 升 0.5.0 并声明 `role: hub` + `satellites`，guide 模式 4 个 capabilities 迁入 video-gen-guide/skill.json；`scripts/validate_skill.py` 改造为家族自检（同级目录解析卫星、半套安装即报错、跨 skill 短语契约与链接检查、description ≤1024 防线）。hub 内全部跨 skill 引用按「安装后同级」约定改写为 `../video-gen-xxx/...` 形式。
- 导演法最终 prompt 立「三段之外零追加」硬规则：实际生成中发现导演法多段任务会把 `multi-segment-continuity.md` Prompt Pattern 的「这是第 X 段 / 上一段结束状态 / 本段结束状态 / 禁止」小节嫁接到三段式骨架前后，把面向执行者的说明性文字（段落编号、承接方式、台账状态、单列禁止清单）发给了视频模型。`references/methods/director-method.md` 三段式骨架开头新增硬规则：最终 prompt 有且只有【基础设定】【氛围与画质】【画面内容】三段，约束折进对应段位（资产不可变特征→基础设定、起始画面/落点/不出现的元素→画面内容、文字水印禁止→画面文字字段）；「跨段复用」节补充多段承接只在【画面内容】首尾表达、台账信息不进 prompt；Self Check 新增对应自检项。`references/methods/storyboard/multi-segment-continuity.md` 的 Prompt Pattern 显式限定只适用于故事板法的 `video-prompt.txt`，导演法多段不得套用。
- 输入指南填法文件按**单一维度**细拆：把两个合并文件拆成六个一维度一文件，每个填法文件只管导演法【画面内容】/【氛围与画质】的一个子字段。`shot-grammar.md`（景别+构图+机位角度+运镜+焦点+镜头词库揉在一起）拆成 `shot-scale.md`（景别，含焦点/景深）、`composition.md`（构图，含机位角度）、`camera-move.md`（运镜，含五类镜头词库附录）三个；`style-library.md`（风格核心+视觉基调）拆成 `style-core.md`（画风/风格核心，即梦官方 94 风格 + Style Bible 翻译规则）、`visual-tone.md`（视觉基调，5 个器材/画幅模板）两个；`lighting-tone.md`（色彩与影调）本就独立、不动。归并口径：机位角度并入构图（都管主体在画框里怎么摆、从什么方位看）、焦点并入景别（都管取景远近与景深）。媒体随正文按维度物理搬迁——`media/shot-grammar/` 的 41 个 Runway gif 按前缀拆进 `media/shot-scale/`（shot_*+focus_* 共 10）、`media/composition/`（comp_*+angle_* 共 11）、`media/camera-move/`（move_* 共 18），两个从未被正文引用的冗余 gif（shot_establishing/shot_wide）随旧目录删除；`media/style-library/` 的 94 webp 全量进 `media/style-core/`；五个新文件零死链、零跨目录引用校验通过。删除旧 `shot-grammar.md` / `style-library.md`（内容已全部迁出，不留空壳）。全链路指针同步：`methods/director-method.md`（【画面内容】景别/构图/运镜三处指针、【氛围与画质】风格核心/视觉基调指针、镜头词库附录指针）、`references/input.md`（Input Route 表 2 行拆 5 行）、`references/input/README.md`（Method Index 表 + 横切性说明 2 项拆 5 项）、`references/concepts.md`（横切维度指针列表 + 现状段文件清单）、`references/input/scene-tokens.md`、`references/assets/setting-director.md`、`references/input/lighting-tone.md`（Avoid/Pairs + 赛博朋克影调指针 + 取用提示）、`references/methods/storyboard/storyboard-board.md` 每格镜头语言与风格指针，全部从旧 2 文件名改指向新 5 文件名。
- 立「输入指南 / Input Guide」横切维度（填料层）：在剧本 / 资产 / 方法论三分之上立一根**横切所有方法论**的轴——剧本回答「拍什么」、资产回答「用什么料」、方法论回答「用什么骨架」，输入指南回答「方法论定下的骨架槽位具体该填什么、怎么填」，被导演法和故事板法共同调用，不是第四个并列基石。物理上新建 `references/input/` 目录：入口 `references/input.md`（对称 `assets.md` 的运行入口）、二级索引 `references/input/README.md`，子文件 `shot-grammar.md` / `style-library.md` / `scene-tokens.md` / `image-input.md`。**A 类既有填料物理搬迁**（正文搬走、原处留指针）：参考图按需投放（Input Economy）、图内零文字（Reference Purity）、全能参考写法 / 参考素材编号搬入 `references/input/image-input.md`；时间光影 / 地点氛围 token 搬入 `references/input/scene-tokens.md`；镜头词库（建立 / 角色 / 运动 / 产品 / 情绪五类）搬入 `references/input/shot-grammar.md`——原处 `references/assets/principles.md`、`references/assets/scene-sheet.md`、`references/methods/director-method.md` 对应正文改为指向新文件的指针。**B 类原创填法理论本轮预填占位**：`references/input/shot-grammar.md`（景别 / 构图 / 运镜各选项的画面语言效果 + 选用判据 + prompt 写法）与 `references/input/style-library.md`（整片风格模板库，雏形提炼自 `setting-director.md` 的 Style Bible，原处保留正文并加指针）留骨架 + `TODO` 占位，正文下轮专门逐项写、过目。全链路加横切指针：`director-method.md`【画面内容】景别子字段 → shot-grammar、【氛围与画质】→ style-library，`references/methods/storyboard/storyboard-board.md` 每格镜头语言与风格 → input；`concepts.md` 新增横切维度定义节、更新物理重组约定与图档梯度 SSOT 指针；`references/README.md`「场景与方法」组与 `SKILL.md` 决策管线第 12 步登记 `input.md` 入口。两个 validator（`scripts/validate_skill.py`、宿主仓库 `scripts/validate_repository.py`）同步：principles.md 原先钉住的三个 Reference Purity 断言串迁到 `references/input/image-input.md` 的 key、新增 input 子文件的 required-substring 断言、`input` 注册进子目录索引机制、input 维度文件并入 canonical 必备文件清单；双 validator 全绿（skill 级保持基线 8 warning、仓库级 0 error）。
- 补输入侧的「参考图按需投放」原则（Input Economy），与既有 Reference Purity 并列：图档梯度（L0→L2）按**复用强度**决定一个资产**做**多重，这条新原则按**当前镜头需要**决定实际**喂**视频模型哪几张、喂多细——参考图数量×单图细节量整体超标会超出模型心智负担、稀释主体，所以按当前镜头精选最小够用集（主体角色给 master、背景一闪而过的给单图、L2 捆绑特写按镜头挑对应情绪那一张而非整组全喂、本镜不复用的场景给单图），每张都得能在 prompt 说清用途。`references/assets/principles.md` 新增 Input Economy 节，并在「多图参考是必要输入」那句后补「多图≠越多越好，是该给的几张精准给到」的限定；`references/methods/director-method.md` 的机器人骑鸵鸟 Example 点评补一笔活案例（机器人主角 L2 三视图+表情单图、鸵鸟/雷管/丧尸/场景 L0 单图，同镜里主体拉满、配角和场景按需从简）；`character-sheet.md` / `scene-sheet.md` / `prop-sheet.md` 三张梯度表后各加一句指针指向 Input Economy。机器人 LED 像素表情只作 Example 里「表情单图」的实例提及，不改 character-sheet 面向真人脸的「面部特写」定义。并把 Input Economy 与既有同源表述互链收口：它定位为「相关性筛选之上再加一层总量精选」——`references/generation-workflow.md`（只提交当前段需要的输入、无关不进 payload）和 `multi-segment-continuity.md` / `script-composed-storyboard.md`（按段控制每轮输入负载）先按**相关性**筛掉无关输入，Input Economy 再在留下的相关输入里按**总量与细节量**精选，两步递进不重复；`references/concepts.md` 图档梯度 SSOT 定义句后也加一句指针，让「做多重」的梯度 SSOT 能索引到「喂多少」的 Input Economy。
- 资产识别从「镜头反推」收口到「剧本拆分」：把资产来源统一为**剧本→资产清单→镜头引用**两步——先从选定剧本分析出本片需要的角色/场景/道具/声线资产清单（可跨剧本复用的单元），再拆镜头并让每个镜头**引用**清单里已有的资产，镜头是资产的使用者而非定义者，缺资产时回到剧本资产清单补登而非在镜头层凭空新造。修正 `references/generation-workflow.md` 导演检查里「镜头转资产：从镜头清单反推」这处与系统其余表述（`references/router.md`、`references/visual-storyboard.md`、`references/methods/storyboard/multi-segment-continuity.md` 早已写「从剧本分析资产」）自相矛盾的病灶。同步 `references/concepts.md`（剧本 Canonical 入口改「剧本→资产清单→镜头引用」，并新增「资产从剧本拆不从镜头反推」「剧本是可伸缩单元：单视频时单视频就是剧本」说明）、`references/methods/director-method.md`（前置条件顺序）、`SKILL.md`（成功标准、决策管线、red lines 三处）、`references/router.md`、`references/generation-workflow.md`（导演检查与导演流程复核）、`agents/openai.yaml`（OpenAI agent default_prompt 的英文导演检查顺序）、两份 `SKILL.md` frontmatter description（根入口壳与 skill 包内的英文描述同步，把 `shot breakdown, and scene-card/asset routing plan` 旧顺序改为「资产先从剧本拆、镜头引用」）和 docs 层 `current-status.md`。两个 validator（`scripts/validate_skill.py`、宿主仓库 `scripts/validate_repository.py`）里钉住旧顺序句的 required-substring 断言同步更新。明确区分「资产来源」与「生成时机」：来源固定（清单一律从剧本拆），但生成时机两种都正式可选——批量预生成（照清单一次做齐，复用/一致性好）或按镜头懒生成（清单先列着、镜头真用到时再生成已规划的资产，适合轻量/探索任务）；「不凭空新造」约束改写为只禁「绕过剧本清单冒出未登记资产」，不禁「懒生成清单里已规划的资产」。并注明「剧本→资产清单→镜头引用」是默认心智模型而非强制流水线，轻量/单镜头任务不必显式产出独立资产清单文档（`references/generation-workflow.md` 剧本转资产清单/镜头引用资产两条、`references/concepts.md` 来源与时机说明同步）。
- 导演法提示词结构重构为三段式骨架：用 **【基础设定】+【氛围与画质】+【画面内容】** 替换原来的 Slate Fields 控场卡、多节拍 Beat 子结构、字段取舍矩阵和无故事板 JSON `shots` 结构。【基础设定】是资产层，以文字为主、`@xxx图片` 只作索引锚点、不盲信依赖图片，每个资产（角色/场景/道具，以及声音、声线等所有索引部分）都靠文字认真详细描述；声音归入【基础设定】（声音/声线是可后续填充的资产），写法仍以 `sound-design.md` 为 canonical。【氛围与画质】是跨段复用区块，四子字段按变化策略分档：风格核心、视觉基调整片基本不变，色彩与影调仅环境变化时微调，氛围基调随剧本改写。【画面内容】才写分镜/景别/构图/运镜手法/画面内容，原 Beat 的时间分段递进并入「画面内容」字段写成连续时序叙述（不再叫 Beat、不再单独分拍）。镜头词库保留为附录，新增「机器人骑鸵鸟炸丧尸」端到端三段式完整示例。资产描述详略明确分情况：**导演法每个资产认真详细描述（无母图兜底），故事板法资产只需简单描述（图已画详细）**，写入 `concepts.md` 两法对比表。`references/methods/director-method.md`（主体重写）、`references/concepts.md`、`references/methods/README.md`、`references/scenes.md`（6 处 Recommended method）、`references/router.md`、`references/visual-storyboard.md`、`SKILL.md`（决策管线第 7 步与 Route 模板）、skill `README.md`、`references/README.md`，以及 docs 层 `current-status.md`、`model-vs-methodology.md`、`source-of-truth.md` 的方法描述与 Beat/控场卡措辞同步更新。
- 澄清两法核心分界并补权衡表：把分界从「要不要先画图像母图」精确为「要不要先**用资产**再生成一层图像中间产物（故事板/分镜图）」，明确导演法**也用资产**（参考图/视频/音频、角色卡/场景卡/道具卡作输入），只是不把资产再合成可视化母图——纠正「导演法=纯文字控场」的误读。`concepts.md` 新增「两法权衡：代价与适用」对比表（主控手段、资产用法、画面可预见性、耗时、抽卡层数、AI 发挥空间、适用场景），并注明故事板法只锁镜头顺序和运动、是「大幅收窄不确定性」而非「100% 所见即所得」。`concepts.md`、`methods/README.md`、skill 包 `README.md` 的核心分界措辞同步；「分镜化文字/Beat 是纯文字子结构」这类描述子结构形态的「纯文字」保留不变。
- 方法论从三种并列收敛为两种：分镜法不再是独立方法，其分镜化文字描述本就是导演法的文字写法之一，连同多节拍 Beat 一起并入导演法作为子结构；`methods/` 现在只有导演法（纯文字控场，含单/少镜头与多节拍 Beat 两种子写法）和故事板法（图像母图主控）。`shot-sequence.md` 内容并入 `director-method.md`「多节拍递进结构（Beat 子结构）」后删除。`concepts.md`（方法论 SSOT，补「分镜」一词按形态归属的去歧义说明）、`source-of-truth` 表、`methods/README.md`、`SKILL.md` 决策管线与 Route 模板、`router.md`、`scenes.md` 各场景 Recommended method、`references/README.md`、`visual-storyboard.md` 和 docs 层方法描述同步更新。

### Added

- 资产维度补齐到五类并落地 CLI：在 `character`、`scene` 之外新增 `prop`（道具）、`graphic`（素材）、`voice`（声线）三种资产类型（`ASSET_TYPES`），各有独立容器目录、ID 前缀和媒体子目录（图像类进 `images/`，声线进 `audio/`）。新增 `references/assets/prop-sheet.md`（道具卡：纯净底单图 / 主图+拆解 / 多视图道具卡，纯图像零文字）和 `references/assets/graphic-sheet.md`（素材：轴=复用范围，一次性 / 项目套件 / 跨项目 master，参考图输入或后期叠加两用）。声线作为人物附属音频资产，用 `--role` 绑定角色名，在 omni 模式下作 `reference_audio` 锁音色，方法写入 `character-sheet.md` 声线小节。`素材` CLI 类型名取 `graphic`，刻意避开既有 `material` 存储字段，避免撞词。

### Changed

- references 三分物理重组（剧本 / 资产 / 方法论）：可跨剧本复用的资产族迁入 `references/assets/`（入口 `references/assets.md`），方法论三种并列方法迁入 `references/methods/`（导演法 `director-method.md`、分镜法 `shot-sequence.md`、故事板法 `methods/storyboard/`）。场记板改名为导演法，废除独立 `director.md`（内容分配到导演法、生成流程和故事板母图），提示词随方法走。两份 validator、source-of-truth 表和全部文档索引同步更新。
- 细化人物三档按需选档逻辑并给 L2 加硬规则：L0 单图草稿用于龙套或只出现一次的角色，可带背景、不必纯白底；L1 三视图左 1/3 头肩胸特写只取常态表情、无表情变化，无特殊演出需求时已够用；L2 多视图 master 本身缺大范围面部写真、脸易走形，**必须额外捆绑高清头肩胸/面部特写单图**（情绪有变化可多张）锚定面部、不可单独交付，板内右上表情区与独立特写单图共存（表情区给情绪广度、特写单图给面部精度），捆绑特写单图各自用 `--type character` 单独登记并标注用途。`character-sheet.md`（形态档位表、第二种、第三种、Registration）与 `concepts.md` 人物形态 SSOT 同步。
- 明确 L2 必配特写单图是可复用资产：不必每个分镜额外做，给角色 master 做几张典型特写（常态 + 该角色典型情绪）跟 multi-view master 一起登记，后续分镜按需调用对应表情、跨镜头跨段复用。`character-sheet.md`（形态档位表 L2、第三种小节、Registration）、`concepts.md` 人物形态 SSOT 和 `source-of-truth` 内容面行同步。
- 放开配套素材的画幅限制：道具 L0 纯净底单图和人物 L2 必配面部/头肩胸特写单图都是配合主资产用的配套图，画幅按对象外形/构图取正方形或长方形均可、不强制 16:9，只保留纯净底/高清等功能性约束和分辨率下限（最低 2K）。`prop-sheet.md`（形态档位表 L0、提示词尺寸行）与 `character-sheet.md`（L2 必配特写单图）同步。
- 资产形态确立从轻到重三档梯度模型（L0 → L2）：人物为单图草稿（L0，非正式草稿档）/ 三视图（L1）/ 设定板多视图（L2），场景为单一场景概念图（L0，内含快速抽卡探索写法与基本场景卡标准写法）/ 多视角联合图（L1）/ 正交四视图（L2，master）；`concepts.md` 为档位 SSOT，character-sheet 和 scene-sheet 同步显式标注档位与选档判据，原有角色卡两种正式提示词和五个场景写法小节锚点全部保留。
- 新增智能编排门：15 秒是单次生成上限，不是默认目标；复杂高信息量的 15 秒内容可拆成多个更短故事板和视频生成轮次。
- 纠正故事板中文文字和复杂排版路线：高能力图像模型可以直接生成包含中文文字、CUT 表、时间码和复杂版式的完整 4K 故事板母图；脚本拼版只作为确定性可编辑文字、指定字体/品牌版式、超密集 CUT 表或程序化复盘路线。
- 补齐智能编排的层级索引：Skill 入口、references 索引、router、visual-assets 入口和 visual-assets 二级索引都指向同一正文源。
- 新增生成前最终输入锁定门：即使用故事板，也必须确认输出规格、实际提交输入、声音策略、说话人声、字幕/标题文字和最终视频提示词。
- 角色卡提示词补齐尺寸和最高档多视图版式：人设三视图和多视图角色卡最低 2K，16:9 为 2560x1440；细节丰富、高一致性或主角 master 优先 4K，推荐 3840x2160；多视图 master 改为纯图像设定板，左 2/3 正侧背三视图、右 1/3 上半表情组下半细节特写组，表情和特写按角色重要度取 4 或 6，图内不写任何文字标签。
- 确立 reference 纯净度原则：作为视频模型参考输入的资产（角色卡、场景卡）必须纯图像、零语义文字，图内标题/字段表/栏目名/标签会被模型还原成画面并污染成片；给人或规划复盘看的中间产物（故事板母图、脚本拼版）可带文字。纯几何测量线和对齐参考线不算文字。设定写进提示词正文和资产登记，不画进图里。`principles.md` 新增 Reference Purity 节，character-sheet 和 scene-sheet 同步落实。
- 场景卡新增强制路由判断：每个主要场景先按镜头角度数、复用强度和空间风险选择基本场景卡、正交四视图或多视角联合图；不能默认只生成简单场景单图。
- 强化导演流程门：复杂生成必须先把自然语言转成剧本候选、镜头清单和角色/场景/道具资产依赖；非抽象镜头缺场景卡时不能直接进入故事板、最终 prompt 或 API。
- 故事板流程改为首版正式故事板即 4K 或等效 4K；当前流程不设置低清预览确认门，低清草稿不能登记、确认或提交 Seedance。
- 恢复 HTML 回复实验之前的格式化标准回复流程：生成前确认和结果复盘使用标准文本块 + 结构化 JSON，承接确认、退回阶段、尺寸和修改字段；HTML review 只保留在归档计划和历史记录中。
- Agent-HTML review gate 已暂停归档，不再作为当前默认交互流程；生成前确认和结果复盘默认回到对话文本 + 结构化 JSON 字段。`review final-input` / `review result`、测试和文档记录保留，用于未来显式重启或复现。
- `review final-input` 和 `review result` 的 Agent-HTML 目标阶段选项不再使用空字符串 value，避免 Agent-HTML runtime / Radix Select 在浏览器中报错后把页面清空；response template 仍用 `target_stage: null` 表示不切换阶段。
- 文档补充 `*.agent.html` 是 Agent-HTML source，带样式浏览应使用 `ahtml preview/build`；多个 artifact 本机预览需要顺序启动并使用独立输出目录，避免 Agent-HTML runtime 共享构建状态导致串页。
- `review final-input` 与 `review result` 改为 Agent-HTML review gates：`final-input` 只用于真实生成视频前最终输入确认，`result` 只用于生成或 dry-run 后结果复盘；默认输出 `*.agent.html`、state JSON 和 response template JSON，不再使用自定义 JS 按钮页。
- 旧版“低清故事板预览 -> 4K 终稿”规则已被首版 4K 故事板规则取代。

## 0.4.3 - 2026-06-10

### Changed

- Skill 主名改为 `video-gen-pro`，CLI 主命令改为 `videogen`；`video-gen-pro` 和旧 `seedance2` 作为命令别名调用同一套实现。
- `skill.json` runtime entrypoint 改为 `scripts/video_gen_pro.py`，`scripts/seedance2_video.py` 只保留旧脚本兼容。
- 默认配置路径改为 Windows `%APPDATA%\video-gen-pro\config.json`、POSIX `~/.config/video-gen-pro/config.json`；运行时代码不再加入旧配置路径自动迁移逻辑。

## 0.4.2 - 2026-05-14

### Added

- 新增 `asset reuse`，可把既有角色/场景资产跨项目复用到当前项目；本地素材复制到目标项目资产目录，外部素材登记同一 source，并在新资产记录写入 `reused_from`，保留来源项目、来源资产、路径和 hash。

### Changed

- 复杂生成流程现在把既有角色卡/场景卡复用写成强确认门：先 `asset search` / `asset show` 展示候选，用户确认后再 `asset reuse` 或一次性引用旧素材；不再只说“找到后复用”。
- 新增 `references/guide-mode.md` 作为功能介绍/使用向导的强制详细输出协议，要求说明能力、边界、输入模式、标准流程、素材准备、确认门和下一步；用户只问某个功能时，也按需解释输入模式、角色卡、场景卡、道具卡、故事板、声音、结构化修改意见、生成前确认、结果复盘、CLI/API/Key 或触发边界，并明确不调用 CLI、不构造 payload、不要求 API Key。
- 新增 `references/generation-workflow.md` 作为端到端生成流程协议，覆盖阶段进度提醒、剧本候选、资产规划、批量图片确认、故事板逐镜头编辑、生成前全输入确认、HTML 结构化修改意见和结果复盘。
- 场景卡提示词补充室内/室外快速场景、单一场景概念图、正交四视图和多视角联合图；这些都是 `scene-sheet.md` 下的类型选择，仍遵守主要场景列表、场景 DNA、光线/道具连续性和禁止穿帮提醒。
- 场景卡类型选择补充按需规则：静止、推进或拉远镜头用基本场景卡；正交四视图只用于严格复用的 master 场景；多视角联合图只用于某一次剧情场景里的多个镜头角度。
- 新增 guide mode 触发语义：用户询问功能介绍、使用向导、支持模式或生成前准备事项时，可以触发 Skill 做说明，但不调用 CLI、不构造 payload、不声明已生成结果。
- 新增提示词详略路由：有故事板时保持短读图 `video-prompt.txt`；无故事板时使用详细分镜化视频 prompt，并逐镜头管理视觉、镜头、音乐、环境音、动作音效、说话人声、字幕/标题文字和转场。
- 自动拆分现在明确按“用户输入 -> 剧本 -> 角色/场景/道具卡需求 -> 生成轮次”执行；是否单段或多段由内容复杂度、总时长、4-15 秒限制和每轮输入负载共同决定。
- 每个生成轮次只提交本段相关故事板、角色卡、场景/背景卡、道具/产品卡和声音 brief；简单内容允许一张故事板，角色一致性场景可用简稿故事板 + 角色卡，多角色多场景宣传片或战斗变化必须拆段。
- 明确 3x3 九宫格和四栏故事板是可按场景裁剪的创作参考，不是固定格数或固定栏目模板。
- 新增 `references/visual-assets/storyboard-board.md` 作为故事板 canonical 概念：故事板是一张按需组织的视频主参考信息母图，九宫格、四栏、8 镜头和制作设定板都只是版式变体。
- 新增 `references/visual-assets/script-composed-storyboard.md`，把类似影视分镜信息图的工作流写清：剧本按时长拆段，生成 CUT / 场景 / 调度原子图，再用脚本拼成 4K 故事板海报后确认并生成视频。
- 故事板母图现在明确要求 4K 或更高规格，可以承载清晰可读的详细文本、表格、镜头说明、对白、灯光、声音和情绪节奏。
- `video-prompt.txt` 现在定位为简短读图指令：说明区域主次、运动目标和禁止项，不全文复述 `storyboard-prompt.txt`。
- 补充故事板法适用边界：清楚可规划、需要一致性的镜头优先故事板；粒子、爆炸、烟雾、混乱战场或强抽象动态优先 prompt-heavy 或混合路径。
- `visual-assets`、`grid-storyboard`、`four-column-storyboard` 和 `seedance-handoff` 现在要求按实际故事板结构写读图顺序，同时保留用户确认和项目库回溯。
- 新增 `references/visual-assets/multi-segment-continuity.md`，说明多段视频连续性台账、每段故事板、上一段尾帧承接、`first-frame` / `first-last` / `extend` 的使用边界，并在 `skill.json` capability 中登记多段连续性规划。
- 多段连续性现在要求剧本拆分时先按剧情节拍和镜头边界切段，尽量不要把同一镜头拆成两次生成；`continuity_mode` 由 Skill/AI 判断，镜头切换不强制尾帧，只有画面硬衔接才用尾帧 / `first-last`，同一长镜头跨段时优先 `extend` 或尾帧硬衔接。
- 故事板、分镜和脚本拼版 CUT 图现在必须绑定并参考已确认角色卡和场景卡；多张分镜拼版时，每张分镜都要保留 `character_refs` 和 `scene_ref` 回溯。
- 角色卡提示词现在明确只能使用人设三视图或多视图模板；第一种人设描述提示词只是基础文本，不单独作为复杂项目最终角色卡。
- 场景卡提示词现在要求先列主要场景，再按单场景和必要多角度逐个生成，必须包含场景 DNA、光线方向、关键道具位置、空间关系和禁止穿帮提醒。
- 为人物设定图、场景设定图、分镜母图和项目故事板补充生成前确认包；`visual-assets.md` 新增逐项确认门，避免复杂任务静默跑完整条资产链。
- 收紧层层索引和路由顺序：复杂故事板路线必须先过 `visual-storyboard.md` 的项目/资产检索门，再由 `visual-assets.md` 选择必要子文件，不把九宫格、四栏或制作设定板当硬模板。
- 修正 `router.md` 的验证命令，使用仓库根可执行的 `python skills/video-gen-pro/scripts/validate_skill.py` 路径。

## 0.4.1 - 2026-05-13

### Added

- `asset add` 支持 `--tag`、`--role` 和 `--alias`，用于给角色/场景图片登记可检索元数据。
- 新增 `asset show`，可查看单个资产的存储路径、来源、hash、标签、角色和所在项目。
- 新增 `asset search`，支持跨项目按类型、关键词、标签、角色和来源类型检索已有角色/场景资产。
- `asset list` 支持项目内关键词、标签、角色和来源类型筛选。

### Changed

- Skill 路由把“生成前先调研和检索已有项目/资产”写入复杂任务默认流程；找到可复用资产时先复用或请用户确认，再决定是否新生成/新登记。

## 0.4.0 - 2026-05-13

### Added

- 新增本地创作项目库 CLI：`project`、`asset`、`script`、`style`、`storyboard`、`history`。
- 新增 `generate --project <id> --storyboard <id>`，默认从已确认故事板读取视频提示词，并把故事板图作为 `omni` 参考图生成。
- 新增 `references/visual-storyboard.md`，定义复杂任务的项目资产库、视觉故事板、确认门和生成历史流程。
- 新增 `references/visual-assets.md`，定义人物设定图、场景设定图、故事板母图和版式变体的提示词方法；图片生成由 Skill 调用外部图像工具，CLI 只登记结果。
- 新增 `references/visual-assets/` 二级方法库，把视觉资产理论拆成 `principles`、`setting-director`、`character-sheet`、`scene-sheet`、`grid-storyboard`、`four-column-storyboard` 和 `seedance-handoff`，避免把完整理论堆在入口文件。
- 项目化运行会保存 `project-generation.json` / `generation-record.json`，并在 `media-manifest.json` 与 `generation-log.json` 中写入 `project_context`。

### Changed

- `SKILL.md` 和 `router.md` 将短剧、广告、系列内容、角色/场景一致性任务默认路由到项目资产库 + 视觉故事板确认。
- `completion.md` 增加项目和故事板汇报要求。

## 0.3.15 - 2026-05-13

### Added

- 新增 `references/completion.md`，定义生成完成、失败、超时或下载后的标准用户回复格式。
- 完成回复必须包含实际提交的提示词、使用的素材清单、结果链接或本地 MP4、任务 ID、参数、证据目录和验收结论。

### Changed

- `SKILL.md` 的强制执行协议接入完成回复规范，要求验收后按 `completion.md` 汇报。
- `references/router.md` 的验证路径补充 completion route，确保执行后不是只返回 URL。

## 0.3.14 - 2026-05-13

### Changed

- 将 Skill 入口的执行顺序升级为硬协议：触发后必须先交互路由、按需读取方法论和 API/CLI 参考，再通过 `seedance2` CLI 执行，最后检查生成 artifact 并按用户意图验收。
- `router.md` 的 API operation route 对齐当前 6 个创建子命令：`text-to-video`、`first-frame`、`first-last`、`omni`、`edit`、`extend`，不再使用旧的 `create` 总命令。
- 验证路径补充生成执行阶段验收：提交前 dry-run、提交后 artifact、完成后 `task-result.json` / `content.video_url` / 下载结果，以及不匹配时进入定向迭代。

## 0.3.13 - 2026-05-12

### Changed

- 收紧 Skill 触发语义：用户需要生成视频、图生视频、文生视频、参考素材生成视频、有声/无声视频、视频生成模型编辑或延长时默认触发本 Skill。
- 明确不触发边界：用户指定其他视频 provider、只要静态图、或只做传统 MP4 剪辑/转码/合并时，不触发本 Skill。

## 0.3.12 - 2026-05-12

### Added

- 新增可选 callback 调试命令：`callback-server` 用于本地接收 webhook POST 并保存 body/headers，`callback-smoke` 用于向 receiver 发送模拟 POST。
- 文档明确 callback 是外部系统集成能力；AI/Skill 默认生成闭环仍使用 `--wait` 轮询。

## 0.3.11 - 2026-05-12

### Added

- 创建命令新增汇总型 `generation-log.json`。它会记录请求参数、prompt 指纹、参考素材编号映射、媒体预处理/校验、URL 预检、CF tunnel 元数据、提交摘要，以及 `--wait` 完成后的最终任务结果。
- CLI 返回值新增 `generation_log_path`，方便 Skill 或外部流程直接定位本次生成日志。

## 0.3.10 - 2026-05-12

### Added

- `seedance2 doctor` 新增可选本地工具检查：Pillow、ffmpeg、ffprobe、cloudflared。缺失不会让 doctor 失败，但会说明在图片格式/尺寸修复、音频/视频转码截断、媒体规格探测、本地视频 Cloudflare 临时 HTTPS 暴露时需要安装什么。

### Changed

- 图片、音频、视频和 Cloudflare tunnel 的阻断报错补充安装命令与替代方案，便于 CLI/Skill 在遇到格式和大小问题时直接告诉用户下一步处理方法。

## 0.3.9 - 2026-05-12

### Changed

- 本地媒体处理从“发现违规先拒绝”改为“可安全修复则先修复”：本地图片在 Pillow 可用时会自动缩放、补边和转 JPEG；音频/视频在 ffmpeg 可用时会尝试转码、截断和规范化。
- `media-manifest.json` 的 `preparation` 会记录自动修复原因，让用户知道哪些素材已被处理过。

## 0.3.8 - 2026-05-12

### Added

- 新增本地媒体规格校验：图片按官方尺寸 / 比例 / 扩展名 / 大小做本地阻断；视频和音频在 `ffprobe` 可用时校验单段时长、总时长、视频 FPS、编码、尺寸、比例和像素数。
- `media-manifest.json` 新增 `validation`，记录本次本地媒体规格校验结果和无法探测的字段 warning。

## 0.3.7 - 2026-05-12

### Added

- 创建命令新增 `--prompt-file`，按 UTF-8 读取导演 prompt，避免 Windows shell 或长中文分镜参数转码破坏提示词。
- CLI stdout/stderr 强制使用 UTF-8，避免 JSON / markdown 输出里的中文 prompt 在 Windows 管道中乱码。

### Fixed

- 同时传 `--prompt` 和 `--prompt-file` 时本地拒绝，避免提交含义不清的 prompt。

## 0.3.6 - 2026-05-11

### Fixed

- `--serve-local-assets cloudflare` 现在只处理本地 `reference_video`。本地图片和音频即使同时传了 `--serve-local-assets cloudflare`，也继续走 Base64 / `--prepare-local-media` 路径，不再暴露到 Cloudflare tunnel。

## 0.3.5 - 2026-05-11

### Added

- `media-manifest.json` 新增 `reference_index`，把 CLI 输入顺序映射为稳定 prompt 标签：`参考图1`、`参考视频1`、`参考音频1` 等。
- `media-manifest.json` 新增 `prompt_reference_warnings`，当 prompt 没有明确提到某个参考素材用途时给出复盘警告。
- prompt 检查兼容官方示例写法：`图片1`、`视频1`、`音频1` 可分别匹配 `参考图1`、`参考视频1`、`参考音频1`。

## 0.3.4 - 2026-05-11

### Added

- 创建命令新增 `--prepare-local-media auto|off`。默认 `auto` 会在本地图片/音频进入 Base64 payload 前执行可控预处理，并把结果写入 `media-manifest.json`。
- 本地图片预处理可使用可选 Pillow；本地音频预处理可使用可选 ffmpeg。素材超过官方大小限制且缺少对应工具时，会在本地明确失败。
- 增加本地图片/音频 Base64 请求体预算检查，避免超过官方 64MB request body 限制。

### Unchanged

- 本地视频仍不转 Base64；涉及 `reference_video` 时继续使用 `--serve-local-assets cloudflare`、signed URL 或 `asset://`。

## 0.3.3 - 2026-05-11

### Added

- 创建命令新增 `--callback-url`、`--execution-expires-after`、`--service-tier`、`--safety-identifier`，对齐火山创建任务请求体字段。
- 补充本地校验：`callback_url` 必须为 HTTP(S)，`execution_expires_after` 必须在 `3600-259200` 秒，`safety_identifier` 最长 64 字符。

### Changed

- Seedance 2.0 内置默认宽高比改为 `adaptive`，与官方创建任务文档一致。
- `--service-tier flex` 会在本地拒绝；本 skill 只覆盖 Seedance 2.0，而 Seedance 2.0 不支持离线/flex 推理。

## 0.3.2 - 2026-05-11

### Added

- 创建命令新增 `--dry-run-payload`、`--run-dir`、`--run-id`，可只构造并保存脱敏 payload，不提交火山 API。
- 所有 create 命令提交前自动写入 `prompt.txt`、`request-payload-redacted.json`、`media-manifest.json`；提交成功后写 `submit-summary.json`，等待完成后写 `task-result.json`。
- `media-manifest.json` 会记录本地素材 sha256、大小、MIME、图片尺寸；若本机安装 `ffprobe`，会额外记录视频/音频时长、编码、FPS、帧数等摘要。
- HTTP(S) 素材 URL 提交前做响应头预检，并把结果写回 manifest。
- 新增 `--serve-local-assets cloudflare`，可把本地视频复制到隔离 run 目录、启动只读 HTTP 服务和 Cloudflare 临时 tunnel，并在命令结束后关闭服务。0.3.6 后该路径只处理本地 `reference_video`。

### Fixed

- 本地 `reference_video` 不再被静默转成 data URL；默认直接提示使用 `--serve-local-assets cloudflare`、HTTPS URL 或 signed URL。
- `edit` 文案降级为 edit-intent，明确当前不是 mask inpaint、区域重绘或强制主体替换。

## 0.3.1 - 2026-05-11

### Fixed

- 对齐火山官方文档：`doubao-seedance-2-0-260128` 允许 `1080p`，`doubao-seedance-2-0-fast-260128` 在 payload 构建阶段拒绝 `1080p`。
- `list --status` 只允许官方 `filter.status` 枚举：`queued` / `running` / `cancelled` / `succeeded` / `failed`。
- 创建命令现在会在省略 CLI 选项时真正使用配置文件默认值；`config set` 会保存布尔/整数类型，不再把 `false` 等值错当字符串。
- 图生视频、首尾帧、参考视频、编辑和延长模式不再强制 `--prompt`，与官方“文本提示词可选”的模式说明一致。
- 本地校验补齐 `duration`、`seed`、列表分页、参考图片/视频/音频数量限制。
- `references/api.md` 的查询任务官方文档链接修正为 `1521309`。

## 0.3.0 - 2026-05-11

### Added

- `scripts/seedance2_video.py` 引入 `setup` / `doctor` / `config (path|list|get|set|unset)` 三个配置入口。
- 6 个顶层模式子命令：`text-to-video` / `first-frame` / `first-last` / `omni` / `edit` / `extend`。原单一 `create` 子命令拆分；调用方按需求选择对应模式。
- 配置文件支持 XDG 风格位置（POSIX `~/.config/seedance2/config.json`、Windows `%APPDATA%\seedance2\config.json`），可由 `SEEDANCE2_CONFIG_DIR` 覆盖；`api_key` 在 `config list` / `config get` / `doctor` 输出中自动脱敏。
- 退出码语义化：`0` 成功，`2` 用法错误，`3` 配置错误，`4` 上游 API 错误，`5` 运行时错误（含超时与任务失败）。

### Changed

- `references/cli.md` 全面重写以匹配 13 个新顶层子命令、首次配置流程和退出码契约。
- 默认输出格式仍为 JSON，所有命令支持 `--format markdown` 切换为人读形态。
- API key 解析顺序固定为 `--api-key` > `ARK_API_KEY` > `SEEDANCE_API_KEY` > 配置文件。

## 0.2.0 - 2026-05-11

### Added

- `references/cli.md`：集中保存 `scripts/seedance2_video.py` 的 CLI 调用模板。
- `scripts/validate_skill.py`：本地自检 frontmatter、加载表、内部链接、payload JSON 和 reference 页头。
- `examples/prompts/first-frame.md` 与 `examples/payloads/first-frame.json`：首帧图生视频示例。
- `examples/prompts/iteration-revision.md` 与 `examples/payloads/iteration-revision.json`：反馈修正示例。
- 所有非索引 reference 文件统一页头：`Load when` / `Avoid` / `Pairs with`。

### Changed

- `SKILL.md` 瘦身为入口与决策路由，不再复述 interaction / router / api / iteration 的细则。
- `references/README.md` 成为 reference 加载表唯一权威。
- `references/methods/storyboard.md` 补齐 Beat Fields、Prompt Pattern、Example 和 Self Check。
- `references/scenes.md` 为每个场景补 `Recommended method`。
- `references/methods/README.md` 为方法索引补 `Primary scenes` 列。
- `references/director.md` 增加按场景裁剪 prompt 字段的矩阵。
- `examples/README.md` 改为按 Input Mode 索引示例。

### Fixed

- `references/router.md` 中不存在的 `scripts/validate_repository.py` 引用改为 `scripts/validate_skill.py`。
- 移除 skill 内部 reference 对宿主仓库 source-of-truth 文档路径的硬引用。

## 0.1.0 - Initial

### Added

- Seedance 2.0 director workflow skill package。
- `scripts/seedance2_video.py` 火山方舟任务创建、查询、轮询和下载入口。
- 初版 references：interaction、router、api、director、scenes、iteration、methods。
- 初版 omnireference prompt 和 payload 示例。
