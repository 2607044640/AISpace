#!/usr/bin/env python3
"""
紧急备份脚本 - 当 Kiro 对话丢失时手动运行
用法: python emergency_backup.py
"""
import os
import shutil
from datetime import datetime
from pathlib import Path

def emergency_backup():
    """创建所有关键文件的紧急备份"""
    
    # 定义关键文件
    critical_files = [
        "KiroWorkingSpace/.kiro/docLastConversationState.md",
        "KiroWorkingSpace/.kiro/ProjectRules.md",
        "KiroWorkingSpace/.kiro/Scratchpad/BackpackTest_BugFix_Guide.md",
        "KiroWorkingSpace/.kiro/Scratchpad/GuiInput_Bug_Fix_Summary.md",
    ]
    
    # 创建备份目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(f"KiroWorkingSpace/.kiro/chat_backups/{timestamp}_emergency")
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🚨 紧急备份开始: {backup_dir}")
    
    backed_up = 0
    for file_path in critical_files:
        src = Path(file_path)
        if src.exists():
            # 保持相对路径结构
            rel_path = src.relative_to("KiroWorkingSpace/.kiro")
            dst = backup_dir / rel_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✅ 已备份: {src.name}")
            backed_up += 1
        else:
            print(f"⚠️  文件不存在: {src}")
    
    # 备份整个 Scratchpad 目录
    scratchpad_src = Path("KiroWorkingSpace/.kiro/Scratchpad")
    scratchpad_dst = backup_dir / "Scratchpad"
    if scratchpad_src.exists():
        shutil.copytree(scratchpad_src, scratchpad_dst, dirs_exist_ok=True)
        print(f"✅ 已备份整个 Scratchpad 目录")
    
    print(f"\n✅ 紧急备份完成！共备份 {backed_up} 个关键文件")
    print(f"📁 备份位置: {backup_dir.absolute()}")
    
    return backup_dir

if __name__ == "__main__":
    emergency_backup()
