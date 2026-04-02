# 师门任务素材截图指南

## 需要截取的素材

请在游戏运行状态下截取以下UI元素的截图：

### 1. 师门任务入口
- 位置：游戏主界面右下角
- 描述：写着"师门"或类似字样的按钮
- 保存为：`assets/shimen/shimen_entry.png`

### 2. 师门师父NPC
- 位置：找到师父的位置
- 描述：师门任务对话框中的师父形象
- 保存为：`assets/shimen/shimen_npc.png`

### 3. 师门任务类型
- 位置：师门任务弹窗
- 描述：显示任务类型（驱逐妖怪我、送信、巡逻等）
- 保存为：`assets/shimen/shimen_task_type.png`

### 4. 领取奖励按钮
- 位置：任务完成后的奖励界面
- 描述：领取奖励按钮
- 保存为：`assets/shimen/reward_btn.png`

### 5. 关闭/返回按钮
- 位置：各种弹窗的右上角
- 描述：X按钮或关闭按钮
- 保存为：`assets/shimen/close_btn.png`

## 截图方法

### 方法1：Mac屏幕截图（推荐）
```bash
# 副屏截图
/usr/sbin/screencapture -x -D 2 /tmp/shimen_entry.png
# 然后复制到assets目录
cp /tmp/shimen_entry.png assets/shimen/shimen_entry.png
```

### 方法2：直接从游戏界面截图
在游戏界面按下 `Cmd + Shift + 4` 选择区域截图

## 素材要求
- 格式：PNG
- 尽量只截取目标元素，周围少留空白
- 分辨率：与游戏窗口分辨率一致（不要拉伸）
- 如果有多个类似按钮，截取最常用的那个

## 坐标说明

游戏窗口位置（副屏D2）：
- 偏移量：(1540, 148)
- 游戏区域：326 x 453

游戏内坐标转绝对坐标：
```
绝对X = 1540 + 游戏内X
绝对Y = 148 + 游戏内Y
```