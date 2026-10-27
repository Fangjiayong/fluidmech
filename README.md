# 流体力学工作区

这个工作区把“解题方法”和“可复用计算”分开沉淀：

- **技能**：`.dsh/skills/fluid-mechanics/SKILL.md`
  - 标准解题流程
  - EGL/HGL 画线规则
  - 常见题型、易错点
  - 题 3-19 基准解答
- **计算库**：`fluidmech/`
  - 水头、压强、连续性、Darcy 损失
  - 水库 + 两段水平管求解
  - 7 个水头站点、EGL/HGL 表、中点压强
- **回归测试**：`tests/test_fluidmech.py`
- **原题资料**：`fluid_hw/`
  - 题 3-19 解答图：`fluid_hw/problem-3-19-head-lines.png`
  - 作图脚本：`fluid_hw/draw_heads.py`

## 快速开始

```powershell
python -m fluidmech.examples.problem_3_19
python -m unittest discover -s tests -v
```

## 目录

```text
.
├─ .dsh/skills/fluid-mechanics/
│  ├─ SKILL.md
│  └─ references/
│     ├─ head-line-rules.md
│     ├─ problem-patterns.md
│     └─ worked-example-3-19.md
├─ fluidmech/
│  ├─ core.py
│  ├─ pipe.py
│  ├─ headlines.py
│  ├─ examples/problem_3_19.py
│  └─ README.md
├─ tests/test_fluidmech.py
└─ fluid_hw/
   ├─ problem-3-19-head-lines.png
   └─ draw_heads.py
```

## 使用约定

- 先加载 `fluid-mechanics` 技能，再解题或扩展库。
- 新题型按“公式 → 函数 → 示例 → 回归测试 → 参考笔记”的顺序沉淀。
- 库默认 SI 单位、`g=9.80665`、`rho=1000`；教材题通常显式传 `g=9.8`。
- 详细 API 和路线图见 `fluidmech/README.md`。
