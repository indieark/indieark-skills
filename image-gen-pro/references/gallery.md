# Gallery Atlas Index

> Load when: 需要从已抽取的 GPT Image 2 prompt atlas 中选择参考类别、案例或 prompt pattern。
> Avoid: 用户只要求 CLI/API 参数、仓库维护，或已给出最终 prompt 且不需要参考。
> Pairs with: `methods/README.md` 做方法选择；`director.md` 将 gallery pattern 改写成当前任务 prompt。

本文件是 prompt gallery 的运行时路由入口。31 个来源 atlas category 已迁入 `gallery/`，但上游预览图片和逐条长 prompt 不迁；不要把全部内容堆在本文件或根 README。

## Loading Policy

- 先从本文件选一个最接近的 category。
- 普通任务只读 1 个 category 文件。
- 混合任务最多读 2-3 个 category 文件。
- 找不到匹配时读 `methods/README.md` 和 `director.md`，不要盲目加载全部 gallery。
- 迁移条目时保留 `Curated` 或外部 source attribution。

## Category Catalog

本表是 gallery category 的 SSOT。新增 / 改名 / 调整 source count 都只在这里改一次，`gallery/README.md` 不再重复列出。

| Category | File | Use First For | Source Count |
| --- | --- | --- | ---: |
| Anime & Manga | `gallery/anime-and-manga.md` | 动画、漫画、轻小说、赛璐璐角色 | 12 |
| Gaming | `gallery/gaming.md` | 游戏 key art、道具、技能图标、游戏场景 | 10 |
| Retro & Cyberpunk | `gallery/retro-and-cyberpunk.md` | 复古未来、霓虹、赛博朋克 | 3 |
| Cinematic & Animation | `gallery/cinematic-and-animation.md` | 电影感、动画剧照、故事瞬间 | 5 |
| Character Design | `gallery/character-design.md` | 角色设定、立绘、头像、服装道具 | 2 |
| Typography & Posters | `gallery/typography-and-posters.md` | 海报、封面、标题、文字安全区 | 13 |
| Illustration | `gallery/illustration.md` | 编辑插画、故事插画、概念插画 | 2 |
| Watercolor | `gallery/watercolor.md` | 水彩、手账、植物、旅行速写 | 2 |
| Ink & Chinese | `gallery/ink-and-chinese.md` | 水墨、山水、笔墨、东方留白 | 2 |
| Pixel Art | `gallery/pixel-art.md` | 像素角色、道具、tile、复古游戏 | 2 |
| Isometric | `gallery/isometric.md` | 等距房间、系统图、模块空间 | 2 |
| Product & Food | `gallery/product-and-food.md` | 商品、包装、食物、商业静物 | 4 |
| Brand Systems & Identity | `gallery/brand-systems-and-identity.md` | 品牌系统、包装系统、mood board | 3 |
| Photography | `gallery/photography.md` | 真实摄影、棚拍、生活方式照片 | 4 |
| Infographics & Field Guides | `gallery/infographics-and-field-guides.md` | 信息图、教学图、field guide、流程说明 | 8 |
| Research Paper Figures | `gallery/research-paper-figures.md` | 论文图、流程图、实验示意 | 21 |
| Official Cookbook Examples | `gallery/official-cookbook-examples.md` | 最小生成/编辑参考案例 | 4 |
| Data Visualization | `gallery/data-visualization.md` | 图表 mockup、数据海报、dashboard chart | 5 |
| Technical Illustration | `gallery/technical-illustration.md` | 机械、硬件、剖面、说明图 | 5 |
| Architecture & Interior | `gallery/architecture-and-interior.md` | 建筑、室内、空间概念 | 5 |
| Scientific & Educational | `gallery/scientific-and-educational.md` | 科普、教育、科学插图 | 7 |
| Fashion Editorial | `gallery/fashion-editorial.md` | 时尚大片、lookbook、服装造型 | 7 |
| Fine Art Painting | `gallery/fine-art-painting.md` | 油画、静物、古典绘画感 | 5 |
| More Illustration Styles | `gallery/more-illustration-styles.md` | 剪纸、黏土、矢量、儿童插画等媒介 | 6 |
| Cinematic Film References | `gallery/cinematic-film-references.md` | 类型片镜头、分镜、灯光方向 | 6 |
| Beauty & Lifestyle | `gallery/beauty-and-lifestyle.md` | 美妆、护肤、生活方式 | 2 |
| Events & Experience | `gallery/events-and-experience.md` | 活动视觉、展览空间、体验设计 | 2 |
| Tattoo Design | `gallery/tattoo-design.md` | 纹身图案、线稿、黑灰、几何 | 4 |
| Screen Photography | `gallery/screen-photography.md` | 设备屏幕、app-on-device、软件展示 | 2 |
| UI/UX Mockups | `gallery/ui-ux-mockups.md` | App、dashboard、网页、编辑器、设计系统 | 5 |
| Edit Endpoint Showcase | `gallery/edit-endpoint-showcase.md` | 换背景、局部编辑、保留主体、风格改写 | 2 |

## Migration Rule

先迁 prompt、metadata、recommended size/quality 和 attribution；图片预览资产后置。每个 category 文件应只包含该类 prompt，不混入 API 调用实现。
