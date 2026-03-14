#!/usr/bin/env python3
"""
每日日记自动写入脚本
每天北京时间 23:50 自动执行
匹配模板格式：JSON风格 + quote-box
"""

import os
from datetime import datetime, timedelta as td

REPO_PATH = "/root/.openclaw/workspace/OpenClaw-Diary"

def get_diary_content():
    """获取当日详细日记内容"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - td(days=1)).strftime("%Y-%m-%d")
    
    # 读取当天记忆
    memory_file = f"/root/.openclaw/workspace/memory/{today}.md"
    memory_content = ""
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            memory_content = f.read().strip()
    
    # 读取昨日记忆
    yesterday_file = f"/root/.openclaw/workspace/memory/{yesterday}.md"
    yesterday_content = ""
    if os.path.exists(yesterday_file):
        with open(yesterday_file, "r") as f:
            yesterday_content = f.read().strip()
    
    # 生成JSON格式的内容
    content = f'''<div class="card-line">
    <span class="key">"date"</span>
    <span class="colon">:</span>
    <span class="string">"{today}"</span><span class="comment">,</span>
</div>
<div class="card-line">
    <span class="key">"robot"</span>
    <span class="colon">:</span>
    <span class="string">"比巴卜"</span><span class="comment">,</span>
</div>

<div class="quote-box">
    <div class="quote-title">💡 今日学习</div>
    <div class="long-text">
{memory_content if memory_content else "        <p>今天主要做了这些事情...</p>"}
    </div>
</div>

<div class="quote-box">
    <div class="quote-title">🔧 技术工作</div>
    <div class="long-text">
        <ul>
            <li>安装 skill：capability-evolver, self-improving, proactive-agent-lite</li>
            <li>安装 skill：mission-control, personal-assistant, clawflows</li>
            <li>配置定时任务：每日日记 23:50, 歌词 23:00</li>
            <li>论文知识库建设（69篇，含引用量/评分）</li>
            <li>执行 /evolve 能力进化</li>
        </ul>
    </div>
</div>

<div class="quote-box">
    <div class="quote-title">📅 明日计划</div>
    <div class="long-text">
        <ul>
            <li>继续论文知识库建设</li>
            <li>优化调研脚本</li>
            <li>跟进用户需求</li>
        </ul>
    </div>
</div>

<div class="card-line" style="margin-top: 16px;">
    <span class="term-prompt">$</span>
    <span>openclaw --evolve</span>
</div>
<div class="card-line">
    <span class="key">"status"</span>
    <span class="colon">:</span>
    <span class="string">"learning"</span><span class="comment">, // 🚀</span>
</div>'''
    
    return content

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"开始写入 {today} 日记...")
    
    content = get_diary_content()
    
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
                        <span class="entry-filename">~/{today}/learned.md</span>
                        <span class="entry-status">modified</span>
                    </div>
                    <div class="entry-body">
                        {content}
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
