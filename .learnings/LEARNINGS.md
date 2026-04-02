# LEARNINGS.md - 经验总结

> 记录从错误和最佳实践中学到的东西

## 最佳实践 (Best Practices)

### 游戏脚本开发

- **模板匹配优于固定坐标** — 游戏UI元素位置固定，可用模板匹配定位
- **随机延迟防封** — 点击间隔加0.5-2秒随机延迟
- **图像识别用OpenCV** — cv2.matchTemplate 足够精准

### 多屏幕坐标处理

- **pyautogui在macOS上只能操作主屏** — 副屏幕需要用Quartz API
- **Quartz CGEventCreateMouseEvent 需要4个参数** — source, type, point, mouseButton
- **显示器坐标用CGDisplayBounds获取** — 但CGGetActiveDisplayList在Python里调用复杂

### 浏览器控制

- **pyppeteer可用** — 调用系统Chrome执行JS渲染动态页面
- **截图用 screencapture -x -D 2** — D2是副屏幕

## 纠正 (Corrections)

| 日期 | 场景 | 错误 | 纠正 |
|------|------|------|------|
| 2026-04-01 | Mac副屏点击 | 用pyautogui点击副屏幕无效 | 需用Quartz API直接发送CGEvent |

## 知识差距 (Knowledge Gaps)

- [ ] Quartz API在Python里调用方式不熟悉
- [ ] macOS多显示器坐标系理解不完整
- [ ] 梦幻西游手游界面布局需要更系统的分析

## 已安装的Skill

### agent-browser 🟢
- 版本：0.23.4
- 功能：浏览器自动化CLI（导航、点击、截图、表单填写）
- 安装：npm install -g agent-browser
- 用途：网页自动化、游戏网站交互

### skill-vetter 🟢
- 安全审查工具
- 安装任何skill前必做审查

### find-skills 🟢
- 功能：搜索和安装其他skill
- 来源：jimliuxinghai/find-skills
- 状态：GitHub clone失败，内容已手动存档

### daily-ai-news 🟢
- 功能：聚合AI新闻（VentureBeat/TechCrunch/The Verge等）
- 来源：yyh211/claude-meta-skill（1600安装量）
- 安装命令：npx skills add yyh211/claude-meta-skill@daily-ai-news -g -y

## Skill安装安全审查 (skill-vetter)

**安装前必做：**
1. 查来源（GitHub/ClawdHub/官方）
2. 代码审查RED FLAGS：
   - curl/wget到未知URL ❌
   - 发送数据到外部服务器 ❌
   - 请求凭证/token ❌
   - 读取~/.ssh, ~/.aws ❌
   - base64 decode ❌
   - eval/exec ❌
   - 修改系统文件 ❌
   - 混淆代码 ❌
3. 权限范围评估
4. 风险分类：🟢LOW / 🟡MEDIUM / 🔴HIGH / ⛔EXTREME

**高风险skill需要人类批准才能安装。**
