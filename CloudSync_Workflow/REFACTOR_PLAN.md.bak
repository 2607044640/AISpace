# 🔄 Kiro Sync 脚本重构计划

## 📋 背景

当前脚本 `kiro_sync_to_drive.py` 将所有文件合并成单一大文件（2.66 MB），导致：
1. Gemini 需要加载整个文件才能查看任何内容
2. 无法选择性查看重要文件
3. 文件过大影响加载速度

## 🎯 重构目标

**分类架构**：将项目文件按重要性和功能分类，生成多个小文件供 AI 选择性查看

**文件分类**：
1. **01_ImportantRules.txt** - 核心规则（MainRules.md + DesignPatterns.md）
2. **02_OtherRules.txt** - 其他规则和文档（steering/docs/specs 中的其他文件）
3. **03_A1_Components.txt** - A1 前缀组件（用户自定义）
4. **04_B1_Components.txt** - B1 前缀组件（用户自定义）
5. **05_ProjectCore.txt** - 项目核心文件（Scenes, Tests, 其他）

**存储策略**：
- **Google Drive** (`C:\Users\26070\My Drive\Kiro_Godot_Brain\`): 5 个分类文件 + AI_Context_Changes.md
- **D 盘** (`D:\Kiro_Godot_Brain_Backup\`): AI_Context_Full_YYYYMMDD_HHMMSS.txt (完整合并，用于 diff)

## 📊 当前脚本分析

### 核心函数
1. `build_pure_code_package()` - 主函数，扫描并合并文件
2. `calculate_file_hash()` - 计算 MD5 哈希
3. `should_include_file()` - 文件过滤逻辑
4. `is_in_whitelist_folder()` - 白名单检查
5. `generate_change_report()` - 生成变更报告
6. `append_to_changes_file()` - 追加变更记录

### 关键配置
- `KIRO_WHITELIST_DIRS` = ['steering', 'docs', 'specs']
- `KIRO_WHITELIST_FILES` = ['ProjectRules.md', 'docLastConversationState.md', 'ConversationReset.md']
- `PROJECT_WHITELIST_PREFIXES` = ['A1', 'B1']
- `PROJECT_WHITELIST_DIRS` = ['Scenes', 'Tests']
- `FILE_CATEGORIES` = 已定义但未使用

### 工作流程
1. 扫描 KiroWorkingSpace/.kiro/ (白名单模式)
2. 扫描 3d-practice/ (扩展名过滤 + 大小限制)
3. 合并成单一 TXT 文件
4. 生成 Manifest (JSON)
5. 对比上次 Manifest，生成 Changes (MD)
6. 备份旧文件到 D 盘

## 🔧 重构步骤

### Step 1: 添加文件分类器
```python
def classify_file(file_path, source_path, kiro_path):
    """
    将文件分类到对应的类别
    
    返回: category_name (str) 或 None
    """
    # 检查是否是 ImportantRules
    if file_path in important_rules_list:
        return 'important_rules'
    
    # 检查是否是 OtherRules
    if file_path.startswith(kiro_path):
        return 'other_rules'
    
    # 检查是否是 A1/B1 组件
    rel_path = file_path.relative_to(source_path)
    if any(part.startswith('A1') for part in rel_path.parts):
        return 'a1_components'
    if any(part.startswith('B1') for part in rel_path.parts):
        return 'b1_components'
    
    # 其他归类为 ProjectCore
    return 'project_core'
```

### Step 2: 重写主函数
```python
def build_categorized_packages():
    """
    生成分类文件包
    
    工作流程：
    1. 扫描所有文件，按分类收集
    2. 生成完整文件到 D 盘（用于 diff）
    3. 生成 5 个分类文件到 Google Drive
    4. 生成 Manifest
    5. 对比生成 Changes
    """
    # 初始化分类容器
    categorized_files = {
        'important_rules': [],
        'other_rules': [],
        'a1_components': [],
        'b1_components': [],
        'project_core': []
    }
    
    # 扫描并分类文件
    for file_path in all_files:
        category = classify_file(file_path, source_path, kiro_path)
        if category:
            categorized_files[category].append(file_path)
    
    # 生成完整文件（D 盘，用于 diff）
    full_file_path = generate_full_file(categorized_files, LOCAL_BACKUP_PATH)
    
    # 生成分类文件（Google Drive）
    for category, files in categorized_files.items():
        generate_category_file(category, files, DRIVE_SYNC_PATH)
    
    # 生成 Manifest 和 Changes
    generate_manifest_and_changes(full_file_path)
```

### Step 3: 实现分类文件生成
```python
def generate_category_file(category, files, output_path):
    """
    生成单个分类文件
    
    参数:
        category: 分类名称
        files: 文件列表
        output_path: 输出路径
    """
    config = FILE_CATEGORIES[category]
    filename = config['filename']
    description = config['description']
    
    output_file = output_path / filename
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# {description}\n")
        f.write(f"# 生成时间: {datetime.now()}\n\n")
        
        for file_path in files:
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"📂 FILE: {file_path}\n")
            f.write("=" * 80 + "\n\n")
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as src:
                f.write(src.read())
                f.write('\n\n')
```

### Step 4: 修改变更检测
- 变更检测使用完整文件（D 盘）
- Changes 文件保存到 Google Drive
- Manifest 保存到 D 盘

### Step 5: 清理旧文件
```python
# 清理 Google Drive 中的旧分类文件
for category_config in FILE_CATEGORIES.values():
    old_files = list(drive_path.glob(f"{category_config['filename'].split('.')[0]}_*.txt"))
    for old_file in old_files:
        shutil.move(str(old_file), str(backup_folder / old_file.name))
```

## 🎨 可扩展性设计

### 添加新分类
只需在 `FILE_CATEGORIES` 中添加新条目：
```python
FILE_CATEGORIES = {
    # ... 现有分类 ...
    'new_category': {
        'filename': '06_NewCategory.txt',
        'description': '新分类描述',
        'filter_func': lambda file_path: custom_filter(file_path)
    }
}
```

### 自定义过滤器
```python
def custom_filter(file_path):
    """自定义过滤逻辑"""
    return file_path.suffix == '.custom'
```

## ⚠️ 注意事项

1. **向后兼容**：保留旧的 Manifest 格式，确保变更检测不中断
2. **性能优化**：只读取一次文件，分类时使用引用
3. **错误处理**：每个分类文件生成失败不影响其他分类
4. **测试验证**：
   - 验证所有文件都被正确分类
   - 验证完整文件包含所有内容
   - 验证变更检测正常工作
   - 验证 Hook 自动触发

## 📝 实施清单

- [ ] 备份当前脚本 ✅
- [ ] 实现 `classify_file()` 函数
- [ ] 重写 `build_pure_code_package()` 为 `build_categorized_packages()`
- [ ] 实现 `generate_category_file()` 函数
- [ ] 实现 `generate_full_file()` 函数
- [ ] 修改变更检测逻辑
- [ ] 更新清理逻辑
- [ ] 测试验证
- [ ] 更新文档

## 🚀 下一步行动

**给下一个 AI 的指令**：

1. 阅读此计划文档
2. 阅读当前脚本 `kiro_sync_to_drive.py`（已备份到 D 盘）
3. 执行 `mcp_sequential_thinking_sequentialthinking` 思考 7 次：
   - 分析当前架构
   - 设计分类逻辑
   - 考虑边界情况
   - 规划错误处理
   - 设计测试方案
   - 评估性能影响
   - 确定实施顺序
4. 实施重构
5. 测试验证
6. 更新 MainRules.md 和 DesignPatterns.md 中的相关说明

## 📚 参考资料

- 当前脚本：`C:\Godot\KiroWorkingSpace\.kiro\CloudSync_Workflow\kiro_sync_to_drive.py`
- 备份脚本：`D:\Kiro_Godot_Brain_Backup\kiro_sync_to_drive_backup_*.py`
- 配置文件：脚本开头的配置区
- 测试数据：`D:\Kiro_Godot_Brain_Backup\AI_Context_Manifest.json`
