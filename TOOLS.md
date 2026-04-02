# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Mac 多屏幕控制

| 工具 | 限制 | 解决方案 |
|------|------|---------|
| pyautogui | 只能操作主屏幕 | 用 Quartz CGEvent API |
| screencapture -x -D N | N=1/2/3 指定屏幕 | D2=副屏 |

### Quartz CGEvent 点击副屏
```python
import Quartz
event = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventLeftMouseDown, (x, y), 0)
Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
```

### 屏幕截图
```bash
/usr/sbin/screencapture -x -D 2 /tmp/screen.png  # 副屏D2
```

### 当前Mac屏幕布局
- 主屏 (D1): 1512x982
- 副屏 (D2): 在主屏右侧，分辨率2560x1440

---

Add whatever helps you do your job. This is your cheat sheet.
