# ERRORS.md - 错误记录

> 记录命令失败、异常情况

## 命令/操作失败

| 日期 | 命令/操作 | 错误 | 解决方案 |
|------|-----------|------|---------|
| 2026-04-01 | pyautogui.click (macOS副屏) | 只能在主屏操作 | 用Quartz CGEvent API |
| 2026-04-01 | CGGetActiveDisplayList (Python) | 返回tuple结构，count取法错误 | 需理解返回值的嵌套结构 |
| 2026-04-01 | CGDisplayMoveCursorTo | AttributeError | 函数名或参数不对 |
| 2026-04-01 | CGEventCreateMouseEvent | TypeError: Need 4 arguments | 需传4个参数(source,type,point,button) |

## 工具失败

| 日期 | 工具 | 失败原因 | 备选方案 |
|------|------|---------|---------|
| 2026-04-01 | Homebrew install cliclick | ruby进程被占用 | 杀进程/等一会重试 |
| 2026-04-01 | web_search DuckDuckGo | 国外网站超时 | 换代理/Bing |
| 2026-04-01 | Git clone GitHub | 超时 | 用代理+curl |

## 外部API/集成失败

| 日期 | API/服务 | 问题 | 处理 |
|------|---------|------|------|
| 2026-04-01 | artale.app | Cloudflare拦截 | 用pyppeteer绕过 |
| 2026-04-01 | Google Sheets导出 | 部分sheet访问受限 | 逐个尝试gid |
