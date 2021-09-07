SHORT_PAUSE = 1
MID_PAUSE = 10
LONG_PAUSE = 30
N_CLICKS = 10
MAX_CONF = 0.95
MIN_CONF = 0.8
DCONF = -0.05
import pyautogui as pag
from pynput import mouse

pag.PAUSE = SHORT_PAUSE

# auxiliary 
def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
        return False # Returning False if you need to stop the program when Left clicked.
    else:
        print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))

class AutoRun(object):
    def __init__(self):
        pass
        # listener = mouse.Listener(on_click=on_click)
        # listener.start()
        # listener.join()
    def check_exists(self, img_name="", base_path="./img"):
        return False

    def run(self):
        ''''''
        self.normal_activity()
        self.time_limited_activity()
        self.union()
    
    def back_to_home(self):
        ''''''
        conf = MAX_CONF
        pos_bth = pag.locateOnScreen('./img/bth.png', confidence=conf)
        while pos_bth is None:
            conf += DCONF
            pos_bth = pag.locateOnScreen('./img/bth.png', confidence=conf)
        if pos_bth is not None:
            pag.moveTo(pos_bth.left, pos_bth.top)
            cnt = 0
            while cnt < N_CLICKS:
                pag.click()
                cnt += 1
        else:
            print('主页未找到')
            exit()

    def normal_activity(self):
        ''' 日常任务 '''
        self.daily_checkin()
        
        self.buy_bali()
        
        self.get_vip_gift()

        self.get_daily_gift()
        # print('locating')
        # ppos = pag.locateOnScreen('./img/bth.png')
        # if ppos is not None:
        #     print('found')
        #     pag.moveTo(ppos.left, ppos.top)
        #     pag.click()
        # else:
        #     print('not found')

    def daily_checkin(self):
        ''' 每日签到 '''
        pass
    def buy_bali(self):
        ''' 购买贝里 '''
        pass
    def get_vip_gift(self):
        ''' VIP礼物 '''
        pass
    def get_daily_gift(self):
        ''' 日常礼包 '''
        pass

    def time_limited_activity(self):
        ''' 限时活动 '''
        self.consecutive_logins()
        self.sales_items()
        self.dollar_shop()
    def consecutive_logins(self):
        ''' 累积登录 '''
        pass
    def sales_items(self):
        ''' 道具折扣 '''
        pass
    def dollar_shop(self):
        ''' 福利商店 '''
        pass
        
    def union(self):
        ''' 工会活动 '''
        print('工会活动开始')
        self.union_construction()
        self.pirate_wanted()
    def union_construction(self):
        ''' 工会建设 '''
        self.back_to_home()
        print('    工会建设开始')
        conf_gh = MAX_CONF
        pos_gh = pag.locateOnScreen('./img/gonghui.png', confidence=conf_gh)
        while pos_gh is None:
            conf_gh += DCONF
            pos_gh = pag.locateOnScreen('./img/gonghui.png', confidence=conf_gh)
        if pos_gh is not None:
            pag.moveTo(pos_gh.left, pos_gh.top)
            # pag.PAUSE = LONG_PAUSE
            pag.click()
            pag.PAUSE = SHORT_PAUSE
            
            conf_ptjs = MAX_CONF
            pos_ptjs = pag.locateOnScreen('./img/gh_ptjs.png', confidence=conf_ptjs)
            while pos_ptjs is None:
                conf_ptjs += DCONF
                pos_ptjs = pag.locateOnScreen('./img/gh_ptjs.png', confidence=conf_ptjs)
            if pos_ptjs is not None:
                pag.moveTo(pos_ptjs.left, pos_ptjs.top)
                pag.click()
            else:
                print('        海盗悬赏未找到')
            print('    工会建设完成')
        else:
            print('    工会建设未找到')
        
    def pirate_wanted(self):
        ''' 海盗悬赏 '''
        pass

ar = AutoRun()
ar.run()
