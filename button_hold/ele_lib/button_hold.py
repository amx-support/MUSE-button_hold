#--------------------------------------------------------------------------------------------------
#
# Button Hold モジュール v1.0
#
# Program: KEI
#
#--------------------------------------------------------------------------------------------------

from threading import Thread
import time

# Hold処理用クラス --------------------------------------------------------------------------------------
class Hold:
    # 初期化
    def __init__(self,button,event_callback,hold_time:float=0.5,delay:float=0.0,repeat:bool=False):
        self.button = button
        self.event_callback = event_callback
        self.hold_time = hold_time
        self.delay = delay
        self.repeat = repeat
        self.event_parm = None
        self.thread = None
        self.button.watch(self.button_update)

    # Push / Release 検知用コールバック関数
    def button_update(self,e):
        self.event_parm = e

        # 押したときHold処理用スレッド生成
        if e.value:
            if self.thread is None:
                self.thread = self.HoldThread(self.event_callback,self.event_parm,self.hold_time,self.delay,self.repeat)
                self.thread.start()

        # 放したときスレッド終了
        else:
            self.thread.shutdown = True
            self.thread = None
    
    # Hold処理用スレッドクラス ------------------------------------------------------------------------------
    class HoldThread(Thread):
        # 初期化
        def __init__(self,event_callback,event_parm,hold_time,delay,repeat):
            self.event_callback = event_callback
            self.event_parm = event_parm
            self.hold_time = hold_time
            self.delay = delay
            self.repeat = repeat
            self.shutdown = False
            super().__init__(daemon=True)
        
        # Hold動作の実行用関数
        def run(self):
            if self.delay > 0:
                time.sleep(self.delay) # ディレイ処理
            else:
                time.sleep(self.hold_time)
            
            if not self.shutdown:
                self.event_callback(self.event_parm)
                if not self.repeat: # 繰り返しでなければ終了
                    return

            # Hold繰り返し
            while not self.shutdown:
                time.sleep(self.hold_time)

                if not self.shutdown:
                    self.event_callback(self.event_parm)