"""
点击控制器 - 整合设备操作与防封
支持速度模式切换和固定坐标点击
"""

from core.antiban import AntiBan
from core.coordinate_manager import CoordinateManager


class ClickController:
    """点击控制：坐标点击 + 随机偏移 + 防封延迟"""

    def __init__(self, device_manager, speed_mode="normal"):
        self.dm = device_manager
        self.antiban = AntiBan(speed_mode=speed_mode)
        self.coord_mgr = CoordinateManager(mode="adb")  # 默认ADB模式

    def set_speed_mode(self, mode):
        """切换速度模式: normal / fast / turbo"""
        self.antiban.set_speed_mode(mode)

    def set_coord_mode(self, mode):
        """切换坐标模式: adb / mac"""
        self.coord_mgr.mode = mode

    def set_game_window(self, offset_x, offset_y, width, height):
        """设置游戏窗口位置(Mac模式用)"""
        self.coord_mgr.set_game_window(offset_x, offset_y, width, height)

    def tap(self, device_index, x, y, use_offset=True):
        """带随机偏移的点击"""
        if use_offset:
            x, y = self.antiban.random_click_offset(x, y)
        self.dm.tap(device_index, x, y)
        self.antiban.click_delay()

    def tap_game(self, device_index, game_x, game_y, use_offset=True):
        """点击游戏窗口内的相对坐标"""
        abs_x, abs_y = self.coord_mgr.game_to_absolute(game_x, game_y)
        self.tap(device_index, abs_x, abs_y, use_offset)

    def tap_fixed(self, device_index, x, y):
        """固定坐标点击（无偏移，用于精准点击）"""
        self.dm.tap(device_index, x, y)
        self.antiban.click_delay()

    def tap_image(self, screen_capture, device_index, template_path, offset=(0, 0)):
        """在截图中找到图像后点击"""
        img = screen_capture.capture(device_index)
        found, center = screen_capture.find_image(img, template_path)
        if found:
            x = center[0] + offset[0]
            y = center[1] + offset[1]
            return self.tap(device_index, x, y)
        return False

    def swipe(self, device_index, x1, y1, x2, y2, duration=None):
        """滑动，duration为空时随机"""
        x1, y1, x2, y2 = self.antiban.random_swipe_offset(x1, y1, x2, y2)
        self.dm.swipe(device_index, x1, y1, x2, y2, duration)
        self.antiban.click_delay()

    def swipe_game(self, device_index, gx1, gy1, gx2, gy2, duration=None):
        """游戏窗口内滑动"""
        ax1, ay1 = self.coord_mgr.game_to_absolute(gx1, gy1)
        ax2, ay2 = self.coord_mgr.game_to_absolute(gx2, gy2)
        self.swipe(device_index, ax1, ay1, ax2, ay2, duration)

    def back(self, device_index):
        """返回键"""
        self.dm.press_back(device_index)
        self.antiban.click_delay()

    def home(self, device_index):
        """Home键"""
        self.dm.press_home(device_index)
        self.antiban.click_delay()

    def wait_and_tap_image(self, screen_capture, device_index, template_path,
                           timeout=30, offset=(0, 0)):
        """等待图像出现后点击"""
        found, center, elapsed = screen_capture.wait_for_image(
            device_index, template_path, timeout=timeout
        )
        if found:
            x = center[0] + offset[0]
            y = center[1] + offset[1]
            self.tap(device_index, x, y)
            return True
        return False

    def multi_tap(self, device_index, coords_list):
        """依次点击多个坐标"""
        for x, y in coords_list:
            self.tap(device_index, x, y)
            self.antiban.action_gap()

    def multi_tap_game(self, device_index, game_coords_list):
        """依次点击多个游戏窗口内坐标"""
        for gx, gy in game_coords_list:
            self.tap_game(device_index, gx, gy)
            self.antiban.action_gap()

    def status(self):
        """返回当前状态"""
        return {
            "speed_mode": self.antiban.speed_mode,
            "coord_mode": self.coord_mgr.mode,
            "window_info": self.coord_mgr.get_window_info(),
        }