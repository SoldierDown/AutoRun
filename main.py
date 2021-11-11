SHORT_PAUSE = 1
MID_PAUSE = 10
LONG_PAUSE = 30
N_CLICKS = 3
N_DRAGS = 30
MAX_CONF = 0.95
MIN_CONF = 0.8
DCONF = -0.03
DPM = 100
MAX_ATTEMPTS = 10
TOTAL_CHANCES = 3
from PIL.Image import FASTOCTREE
from numpy import copysign, true_divide
import pyautogui as pag
from pynput import mouse
from pynput.mouse import Button, Controller
import time
import json
import os

pag.PAUSE = SHORT_PAUSE

# error handling

# auxiliary 
def on_click(x, y, button, pressed):
    if button == mouse.Button.left:
        print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
        return False # Returning False if you need to stop the program when Left clicked.
    else:
        print('{} at {}'.format('Pressed Right Click' if pressed else 'Released Right Click', (x, y)))



def user_print(txt='', ind=0):
    output=''
    for iter in range(ind):
        output+='    '
    output += txt
    print(output)

class AutoRun(object):
    def __init__(self, role='xl', to_test=False, to_reset=True):
        self.test = to_test
        self.role = role
        filename = 'checklist_' + self.role + '.json'

        # open and reset
        with open(filename, 'r') as f:
            self.record = json.load(f)
        if to_reset:
            self.reset(self.record)



    def reset(self, value):
        for key in value:
            val = value[key]
            if isinstance(val, int):
                value[key] = 0
            else:
                if not isinstance(val, str) and not isinstance(val, list):
                    self.reset(val)
    


    def move_and_click(self, pos=[], offset=[], n_clicks=1):
        if len(pos) != 0:
            pag.moveTo(pos[0], pos[1])
        if len(offset) != 0:
            pag.move(offset[0], offset[1])
        pag.click(clicks=n_clicks)



    def find_all_and_return(self, img_path='', name='', max_conf=MAX_CONF, grayscale=False, mute=False, ind=1):
        conf = max_conf
        results = list(pag.locateAllOnScreen(img_path, grayscale=grayscale, confidence=conf))
        while len(results) == 0 and conf > MIN_CONF:
            conf += DCONF
            results = list(pag.locateAllOnScreen(img_path, grayscale=grayscale, confidence=conf))
        if len(results) > 0:
            return results
        else:
            if not mute:
                output=name
                output+='未找到'
                user_print(txt=output, ind=ind)
            time.sleep(3)
            return []



    def find_and_click(self, img_path='', name='', offset=[0, 0], ind=1, n_clicks=1, mute=False, pause=SHORT_PAUSE):
        conf = MAX_CONF
        pos = pag.locateOnScreen(img_path, confidence=conf)
        while pos is None and conf > MIN_CONF:
            conf += DCONF
            pos = pag.locateOnScreen(img_path, confidence=conf)
        if pos is not None:
            pag.moveTo(pos.left + offset[0], pos.top + offset[1])
            pag.PAUSE=pause
            for iter in range(n_clicks):
                pag.click()
                time.sleep(pause)
            pag.PAUSE=SHORT_PAUSE
            time.sleep(3)
            return True, pos.left, pos.top
        else:
            if not mute:
                output=name
                output+='未找到'
                user_print(txt=output, ind=ind)
            time.sleep(3)
            return False, 0, 0



    def drag(self, fp=[0, 0], dragto=[0, 0], dx=1, dir=0, n_drags=1):
        ctl = Controller()
        for iter in range(n_drags):
            pag.moveTo(fp[0], fp[1])
            x, y = ctl.position
            ctl.press(Button.left)
            cnt = 0
            while cnt < abs(dragto[dir]):
                cnt += 1                    
                # ++
                if dragto[dir] > 0:
                    if dir == 0:
                        x += dx
                    else:
                        y += dx
                # --
                else:
                    if dir == 0:
                        x -= dx
                    else:
                        y -= dx 
                time.sleep(0.01)                   
                ctl.position = (x, y)
            ctl.release(Button.left)



    def drag_find_and_click(self, fp=[0, 0], dir=0, dragto=[0, 0], dx=1, img_path='', name='', offset=[0, 0], ind=1, n_clicks=1, n_drags=1, extra_drag=False):
        if img_path == '':
            self.drag(fp=fp, dragto=dragto, dir=dir, n_drags=n_drags)
            return True, 0, 0
        pag.moveTo(fp[0], fp[1])
        cnt_drags = 0
        conf = MAX_CONF
        pos = pag.locateOnScreen(img_path, confidence=conf)
        while pos is None and cnt_drags < N_DRAGS:
            while pos is None and conf > MIN_CONF:
                conf += DCONF
                pos = pag.locateOnScreen(img_path, confidence=conf)
            if pos is None:
                conf = MAX_CONF
                self.drag(fp=fp, dir=dir, dragto=dragto, dx=dx, n_drags=1)
                pos = pag.locateOnScreen(img_path, confidence=conf)
        if pos is not None:
            print(pos)
            time.sleep(MID_PAUSE)
            found = False
            while not found:
                pos = pag.locateOnScreen(img_path, confidence=conf)
                print(pos)
                if pos != None:
                    found = True
            pag.moveTo(pos[0] + offset[0], pos[1] + offset[1])
            for iter in range(n_clicks):
                pag.click()
            time.sleep(3)
            return True, pos.left, pos.top
        else:
            output=name
            output+='未找到'
            user_print(txt=output, ind=ind)
            time.sleep(3)
            return False, 0, 0



    def run(self):
        ''''''
        # self.recruit(is_final=False)
        self.dbf()
        self.time_limited_activity()              # looks good now
        self.cabin()
        self.union()                              # looks good now
        self.game_assistant()                     # looks good now
        self.lineup()                             # looks good now
        self.bag()                                # looks good now
        self.adventure()
        self.harbor()                             # looks good now
        self.functions()                          # looks good now
        self.recruit(is_final=False)
        self.shop()
        self.get_task_reward(is_final=False)       # looks good now
        self.boyos()                              # looks good now            
        self.normal_activity()                    # not efficient
        self.recruit(is_final=True)
        self.get_task_reward(is_final=True)       # looks good now
        self.reward_center()

    
    def back_to_home(self, ind=0, n_clicks=1):
        ''' 回到主页 '''
        self.find_and_click(img_path='./tasks/error_fh3.png', name='返回', mute=True, n_clicks=n_clicks, ind=ind)
        return self.find_and_click(img_path='./tasks/bth.png', name='主页', n_clicks=n_clicks, ind=ind)



    def dbf(self, ind=0):
        ''' DBF '''
        user_print('DBF开始', ind=ind)
        done = self.record['DBF']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/rc.png', name='日常', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/rc_dbf.png', name='DBF', ind=ind+1)
            if not f2: continue
            f3, _, _ = self.find_and_click(img_path='./tasks/rc_dbf_+.png', name='+', ind=ind+1)
            if not f3: continue
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/rc_dbf_+_qd.png', name='确定', ind=ind+1)
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/rc_dbf_fh.png', name='返回', ind=ind+1)
            if not self.test:
                self.record['DBF'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('DBF完成', ind=ind)
        else:
            user_print('DBF未完成', ind=ind)


    def normal_activity(self, ind=0):
        ''' 日常任务 '''
        user_print('日常任务开始', ind=ind)
        # self.daily_checkin()
        self.buy_bali()
        self.get_vip_gift()
        # self.get_daily_gift()
        user_print('日常任务完成', ind=ind)

    # TODO
    def daily_checkin(self, ind=1):
        ''' 每日签到 '''
        user_print('每日签到开始', ind=ind)
        done = self.record['normal_activity']['daily_checkin']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/na_dci.png', name='每日签到', ind=ind+1)
            if not f2: continue
            f3, _, _ = self.find_and_click(img_path='./tasks/na_dci_cell.png', name='每日签到格', ind=ind+1)
            if not f3: continue
            f4, _, _ = self.find_and_click(img_path='./tasks/na_dci_lq_o.png', name='领取', ind=ind+1)
            if not f4:
                f5 = False
                while not f5:
                    f5, _, _ = self.find_and_click(img_path='./tasks/na_dci_lq_b.png', name='领取', ind=ind+1)
            self.back_to_home(ind=ind+1)
            if not self.test:
                self.record['normal_activity']['daily_checkin'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('每日签到完成', ind=ind)
        else:
            user_print('每日签到未完成', ind=ind)


    def buy_bali(self, ind=1):
        ''' 购买贝里 '''
        user_print('购买贝里开始', ind=ind)
        done = self.record['normal_activity']['buy_bali']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            if not f1: continue
            f2, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            if not f2: continue
            fpx, fpy = fpx, fpy - 7 * DPM
            f3, _, _ = self.drag_find_and_click(fp=[fpx + 4 * DPM, fpy], dragto=[-2*DPM, 0], dir=0, img_path='./tasks/na_bb.png', name='购买贝里', ind=ind+1)
            if not f3: continue
            f4, _, _ = self.find_and_click(img_path='./tasks/na_bb_bo.png', name='购买贝里一次', ind=ind+1)
            if not f4: continue
            if not self.test:
                self.record['normal_activity']['buy_bali'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('购买贝里完成', ind=ind)
        else:
            user_print('购买贝里未完成', ind=ind)


    def get_vip_gift(self, ind=1):
        ''' VIP礼物 '''
        user_print('VIP礼物开始', ind=ind)
        done = self.record['normal_activity']['get_vip_gift']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            if not f1: continue
            f2, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            if not f2: continue
            fpx, fpy = fpx, fpy - 7 * DPM
            f3, _, _ = self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], dir=0, img_path='./tasks/na_vipg.png', name='VIP礼包', ind=ind+1)
            if not f3: continue
            f4, _, _ = self.find_and_click(img_path='./tasks/na_vipg_mrg.png', name='VIP每日礼包', ind=ind+1)
            if not f4: continue
            f5, _, _ = self.find_and_click(img_path='./tasks/na_vipg_mrg_lq.png', name='VIP每日礼包领取', ind=ind+1)
            if not f5: continue
            if not self.test:
                self.back_to_home(ind=ind+1, n_clicks=1)
                self.record['normal_activity']['get_vip_gift'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('VIP礼物完成', ind=ind)
        else:
            user_print('VIP礼物未完成', ind=ind)
        
    
    def get_daily_gift(self, ind=1):
        '''' 日常礼包 '''
        user_print('日常礼包开始', ind=ind)
        self.get_mr_gift()
        user_print('日常礼包完成', ind=ind)
    
    def get_mr_gift(self, ind=2):
        ''' 每日礼包 '''
        user_print('每日礼包开始', ind=ind)
        done = self.record['normal_activity']['get_daily_gift']['mr']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            if not f1: continue
            f2, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            if not f2: continue
            fpx, fpy = fpx, fpy - 7 * DPM
            f3, _, _ = self.drag_find_and_click(fp=[fpx + 4 * DPM, fpy], dragto=[-2*DPM, 0], dir=0, img_path='./tasks/na_rcg.png', name='VIP礼包', ind=ind+1)
            if not f3: continue
            f4, _, _ = self.find_and_click(img_path='./tasks/na_rcg_mrg_mf.png', name='日常礼包每日礼包领取', ind=ind+1)
            if not f4: continue
            if not self.test:
                self.back_to_home(ind=ind+1, n_clicks=1)
                self.record['normal_activity']['get_daily_gift']['mr'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('每日礼包完成', ind=ind)
        else:
            user_print('每日礼包未完成', ind=ind)
    
    
    
    def shop(self, ind=0):
        ''' 商店 '''
        user_print('商店开始', ind=ind)
        self.bw_shop()
        self.hb_shop()
        self.cw_shop()
        self.xz_shop()
        user_print('商店完成', ind=ind)

        
    def bw_shop(self, ind=1):
        ''' 宝物商店 '''
        user_print('宝物商店开始', ind=ind)
        todo = self.record['shop']['bwshop']['todo']
        if todo != 'true':
            user_print('宝物商店跳过', ind=ind)
            return
        done = self.record['shop']['bwshop']['done']
        if self.test:
            done = 0
        total_chances = TOTAL_CHANCES
        wishlist = self.record['shop']['bwshop']['wishlist']
        cur_chances = self.record['shop']['bwshop']['cur_chances']
        att = 0
        while done != 1 and att < 1:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/shop.png', name='商店', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/shop_bwshop.png', name='宝物商店', ind=ind+1)
            while not f2:
                f2, _, _ = self.back_to_home(ind=ind+1)
                continue
            to_break = False
            while cur_chances <= total_chances and not to_break:
                if cur_chances == total_chances:
                    to_break = True
                for item in wishlist:
                    item_path = './tasks/shop_bwshop_' + item + '.png'
                    to_buys = self.find_all_and_return(img_path=item_path, max_conf=0.9, grayscale=True, mute=True, name=item, ind=ind+1)
                    user_print(txt='{}: {}'.format(item, len(to_buys)), ind=ind+1)
                    if len(to_buys) > 0:
                        for pos in to_buys:
                            self.move_and_click(pos=[pos[0], pos[1]], offset=[0, 0.7*DPM])
                            need_hh, _, _ = self.find_and_click(img_path='./tasks/shop_bwshop.png', name='宝物结晶', mute=True, n_clicks=0, ind=ind+1)
                            if need_hh:
                                to_break = True
                                found = False
                                while not found:
                                    found, _, _ = self.find_and_click(img_path='./tasks/shop_bwshop_nq.png', name='金币', mute=True, ind=ind+1)
                                break
                            self.find_and_click(img_path='./tasks/shop_bwshop_nq.png', name='金币', mute=True, ind=ind+1)
                if not to_break:
                    if cur_chances < total_chances:
                        found = False
                        while not found:
                           found, _, _ = self.find_and_click(img_path='./tasks/shop_bwshop_sx.png', name='刷新', ind=ind+1)
                        cur_chances += 1
                        self.find_and_click(img_path='./tasks/shop_bwshop_qdsx.png', name='确定刷新', mute=True, ind=ind+1)
            if not self.test:
                self.record['shop']['bwshop']['done'] = 1
                done = 1
                self.save_to_json()
                self.back_to_home(ind=ind+1)
        if done == 1:
            user_print('宝物商店完成', ind=ind)
        else:
            user_print('宝物商店未完成', ind=ind)
    def hb_shop(self, ind=1):
        ''' 伙伴商店 '''
        user_print('伙伴商店开始', ind=ind)
        done = self.record['shop']['hbshop']['done']
        total_chances = TOTAL_CHANCES
        cur_chances = self.record['shop']['hbshop']['cur_chances']
        wishlist = self.record['shop']['hbshop']['wishlist']
        att = 0
        while done != 1 and att < 1:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/shop.png', name='商店', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/shop_hbshop.png', name='伙伴商店', ind=ind+1)
            if not f2: continue
            to_break = False
            while cur_chances <= total_chances and not to_break:
                if cur_chances == total_chances:
                    to_break = True
                for item in wishlist:
                    item_path = './tasks/shop_hbshop_' + item + '.png'
                    to_buys = self.find_all_and_return(img_path=item_path, max_conf=0.9, grayscale=True, mute=True, name=item, ind=ind+1)
                    user_print(txt='{}: {}'.format(item, len(to_buys)), ind=ind+1)
                    if len(to_buys) > 0:
                        for pos in to_buys:
                            self.move_and_click(pos=[pos[0], pos[1]], offset=[0, 0.7*DPM])
                            need_hh, _, _ = self.find_and_click(img_path='./tasks/shop_hbshop.png', name='宝物结晶', mute=True, n_clicks=0, ind=ind+1)
                            if need_hh:
                                to_break = True
                                self.find_and_click(img_path='./tasks/shop_hbshop_nq.png', name='金币', mute=True, ind=ind+1)
                                break
                            self.find_and_click(img_path='./tasks/shop_hbshop_nq.png', name='金币', mute=True, ind=ind+1)
                if not to_break:
                    if cur_chances < total_chances:
                        f3 = False
                        while not f3:
                            f3, _, _ = self.find_and_click(img_path='./tasks/shop_hbshop_sx.png', name='刷新', ind=ind+1)
                        cur_chances += 1
                        self.find_and_click(img_path='./tasks/shop_hbshop_qdsx.png', name='确定刷新', mute=True, ind=ind+1)
            self.record['shop']['hbshop']['done'] = 1
            done = 1
            self.save_to_json()
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/shop_hbshop_fh.png', name='返回', mute=True, ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/shop_fh.png', name='返回', mute=True, ind=ind+1)
            if not f5: continue
        if done == 1:
            user_print('伙伴商店完成', ind=ind)
        else:
            user_print('伙伴商店未完成', ind=ind)


    def cw_shop(self, ind=1):
        ''' 宠物商店 '''
        user_print('宠物商店开始', ind=ind)
        done = self.record['shop']['cwshop']['done']
        total_chances = TOTAL_CHANCES
        cur_chances = self.record['shop']['cwshop']['cur_chances']
        wishlist = self.record['shop']['cwshop']['wishlist']
        att = 0
        while done != 1 and att < 1:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/shop.png', name='商店', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/shop_cwshop.png', name='宠物商店', ind=ind+1)
            to_break = False
            while cur_chances <= total_chances and not to_break:
                if cur_chances == total_chances:
                    to_break = True
                for item in wishlist:
                    item_path = './tasks/shop_cwshop_' + item + '.png'
                    to_buys = self.find_all_and_return(img_path=item_path, max_conf=0.9, grayscale=False, mute=True, name=item, ind=ind+1)
                    user_print(txt='{}: {}'.format(item, len(to_buys)), ind=ind+1)
                    if len(to_buys) > 0:
                        for pos in to_buys:
                            self.move_and_click(pos=[pos[0], pos[1]], offset=[0, 0.7*DPM])
                            need_hh, _, _ = self.find_and_click(img_path='./tasks/shop_cwshop.png', name='宝物结晶', mute=True, n_clicks=0, ind=ind+1)
                            if need_hh:
                                to_break = True
                                self.find_and_click(img_path='./tasks/shop_cwshop_nq.png', name='金币', mute=True, ind=ind+1)
                                break
                            self.find_and_click(img_path='./tasks/shop_cwshop_nq.png', name='金币', mute=True, ind=ind+1)
                if not to_break:
                    if cur_chances < total_chances:
                        self.find_and_click(img_path='./tasks/shop_cwshop_sx.png', name='刷新', ind=ind+1)
                        cur_chances += 1
            self.record['shop']['cwshop']['done'] = 1
            done = 1
            self.save_to_json()
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/shop_cwshop_fh.png', name='返回', mute=True, ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/shop_fh.png', name='返回', mute=True, ind=ind+1)
            if not f4: continue
        if done == 1:
            user_print('宠物商店完成', ind=ind)
        else:
            user_print('宠物商店未完成', ind=ind)
    def xz_shop(self, ind=1):
        ''' 勋章商店 '''
        user_print('勋章商店开始', ind=ind)
        done = self.record['shop']['xzshop']['done']
        total_chances = TOTAL_CHANCES
        cur_chances = self.record['shop']['xzshop']['cur_chances']
        wishlist = self.record['shop']['xzshop']['wishlist']
        att = 0
        while done != 1 and att < 1:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/shop.png', name='商店', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/shop_xzshop.png', name='宠物商店', ind=ind+1)
            to_break = False
            while cur_chances <= total_chances and not to_break:
                if cur_chances == total_chances:
                    to_break = True
                for item in wishlist:
                    item_path = './tasks/shop_xzshop_' + item + '.png'
                    to_buys = self.find_all_and_return(img_path=item_path, max_conf=0.9, grayscale=False, mute=True, name=item, ind=ind+1)
                    user_print(txt='{}: {}'.format(item, len(to_buys)), ind=ind+1)
                    if len(to_buys) > 0:
                        for pos in to_buys:
                            self.move_and_click(pos=[pos[0], pos[1]], offset=[0, 0.7*DPM])
                            need_xzjj, _, _ = self.find_and_click(img_path='./tasks/shop_xzshop_ne.png', name='勋章结晶不够', mute=True, n_clicks=0, ind=ind+1)
                            if need_xzjj:
                                to_break = True
                                break
                            self.find_and_click(img_path='./tasks/shop_xzshop_nq.png', name='金币', mute=True, ind=ind+1)
                if not to_break:
                    if cur_chances < total_chances:
                        self.find_and_click(img_path='./tasks/shop_xzshop_sx.png', name='刷新', ind=ind+1)
                        cur_chances += 1
            self.record['shop']['xzshop']['done'] = 1
            done = 1
            self.save_to_json()
            self.back_to_home(ind=ind+1)
        if done == 1:
            user_print('勋章商店完成', ind=ind)
        else:
            user_print('勋章商店未完成', ind=ind)



    def time_limited_activity(self, ind=0):
        ''' 限时活动 '''
        user_print('限时活动开始', ind=ind)
        self.consecutive_logins()
        self.sales_items()
        self.dollar_shop()
        user_print('限时活动完成', ind=ind)
    def consecutive_logins(self, ind=1):
        ''' 累计登录 tbc'''
        user_print('累计登录开始', ind=ind)
        done = self.record['time_limited_activity']['consecutive_logins']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/la.png', name='限时活动', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/la_lj.png', name='累计登录', ind=ind+1)
            if not f2:
                self.record['time_limited_activity']['consecutive_logins'] = 1
                done = 1
                self.save_to_json()
                break
            f3, _, _ = self.find_and_click(img_path='./tasks/la_lj_lq.png', name='累计登录领取', n_clicks=1, ind=ind+1)
            if not f3: continue
            # add an offset to quit
            self.move_and_click(offset=[0, 2*DPM], n_clicks=4)
            # todo: add offset
            if not self.test:
                self.record['time_limited_activity']['consecutive_logins'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('累计登录完成', ind=ind)
        else:
            user_print('累计登录未完成', ind=ind)
    def dollar_shop(self, ind=1):
        ''' 福利商店 '''
        user_print('福利商店开始', ind=ind)
        done = self.record['time_limited_activity']['dollar_shop']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/la.png', name='限时活动', ind=ind+1)
            if not f1: continue
            f2, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            if not f2: continue
            fpx, fpy = fpx, fpy - 7 * DPM
            f3, _, _ = self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], dir=0, img_path='./tasks/la_fl.png', name='福利商店', ind=ind+1)
            if not f3: continue
            f4, _, _ = self.find_and_click(img_path='./tasks/la_fl_tl.png', name='福利商店购买体力', offset=[3.5*DPM, 0.5*DPM], n_clicks=5, ind=ind+1)
            if not f4: continue
            if not self.test:
                self.back_to_home(ind=ind+1, n_clicks=1)
                self.record['time_limited_activity']['dollar_shop'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('福利商店完成', ind=ind)
        else:
            user_print('福利商店未完成', ind=ind)
    def sales_items(self, ind=1):
        ''' 道具折扣 '''
        user_print('道具折扣开始', ind=ind)
        done = self.record['time_limited_activity']['sales_items']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/la.png', name='限时活动', ind=ind+1)
            if not f1: continue
            f2, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            if not f2: continue
            fpx, fpy = fpx, fpy - 7 * DPM
            f3, _, _ = self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], dir=0, img_path='./tasks/la_dj.png', name='道具折扣', ind=ind+1)
            if not f3: continue
            f4, _, _ = self.find_and_click(img_path='./tasks/la_dj_tl.png', name='道具折扣购买体力', offset=[3.5*DPM, 0.5*DPM], n_clicks=5, ind=ind+1)
            if not f4: continue
            if not self.test:
                self.back_to_home(ind=ind+1, n_clicks=1)
                self.record['time_limited_activity']['sales_items'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('道具折扣完成', ind=ind)
        else:
            user_print('道具折扣未完成', ind=ind)



    def game_assistant(self, ind=0):
        ''' 游戏助手 '''
        user_print('游戏助手开始', ind=ind)
        done = self.record['game_assistant']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/ga.png', name='游戏助手', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/ga_da.png', name='全部执行', pause=LONG_PAUSE, ind=ind+1)
            if not f2: 
                f3 = False
                while not f3:
                    f3, _, _ = self.find_and_click(img_path='./tasks/ga_da_back_back.png', name='退出游戏助手', pause=LONG_PAUSE, ind=ind+1)
                continue
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/ga_da_back.png', name='游戏执行完成', ind=ind+1)
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/ga_da_back_back.png', name='退出游戏助手', ind=ind+1)
            if not self.test:
                self.record['game_assistant'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('游戏助手完成', ind=ind)
        else:
            user_print('游戏助手未完成', ind=ind)

    def daily_tasks(self, ind=0):
        ''' 每日任务 '''
        user_print("每日任务开始", ind=ind)
        self.get_task_reward()
        user_print("每日任务完成", ind=ind)
        

    
    def reward_center(self, ind=0):
        ''' 奖励中心 '''
        user_print('奖励中心开始', ind=ind)
        done = self.record['reward_center']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/rewardcenter.png', name='奖励中心', ind=ind+1)
            if not f1:
                self.record['reward_center'] = 1
                done = 1
                self.save_to_json()
                continue
            f2 = False
            while not f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/rewardcenter_qblq.png', name='全部领取', ind=ind+1)
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/rewardcenter_qblq_qd.png', name='确定', ind=ind+1)
            if not self.test:
                # self.record['reward_center'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('奖励中心完成', ind=ind)
        else:
            user_print('奖励中心未完成', ind=ind)



    def union(self, ind=0):
        ''' 工会活动 '''
        user_print('工会活动开始', ind=ind)
        self.union_construction()
        self.pirate_wanted()
        self.get_coffee()
        # self.get_union_bonus()
        self.official_pirates()
        user_print('工会活动完成', ind=ind)
    def union_construction(self, ind=1):
        ''' 工会建设 '''
        user_print('工会建设开始', ind=ind)
        done = self.record['union']['union_construction']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=MID_PAUSE, ind=ind+1)
            if not f1: continue
            f2 = False
            while not f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt.png', name='工会大厅', ind=ind+1)
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_ptjs.png', name='普通建设', offset=[DPM/3, DPM*2.5], ind=ind+1)
            time.sleep(MID_PAUSE)
            pag.click()
            time.sleep(MID_PAUSE)
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_lq.png', name='领取奖励', ind=ind+1)
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_lq_qd.png', name='确定领取', ind=ind+1)
            f6 = False
            while not f6:
                f6, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_fh.png', name='返回工会大厅', ind=ind+1)
            time.sleep(2*MID_PAUSE)
            f7 = False
            while not f7:
                f7, _, _ = self.find_and_click(img_path='./tasks/gh_fh.png', name='退出公会', ind=ind+1)
            if not self.test:
                self.record['union']['union_construction'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('工会建设完成', ind=ind)
        else:
            user_print('工会建设未完成', ind=ind)
    def pirate_wanted(self, ind=1):
        ''' 海盗悬赏 tbc '''
        user_print('海盗悬赏开始', ind=ind)
        done = self.record['union']['pirate_wanted']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=MID_PAUSE, ind=ind+1)
            if not f1: continue
            f2 = False
            while not f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/gh_hdxs.png', name='海盗悬赏', ind=ind+1)
            f3 = False
            while not f3:
                f3, tzx, tzy = self.find_and_click(img_path='./tasks/gh_hdxs_tz.png', name='海盗悬赏挑战', ind=ind+1)
            pag.moveTo(tzx, tzy+DPM)
            pag.click()
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/gh_hdxs_fh.png', name='退出海盗悬赏', ind=ind+1)
            time.sleep(MID_PAUSE)
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/gh_fh.png', name='退出工会', ind=ind+1)
            if not self.test:
                self.record['union']['pirate_wanted'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('海盗悬赏完成', ind=ind)
        else:
            user_print('海盗悬赏未完成', ind=ind)
    def get_coffee(self, ind=1):
        ''' 人鱼咖啡厅 '''
        user_print('喝咖啡开始', ind=ind)
        done = self.record['union']['get_coffee']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=MID_PAUSE, ind=ind+1)
            if not f1: continue
            f2 = False
            while not f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/gh_rykft.png', name='人鱼咖啡厅', ind=ind+1)
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/gh_rykft_hkf.png', name='喝咖啡', ind=ind+1)
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/gh_rykft_hkf_qd.png', name='确定', ind=ind+1)
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/gh_rykft_fh.png', name='返回', ind=ind+1)
            time.sleep(2*MID_PAUSE)
            f6 = False
            while not f6:
                f6, _, _ = self.find_and_click(img_path='./tasks/gh_fh.png', name='退出工会', ind=ind+1)
            if not self.test:
                self.record['union']['get_coffee'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('喝咖啡完成', ind=ind)
        else:
            user_print('喝咖啡未完成', ind=ind)
    def get_union_bonus(self, ind=1):
        ''' 工会福利 '''
        user_print('工会福利开始', ind=ind)
        total_bonus = 10
        cur_chances = self.record['union']['get_union_bonus']['cur_chances']
        done = self.record['union']['get_union_bonus']['done']
        if cur_chances == total_bonus:
            done = 1
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=MID_PAUSE, ind=ind+1)
            if not f1: continue
            f2 = False
            while not f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/gh_ghfl.png', name='工会福利', ind=ind+1)
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/gh_ghfl_grhb.png', name='个人红包', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/gh_ghfl_grhb_hb.png', name='红包', n_clicks=0, ind=ind+1)
            time.sleep(3)
            while f4 and cur_chances < total_bonus:
                pag.click()
                f5, _, _ = self.find_and_click(img_path='./tasks/gh_ghfl_grhb_hb_dk.png', name='打开', ind=ind+1)
                time.sleep(3)
                if not f5:
                    self.find_and_click(img_path='./tasks/gh_ghfl_grhb_ylq_qd.png', name='确定', ind=ind+1)
                    break
                f6, _, _ = self.find_and_click(img_path='./tasks/gh_ghfl_grhb_hb_dk_qd.png', name='确定', ind=ind+1)
                time.sleep(3)
                if f5 and f6:
                    cur_chances += 1
                else:
                    break
                f4, _, _ = self.find_and_click(img_path='./tasks/gh_ghfl_grhb_hb.png', name='红包', n_clicks=0, ind=ind+1)
                time.sleep(3)
            f7 = False
            while not f7:
                f7, _, _ = self.find_and_click(img_path='./tasks/gh_ghfl_fh.png', name='返回', ind=ind+1)
            time.sleep(2*MID_PAUSE)
            f8 = False
            while not f8:
                f8, _, _ = self.find_and_click(img_path='./tasks/gh_fh.png', name='返回', ind=ind+1)
            if not self.test:
                self.record['union']['get_union_bonus']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('工会福利完成', ind=ind)
        else:
            user_print('工会福利未完成', ind=ind)
    def official_pirates(self, ind=1):
        ''' 七武海 '''
        user_print('七武海开始', ind=ind)
        done = self.record['union']['official_pirates']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=MID_PAUSE, ind=ind+1)
            if not f1: continue
            f2 = False
            while not f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/gh_qwh.png', name='七武海', ind=ind+1)
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_jsjl.png', name='击杀奖励', ind=ind+1)
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_jsjl_yjlq.png', name='一键领取', n_clicks=5, ind=ind+1)
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_jsjl_tc.png', name='退出', ind=ind+1)
            time.sleep(5)

            f6 = False
            while not f6:
                f6, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_sdqb.png', name='扫荡全部', ind=ind+1)
            time.sleep(2*MID_PAUSE)
            f7, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_sdqb_sdwc.png', name='扫荡完成', ind=ind+1)
            if not f7:
                self.find_and_click(img_path='./tasks/gh_qwh_sdqb_tc.png', name='退出', ind=ind+1)
                self.find_and_click(img_path='./tasks/gh_qwh_fh.png', name='返回', ind=ind+1)
                self.find_and_click(img_path='./tasks/gh_fh.png', name='返回', ind=ind+1)
                break
            f8, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_fh.png', name='返回', ind=ind+1)
            if not f8:
                self.find_and_click(img_path='./tasks/gh_qwh_sdqb_tc.png', name='退出', ind=ind+1)
                self.find_and_click(img_path='./tasks/gh_qwh_fh.png', name='返回', ind=ind+1)
                self.find_and_click(img_path='./tasks/gh_fh.png', name='返回', ind=ind+1)
                break
            time.sleep(10)
            f9 = False
            while not f9:
                f9, _, _ = self.find_and_click(img_path='./tasks/gh_fh.png', name='返回', ind=ind+1)
            if not self.test:
                self.record['union']['official_pirates'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('七武海完成', ind=ind)
        else:
            user_print('七武海未完成', ind=ind)


    def harbor(self, ind=0):
        ''' 港口 '''
        user_print('港口开始', ind=ind)
        self.harbor_reward()
        user_print('港口完成', ind=ind)
    def harbor_reward(self, ind=1):
        ''' 港口领奖 '''
        user_print('港口领奖开始', ind=ind)
        done = self.record['harbor']['harbor_reward']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gk.png', name='港口', ind=ind+1)
            if not f1: continue
            f2 = False
            while not f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/gk_lj.png', name='港口领奖', ind=ind+1)
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/gk_lj_qd.png', name='港口领奖确定', ind=ind+1)
            time.sleep(5)
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/gk_fh.png', name='退出港口', ind=ind+1)
            if not self.test:
                self.record['harbor']['harbor_reward'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('港口领奖完成', ind=ind)
        else:
            user_print('港口领奖未完成', ind=ind)



    def functions(self, ind=0):
        ''' 功能 '''
        user_print('功能开始', ind=ind)
        self.adventure_logs()
        user_print('功能完成', ind=ind)


    def adventure_logs(self, ind=1):
        ''' 冒险日志 '''
        user_print('冒险日志开始', ind=ind)
        self.gumball_machine()
        self.adventure_fights()
        user_print('冒险日志完成', ind=ind)

    def gumball_machine(self, ind=2):
        ''' 扭蛋机 '''
        user_print('扭蛋机开始', ind=ind)
        cur_chances = self.record['functions']['adventure_logs']['gumball_machine']['current_chances']
        done = self.record['functions']['adventure_logs']['gumball_machine']['done']
        total_chances = TOTAL_CHANCES
        att = 0
        if cur_chances == total_chances:
            done = 1
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gn.png', name='功能', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz.png', name='冒险日志', ind=ind+1)
            if not f2:
                self.back_to_home(ind=ind+1)
                continue
            f3, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_ndj.png', name='扭蛋机', ind=ind+1)
            if not f3: continue
            while cur_chances < total_chances:
                f4, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_ndj_tbyc.png', name='投币一次', ind=ind+1)
                f5, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_ndj_tbyc_qd.png', name='投币确定', ind=ind+1)
                if f4 and f5:
                    cur_chances += 1
            if cur_chances == total_chances: 
                self.record['functions']['adventure_logs']['gumball_machine']['current_chances'] = total_chances
                self.record['functions']['adventure_logs']['gumball_machine']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('扭蛋机完成', ind=ind)
        else:
            user_print('扭蛋机未完成', ind=ind)

    def adventure_fights(self, ind=2):
        ''' 冒险挑战 '''
        user_print('冒险挑战开始', ind=ind)
        todo = self.record['functions']['adventure_logs']['adventure_fights']['todo']
        if todo != 'true':
            user_print('冒险挑战跳过', ind=ind)
            return
        att = 0
        total_changes = 3
        total_fights = 3
        cur_changes = self.record['functions']['adventure_logs']['adventure_fights']['current_changes']
        cur_fights = self.record['functions']['adventure_logs']['adventure_fights']['current_fights']
        done = self.record['functions']['adventure_logs']['adventure_fights']['done']
        if cur_fights == total_fights:
            done = 1
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/gn.png', name='功能', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz.png', name='冒险日志', ind=ind+1)
            if not f2:
                self.back_to_home(ind=ind+1)
                continue
            f3, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_mxtz.png', name='冒险挑战', ind=ind+1)
            if not f3: continue
            while cur_fights < total_fights:
                found, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_mxtz_jf10.png', name='低分海贼', n_clicks=0, ind=ind+1)
                # 低积分海贼
                if found:
                    user_print('发现低分海贼', ind=ind+1)
                    # 还可免费更改
                    if cur_changes < total_changes:
                        user_print('更换海贼', ind=ind+1)
                        self.find_and_click(img_path='./tasks/gn_mxrz_mxtz_cxmb.png', name='重选目标', ind=ind+1)
                        cur_changes += 1
                    # 只能打了
                    else:
                        user_print('攻打低分海贼', ind=ind+1)
                        self.find_and_click(img_path='./tasks/gn_mxrz_mxtz_fqtz.png', name='发起挑战', ind=ind+1)
                        pag.click()
                        cur_fights += 1
                # 高积分海贼: 直接打
                else:
                    user_print('发现高分海贼', ind=ind+1)
                    self.find_and_click(img_path='./tasks/gn_mxrz_mxtz_fqtz.png', name='发起挑战', ind=ind+1)
                    pag.click()
                    cur_fights += 1
            self.find_and_click(img_path='./tasks/gn_mxrz_mxtz_fh.png', name='返回', ind=ind+1)
            if cur_fights == total_fights:
                self.record['functions']['adventure_logs']['adventure_fights']['current_changes'] = 3
                self.record['functions']['adventure_logs']['adventure_fights']['current_fights'] = 3
                self.record['functions']['adventure_logs']['adventure_fights']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('冒险挑战完成', ind=ind)
        else:
            user_print('冒险挑战未完成', ind=ind)

    def forest_adventure(self, ind=0):
        ''' 密林冒险 '''
        user_print('密林冒险开始')
        done = self.record['forest_adventure']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/rc.png', name='日常', ind=ind+1)
            f1, fpx, fpy = self.find_and_click(img_path='./tasks/zl.png', name='固定点', n_clicks=0, ind=ind+1)
            f2, _, _ = self.drag_find_and_click(fp=[fpx, fpy + 0.5*DPM], dragto=[-DPM, 0], dir=0, img_path='./tasks/rc_mlmx.png', name="密林冒险", ind=ind+1, n_clicks=1)
            
            f3, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_cz.png', name='重置', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_cz_qd.png', name='重置确定', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_ksyd.png', name='快速移动', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_ksyd_qd.png', name='快速移动确定', ind=ind+1)
            f7, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_ksyd_qd_qd.png', name='快速移动确定确定', ind=ind+1)
            
            f8, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd.png', name='扫荡', ind=ind+1)
            f9, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_-.png', name='-', ind=ind+1)
            f10, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_kssd.png', name='快速扫荡', ind=ind+1)
            time.sleep(90)
            f11, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_kssd_wcsd.png', name='完成扫荡', ind=ind+1)
            f12, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_kssd_wcsd_tcgm.png', name='退出购买', ind=ind+1)
            f13, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_fh.png', name='退出密林', ind=ind+1)
            finished = f0 and f1 and f2 and f3 and f4 and f5 and f6 and f7 and f8 and f9 and f10 and f11 and f12 and f13
            if finished and not self.test:
                self.record['forest_adventure'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('密林冒险完成', ind=ind)
        else:
            user_print('密林冒险未完成', ind=ind)

    def boyos(self, ind=0):
        ''' 伙伴 '''
        user_print('伙伴开始', ind=ind)
        self.train_boyo()
        user_print('伙伴完成', ind=ind)
    def train_boyo(self, ind=1):
        ''' 伙伴培养 '''
        user_print('伙伴培养开始', ind=ind)
        done = self.record['boyos']['train_boyo']['done']
        hz_name = self.record['boyos']['train_boyo']['hz_name']
        timed = self.record['boyos']['train_boyo']['timed']
        if timed == 'true':
            timed = True
        else:
            timed = False
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/hb.png', name='伙伴', ind=ind+1)
            if not f1: continue
            hz_path = './tasks/hb_' + hz_name + '.png'
            f2, _, _ = self.find_and_click(img_path=hz_path, name='待培养海贼', ind=ind+1)
            if not f2: continue
            f3 = False
            while not f3:
                f3, _, _ = self.find_and_click(img_path='./tasks/hb_py.png', name='培养', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/hb_py_djpy.png', name='道具培养', ind=ind+1)
            if not f4: continue
            f5, _, _ = self.find_and_click(img_path='./tasks/hb_py_djpy_py.png', name='自动培养培养', ind=ind+1)
            if not f5: continue
            if not timed:
                time.sleep(60)
                f6 = False
                while not f6:
                    f6, _, _ = self.find_and_click(img_path='./tasks/hb_pyhb_tc.png', name='结束培养', ind=ind+1)
            else:
                time.sleep(5)
                f7 = False
                while not f7:
                    f7, _, _ = self.back_to_home(ind=ind+1, n_clicks=5)
            if not self.test:
                self.record['boyos']['train_boyo']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('伙伴培养完成', ind=ind)
        else:
            user_print('伙伴培养未完成', ind=ind)
    


    def recruit(self, is_final=False, ind=0):
        ''' 招募 '''
        user_print('招募开始', ind=ind)
        self.rc_recruit(is_final=is_final)
        user_print('招募完成', ind=ind)


    def rc_recruit(self, is_final=False, ind=1):
        ''' 日常招募 '''
        user_print('日常招募开始', ind=ind)
        self.bw_recruit(is_final=is_final)
        # self.qw_recruit()
        user_print('日常招募完成', ind=ind)
        

    def bw_recruit(self, is_final=False, ind=2):
        ''' 百万招募 '''
        user_print('百万招募开始', ind=ind)
        done = self.record['recruit']['rc_recruit']['bw']['done']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, hx, hy = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/recruit.png', name='招募', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/recruit_rc.png', name='日常招募', ind=ind+1)
            if not f2: continue
            f3, _, _ = self.find_and_click(img_path='./tasks/recruit_rc_bw.png', name='百万招募', ind=ind+1)
            if not f3:
                self.move_and_click(pos=[hx, hy])
                continue
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/recruit_rc_bw_tc.png', name='退出', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/recruit_dj.png', name='道具', ind=ind+1)
            self.find_and_click(img_path='./tasks/recruit_dj_qd.png', name='确定', mute=True, ind=ind+1)
            
            done = 1
            if not self.test and is_final:
                self.record['recruit']['rc_recruit']['bw']['done'] = 1
                self.save_to_json()
        if done == 1:
            user_print('百万招募完成', ind=ind)
        else:
            user_print('百万招募未完成', ind=ind)
    def qw_recruit(self, ind=2):
        ''' 千万招募 '''
        user_print('千万招募开始', ind=ind)
        done = self.record['recruit']['rc_recruit']['qw']['done']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, hx, hy = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/recruit.png', name='招募', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/recruit_rc.png', name='日常招募', ind=ind+1)
            if not f2: continue
            f3, _, _ = self.find_and_click(img_path='./tasks/recruit_rc_qw.png', name='千万招募', ind=ind+1)
            if not f3:
                self.move_and_click(pos=[hx, hy])
                continue
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/recruit_rc_bw_tc.png', name='退出', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/recruit_dj.png', name='道具', ind=ind+1)
            self.find_and_click(img_path='./tasks/recruit_dj_qd.png', name='确定', mute=True, ind=ind+1)
            
            if not self.test:
                self.record['recruit']['rc_recruit']['bw']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('千万招募完成', ind=ind)
        else:
            user_print('千万招募未完成', ind=ind)


    def cabin(self, ind=0):
        ''' 船舱 '''
        user_print('船舱开始', ind=ind)
        # self.cruise()
        self.factory()
        user_print('船舱完成', ind=ind)

    
    def cruise(self, ind=1):
        ''' 巡航 '''
        user_print('巡航开始', ind=ind)
        todo = self.record['cabin']['cruise']['todo']
        if todo != "true":
            user_print('巡航跳过', ind=ind)
            return
        done = self.record['cabin']['cruise']['done']
        zone = self.record['cabin']['cruise']['zone']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/cabin.png', name='船舱', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/cabin_hhs.png', name='航海室', ind=ind+1)
            if not f2: continue
            f3, _, _ = self.find_and_click(img_path='./tasks/cabin_hhs_xhhy.png', name='巡航海域', ind=ind+1)
            if not f3: continue
            zone_path = './tasks/cabin_hhs_xhhy_' + zone + '.png'
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path=zone_path, name='巡航', ind=ind+1)
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/cabin_hhs_xhhy_lqjl.png', name='领取奖励', ind=ind+1)
            f6 = False
            while not f6:
                f6, _, _ = self.find_and_click(img_path='./tasks/cabin_hhs_xhhy_lqjl_lq.png', name='领取', n_clicks=2, ind=ind+1)
            f7 = False
            while not f7:
                f7, _, _ = self.find_and_click(img_path='./tasks/cabin_hhs_xhhy_' + zone + '_ksxh.png', name='开始巡航', ind=ind+1)
            f8 = False
            while not f8:
                f8, _, _ = self.find_and_click(img_path='./tasks/cabin_hhs_xhhy_' + zone + '_fh.png', name='返回', ind=ind+1)
            f9 = False
            while not f9:
                f9, _, _ = self.find_and_click(img_path='./tasks/cabin_hhs_xhhy_fh.png', name='返回', ind=ind+1)
            if not self.test:
                self.record['cabin']['cruise']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('巡航完成', ind=ind)
        else:
            user_print('巡航未完成', ind=ind)
    
    def factory(self, ind=1):
        ''' 工厂 '''
        user_print('工厂开始', ind=ind)
        todo = self.record['cabin']['factory']['todo']
        if todo != "true":
            user_print('工厂跳过', ind=ind)
            return
        done = self.record['cabin']['factory']['done']
        zone = self.record['cabin']['factory']['zone']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/cabin.png', name='船舱', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/cabin_gc.png', name='工厂', ind=ind+1)
            if not f2: continue
            f3, _, _ = self.find_and_click(img_path='./tasks/cabin_gc_sjt.png', name='升级台', ind=ind+1)
            if not f3: continue
            zone_path = './tasks/cabin_gc_sjt_' + zone + '.png'
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path=zone_path, name='升级区域', ind=ind+1)
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/cabin_gc_sjt_sj.png', name='升级', ind=ind+1)
            self.find_and_click(img_path='./tasks/cabin_gc_sjt_sj_tc.png', name='退出', mute=True, ind=ind+1)
            f6 = False
            while not f6:
                f6, _, _ = self.find_and_click(img_path='./tasks/cabin_gc_sjt_fh.png', name='返回', mute=True, ind=ind+1)
            if not self.test:
                self.record['cabin']['factory']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('工厂完成', ind=ind)
        else:
            user_print('工厂未完成', ind=ind)



    def bag(self, ind=0):
        ''' 背包 '''
        user_print('背包开始', ind=ind)
        self.pet()
        self.assistance_punch()
        user_print('背包完成', ind=ind)


    def pet(self, ind=1):
        ''' 宠物 '''
        user_print('宠物开始', ind=ind)
        self.play_with_pet()
        self.pet_growing()
        user_print('宠物完成', ind=ind)

    def play_with_pet(self, ind=2):
        ''' 好感度 updated'''
        user_print('好感度开始', ind=ind)
        done = self.record['bag']['pet']['play_with_pet']['done']
        pet_name = self.record['bag']['pet']['play_with_pet']['pet_name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/bag.png', name='背包', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/bag_pet.png', name='宠物', ind=ind+1)
            if not f2: continue
            self.find_and_click(img_path='./tasks/bag_pet_qd.png', name='确定', mute=True, ind=ind+1)
            pet_path = './tasks/bag_pet_' + pet_name + '.png'
            f3, _, _ = self.find_and_click(img_path=pet_path, name='主宠', offset=[3.9*DPM,0.2*DPM], ind=ind+1)
            if not f3: continue
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/bag_pet_hg.png', name='好感', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/bag_pet_hg_yjwy.png', name='一键喂养', ind=ind+1)
            if not f5: continue
            if not self.test:
                self.record['bag']['pet']['play_with_pet']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('好感度完成', ind=ind)
        else:
            user_print('好感度未完成', ind=ind)

    def pet_growing(self, ind=2):
        ''' 升级 '''
        user_print('升级开始', ind=ind)
        done = self.record['bag']['pet']['pet_growing']['done']
        pet_name = self.record['bag']['pet']['pet_growing']['pet_name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/bag.png', name='背包', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/bag_pet.png', name='宠物', ind=ind+1)
            if not f2: continue
            self.find_and_click(img_path='./tasks/bag_pet_qd.png', name='确定', mute=True, ind=ind+1)
            pet_path = './tasks/bag_pet_' + pet_name + '.png'
            f3, _, _ = self.find_and_click(img_path=pet_path, name='副宠', offset=[3.9*DPM,0.2*DPM], ind=ind+1)
            if not f3: continue
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/bag_pet_sj.png', name='升级', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/bag_pet_sj_zdtj.png', name='自动添加', ind=ind+1)
            if not f6: continue
            f7, _, _ = self.find_and_click(img_path='./tasks/bag_pet_sj_yjsj.png', name='一键升级', ind=ind+1)
            if not f7:
                continue
            if not self.test:
                self.record['bag']['pet']['pet_growing']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('升级完成', ind=ind)
        else:
            user_print('升级未完成', ind=ind)


    def assistance_punch(self, ind=0):
        user_print('援助招式开始')
        todo = self.record['assistance_punch']['todo']
        if todo != "true":
            user_print('援助招式跳过')
            return
        ''' 援助招式 '''
        done = self.record['assistance_punch']['done']
        zs_name = self.record['assistance_punch']['name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/bag.png', name='背包', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/bag_zs.png', name='招式', ind=ind+1)
            if not f2: continue
            f3, _, _ = self.find_and_click(img_path='./tasks/bag_zs_yzzssp.png', name='援助招式碎片', ind=ind+1)
            if not f3: continue
            zs_path = './tasks/bag_zs_' + zs_name + '.png'
            f4, _, _ = self.find_and_click(img_path=zs_path, name='招式', ind=ind+1)
            if not f4: continue
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/bag_zs_hqtj.png', name='获取途径', ind=ind+1)
            f6 = False
            while not f6:
                f6, _, _ = self.find_and_click(img_path='./tasks/bag_zs_qw.png', name='前往', ind=ind+1)
            zs_avatar_path = './tasks/bag_zs_avatar_' + zs_name + '.png'
            f7 = False
            while not f7:
                f7, _, _ = self.find_and_click(img_path=zs_avatar_path, name='招式', ind=ind+1)
            f8 = False
            while not f8:
                f8, _, _ = self.find_and_click(img_path='./tasks/bag_zs_yjxl.png', name='一键训练', ind=ind+1)
            f9 = False
            while not f9:
                f9, _, _ = self.find_and_click(img_path='./tasks/bag_zs_yjxl_qd.png', name='确定', ind=ind+1)
            time.sleep(2*MID_PAUSE)
            f10 = False
            while not f10:
                f10, _, _ = self.find_and_click(img_path='./tasks/bag_zs_fh2.png', name='返回', ind=ind+1)
            
            f11 = False
            while not f11:
                f11, _, _ = self.find_and_click(img_path='./tasks/bag_zs_xllb.png', name='训练礼包', ind=ind+1)
            f12 = False
            while not f12:
                f12, _, _ = self.find_and_click(img_path='./tasks/bag_zs_xllb_+100.png', name='+100', ind=ind+1, n_clicks=7)
            f13 = False
            while not f13:
                f13, _, _ = self.find_and_click(img_path='./tasks/bag_zs_xllb_qr.png', name='确认', ind=ind+1)
            f14 = False
            while not f14:
                f14, _, _ = self.find_and_click(img_path='./tasks/bag_zs_xllb_qr_qd.png', name='确定', ind=ind+1)
            f15 = False
            while not f15:
                f15, _, _ = self.find_and_click(img_path='./tasks/bag_zs_xllb_fh.png', name='返回', ind=ind+1)
            f16 = False
            while not f16:
                f16, _, _ = self.find_and_click(img_path='./tasks/bag_zs_fh.png', name='返回', ind=ind+1)
            f17 = False
            while not f17:
                f17, _, _ = self.find_and_click(img_path='./tasks/bag_zs_fh2.png', name='返回', ind=ind+1)
            f18 = False
            while not f18:
                f18, _, _ = self.find_and_click(img_path='./tasks/bag_zs_fh3.png', name='返回', ind=ind+1)
            att += 1
            if not self.test:
                self.record['assistance_punch']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('援助招式完成', ind=ind)
        else:
            user_print('援助招式未完成', ind=ind)
    


    def adventure(self, ind=0):
        ''' 冒险 '''
        user_print('日常开始', ind=ind)
        self.elite_task()
        self.awaken_task()
        user_print('日常完成', ind=ind)
    def elite_task(self, ind=1):
        ''' 精英副本 '''
        user_print('精英副本开始', ind=ind)
        done = self.record['adventure']['elite_task']['done']
        hz_name = self.record['adventure']['elite_task']['hz_name']
        task_name = self.record['adventure']['elite_task']['task_name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/hb.png', name='伙伴', ind=ind+1)
            if not f1: continue
            f2, fpx, fpy = self.find_and_click(img_path='./tasks/hb_wzm.png', name='未招募', ind=ind+1)
            if not f2: continue
            fpx, fpy = fpx, fpy + 2 * DPM
            hz_path = './tasks/hb_' + hz_name + '.png'
            f3, _, _ = self.drag_find_and_click(fp=[fpx, fpy + 4 * DPM], dragto=[0, -2 * DPM], dir=1, dx=2, img_path=hz_path, name='海贼', ind=ind+1)
            if not f3: continue
            f4 = False
            while not f4:
                f4, _, _ = self.find_and_click(img_path='./tasks/hb_hqtj.png', name='获取途径', ind=ind+1)
            f5 = False
            fpx, fpy = 0, 0
            while not f5:
                f5, fpx, fpy = self.find_and_click(img_path='./tasks/hb_hqtj_fp.png', name='固定点', ind=ind+1)
            fpx, fpy = fpx, fpy + 2 * DPM
            elite_task_path = './tasks/adventure_elite_' + task_name + '.png'
            f6 = False
            while not f6:
                f6, _, _ = self.drag_find_and_click(fp=[fpx, fpy], dragto=[0, -DPM], dir=1, dx=2, img_path=elite_task_path, offset=[3*DPM, 0], name='精英副本', ind=ind+1)
            f7, _, _ = self.find_and_click(img_path='./tasks/adventure_elite_fight.png', name='开始副本', ind=ind+1)
            if not f7: continue
            f8 = False
            while not f8:
                f8, _, _ = self.find_and_click(img_path='./tasks/adventure_elite_fight_3times.png', name='扫荡三次', ind=ind+1)
            time.sleep(MID_PAUSE)
            f9 = False
            while not f9:
                f9, _, _ = self.find_and_click(img_path='./tasks/adventure_elite_fight_end.png', name='扫荡结束', ind=ind+1)
            if not self.test:
                self.record['adventure']['elite_task']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('精英副本完成', ind=ind)
        else:
            user_print('精英副本未完成', ind=ind)


    def awaken_task(self, ind=1):
        ''' 觉醒副本 '''
        user_print('觉醒副本开始', ind=ind)
        done = self.record['adventure']['awaken_task']['done']
        item_name = self.record['adventure']['awaken_task']['item_name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/bag.png', name='背包', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/bag_jx.png', name='觉醒', ind=ind+1)
            if not f2: continue
            f3, fpx, fpy = self.find_and_click(img_path='./tasks/bag_jx_fp.png', name='固定点', n_clicks=0, ind=ind+1)
            if not f3: continue
            fpx, fpy = fpx, fpy + 6 * DPM
            item_path = './tasks/bag_jx_' + item_name + '.png'
            f4, _, _ = self.drag_find_and_click(fp=[fpx, fpy], dragto=[0, -2 * DPM], dir=1, dx=1, img_path=item_path, offset=[4*DPM, 0], name='觉醒材料', ind=ind+1)
            if not f4: continue
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/bag_jx_yjsd.png', name='一键扫荡', ind=ind+1)
            f6 = False
            while not f6:
                f6, _, _ = self.find_and_click(img_path='./tasks/bag_jx_yjsd_-10.png', name='-10', n_clicks=10, ind=ind+1)
            f7 = False
            while not f7:
                f7, _, _ = self.find_and_click(img_path='./tasks/bag_jx_yjsd_+.png', name='+', n_clicks=4, ind=ind+1)
            f8 = False
            while not f8:
                f8, _, _ = self.find_and_click(img_path='./tasks/bag_jx_yjsd_qd.png', name='确定', ind=ind+1)
            f9 = False
            while not f9:
                f9, _, _ = self.find_and_click(img_path='./tasks/bag_jx_yjsd_sdjs.png', name='扫荡结束', ind=ind+1)
            
            if not self.test:
                self.record['adventure']['awaken_task']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('精英副本完成', ind=ind)
        else:
            user_print('精英副本未完成', ind=ind)


    def routine(self, ind=0):
        ''' 日常 '''
        user_print('日常开始', ind=ind)
        self.bullfight()
        self.SOP()
        user_print('日常完成', ind=ind)
    # NOT YET
    def bullfight(self, ind=1):
        ''' 斗牛竞技场 '''
        user_print('斗牛竞技场开始', ind=ind)
        todo = self.record['routine']['bullfight']['todo']
        if todo != "true":
            user_print('斗牛竞技场跳过', ind=ind)
            return
        done = self.record['routine']['bullfight']['done']
        hz_name = self.record['routine']['bullfight']['hz_name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/hb.png', name='伙伴', ind=ind+1)
            hz_path = './tasks/hb_' + hz_name + '.png'
            f2, _, _ = self.find_and_click(img_path=hz_path, name='海贼', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./tasks/hb_yz.png', name='意志', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/hb_yz_yzjj.png', name='意志结晶', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/hb_yz_yzjj_qw.png', name='前往', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_cz.png', name='重置', ind=ind+1)
            f7, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_cz_qr.png', name='重置确认', ind=ind+1)
            finished1 = f1 and f2 and f3 and f4 and f5 and f6
            fcs, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_tzcs.png', name='挑战次数', ind=ind+1, n_clicks=0)
            while not fcs:
                f8, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_sd.png', name='扫荡', ind=ind+1)
                f9, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_sd_qd.png', name='确定', ind=ind+1)
                time.sleep(5)
                f10, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_sd_qd_sdjs.png', name='扫荡结束', ind=ind+1)
                f11, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_mfkq.png', name='免费开启', ind=ind+1)
                f12, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_mfkq_gb.png', name='关闭', ind=ind+1)
                f13, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_xyg.png', name='下一关', ind=ind+1)
                fcs, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_tzcs.png', name='挑战次数', ind=ind+1)
            
            if fcs:
                f14, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_mrbx.png', name='每日宝箱', ind=ind+1)
                f15, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_mrbx_yzjj.png', name='意志结晶', offset=[0, DPM], ind=ind+1)
                if f15:
                    f16, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_mrbx_qrkq.png', name='确认开启', ind=ind+1)
                    f17, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_mrbx_qd.png', name='确定', ind=ind+1)
                f18, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_mrbx_fh.png', name='返回', ind=ind+1)
            f19, _, _ = self.find_and_click(img_path='./tasks/routine_bullfight_fh.png', name='返回', ind=ind+1)
            f20, _, _ = self.find_and_click(img_path='./tasks/hb_yz_yzjj_fh', name='返回', ind=ind+1)
            f21, _, _ = self.find_and_click(img_path='./tasks/hb_yz_fh', name='返回', ind=ind+1)
            finished2 = fcs and f19 and f20 and f21
            finished = finished1 and finished2
            if finished and not self.test:
                self.record['routine']['bullfight']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('斗牛竞技场完成', ind=ind)
        else:
            user_print('斗牛竞技场未完成', ind=ind)
    # NOT YET
    def SOP(self, ind=1):
        ''' SOP大作战 '''
        todo = self.record['routine']['SOP']['todo']
        if todo != "true":
            return
        user_print('SOP大作战开始', ind=ind)
        done = self.record['routine']['SOP']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            self.back_to_home(ind=ind+1)
            f0, _, _ = self.find_and_click(img_path='./tasks/gn.png', name='功能', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/gn_hjk.png', name='环境卡', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fsqqh.png', name='发射器强化', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fsqqh_djsls.png', name='低级试炼石', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fsqqh_djsls_qw.png', name='前往', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/routine_SOP_y.png', name='摇', ind=ind+1)
            # todo
            f7, _, _ = self.find_and_click(img_path='./tasks/routine_SOP_fh.png', name='返回', ind=ind+1)
            f8, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fsqqh_djsls_tc.png', name='退出', ind=ind+1)
            f9, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fsqqh_fh.png', name='返回', ind=ind+1)
            f10, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fh.png', name='返回', ind=ind+1)
            
            self.back_to_home(ind=ind+1)
            f11, _, _ = self.find_and_click(img_path='./tasks/gn.png', name='功能', ind=ind+1)
            f12, _, _ = self.find_and_click(img_path='./tasks/gn_hjk.png', name='环境卡', ind=ind+1)
            f13, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fsqqh.png', name='发射器强化', ind=ind+1)
            f14, _, _ = self.find_and_click(img_path='./tasks/gn_hjk_fsqqh_qbxh.png', name='全部消耗', ind=ind+1)

            finished = f0 and f1 and f2 and f4 and f5 and f6 and f7 and f8 and f9 and f10 and f11 and f12 and f13 and f14
            if finished and not self.test:
                self.record['routine']['SOP'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('SOP大作战完成', ind=ind)
        else:
            user_print('SOP大作战未完成', ind=ind)



    def lineup(self, ind=0):
        ''' 阵容 '''
        user_print('阵容开始', ind=ind)
        self.accessory_strengthen()             
        self.equipment_enchant()                
        user_print('阵容完成', ind=ind)


    def accessory_strengthen(self, ind=1):
        ''' 饰品强化 '''
        user_print('饰品强化开始', ind=ind)
        done = self.record['lineup']['accessory_strengthen']['done']
        if self.test:
            done = 0
        hz_name = self.record['lineup']['accessory_strengthen']['hz_name']
        sp_name = self.record['lineup']['accessory_strengthen']['sp_name']
        quality = self.record['lineup']['accessory_strengthen']['quality']
        att = 0
        if quality == 'high':
            while done != 1 and att < MAX_ATTEMPTS:
                att += 1
                f0, _, _ = self.back_to_home(ind=ind+1)
                if not f0: continue
                f1, _, _ = self.find_and_click(img_path='./tasks/zr.png', name='阵容', ind=ind+1)
                if not f1: continue
                # if it is the target already: no need to search for avatar
                hz_text_path = './tasks/zr_text_' + hz_name + '.png'
                f2, _, _ = self.find_and_click(img_path=hz_text_path, name='寻找海贼', ind=ind+1, n_clicks=0)
                if not f2:
                    avatar_path = './tasks/zr_avatar_' + hz_name + '.png'
                    f3, _, _ = self.find_and_click(img_path=avatar_path, name='选择海贼', ind=ind+1)
                    if not f3: continue
                sp_path = './tasks/zr_sp_' + sp_name + '.png'
                f4, _, _ = self.find_and_click(img_path=sp_path, name='选择饰品', ind=ind+1)
                if not f4: continue
                f5 = False
                while not f5:
                    f5, _, _ = self.find_and_click(img_path='./tasks/zr_sp_spqh.png', name='强化', ind=ind+1)
                for i in range(5):
                    self.find_and_click(img_path='./tasks/zr_sp_spqh_zdtj.png', name='自动添加', ind=ind+1)
                    self.find_and_click(img_path='./tasks/zr_sp_spqh_yjqh.png', name='一键强化', ind=ind+1)
                if not self.test:
                    self.record['lineup']['accessory_strengthen']['done'] = 1
                    done = 1
                    self.save_to_json()
        else:
            while done != 1 and att < MAX_ATTEMPTS:
                att += 1
                f0, _, _ = self.back_to_home(ind=ind+1)
                if not f0: continue
                f1, _, _ = self.find_and_click(img_path='./tasks/zr.png', name='阵容', ind=ind+1)
                if not f1: continue
                # if it is the target already: no need to search for avatar
                hz_text_path = './tasks/zr_text_' + hz_name + '.png'
                f2, _, _ = self.find_and_click(img_path=hz_text_path, name='寻找海贼', ind=ind+1, n_clicks=0)
                if not f2:
                    avatar_path = './tasks/zr_avatar_' + hz_name + '.png'
                    f3, _, _ = self.find_and_click(img_path=avatar_path, name='选择海贼', ind=ind+1)
                    if not f3: continue
                sp_path = './tasks/zr_sp_' + sp_name + '.png'
                f4, spx, spy = self.find_and_click(img_path=sp_path, name='选择饰品', ind=ind+1)
                if not f4: continue
                f5 = False
                while not f5:
                    f5, _, _ = self.find_and_click(img_path='./tasks/zr_sp_gh.png', name='更换', ind=ind+1)
                f6, fpx, fpy = self.find_and_click(img_path='./tasks/zr_sp_gh_fp.png', name='拖动', ind=ind+1)
                if not f6: continue
                fpx, fpy = fpx, fpy + 6 * DPM
                f7, _, _ = self.drag_find_and_click(fp=[fpx, fpy], dir=1, dragto=[0, -4*DPM], dx=2, n_drags=10)
                if not f7: continue
                time.sleep(5*SHORT_PAUSE)
                f8, _, _ = self.find_and_click(img_path='./tasks/zr_sp_gh_zb.png', name='装备', ind=ind+1)
                if not f8: continue
                time.sleep(5*SHORT_PAUSE)
                self.move_and_click(pos=[spx, spy])
                f9 = False
                while not f9:
                    f9, _, _ = self.find_and_click(img_path='./tasks/zr_sp_spqh.png', name='饰品强化', ind=ind+1)
                for i in range(5):
                    self.find_and_click(img_path='./tasks/zr_sp_spqh_zdtj.png', name='自动添加', ind=ind+1)
                    self.find_and_click(img_path='./tasks/zr_sp_spqh_yjqh.png', name='一键强化', ind=ind+1)
                f0, _, _ = self.back_to_home(ind=ind+1)
                if not f0: continue
                f1, _, _ = self.find_and_click(img_path='./tasks/zr.png', name='阵容', ind=ind+1)
                if not f1: continue
                # if it is the target already: no need to search for avatar
                hz_text_path = './tasks/zr_text_' + hz_name + '.png'
                f2, _, _ = self.find_and_click(img_path=hz_text_path, name='寻找海贼', ind=ind+1, n_clicks=0)
                if not f2:
                    avatar_path = './tasks/zr_avatar_' + hz_name + '.png'
                    f3, _, _ = self.find_and_click(img_path=avatar_path, name='选择海贼', ind=ind+1)
                    if not f3: continue
                self.move_and_click(pos=[spx, spy])
                f5 = False
                while not f5:
                    f5, _, _ = self.find_and_click(img_path='./tasks/zr_sp_gh.png', name='更换', ind=ind+1)
                f8, _, _ = self.find_and_click(img_path='./tasks/zr_sp_gh_zb.png', name='装备', ind=ind+1)
                if not f8: continue
                if not self.test:
                    self.record['lineup']['accessory_strengthen']['done'] = 1
                    done = 1
                    self.save_to_json()
        if done == 1:
            user_print('饰品强化完成', ind=ind)
        else:
            user_print('饰品强化未完成', ind=ind)

    def equipment_enchant(self, ind=1):
        ''' 装备附魔 '''
        user_print('装备附魔开始', ind=ind)
        done = self.record['lineup']['equipment_enchant']['done']
        if self.test:
            done = 0
        hz_name = self.record['lineup']['equipment_enchant']['hz_name']
        zb_name = self.record['lineup']['equipment_enchant']['zb_name']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/zr.png', name='阵容', ind=ind+1)
            # if it is the target already: no need to search for avatar
            hz_text_path = './tasks/zr_text_' + hz_name + '.png'
            f2, _, _ = self.find_and_click(img_path=hz_text_path, name='寻找海贼', ind=ind+1, n_clicks=0)
            if not f2:
                avatar_path = './tasks/zr_avatar_' + hz_name + '.png'
                f3, _, _ = self.find_and_click(img_path=avatar_path, name='选择海贼', ind=ind+1)
                if not f3: continue
            zb_path = './tasks/zr_zb_' + zb_name + '.png'
            f4, _, _ = self.find_and_click(img_path=zb_path, name='选择装备', ind=ind+1)
            if not f4: continue
            f5 = False
            while not f5:
                f5, _, _ = self.find_and_click(img_path='./tasks/zr_zb_fm.png', name='附魔', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/zr_zb_fm_yjfm.png', name='一键附魔', ind=ind+1)
            if not f6: continue
            f7 = False
            while not f7:
                f7, _, _ = self.find_and_click(img_path='./tasks/zr_zb_fm_yjfm_+10.png', name='+10', ind=ind+1)
            f8 = False
            while not f8:
                f8, _, _ = self.find_and_click(img_path='./tasks/zr_zb_fm_yjfm_qd.png', name='确定', ind=ind+1)
            if not self.test:
                self.record['lineup']['equipment_enchant']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('装备附魔完成', ind=ind)
        else:
            user_print('装备附魔未完成', ind=ind)



    def save_to_json(self):
        ''' 保存 '''
        with open("tmp.json", "w") as jsonFile:
            json.dump(self.record, jsonFile, indent=4)
        # if Windows
        if os.name == 'nt':
            del_command = 'del ' + 'checklist_' + self.role + '.json'
            os.system(del_command)
            time.sleep(3)
            rename_command = 'ren tmp.json checklist_' + self.role + '.json'
            os.system(rename_command)
        else:
            if HIGH_LEVEL:
                os.system('rm checklist.json')
                time.sleep(3)
                os.system('mv tmp.json checklist.json')
            else:
                os.system('rm tmp.json')
                time.sleep(3)
                os.system('mv tmp.json checklist.json')

    

    def cross_servers(self, ind=0):
        ''' 跨服 '''
        user_print('跨服开始', ind=ind)
        self.treasures()
        user_print('跨服完成', ind=ind)
    def treasures(self, ind=1):
        ''' 宝藏争夺 '''
        user_print('宝藏争夺开始', ind=ind)
        done = self.record['cross_servers']['treasures']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/kf.png', name='跨服', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/kf_bzzd.png', name='宝藏争夺', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/kf_bzzd_lj.png', name='领取', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./tasks/kf_bzzd_lj_qd.png', name='确定', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/kf_bzzd_fh.png', name='返回', ind=ind+1)
            finished = f0 and f1 and f2 and f3 and f4
            if finished:
                self.record['cross_servers']['treasures'] = 1
                done = 1
                self.save_to_json()
            else:
                self.find_and_click(img_path='./tasks/kf_bzzd_fh.png', name='返回', ind=ind+1)
        if done == 1:
            user_print('宝藏争夺完成', ind=ind)
        else:
            user_print('宝藏争夺未完成', ind=ind)



    def get_task_reward(self, is_final=False, ind=0):
        ''' 任务领奖 '''
        user_print('任务领奖开始', ind=ind)
        done = self.record['get_task_reward']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            att += 1
            f0, _, _ = self.back_to_home(ind=ind+1)
            if not f0: continue
            f1, _, _ = self.find_and_click(img_path='./tasks/rw.png', name='任务', ind=ind+1)
            if not f1: continue
            f2, _, _ = self.find_and_click(img_path='./tasks/rw_ljl.png', name='任务领奖', mute=True, ind=ind+1)
            while f2:
                f2, _, _ = self.find_and_click(img_path='./tasks/rw_ljl.png', name='任务领奖', mute=True, ind=ind+1)
            done = 1
            if is_final:
                self.record['get_task_reward'] = 1
                self.save_to_json()
        if done == 1:
            user_print('任务领奖完成', ind=ind)
        else:
            user_print('任务领奖未完成', ind=ind)
    def test(self):
        found, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_mxtz_jf10.png', name='低分海贼', n_clicks=0, ind=2)

    def tmp(self, ind=0):
        _, fpx, fpy = self.find_and_click(img_path='./tasks/mly.png', name='莫利亚', ind=ind+1)
        _, mlyx, mlyy = self.find_and_click(img_path='./tasks/mly_belly.png', name='莫利亚', ind=ind+1, n_clicks=6)
        _, zdx, zdy = self.find_and_click(img_path='./tasks/mly_zd.png', name='战斗', ind=ind+1)
        _, tgx, tgy = self.find_and_click(img_path='./tasks/mly_zd_tg.png', name='跳过', ind=ind+1)
        pag.moveTo(mlyx, mlyy)
        for i in range(2):
            pag.click()
        time.sleep(5)
        pag.moveTo(tgx, tgy)
        pag.click()
        time.sleep(2)
        pag.click()
        while True:
            pag.moveTo(fpx, fpy)
            pag.click()
            pag.moveTo(mlyx, mlyy)
            for i in range(5):
                pag.click()
            pag.moveTo(zdx, zdy)
            pag.click()
            time.sleep(3)
            pag.moveTo(tgx, tgy)
            pag.click()
            pag.moveTo(mlyx, mlyy)
            for i in range(2):
                pag.click()
            pag.moveTo(tgx, tgy)
            pag.click()
            time.sleep(3)
            pag.click()



# import win32gui, win32con
# hwnd = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

ar = AutoRun(role='lf',to_test=False, to_reset=True)
ar.run()
# ar.bw_shop()
# ar.hb_shop()


# todo:  xunhang
# output = list(pag.locateAllOnScreen('./tasks/shop_hbshop_nls.png', confidence=0.9))
# if len(output) > 0:
#     for pos in output:
#         print(pos)
# ar.assistance_punch()
# ar.lineup()
# ar.bullfight()
# ar.elite_task()
# ar.boyos()
# ar.get_coffee()
# ar.tmp()
# ar.bag()
# ar.get_union_bonus()
# todo: qwh

# ar.get_task_reward()
# ar.gumball_machine()
# todo:
'''
add error handling
'''