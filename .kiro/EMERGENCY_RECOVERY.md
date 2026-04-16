# 🚨 Kiro 对话丢失紧急恢复指南

## 立即执行（对话刚丢失时）

### 1. 紧急备份当前状态
```bash
cd KiroWorkingSpace
python .kiro/scripts/emergency_backup.py
```

### 2. 查看最近的备份
```bash
ls -lt KiroWorkingSpace/.kiro/chat_backups/
```

### 3. 恢复上次对话状态
```bash
# 找到最新的备份目录，例如 20260417_153000
cd KiroWorkingSpace/.kiro/chat_backups/20260417_153000

# 查看备份的状态文件
cat docLastConversationState.md
```

## 防御机制（已自动启用）

### ✅ Hook: 自动备份对话状态
- **触发**: 每次你发送消息时
- **动作**: 自动更新 `docLastConversationState.md`
- **位置**: `.kiro/hooks/auto-backup-on-prompt.json`

### ✅ 紧急备份脚本
- **位置**: `.kiro/scripts/emergency_backup.py`
- **用法**: 对话丢失后立即运行
- **备份内容**: 所有关键状态文件 + Scratchpad 目录

## 新对话启动清单

当你开启新对话时，**第一句话**应该是：

```
读取以下文件恢复上下文：
1. KiroWorkingSpace/.kiro/docLastConversationState.md
2. KiroWorkingSpace/.kiro/ProjectRules.md
3. KiroWorkingSpace/.kiro/Scratchpad/BackpackTest_BugFix_Guide.md
```

## 关键文件位置速查

| 文件 | 用途 | 路径 |
|------|------|------|
| 对话状态 | 当前任务进度 | `KiroWorkingSpace/.kiro/docLastConversationState.md` |
| 项目规则 | 架构和规范 | `KiroWorkingSpace/.kiro/ProjectRules.md` |
| Bug 修复指南 | 当前 Bug 追踪 | `KiroWorkingSpace/.kiro/Scratchpad/BackpackTest_BugFix_Guide.md` |
| 备份目录 | 历史备份 | `KiroWorkingSpace/.kiro/chat_backups/` |

## 最坏情况恢复

如果所有备份都失效：

1. **检查 Git 历史**
   ```bash
   cd 3d-practice
   git log --oneline -10
   git show HEAD
   ```

2. **检查 Godot 日志**
   ```bash
   cat $env:APPDATA/Godot/app_userdata/Tesseract_Backpack/logs/godot.log
   ```

3. **重建状态文件**
   - 查看最近修改的 C# 文件
   - 查看 Scratchpad 中的其他文档
   - 查看 Git diff

## 预防措施

### 每完成一个功能模块后：
1. ✅ 提交代码到 Git
2. ✅ 更新 `docLastConversationState.md`
3. ✅ 运行紧急备份脚本
4. ✅ 开启新对话

### 对话达到 15 轮时：
1. ✅ 主动总结当前进度
2. ✅ 更新所有 Scratchpad 文档
3. ✅ 提交 Git
4. ✅ 开启新对话

## 当前状态（从上次备份恢复）

根据 `docLastConversationState.md` (2026-04-15)：

- **当前任务**: TscnBuilder 测试与修复
- **已完成**: Bug #1 (NodePath 绑定), Bug #2 (GuiInput 事件)
- **下一步**: 用户在 Godot 编辑器中测试拖拽功能

---

**记住**: Kiro 对话丢失是已知 bug，但通过这套防御机制，你最多损失 1-2 轮对话，而不是整个 session。
