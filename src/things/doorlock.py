from common.utils import Utils
from common.device_command import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


LOCKED = 1
UNLOCKED = 2


class DoorlockWindow(QDialog):

    toogle_text = {
        True: 'UNLOCK',
        False: 'LOCK',
    }
    toggle_icon = {
        True: 'doorlock_on.png',
        False: 'doorlock_off.png',
    }

    def __init__(self, device_info, window_class, window_manager):
        super().__init__()

        self.device_info = device_info

        self.pre_setup_window(window_class, window_manager)
        self.post_setup_window()

    def __del__(self):
        del self.common_window

    def get_window(self):
        return self.common_window

    def pre_setup_window(self, window_class, window_manager):
        self.common_window = window_class(
            'doorlock.ui', 'doorlock_off.png', self.device_info, self, window_manager)
        self.get_ui_component_from_common_window(self.common_window)

    def post_setup_window(self):
        # variables
        self.state = False
        self.toggle_update_from_remote = False
        # device specific handler
        self.common_window.init_toggle_button()
        self.common_window.add_toggle_button_handler(self.toggle_handler)
        self.common_window.add_pipe_event_handler(self.event_handler)
        self.common_window.add_autotest_event_handler(
            self.autotest_event_handler)

    def get_ui_component_from_common_window(self, common_window):
        # device specific ui component
        self.pushButtonStatus = common_window.pushButtonStatus
        self.textBrowserLog = common_window.textBrowserLog
        self.labelStatePicture = common_window.labelDevicePicture

    @pyqtSlot(bool)
    def toggle_handler(self, state):
        """
        doorlock toggle button handler
        """
        # print(f'toggle_handler old ({self.state}), new ({state})')
        self.state = state
        self.update_ui()
        if self.toggle_update_from_remote:
            self.toggle_update_from_remote = False
        else:
            self.send_doorlock_command(self.state)

    def update_ui(self):
        self.pushButtonStatus.setStyleSheet(
            Utils.get_ui_style_toggle_btn(self.state))
        self.pushButtonStatus.setText(self.toogle_text.get(self.state))
        self.labelStatePicture.setPixmap(Utils.get_icon_img(
            Utils.get_icon_path(self.toggle_icon.get(self.state)), 70, 70))

    def send_doorlock_command(self, state):
        DoorlockCommand.lockUnlock(self.device_info.device_num, state)
        self.textBrowserLog.append(
            f'[Send] {self.toogle_text.get(self.state)}')

    def is_need_toggle(self, lock_state):
        if lock_state is LOCKED and not self.state:
            return True
        elif lock_state is UNLOCKED and self.state:
            return True
        else:
            return False

    def update_doorlock(self, lock_state):
        if self.is_need_toggle(lock_state):
            self.textBrowserLog.append(
                f'[Recv] {self.toogle_text.get(not self.state)}')
            self.toggle_update_from_remote = True
            self.pushButtonStatus.toggle()

    def event_handler(self, event):
        if 'lock' in event:
            lock_state = event.split(":")[1]
            self.update_doorlock(int(lock_state))

    def autotest_event_handler(self, used_device):
        self.pushButtonStatus.setEnabled(not used_device)
