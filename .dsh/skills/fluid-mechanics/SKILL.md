---
name: fluid-mechanics
description: 求解稳态不可压缩流体问题：连续性、伯努利/能量方程、管道沿程与局部损失、EGL/HGL 水头线、断面压强；并维护、扩展 fluidmech Python 计算库。
whenToUse: 当题目涉及水库、管道、虹吸、孔口、泵/水轮机、水头线、压强分布，或需要给 fluidmech 库新增公式、示例和回归测试时使用。
---

# 流体力学解题技能

## 目标

把每个流体力学题都按同一套流程做完，并把可复用的部分沉淀到
`fluidmech/`，而不是只给一次性的数字答案。

适用边界：稳态、不可压缩、单相、以水为主的管流/孔口/水库问题。
可压缩流、明渠、边界层、势流等暂不在 V0 范围内；遇到时先说明适用条件，
不要硬套伯努利方程。

## 标准解题流程

1. **画简图并定基准面。** 标出水库液面、管道进口、收缩/放大、出口、
   泵/水轮机、测压管等位置。通常取管轴或出口中心线为 \(z=0\)。
2. **选两个断面。** 最常用：水库自由液面（\(v\approx0,p=0\)）到出口
   （自由射流，\(p=0\)）。中间断面用于求压强。
3. **写连续性方程。** 先统一用面积，不要用直径：
   \[
   Q=v_1A_1=v_2A_2,\qquad \frac{v_1}{v_2}=\frac{A_2}{A_1}.
   \]
   面积比 \(2:1\) 对应速度比 \(1:2\)，不是 \(1:\sqrt2\)。
4. **写能量方程。** 从上游到下游：
   \[
   z_1+\frac{p_1}{\rho g}+\frac{v_1^2}{2g}
   =
   z_2+\frac{p_2}{\rho g}+\frac{v_2^2}{2g}
   +h_f+h_j-h_{\text{泵}}+h_{\text{轮机}}.
   \]
   先判断哪些项为零，再代数求解。
5. **先求速度，再求水头。** 速度水头 \(v^2/(2g)\) 是连接 EGL 与 HGL 的桥。
6. **列水头表。** 至少包括：水库液面、进口、第一段中点、第一段末、
   第二段起点、第二段中点、出口。每行写 EGL、HGL、速度水头。
7. **按水头表画图。** EGL 与 HGL 的竖直间距就是 \(v^2/(2g)\)。
8. **由 HGL 求压强。** 对水平管 \(z=0\)：
   \[
   \frac{p}{\rho g}=\mathrm{HGL},\qquad p=\rho g\,\mathrm{HGL}.
   \]
   非水平管必须减去位置水头：\(p/\rho g=\mathrm{HGL}-z\)。
9. **校核。** 检查总水头预算：
   \[
   H=h_{v2}+h_{f1}+h_{f2}
   \]
   （有泵/轮机时加上或减去相应水头），并检查 HGL 不低于汽化压力
   （虹吸、泵进口等）。

## 水头线铁律

- **水库内**：\(v=0,\ p=0\)，所以 EGL = HGL = 自由液面高度。
- **等直径管、无损失**：EGL 水平；HGL 也水平，且比 EGL 低 \(v^2/(2g)\)。
- **等直径管、有沿程损失**：EGL 沿流向直线下降，坡度
  \(J=h_f/L\)；HGL 与 EGL 平行，因为同一段管内 \(v^2/(2g)\) 不变。
- **收缩/放大、不计局部损失**：EGL 连续；HGL 竖直突变
  \(\Delta h_v\)。收缩时 HGL 向下跳，放大时向上跳。
- **局部损失**：EGL 在局部位置竖直下降 \(h_j\)；HGL 同时受 \(h_j\)
  和速度水头变化影响。
- **出口到大气**：\(p=0\)，所以 HGL \(=z_{\text{出口}}\)，
  EGL \(=z_{\text{出口}}+v_{\text{出口}}^2/(2g)\)。
- **沿程损失画斜线，局部损失画竖线。** 题目说“不计局部损失”时，
  收缩处 EGL 不能画竖直下降。

## 常见坑

1. 把 HGL 当成总能量。HGL 不含速度水头。
2. 等直径管有沿程损失时，把 HGL 画成水平。
3. 收缩处把 EGL 也画成竖直下降，但题目明确不计局部损失。
4. 用直径比代替面积比做连续性。
5. 出口射流额外加“出口损失”，导致速度水头算重。
6. 表压/绝对压强混用。除特别说明，作业一般采用表压。
7. 虹吸最高点只算能量方程，忘记检查负压/汽化。
8. 题目未给管长时，硬画两段斜率相等。应说明“横向长度未按比例；
   严格斜率为 \(h_f/L\)”。

## 推荐输出格式

作业答案按以下顺序写：

1. 取基准面、取断面、取 \(g\) 和 \(\rho\)；
2. 连续性方程；
3. 能量方程及损失项；
4. 速度、速度水头、损失；
5. 水头表；
6. EGL/HGL 图；
7. 压强结果；
8. 必要时加一句校核或适用条件。

图要能直接看出：水库液面、\(H\)、两段面积、\(v_1,v_2\)、EGL/HGL、
收缩处 HGL 的竖直跌落、出口 HGL=0。

## 计算库

工作区已有 `fluidmech/`，V0 覆盖：

- `velocity_head`, `velocity_from_head`
- `circular_area`, `diameter_from_area`, `flow_rate`,
  `velocity_from_flow`, `velocity_ratio_from_areas`
- `pressure_head`, `pressure_from_head`, `piezometric_head`,
  `total_head`, `pressure_from_hgl`
- `darcy_head_loss`, `minor_head_loss`, `hydraulic_gradient`
- `solve_two_section_pipe`：水库 + 两段水平管 + 出口大气
- `head_stations`, `head_table`, `station_map`,
  `midpoint_pressure`

两段管损失系数的定义：

\[
K_1=\frac{h_{f1}}{v_1^2/(2g)},\qquad
K_2=\frac{h_{f2}}{v_2^2/(2g)}.
\]

示例：

```python
from fluidmech import solve_two_section_pipe, head_stations, midpoint_pressure

case = solve_two_section_pipe(
    area1=0.2, area2=0.1, reservoir_head=4.0,
    loss_coeff1=4.0, loss_coeff2=3.0, g=9.8,
)
print(case.v1, case.v2, case.hf1, case.hf2)
for s in head_stations(case):
    print(s.key, s.egl, s.hgl)
print(midpoint_pressure(case, 1) / 1000, "kPa")
```

约定：库默认 \(g=9.80665\)、\(\rho=1000\ \mathrm{kg/m^3}\)；
中国教材题通常要显式传 `g=9.8`。

## 扩展库的规则

新增一类题时，按“公式 → 函数 → 示例 → 回归测试 → 参考笔记”的顺序做：

1. 在 `fluidmech/` 新增纯函数或 dataclass，保持 SI 单位；
2. 在 `fluidmech/examples/` 加一个可运行例子；
3. 在 `tests/` 加已知答案的回归测试；
4. 在本 skill 的 `references/` 记下题型、假设和易错点；
5. 跑 `python -m unittest discover -s tests -v`。

不要把某一道题的硬编码数字写进通用函数。

## 按需读取

- 水头线细则、表格模板：`references/head-line-rules.md`
- 常见题型与公式选择：`references/problem-patterns.md`
- 题 3-19 完整基准：`references/worked-example-3-19.md`
- 可运行代码：`fluidmech/examples/problem_3_19.py`

## 当前版本

`fluidmech 0.1.0`：核心水头关系 + 两段管 + 水头站点 + 题 3-19 回归测试。
后续路线见 `fluidmech/README.md`。
