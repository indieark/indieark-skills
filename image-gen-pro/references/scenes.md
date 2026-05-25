# Scene Routes

> Load when: 用户指定具体用途、画面类型、交付物或素材组合，需要选择场景策略。
> Avoid: 用户只问 CLI、API 参数或仓库维护。
> Pairs with: `director.md` 将场景字段转成 prompt；`methods/README.md` 选择方法。

本文件只定义场景入口和字段，不展开完整方法论。完整方法后续放入 `methods/`。

## Scene Matrix

| Scene | Use When | Key Fields | Recommended Method |
| --- | --- | --- | --- |
| Store Art / Key Art | 商店封面、宣传主视觉、key art | 类型、主角/核心物、情绪、logo 留白、平台规格 | product |
| Product / Commercial | 商品图、广告图、卖点展示 | 产品、卖点、材质、场景、光线、背景复杂度 | product |
| Character / Portrait | 角色立绘、头像、人物概念 | 身份、服装、姿态、表情、时代/风格、一致性要求 | consistency |
| Icon / App Asset | 图标、小尺寸 UI 资产 | 轮廓、识别度、背景、透明需求、尺寸 | composition |
| Social / Poster | 社媒图、海报、活动图 | 受众、标题/无字、焦点、构图节奏、平台比例 | composition |
| UI / Game Asset | 道具、技能图、界面素材 | 用途、边界、透明/底色、阅读距离、风格统一 | style |
| Infographic / Educational | 信息图、教学图、field guide、说明图 | 主题、区域、标签、阅读顺序、数据真实性 | infographics |
| Image Edit / Restoration | 改图、换风格、修复、局部调整 | 保留什么、改变什么、mask/输入图、容忍变化 | edit |

## Scene Rules

- 用户指定用途时，以用途为主，不自动改成更宏大的风格。
- 商业和商店素材优先明确留白、主体可读性和裁切风险。
- 角色和商品一致性需求要记录 reference 的用途。
- 小尺寸资产优先轮廓和识别度，不堆细节。
- 编辑任务必须拆成“保留项”和“修改项”。
