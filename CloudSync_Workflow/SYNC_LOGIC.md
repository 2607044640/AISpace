# ☁️ Kiro & Gemini 云端自动同步架构

## 核心逻辑

Gemini 的自定义 Gem 不支持自动解析 `.gitignore`，也不支持直接拉取 GitHub 活体代码。但它支持 **Google Drive 文件夹的热更新**。

**重要：Gemini 无法读取 ZIP 文件！** 我们使用文件夹镜像同步，让 AI 直接索引每个代码文件。

## 对接步骤 (如何让 AI 自动看到最新代码)

**第一步：准备"管道" (一次性配置)**

1. 在电脑上下载并安装 [Google Drive 客户端](https://www.google.com/drive/download/)。
2. 在你的 Google Drive 网页端新建一个文件夹，例如命名为 `Kiro_Godot_Brain`。
3. 确保该文件夹在你的本地电脑上有一个映射路径 (例如 `G:\My Drive\Kiro_Godot_Brain`)。

**第二步：连接"直饮机" (一次性配置)**

1. 打开浏览器进入 Google Gemini，编辑你的自定义 Gem (Godot Sensei)。
2. 在 Knowledge 区域，选择 **"+" -> Add from Google Drive**。
3. **关键：选中整个 `Kiro_Godot_Brain` 文件夹**（不是单个文件！）。
4. 点击 Update 保存 Gem。

**第三步：日常"开启净水器" (高频操作)**

1. 修改了项目代码后，只需运行配套的脚本 `kiro_sync_to_drive.py`。
2. 脚本会自动过滤掉美术素材、音频和编译缓存，提取纯粹的 `.cs`, `.tscn`, `.md` 等文件。
3. 脚本将纯净代码以**原始文件夹结构**直接复制到 `G:\My Drive\Kiro_Godot_Brain` 中。
4. Google Drive 会在后台静默上传。
5. **完成！** 下次向 AI 提问时，它已经拥有了你最新的代码库，无需任何网页端操作！

## 工作原理

```
本地项目 (C:\Godot\3d-practice)
    ↓ [过滤噪音文件]
    ↓ [保持目录结构]
    ↓ [复制纯代码]
Google Drive 文件夹 (G:\My Drive\Kiro_Godot_Brain)
    ↓ [自动同步]
    ↓ [AI 自动索引]
Gemini 知识库 (实时更新)
```

## 快速使用

### Windows 用户
双击运行 `SYNC_TO_GEMINI.bat` 即可完成同步。

### 手动运行
```bash
python AISpace/.kiro/CloudSync_Workflow/kiro_sync_to_drive.py
```

## 配置说明

首次使用前，请编辑 `kiro_sync_to_drive.py` 中的配置变量：

```python
SOURCE_PROJECT_DIR = r"C:\Godot\3d-practice"  # 你的项目路径
DRIVE_SYNC_PATH = r"G:\My Drive\Kiro_Godot_Brain"  # 你的 Drive 路径
CLEAN_BEFORE_SYNC = True  # 是否清空旧文件（推荐开启）
```

## 同步内容

脚本会扫描 `3d-practice` 项目，以文件夹镜像方式同步到 Google Drive。

自动过滤：
- 二进制文件 (.png, .jpg, .glb, .dll 等)
- 编译缓存 (.godot, bin, obj 等)
- 版本控制文件 (.git)

只同步纯代码：
- C# 脚本 (.cs)
- GDScript (.gd)
- Godot 场景 (.tscn, .tres)
- 文档 (.md)
- 配置文件 (.json, .cfg, .xml, .csproj, .sln)
