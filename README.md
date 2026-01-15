# 2026 米兰冬奥会数据可视化 Dashboard

一个基于 Streamlit 的交互式可视化页面，围绕冬奥会历史奖牌数据和 2026 米兰冬奥会中国队前瞻，呈现多维度的可视化分析，包括奖牌分布、国家表现趋势、项目演变以及中国队重点项目与核心选手预测。

---

## 一、项目简介

本项目使用公开的冬奥会奖牌数据和自定义的中国队预测数据，构建了一个视觉效果精致、交互性强的 Web Dashboard，帮助用户：

- 按年份和国家探索冬奥会奖牌分布
- 对比强国在历届冬奥会中的成绩变化
- 理解冬奥会项目在过去百年中的演变
- 直观查看 2026 米兰冬奥会中国队重点项目与核心选手的“预测成绩”

应用基于 `Streamlit` 开发，运行后在浏览器中访问本地 `localhost` 即可查看。

---

## 二、主要功能

- **年份与国家筛选**
  - 通过侧边栏选择某一冬奥会年份
  - 可选择“全部国家”或某一具体国家进行深入分析

- **奖牌分布 Treemap（中间主视图）**
  - 以矩形树图展示奖牌分布层级：
    - 视角一（全部国家）：大项 → 国家 → 奖牌颜色 → 小项/运动员
    - 视角二（指定国家）：大项 → 奖牌颜色 → 小项/运动员
  - 通过颜色深浅与面积体现奖牌数量与含金量（Gold / Silver / Bronze）

<img width="2728" height="1424" alt="image" src="https://github.com/user-attachments/assets/457e7f73-deba-4701-b065-6198df149aee" />


- **国家历史表现趋势折线图**
  - 若选择“全部国家”：自动找出当前年份奖牌得分最高的国家，展示其历届得分变化
  - 若选择具体国家：展示该国在历届冬奥会中的积分趋势

<img width="2772" height="1416" alt="image" src="https://github.com/user-attachments/assets/cd766662-e285-4190-9079-4ab16614499a" />



- **当届前五表现国家柱状图（右侧）**
  - 展示所选年份中得分最高的前五个国家
  - 水平条形图突出对比，配合柔和金色配色

- **冬奥项目百年变迁（ECharts Tree）**
  - 使用树图展示：冬奥会 → 具体大项（discipline）→ 各个小项（event）
  - 每个项目节点包含：
    - 启用年份与停办年份
    - 当前是否仍在举办（Active / Discontinued）
    - 最近新增项目使用特殊颜色高亮
  - 帮助理解从少量“生存技能型项目”发展至现代多元化的观赏性项目的过程

<img width="2756" height="1428" alt="image" src="https://github.com/user-attachments/assets/8e02282b-34f3-4c6d-92ce-4a21a60888a8" />


<img width="475" height="290" alt="image" src="https://github.com/user-attachments/assets/e0f79baa-2393-48c7-9843-d544150a137a" />

<img width="518" height="214" alt="image" src="https://github.com/user-attachments/assets/daa0bdac-05bb-4cf3-842c-30c429d2dc65" />

- **中国队米兰 2026 前瞻（Sunburst + 卡片）**
  - 使用旭日图展示中国队重点项目及对应运动员：
    - 外层：运动员
    - 内层：项目（如自由式滑雪、单板滑雪、短道速滑等）
  - 右侧卡片区域：
    - 显示当前选中项目的总“预测奖牌数”
    - 为每位核心运动员展示头像（如有）、介绍文案与个人预测奖牌
  - 支持通过点击旭日图不同扇区切换关注项目/运动员

<img width="2762" height="1416" alt="image" src="https://github.com/user-attachments/assets/bd5e4ddb-4ab2-47a7-b2ce-7b74cc18e76f" />

<img width="2764" height="1362" alt="image" src="https://github.com/user-attachments/assets/836ef0a6-8fcf-4695-8f2a-79f3932f34ef" />

- **整体视觉与动效**
  - 自定义 CSS 实现渐变背景、玻璃拟态卡片和动态雪花效果
  - 使用多种字体与细节动画营造冬奥主题氛围

<img width="2774" height="1400" alt="image" src="https://github.com/user-attachments/assets/ab224223-eb47-4f32-a88d-6c74453061d2" />

---

## 三、文件结构

- `app.py`  
  核心 Streamlit 应用脚本，包含页面布局、样式定义和全部可视化逻辑。

- `data.csv`  
  冬奥会历史奖牌数据文件，包含年份、国家/地区代码、中英文项目名、奖牌类型等字段。

- `china_data.csv`  
  2026 米兰冬奥会中国队预测数据，包含：
  - `sport`：项目名称（如“自由式滑雪”）
  - `icon`：项目图标
  - `athlete`：运动员姓名
  - `medals`：预测奖牌数
  - `desc`：运动员简介/观点
  - `img`：对应头像图片路径（可关联到 `image/` 文件夹）

- `image/`  
  中国队运动员等图片资源，用于右侧卡片展示。

- `requirements.txt`  
  Python 依赖列表。

- `提示.txt`  
  简要运行提示（中文）。

---
