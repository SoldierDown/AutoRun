SHORT_PAUSE = 1
MID_PAUSE = 10
LONG_PAUSE = 30
N_CLICKS = 10
MAX_CONF = 0.95
MIN_CONF = 0.8
DCONF = -0.05
DPM = 100
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
        conf_bth = MAX_CONF
        pos_bth = pag.locateOnScreen('./img/bth.png', confidence=conf_bth)
        while pos_bth is None and conf_bth > MIN_CONF:
            conf_bth += DCONF
            pos_bth = pag.locateOnScreen('./img/bth.png', confidence=conf_bth)
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
        print('日常任务开始')
        self.daily_checkin()
        self.buy_bali()
        self.get_vip_gift()
        self.get_daily_gift()
        print('日常任务完成')

    def daily_checkin(self):
        ''' 每日签到 '''
        self.back_to_home()
        finished = False
        print('    每日签到开始')
        conf_na = MAX_CONF
        pos_na = pag.locateOnScreen('./img/na.png', confidence=conf_na)
        while pos_na is None and conf_na > MIN_CONF:
            conf_na += DCONF
            pos_na = pag.locateOnScreen('./img/na.png', confidence=conf_na)
        if pos_na is not None:
            pag.moveTo(pos_na.left, pos_na.top)
            pag.click()

            conf_dci = MAX_CONF
            pos_dci = pag.locateOnScreen('./img/na_dci.png', confidence=conf_dci)
            while pos_dci is None and conf_dci > MIN_CONF:
                conf_dci += DCONF
                pos_dci = pag.locateOnScreen('./img/na_dci.png', confidence=conf_dci)
            if pos_dci is not None:
                pag.moveTo(pos_dci.left, pos_dci.top)
                pag.click()

                conf_aci = MAX_CONF
                pos_aci = pag.locateOnScreen('./img/na_dci_aci.png', confidence=conf_aci)
                while pos_aci is None and conf_aci > MIN_CONF:
                    conf_aci += DCONF
                    pos_aci = pag.locateOnScreen('./img/na_dci_aci.png', confidence=conf_aci)
                if pos_aci is not None:
                    pag.moveTo(pos_aci.left, pos_aci.top)
                    pag.click()

                    conf_lq = MAX_CONF
                    pos_lq = pag.locateOnScreen('./img/na_dci_aci_lq.png', confidence=conf_lq)
                    while pos_lq is None and conf_lq > MIN_CONF:
                        conf_lq += DCONF
                        pos_lq = pag.locateOnScreen('./img/na_dci_aci_lq.png', confidence=conf_lq)
                    if pos_lq is not None:
                        pag.moveTo(pos_lq.left, pos_lq.top)
                        pag.click()
                        finished = True
                    else:
                        print('    每日签到领取未找到')
                else:
                    print('    每日签到格未找到')
            else:
                print('    每日签到未找到')
        else:
            print('    日常活动未找到')
        if finished:
            print('    每日签到完成')

    def buy_bali(self):
        ''' 购买贝里 '''
        self.back_to_home()
        finished = False
        print('    购买贝里开始')
        conf_na = MAX_CONF
        pos_na = pag.locateOnScreen('./img/na.png', confidence=conf_na)
        while pos_na is None and conf_na > MIN_CONF:
            conf_na += DCONF
            pos_na = pag.locateOnScreen('./img/na.png', confidence=conf_na)
        if pos_na is not None:
            pag.moveTo(pos_na.left, pos_na.top)
            pag.click()

            # fixed point for dragging
            conf_fp = MAX_CONF
            pos_fp = pag.locateOnScreen('./img/na_fp', confidence=conf_fp)
            while pos_fp is None and conf_fp > MIN_CONF:
                conf_fp += DCONF
                pos_fp = pag.locateOnScreen('./img/na_fp', confidence=conf_fp)
            if pos_fp is not None:
                pag.moveTo(pos_fp.left + 2 * DPM, pos_fp.top)
                pos_bb = None
                conf_bb = MAX_CONF
                pos_bb = pag.locateOnScreen('./img/na_bb', confidence=conf_bb)
                while pos_bb is None and conf_bb > MIN_CONF:
                    pag.drag(-DPM, 0)
                    conf_bb += DCONF
                    pos_bb = pag.locateOnScreen('./img/na_bb', confidence=conf_bb)
                    pag.moveTo(pos_fp.left + 2 * DPM, pos_fp.top)
                if pos_bb is not None:
                    pag.moveTo(pos_bb.left, pos_bb.top)
                    pag.click()

                    conf_bo = MAX_CONF
                    pos_bo = pag.locateOnScreen('./img/na_bb_bo.png', confidence=conf_bo)
                    while pos_bo is None and conf_bo > MIN_CONF:
                        conf_bo += DCONF
                        pos_bo = pag.locateOnScreen('./img/na_bb_bo.png', confidence=conf_bo)
                    if pos_bo is not None:
                        pag.moveTo(pos_bo.left, pos_bo.top)
                        pag.click()
                        finished = True
                    else:
                        print('    购买贝里一次未找到')
                else:
                    print('    购买贝里未找到')
            else:
                print('    固定点未找到')
                exit()
        else:
            print('    日常活动未找到')
        if finished:
            print('    购买贝里完成')
        
    def get_vip_gift(self):
        ''' VIP礼物 '''
        self.back_to_home()
        finished = False
        print('    VIP礼物开始')
        conf_na = MAX_CONF
        pos_na = pag.locateOnScreen('./img/na.png', confidence=conf_na)
        while pos_na is None and conf_na > MIN_CONF:
            conf_na += DCONF
            pos_na = pag.locateOnScreen('./img/na.png', confidence=conf_na)
        if pos_na is not None:
            pag.moveTo(pos_na.left, pos_na.top)
            pag.click()

            # fixed point for dragging
            conf_fp = MAX_CONF
            pos_fp = pag.locateOnScreen('./img/na_fp', confidence=conf_fp)
            while pos_fp is None and conf_fp > MIN_CONF:
                conf_fp += DCONF
                pos_fp = pag.locateOnScreen('./img/na_fp', confidence=conf_fp)
            if pos_fp is not None:
                pag.moveTo(pos_fp.left + 2 * DPM, pos_fp.top)
                pos_bb = None
                conf_bb = MAX_CONF
                pos_bb = pag.locateOnScreen('./img/na_bb', confidence=conf_bb)
                while pos_bb is None and conf_bb > MIN_CONF:
                    pag.drag(-DPM, 0)
                    conf_bb += DCONF
                    pos_bb = pag.locateOnScreen('./img/na_bb', confidence=conf_bb)
                    pag.moveTo(pos_fp.left + 2 * DPM, pos_fp.top)
                if pos_bb is not None:
                    pag.moveTo(pos_bb.left, pos_bb.top)
                    pag.click()

                    conf_bo = MAX_CONF
                    pos_bo = pag.locateOnScreen('./img/na_bb_bo.png', confidence=conf_bo)
                    while pos_bo is None and conf_bo > MIN_CONF:
                        conf_bo += DCONF
                        pos_bo = pag.locateOnScreen('./img/na_bb_bo.png', confidence=conf_bo)
                    if pos_bo is not None:
                        pag.moveTo(pos_bo.left, pos_bo.top)
                        pag.click()
                    else:
                        print('    购买贝里一次未找到')
                else:
                    print('    购买贝里未找到')
            else:
                print('    固定点未找到')
                exit()
        else:
            print('    日常活动未找到')
        if finished:
            print('    购买贝里完成')
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
        pos_gh = pag.locateOnScreen('./img/gh.png', confidence=conf_gh)
        while pos_gh is None:
            conf_gh += DCONF
            pos_gh = pag.locateOnScreen('./img/gh.png', confidence=conf_gh)
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
