# fluidmech

一个无第三方依赖的流体力学计算小库，目标是把教材习题里反复出现的
“连续性 + 伯努利/能量方程 + 水头损失 + EGL/HGL”沉淀成可复用函数，
并用已知答案的回归测试锁住结果。

当前版本：**0.1.0**。Python 3.10+。

## 快速开始

在仓库根目录直接运行，不需要安装：

```python
from fluidmech import solve_two_section_pipe, head_stations, midpoint_pressure

case = solve_two_section_pipe(
    area1=0.2,          # m^2
    area2=0.1,          # m^2
    reservoir_head=4.0, # m
    loss_coeff1=4.0,    # h_f1 / (v1^2/2g)
    loss_coeff2=3.0,    # h_f2 / (v2^2/2g)
    g=9.8,
)

print(case.v1, case.v2)
print(case.hv1, case.hv2)
print(case.hf1, case.hf2)

for station in head_stations(case):
    print(station.key, station.egl, station.hgl)

print(midpoint_pressure(case, 1) / 1000, "kPa")
print(midpoint_pressure(case, 2) / 1000, "kPa")
```

运行完整基准题：

```powershell
python -m fluidmech.examples.problem_3_19
```

输出包括两种工况的速度、速度水头、损失、各站点 EGL/HGL 和中点压强。

## 约定

- 所有输入输出使用 SI：m、m²、m/s、Pa、m³/s；水头用 m 液柱。
- 默认 \(g=9.80665\ \mathrm{m/s^2}\)，\(\rho=1000\ \mathrm{kg/m^3}\)。
  中国教材题通常显式传 `g=9.8`。
- 默认压强为表压；需要绝对压强时自行加大气压。
- 两段管模型以管轴为基准面，管道水平，出口为自由射流。
- 损失系数定义为该段的**总损失水头**除以该段速度水头：
  \[
  K_1=\frac{h_{f1}}{v_1^2/(2g)},\qquad
  K_2=\frac{h_{f2}}{v_2^2/(2g)}.
  \]
  局部损失若需要计入，可折算进 \(K_1,K_2\)，但要在文档中说明。

## 主要 API

### 水头与压强

| 函数 | 作用 |
|---|---|
| `velocity_head(v, g)` | \(v^2/(2g)\) |
| `velocity_from_head(h, g)` | \(\sqrt{2gh}\) |
| `pressure_head(p, rho, g)` | \(p/(\rho g)\) |
| `pressure_from_head(h, rho, g)` | \(\rho g h\) |
| `piezometric_head(z, p, rho, g)` | \(z+p/(\rho g)\)，即 HGL |
| `total_head(z, p, v, rho, g)` | \(z+p/(\rho g)+v^2/(2g)\)，即 EGL |
| `pressure_from_hgl(hgl, z, rho, g)` | \(\rho g(\mathrm{HGL}-z)\) |

### 几何、连续性与损失

| 函数 | 作用 |
|---|---|
| `circular_area(D)` | \(\pi D^2/4\) |
| `diameter_from_area(A)` | \(\sqrt{4A/\pi}\) |
| `flow_rate(A, v)` | \(Q=Av\) |
| `velocity_from_flow(Q, A)` | \(v=Q/A\) |
| `velocity_ratio_from_areas(A1, A2)` | \(v_2/v_1=A_1/A_2\) |
| `darcy_head_loss(f, L, D, v, g)` | \(f(L/D)v^2/(2g)\) |
| `minor_head_loss(zeta, v, g)` | \(\zeta v^2/(2g)\) |
| `hydraulic_gradient(hf, L)` | \(J=h_f/L\) |

### 两段管系统

```python
case = solve_two_section_pipe(area1, area2, reservoir_head,
                              loss_coeff1=0.0, loss_coeff2=0.0, g=9.8)
```

求解方程：

\[
H=\frac{v_2^2}{2g}+K_1\frac{v_1^2}{2g}+K_2\frac{v_2^2}{2g},
\qquad v_1=\frac{A_2}{A_1}v_2.
\]

结果对象 `TwoSectionPipeResult` 提供：

- `v1, v2, hv1, hv2, hf1, hf2, flow_rate`
- `egl_reservoir, egl_contraction, egl_outlet`
- `hgl_inlet, hgl_before_contraction, hgl_after_contraction, hgl_outlet`
- `egl_at(section, fraction)`、`hgl_at(section, fraction)`
- `contraction_hgl_drop`、`head_balance_error`

### 水头站点

`head_stations(case)` 返回 7 个站点：

1. `reservoir`：水库液面
2. `inlet`：进口 A
3. `section1_mid`：第一段中点
4. `section1_end`：第一段末
5. `section2_start`：第二段起点（收缩后）
6. `section2_mid`：第二段中点
7. `outlet`：出口

每个 `HeadStation` 含有 `key, label, section, fraction, egl, hgl,
velocity_head`。`head_table(case)` 可直接得到可打印/可导出的字典列表。

## 题 3-19 基准

\(H=4\ \mathrm{m}\)，\(A_1=0.2\ \mathrm{m^2}\)，
\(A_2=0.1\ \mathrm{m^2}\)，取 \(g=9.8\)。

| 工况 | \(v_1\) | \(v_2\) | \(h_{f1}\) | \(h_{f2}\) |
|---|---:|---:|---:|---:|
| 不计损失 | 4.427 m/s | 8.854 m/s | 0 | 0 |
| 计入损失 | 1.980 m/s | 3.960 m/s | 0.800 m | 2.400 m |

计入损失时：

| 位置 | EGL/m | HGL/m |
|---|---:|---:|
| 水库液面 | 4.000 | 4.000 |
| 进口 A | 4.000 | 3.800 |
| 第一段中点 | 3.600 | 3.400 |
| 第一段末 | 3.200 | 3.000 |
| 第二段起点 | 3.200 | 2.400 |
| 第二段中点 | 2.000 | 1.200 |
| 出口 | 0.800 | 0 |

中点表压：\(p_1=33.32\ \mathrm{kPa}\)，
\(p_2=11.76\ \mathrm{kPa}\)。

## 测试

```powershell
python -m unittest discover -s tests -v
```

测试覆盖：

- 速度水头、圆管面积、Darcy 损失、HGL→压强；
- 题 3-19 无损失/有损失两组速度与损失；
- 7 个水头站点的 EGL/HGL；
- 收缩处 HGL 跌落；
- 水头线线性插值；
- 中点压强；
- 非法输入。

## 设计原则

1. **公式与题型分离**：通用公式进 `core.py`，特定系统进 `pipe.py`。
2. **纯函数优先**：不依赖全局状态，不读文件，方便测试和复用。
3. **单位显式**：函数名和文档写清 SI 单位，不搞隐式换算。
4. **先算水头，再算压强**：HGL 是压强的直接来源。
5. **每个新题型配一个已知答案测试**，避免“看起来对”的公式。

## 路线图

- **0.2**：任意管段串联/并联、Darcy 摩擦系数（Colebrook）、局部损失汇总。
- **0.3**：泵/水轮机能量方程、虹吸、孔口/管嘴出流、测压管。
- **0.4**：通用 EGL/HGL SVG 渲染器（水库、管径变化、泵/轮机）。
- **0.5**：单位与物性模块、更多教材题回归集。
- **1.0**：稳定的 API、完整文档和典型题型覆盖。

新增功能时，按“公式 → 函数 → 示例 → 回归测试 → 参考笔记”的顺序做；
具体解题流程见 `.dsh/skills/fluid-mechanics/SKILL.md`。
