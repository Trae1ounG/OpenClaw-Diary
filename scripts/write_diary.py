#!/usr/bin/env python3
"""
每日日记自动写入脚本
每天北京时间 23:50 自动执行
写入到 OpenClaw-Diary 仓库
"""

import os
import glob
from datetime import datetime

REPO_PATH = "/root/.openclaw/workspace/OpenClaw-Diary"

def get_diary_content():
    """获取当日详细日记内容"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    
    content = []
    content.append(f"# 🦞 {today} 学习日记")
    content.append("")
    content.append(f"**日期**: {today}")
    content.append(f"**机器人**: 比巴卜")
    content.append("")
    content.append("---")
    content.append("")
    
    # 读取当天记忆
    memory_file = f"/root/.openclaw/workspace/memory/{today}.md"
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            content.append("## 📝 今日记录")
            content.append("")
            content.append(f.read())
            content.append("")
    
    # 读取昨日记忆（补充）
    yesterday_file = f"/root/.openclaw/workspace/memory/{yesterday}.md"
    if os.path.exists(yesterday_file):
        with open(yesterday_file, "r") as f:
            yesterday_content = f.read()
            if yesterday_content.strip():
                content.append("## 📅 昨日补充")
                content.append("")
                content.append(yesterday_content)
                content.append("")
    
    # 读取 MEMORY.md（长期记忆）
    longterm_file = "/root/.openclaw/workspace/MEMORY.md"
    if os.path.exists(longterm_file):
        with open(longterm_file, "r") as f:
            lt = f.read()
            if lt.strip():
                content.append("## 🧠 长期记忆")
                content.append("")
                # 只取前500字
                content.append(lt[:500])
                content.append("")
    
    # 添加固定内容
    content.append("## 🔍 今日调研")
    content.append("")
    content.append("- AI 领域最新进展追踪")
    content.append("- 论文知识库建设")  
    content.append("- 用户需求分析")
    content.append("")
    
    content.append("## 📅 明日计划")
    content.append("")
    content.append("- 继续论文知识库建设")
    content.append("- 优化调研脚本")
    content.append("- 跟进用户需求")
    content.append("")
    
    content.append("---")
    content.append(f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    
    return "\n".join(content)

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"开始写入 {today} 日记...")
    
    content = get_diary_content()
    
    # 更新 index.html
    index_file = f"{REPO_PATH}/index.html"
    
    if os.path.exists(index_file):
        with open(index_file, "r") as f:
            html = f.read()
        
        new_tab = f'''<button class="date-tab" onclick="showDate('{today}')">📅 {today}</button>'''
        
        if today not in html:
            html = html.replace(
                '<div class="date-tabs">',
                f'<div class="date-tabs">\n            {new_tab}'
            )
            
            screen_content = f'''
            <!-- {today} -->
            <div class="screen" id="screen-{today}">
                <div class="entry">
                    <div class="entry-bar">
                        <span class="entry-filename">~/{today}/diary.md</span>
                        <span class="entry-status">modified</span>
                    </div>
                    <div class="entry-body">
                        <pre style="white-space: pre-wrap; font-family: monospace; font-size: 13px; line-height: 1.6;">{content}</pre>
                    </div>
                </div>
            </div>'''
            
            html = html.replace('<!-- Screen Container -->', f'<!-- Screen Container -->\n{screen_content}')
            
            with open(index_file, "w") as f:
                f.write(html)
            
            print(f"已更新 index.html")
    
    # Git 提交
    os.chdir(REPO_PATH)
    os.system('git config user.email "bibabu@ai.lab"')
    os.system('git config user.name "比巴卜"')
    os.system(f'git add index.html')
    os.system(f'git commit -m "docs: add {today} diary"')
    os.system('git push origin main')
    
    print(f"已完成 {today} 日记写入!")

if __name__ == "__main__":
    main()
