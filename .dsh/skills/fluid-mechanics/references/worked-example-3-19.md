# 基准题：3-19 两段管水头线

## 题目

水库水面高出水平管轴 \(H=4\ \mathrm{m}\)。水平输水管由两段组成：

\[
A_1=0.2\ \mathrm{m^2},\qquad A_2=0.1\ \mathrm{m^2},
\]

出口排入大气。

1. 不计损失：求 \(v_1,v_2\)，画 EGL/HGL，求进口 A 点压强。
2. 计入损失：
   \[
   h_{f1}=4\frac{v_1^2}{2g},\qquad
   h_{f2}=3\frac{v_2^2}{2g},
   \]
   求 \(v_1,v_2\)，画 EGL/HGL，求各段中点压强；不计局部损失。

取 \(g=9.8\ \mathrm{m/s^2}\)，管轴为基准面，压强为表压。

## 基本关系

\[
v_1A_1=v_2A_2
\Rightarrow v_1=\frac{A_2}{A_1}v_2=\frac12v_2.
\]

因此：

\[
\frac{v_1^2}{2g}=\frac14\frac{v_2^2}{2g}.
\]

## （1）不计损失

\[
H=\frac{v_2^2}{2g}
\Rightarrow v_2=\sqrt{2gH}=8.85\ \mathrm{m/s}.
\]

\[
v_1=4.43\ \mathrm{m/s}.
\]

速度水头：

\[
\frac{v_1^2}{2g}=1.00\ \mathrm{m},\qquad
\frac{v_2^2}{2g}=4.00\ \mathrm{m}.
\]

水头线：

- EGL：\(4.00\ \mathrm{m}\) 水平线；
- HGL：第一段 \(3.00\ \mathrm{m}\)，第二段 \(0\)；
- 进口 HGL 从 \(4.00\) 降到 \(3.00\)；
- 收缩处 HGL 从 \(3.00\) 降到 \(0\)。

A 点（管内紧靠进口，速度取 \(v_1\)）：

\[
\frac{p_A}{\rho g}=H-\frac{v_1^2}{2g}=3.00\ \mathrm{m},
\]

\[
p_A=9.8\times3.00=29.4\ \mathrm{kPa}.
\]

## （2）计入损失

\[
H=\frac{v_2^2}{2g}
+4\frac{v_1^2}{2g}
+3\frac{v_2^2}{2g}.
\]

代入 \(v_1^2/(2g)=\frac14v_2^2/(2g)\)：

\[
4=5\frac{v_2^2}{2g}
\Rightarrow \frac{v_2^2}{2g}=0.80\ \mathrm{m}.
\]

\[
v_2=3.96\ \mathrm{m/s},\qquad v_1=1.98\ \mathrm{m/s}.
\]

速度水头：

\[
\frac{v_1^2}{2g}=0.20\ \mathrm{m},\qquad
\frac{v_2^2}{2g}=0.80\ \mathrm{m}.
\]

损失：

\[
h_{f1}=4\times0.20=0.80\ \mathrm{m},\qquad
h_{f2}=3\times0.80=2.40\ \mathrm{m}.
\]

校核：

\[
0.80+0.80+2.40=4.00\ \mathrm{m}.
\]

水头表：

| 位置 | EGL/m | HGL/m |
|---|---:|---:|
| 水库液面 | 4.00 | 4.00 |
| 进口 A | 4.00 | 3.80 |
| 第一段中点 | 3.60 | 3.40 |
| 第一段末 | 3.20 | 3.00 |
| 第二段起点 | 3.20 | 2.40 |
| 第二段中点 | 2.00 | 1.20 |
| 出口 | 0.80 | 0 |

收缩处：

- EGL 连续：\(3.20\to3.20\)；
- HGL 下降：
  \[
  3.00-2.40=0.60\ \mathrm{m}
  =0.80-0.20.
  \]

中点压强：

\[
p_1=9.8\times3.40=33.3\ \mathrm{kPa},
\]

\[
p_2=9.8\times1.20=11.8\ \mathrm{kPa}.
\]

## 画图结论

- 不计损失：EGL 水平；HGL 在每段内水平，进口和收缩处竖直跳变。
- 计入损失：EGL 沿两段分别从 \(4.00\to3.20\to0.80\) 倾斜下降；
  HGL 与 EGL 平行，间距分别为 \(0.20\ \mathrm{m}\) 和 \(0.80\ \mathrm{m}\)。
- 收缩处 EGL 连续，HGL 向下跳 \(0.60\ \mathrm{m}\)，因为速度水头增大，
  且题目不计局部损失。

图见：`fluid_hw/problem-3-19-head-lines.png`。

## 这题沉淀出的通用规则

1. 先连续性把两个速度变成一个未知量。
2. 能量方程中损失项要乘对应的速度水头，不能都乘 \(v_2^2/(2g)\)。
3. EGL 与 HGL 的间距是该段速度水头。
4. 沿程损失画斜线，局部损失画竖线；不计局部损失时收缩处 EGL 连续。
5. 水平管 \(p/\gamma=\mathrm{HGL}\)。
6. 求出速度后先列水头表，再画图，最后读压强，最不容易乱。

## 对应代码

```python
from fluidmech import solve_two_section_pipe, head_stations, midpoint_pressure

case = solve_two_section_pipe(
    area1=0.2, area2=0.1, reservoir_head=4.0,
    loss_coeff1=4.0, loss_coeff2=3.0, g=9.8,
)
for station in head_stations(case):
    print(station.key, station.egl, station.hgl)
print(midpoint_pressure(case, 1), midpoint_pressure(case, 2))
```
