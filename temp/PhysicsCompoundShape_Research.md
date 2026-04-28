# Godot 2D 复合物理形状 (Compound Shapes) 深度研究报告

## 1. 核心问题分析 (The Problem)
在类似《背包乱斗》或《俄罗斯方块》的网格系统中，物品往往呈现 L 形、T 形或带有空洞的不规则多边形。
目前 `ItemPhysicsComponent.cs` 的实现是**直接取物品的最大边界 (Bounding Box) 生成一个巨大的 RectangleShape2D**。
**致命后果：** 物理引擎会认为 L 形物品的空白区域也是“实体”。当多个 L 形物品在物理掉落区挤压时，它们会因为那些看不见的空白碰撞框而互相排斥，永远无法完美贴合或“粘合”在一起。这在 Rapier2D 和 Godot 默认物理引擎中都是灾难性的。

## 2. 业界主流解决方案深度对比 (Deep Research on Methods)

我们在 Godot 2D 物理生态中调研了处理多网格拼接实体（Compound RigidBody2D）的三种主流实现路径：

### 方法一：多碰撞体子节点法 (Multiple CollisionShape2D Nodes) - 【原生推荐】
**原理：** Godot 和 Rapier2D 原生支持将多个 `CollisionShape2D` 挂载在同一个 `RigidBody2D` 下。物理引擎在底层会自动将它们“粘合”拼装成一个刚性整体，同步受力和旋转。
*   **实现方式：** 遍历物品网格形状的 `Vector2I[]`，为每一个格子实例化一个 `CollisionShape2D` (内含格子大小的 `RectangleShape2D`)，调整它们的局部 `Position` 拼出完整形状。
*   **优点：** 
    *   **极度简单可靠 (KISS原则)：** 引擎底层代劳了复杂的质心、惯性张量计算。
    *   **完美支持凹多边形和空洞：** 俄罗斯方块的任意形状都能完美重现。
    *   **物理稳定：** 多个 Convex（凸）形状组合，避免了 Concave（凹）碰撞带来的穿模 Bug。
*   **缺点：** 节点数量增多。如果是极大的网格 (如 100x100) 性能会受影响，但背包物品通常仅为 1~10 个格子，性能损耗微乎其微。

### 方法二：算法生成多边形轮廓 (Procedural CollisionPolygon2D)
**原理：** 编写轮廓追踪算法 (如 Marching Squares 或边界线段合并)，算出所有网格最外圈的顶点集 `Vector2[]`，赋值给一个单一的 `CollisionPolygon2D`。
*   **优点：** 场景树最干净，只有一个碰撞节点。
*   **缺点：** 
    *   **算法极其复杂 (Over-engineering)：** 处理带有内侧空洞（如 O 形）、锐角凹陷的网格时算法极易出错。
    *   **底层物理惩罚：** 凹多边形 (Concave Polygon) 在 Godot 物理底层最终仍会被强行切割 (Decomposition) 为多个凸多边形进行计算。我们花大力气写的算法并没有带来实质性的底层性能优化。

### 方法三：贪心网格合并 (Greedy Meshing)
**原理：** 类似于 Voxel 游戏，通过算法将相邻的 1x1 网格合并成更大的矩形（例如把 4 个格子合并为一个 2x2 的大矩形）。
*   **优点：** 在方法一和方法二之间取得了平衡。
*   **缺点：** 对于背包物品这种格子数很少的情况，完全属于杀鸡用牛刀。

---

## 3. 最终架构决策 (Final Decision)

结合我们的架构最高指令：**<prime_directive> KISS & YAGNI: Keep It Simple. Never invent abstractions that complicate straightforward tasks. </prime_directive>**

**✅ 最终选择：方法一 —— 动态生成多个 CollisionShape2D 子节点 (Compound Convex Shapes)。**

### 为什么现在的单矩形 (Bounding Box) 肯定不行？
因为它用一个包裹全图的大方块欺骗了物理引擎。

### 为什么选择方法一？
1.  **引擎最懂引擎：** Rapier2D 处理多个 Box 组合的性能是极致优化的。这是官方文档中最正统的组合刚体解决方案。
2.  **代码极简：** 不需要写复杂的轮廓寻路算法。只需一个简单的 `foreach` 循环遍历 `_gridShapeComp.CurrentLocalCells`。
3.  **完美贴合：** 每个 1x1 的格子就是一个精确的物理块。L 形物品能完美互相勾连。

## 4. 行动蓝图 (Execution Blueprint for ItemPhysicsComponent.cs)

**改造计划：**
我们需要废弃目前在 `EnablePhysics()` 里修改单个 `%PhysicsCollisionShape` 的逻辑，改为：
1. 预先清空旧的碰撞形状。
2. 遍历 `_gridShapeComp.CurrentLocalCells`（表示物品当前占用的网格相对坐标）。
3. 为每个网格 `Vector2I` 创建一个新的 `CollisionShape2D` 节点，赋予大小为 `CellSize` 的 `RectangleShape2D`。
4. 将它的 `Position` 设置为该网格对应的局部像素中心点。
5. 将这些 `CollisionShape2D` 作为子节点加入到本刚体 (`this`) 中。

这样，Rapier2D 就会自动把这些散装的方块“粘接”成一个无懈可击的不规则刚体！
