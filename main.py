SHORT_PAUSE = 1
MID_PAUSE = 10
LONG_PAUSE = 30
N_CLICKS = 10
N_DRAGS = 30
MAX_CONF = 0.95
MIN_CONF = 0.8
DCONF = -0.03
DPM = 100
MAX_ATTEMPTS = 10
level = 93
HIGH_LEVEL = True
if level < 81:
    HIGH_LEVEL = False
import pyautogui as pag
from pynput import mouse
import time
import json
import os

pag.PAUSE = SHORT_PAUSE

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
    def __init__(self, to_test=False, to_reset=True):
        self.test = to_test
        filename = ''
        filename = 'checklist_xl.json'

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
                if not isinstance(val, str):
                    self.reset(val)
    
        
    def move_and_click(self, offset=[0, 0], n_clicks=1):
        pag.move(offset[0], offset[1])
        pag.click(clicks=n_clicks)
    
    def find_and_click(self, img_path='', name='', offset=[0, 0], ind=1, n_clicks=1, pause=SHORT_PAUSE):
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
            pag.PAUSE=SHORT_PAUSE
            time.sleep(3)
            return True, pos.left, pos.top
        else:
            output=name
            output+='未找到'
            user_print(txt=output, ind=ind)
            time.sleep(3)
            return False, 0, 0
    
    def drag_find_and_click(self, fp=[0, 0], dragto=[0, 0], img_path='', name='', offset=[0, 0], ind=1, n_clicks=1, n_drags=1, extra_drag=False):
        if img_path == '':
            for iter in range(n_drags):
                pag.moveTo(fp[0], fp[1])
                pag.drag(dragto[0], dragto[1])
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
                pag.moveTo(fp[0], fp[1])
                time.sleep(1)
                # pag.click()
                time.sleep(1)
                pag.drag(dragto[0], dragto[1])
                # cnt_drags += 1
                time.sleep(1)
                pos = pag.locateOnScreen(img_path, confidence=conf)
        if pos is not None:
            # one more drag is applicable
            if extra_drag:
                for i in range(2):
                    pag.moveTo(fp[0], fp[1])
                    time.sleep(1)
                    # pag.click()
                    time.sleep(1)
                    pag.drag(dragto[0], dragto[1])
                    # cnt_drags += 1
                    time.sleep(1)
            pos = pag.locateOnScreen(img_path, confidence=conf)
            pag.moveTo(pos.left + offset[0], pos.top + offset[1])
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
        if HIGH_LEVEL:
            self.normal_activity()
            self.time_limited_activity()
            self.union()
            self.harbor()
            self.game_assistant()
            self.functions()
            self.daily_tasks()
            self.bag()
            self.forest_adventure()
            self.get_task_reward(is_final=True)
        else:
            self.normal_activity()
            self.time_limited_activity()
            self.union()
            self.bag()
            self.get_task_reward()
    
    def back_to_home(self, ind=0, n_clicks=N_CLICKS):
        ''' 回到主页 '''
        self.find_and_click(img_path='./tasks/bth.png', name='主页', n_clicks=n_clicks, ind=ind)

    def recruit(self, ind=0):
        ''' 招募 '''
        pass

    def normal_activity(self, ind=0):
        ''' 日常任务 '''
        user_print('日常任务开始', ind=ind)
        self.daily_checkin()
        self.buy_bali()
        self.get_vip_gift()
        self.get_daily_gift()
        user_print('日常任务完成', ind=ind)
    def daily_checkin(self, ind=1):
        ''' 每日签到 updated '''
        user_print('每日签到开始', ind=ind)
        done = self.record['normal_activity']['daily_checkin']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            f0, _, _ = self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/na_dci.png', name='每日签到', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/na_dci_lq.png', name='每日签到格', ind=ind+1)
            finished = f0 and f1 and f2
            if not finished:
                finished, _, _ = self.find_and_click(img_path='./tasks/na_dci_lq_b.png', name='每日签到领取', ind=ind+1)
            att += 1
            if finished and not self.test:
                self.record['normal_activity']['daily_checkin'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('每日签到完成', ind=ind)
        else:
            user_print('每日签到未完成', ind=ind)
    def buy_bali(self, ind=1):
        ''' 购买贝里 updated '''
        user_print('购买贝里开始', ind=ind)
        done = self.record['normal_activity']['buy_bali']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 7 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], img_path='./tasks/na_bb.png', name='购买贝里', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/na_bb_bo.png', name='购买贝里一次', ind=ind+1)
            att += 1
            if finished:
                self.record['normal_activity']['buy_bali'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('购买贝里完成', ind=ind)
        else:
            user_print('购买贝里未完成', ind=ind)
    def get_vip_gift(self, ind=1):
        ''' VIP礼物 updated '''
        user_print('VIP礼物开始', ind=ind)
        done = self.record['normal_activity']['get_vip_gift']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 7 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], img_path='./tasks/na_vipg.png', name='VIP礼包', ind=ind+1)
            self.find_and_click(img_path='./tasks/na_vipg_mrg.png', name='VIP每日礼包', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/na_vipg_mrg_lq.png', name='VIP每日礼包领取', ind=ind+1)
            att += 1
            if finished and not self.test:
                self.back_to_home(ind=ind+1, n_clicks=1)
                self.record['normal_activity']['get_vip_gift'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('VIP礼物完成', ind=ind)
        else:
            user_print('VIP礼物未完成', ind=ind)
    def get_daily_gift(self, ind=1):
        '''' 日常礼包 updated '''
        user_print('日常礼包开始', ind=ind)
        self.get_mr_gift()
        # self.get_mz_gift()
        # self.get_my_gift()
        user_print('日常礼包完成', ind=ind)
    def get_mr_gift(self, ind=2):
        ''' 每日礼包 updated '''
        user_print('每日礼包开始', ind=ind)
        done = self.record['normal_activity']['get_daily_gift']['mr']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 7 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], n_drags=8, ind=ind+1)
            self.find_and_click(img_path='./tasks/na_rcg.png', name='日常礼包', ind=ind+1)

            finished, _, _ = self.find_and_click(img_path='./tasks/na_rcg_mrg_mf.png', name='日常礼包每日礼包领取', ind=ind+1)
            # self.find_and_click(img_path='./tasks/na_rcg_mrg_mf_qd.png', name='日常礼包每日礼包领取', ind=ind+1)
            time.sleep(3)
            att += 1
            if finished and not self.test:
                self.back_to_home(ind=ind+1, n_clicks=1)
                self.record['normal_activity']['get_daily_gift']['mr'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('每日礼包完成', ind=ind)
        else:
            user_print('每日礼包未完成', ind=ind)
    def get_mz_gift(self, ind=2):
        ''' 每周礼包 '''
        user_print('每周礼包开始', ind=ind)
        done = self.record['normal_activity']['get_daily_gift']['mz']
        att = 0
        while done != 1 and att < 1:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], n_drags=8, ind=ind+1)
            self.find_and_click(img_path='./tasks/na_rcg.png', name='日常礼包', ind=ind+1)
            self.find_and_click(img_path='./tasks/na_rcg_mzg.png', name='日常礼包每周礼包', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/na_rcg_mzg_mf.png', name='日常礼包每周礼包领取', ind=ind+1)
            time.sleep(3)
            att += 1
            self.record['normal_activity']['get_daily_gift']['mz'] = 1
            done = 1
            self.save_to_json()
        if done == 1:
            user_print('每周礼包完成', ind=ind)
        else:
            user_print('每周礼包未完成', ind=ind)
    def get_my_gift(self, ind=2):
        ''' 每月礼包 '''
        user_print('每月礼包开始', ind=ind)
        done = self.record['normal_activity']['get_daily_gift']['my']
        att = 0
        while done != 1 and att < 1:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], n_drags=8, ind=ind+1)
            self.find_and_click(img_path='./tasks/na_rcg.png', name='日常礼包', ind=ind+1)

            self.find_and_click(img_path='./tasks/na_rcg_myg.png', name='日常礼包每月礼包', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/na_rcg_myg_mf.png', name='日常礼包每月礼包领取', ind=ind+1)
            time.sleep(3)
            att += 1
            self.record['normal_activity']['get_daily_gift']['my'] = 1
            done = 1
            self.save_to_json()
        if done == 1:
            user_print('每月礼包完成', ind=ind)
        else:
            user_print('每月礼包未完成', ind=ind)

    def time_limited_activity(self, ind=0):
        ''' 限时活动 '''
        user_print('限时活动开始', ind=ind)
        # self.consecutive_logins()
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
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/la.png', name='限时活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 7 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], img_path='./tasks/la_lj.png', name='累计登录', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/la_lj_lq.png', name='累计登录领取', n_clicks=1, ind=ind+1)
            # add an offset to quit
            self.move_and_click(offset=[0, 2*DPM], n_clicks=4)
            # todo: add offset
            att += 1
            if finished:
                self.record['time_limited_activity']['consecutive_logins'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('累计登录完成', ind=ind)
        else:
            user_print('累计登录未完成', ind=ind)
    def dollar_shop(self, ind=1):
        ''' 福利商店 updated '''
        user_print('福利商店开始', ind=ind)
        done = self.record['time_limited_activity']['dollar_shop']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/la.png', name='限时活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 7 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], img_path='./tasks/la_fl.png', name='福利商店', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/la_fl_tl.png', name='福利商店购买体力', offset=[3.5*DPM, 0.5*DPM], n_clicks=5, ind=ind+1)
            att += 1
            if finished and not self.test:
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
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/la.png', name='限时活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./tasks/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 7 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-0.5*DPM, 0], img_path='./tasks/la_dj.png', name='道具折扣', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/la_dj_tl.png', name='道具折扣购买体力', offset=[3.5*DPM, 0.5*DPM], n_clicks=5, ind=ind+1)
            att += 1
            if finished and not self.test:
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
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/ga.png', name='游戏助手', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/ga_da.png', name='全部执行', pause=LONG_PAUSE, ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/ga_da_back.png', name='游戏执行完成', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./tasks/ga_da_back_back.png', name='退出游戏助手', ind=ind+1)
            att += 1
            finished = f0 and f1 and f2 and f3
            if finished and not self.test:
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
        self.train_boyo()
        self.accessory_strengthen()
        self.equipment_enchant()

    def accessory_strengthen(self, ind=1):
        ''' 饰品强化 '''
        user_print('饰品强化开始', ind=ind)
        done = self.record['daily_tasks']['accessory_strengthen']['done']
        if self.test:
            done = 0
        name = self.record['daily_tasks']['accessory_strengthen']['name']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            f0, _, _ = self.find_and_click(img_path='./tasks/rw.png', name='任务', ind=ind+1)
            f1, fpx, fpy = ar.find_and_click(img_path='./tasks/rw_cjrw.png', name='固定点', n_clicks=0, ind=ind+1)
            f2, _, _ = ar.drag_find_and_click(fp=[fpx, fpy + 4 * DPM], dragto=[0, -2*DPM], img_path='./tasks/rw_spqh.png', name="饰品强化", offset=[4*DPM,0.5*DPM], ind=ind+1, n_clicks=1)
            sp_path = './tasks/rw_spqh_' + name + '.png'
            f3, _, _ = ar.drag_find_and_click(fp=[fpx, fpy + 4 * DPM], dragto=[0, -2*DPM], img_path=sp_path, name="饰品强化", offset=[3.7*DPM,0.1*DPM], ind=ind+1, n_clicks=1, extra_drag=True)
            
            f4, _, _ = self.find_and_click(img_path='./tasks/rw_spqh_qh.png', name='强化', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/rw_spqh_qh_zdtj.png', name='自动添加', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/rw_spqh_qh_zdtj_yjqh.png', name='一键强化', ind=ind+1)
            finished = f1 and f2 and f3 and f4 and f5 and f6
            if finished and not self.test:
                self.record['daily_tasks']['accessory_strengthen']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('饰品强化完成', ind=ind)
        else:
            user_print('饰品强化未完成', ind=ind)

    def equipment_enchant(self, ind=1):
        ''' 装备附魔 '''
        user_print('装备附魔开始', ind=ind)
        done = self.record['daily_tasks']['equipment_enchant']['done']
        name = self.record['daily_tasks']['equipment_enchant']['name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/rw.png', name='任务', ind=ind+1)
            f1, fpx, fpy = ar.find_and_click(img_path='./tasks/rw_cjrw.png', name='固定点', n_clicks=0, ind=ind+1)
            f2, _, _ = ar.drag_find_and_click(fp=[fpx, fpy + 4 * DPM], dragto=[0, -2*DPM], img_path='./tasks/rw_zbfm.png', name="装备附魔", offset=[4*DPM,0.5*DPM], ind=ind+1, n_clicks=1)
            sp_path = './tasks/rw_zbfm_' + name + '.png'
            f3, _, _ = ar.drag_find_and_click(fp=[fpx, fpy + 4 * DPM], dragto=[0, -2*DPM], img_path=sp_path, name="武装皮靴", ind=ind+1, n_clicks=1, extra_drag=True)
            
            f4, _, _ = self.find_and_click(img_path='./tasks/rw_zbfm_fm.png', name='附魔', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/rw_zbfm_fm_yjfm.png', name='一键附魔', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/rw_zbfm_fm_yjfm_p10.png', name='+10', ind=ind+1)
            f7, _, _ = self.find_and_click(img_path='./tasks/rw_zbfm_fm_yjfm_qd.png', name='确定', ind=ind+1)
            finished = f1 and f2 and f3 and f4 and f5 and f6 and f7
            if finished:
                self.record['daily_tasks']['equipment_enchant']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('装备附魔完成', ind=ind)
        else:
            user_print('装备附魔未完成', ind=ind)

    def union(self, ind=0):
        ''' 工会活动 updated '''
        user_print('工会活动开始', ind=ind)
        self.union_construction()
        self.pirate_wanted()
        # self.official_pirates()
        user_print('工会活动完成', ind=ind)
    def official_pirates(self, ind=1):
        ''' 七武海 '''
        user_print('七武海开始', ind=ind)
        done = self.record['union']['official_pirates']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=LONG_PAUSE, ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/gh_qwh.png', name='七武海', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_jsjl.png', name='击杀奖励', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_jsjl_yjlq.png', name='一键领取', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_jsjl_yjlq_qd.png', name='确定', ind=ind+1)
            time.sleep(5)
            f5, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_jsjl_yjlq_qd_tc.png', name='退出', ind=ind+1)
            time.sleep(5)
            # f6, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_sdqb.png', name='扫荡全部', ind=ind+1)
            # time.sleep(30)
            # f7, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_sdqb_tc.png', name='退出', ind=ind+1)
            f8, _, _ = self.find_and_click(img_path='./tasks/gh_qwh_fh.png', name='返回', ind=ind+1)
            f9, _, _ = self.find_and_click(img_path='./tasks/gh_fh.png', name='返回', ind=ind+1)

            finished = f0 and f1 and f2 and f4 and f5 and f8 and f9
            att += 1
            if finished:
                self.record['union']['official_pirates'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('七武海完成', ind=ind)
        else:
            user_print('七武海未完成', ind=ind)

    def union_construction(self, ind=1):
        ''' 工会建设 updated '''
        user_print('工会建设开始', ind=ind)
        done = self.record['union']['union_construction']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=LONG_PAUSE, ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt.png', name='工会大厅', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_ptjs.png', name='普通建设', offset=[DPM/3, DPM*2.5], ind=ind+1)
            time.sleep(3)
            pag.click()
            f3, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_lq.png', name='领取奖励', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_lq_qd.png', name='确定领取', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_fh.png', name='返回工会大厅', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_fh.png', name='退出公会', ind=ind+1)
            att += 1
            finished = f0 and f1 and f2 and f3 and f4 and f5 and f6
            if finished:
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
            self.back_to_home(ind=ind+1)
            self.find_and_click(img_path='./tasks/gh.png', name='工会', pause=LONG_PAUSE, ind=ind+1)
            self.find_and_click(img_path='./tasks/gh_hdxs.png', name='海盗悬赏', ind=ind+1)
            _, tzx, tzy = self.find_and_click(img_path='./tasks/gh_hdxs_tz.png', name='海盗悬赏挑战', ind=ind+1)
            pag.moveTo(tzx, tzy+DPM)
            pag.click()
            self.find_and_click(img_path='./tasks/gh_hdxs_fh.png', name='退出海盗悬赏', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/gh_ghdt_qwlq_fh.png', name='退出工会', ind=ind+1)
            att += 1
            if finished and not self.test:
                self.record['union']['pirate_wanted'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('海盗悬赏完成', ind=ind)
        else:
            user_print('海盗悬赏未完成', ind=ind)



    def harbor(self, ind=0):
        ''' 港口 updated '''
        user_print('港口开始', ind=ind)
        self.harbor_reward()
        user_print('港口完成', ind=ind)
    def harbor_reward(self, ind=1):
        ''' 港口领奖 updated '''
        user_print('港口领奖开始', ind=ind)
        done = self.record['harbor']['harbor_reward']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/gk.png', name='港口', ind=ind+1)
            self.find_and_click(img_path='./tasks/gk_lj.png', name='港口领奖', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./tasks/gk_lj_qd.png', name='港口领奖确定', ind=ind+1)
            time.sleep(5)
            self.find_and_click(img_path='./tasks/gk_fh.png', name='退出港口', ind=ind+1)
            att += 1
            if finished and not self.test:
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
        ''' 扭蛋机 updated '''
        user_print('扭蛋机开始', ind=ind)
        cur_chances = self.record['functions']['adventure_logs']['gumball_machine']['current_chances']
        done = self.record['functions']['adventure_logs']['gumball_machine']['done']
        total_chances = 3
        att = 0
        if cur_chances == total_chances:
            done = 1
        while done != 1 and att < MAX_ATTEMPTS:
            # TODO
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/gn.png', name='功能', ind=ind+1)
            self.find_and_click(img_path='./tasks/gn_mxrz.png', name='冒险日志', ind=ind+1)
            self.find_and_click(img_path='./tasks/gn_mxrz_ndj.png', name='扭蛋机', ind=ind+1)
            while cur_chances < total_chances:
                f0, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_ndj_tbyc.png', name='投币一次', ind=ind+1)
                f1, _, _ = self.find_and_click(img_path='./tasks/gn_mxrz_ndj_tbyc_qd.png', name='投币确定', ind=ind+1)
                if f0 and f1:
                    cur_chances += 1
            att += 1
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
        # TODO
        ''' 冒险挑战 updated '''
        user_print('冒险挑战开始', ind=ind)
        att = 0
        total_changes = 3
        total_fights = 3
        cur_changes = self.record['functions']['adventure_logs']['adventure_fights']['current_changes']
        cur_fights = self.record['functions']['adventure_logs']['adventure_fights']['current_fights']
        done = self.record['functions']['adventure_logs']['adventure_fights']['done']
        if cur_fights == total_fights:
            done = 1
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./tasks/gn.png', name='功能', ind=ind+1)
            self.find_and_click(img_path='./tasks/gn_mxrz.png', name='冒险日志', ind=ind+1)
            self.find_and_click(img_path='./tasks/gn_mxrz_mxtz.png', name='冒险挑战', ind=ind+1)
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
            att += 1
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
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/rc.png', name='日常', ind=ind+1)
            f1, fpx, fpy = self.find_and_click(img_path='./tasks/zl.png', name='固定点', n_clicks=0, ind=ind+1)
            f2, _, _ = self.drag_find_and_click(fp=[fpx, fpy + 0.5*DPM], dragto=[-DPM, 0], img_path='./tasks/rc_mlmx.png', name="密林冒险", ind=ind+1, n_clicks=1)
            
            # f3, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_cz.png', name='重置', ind=ind+1)
            # f4, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_cz_qd.png', name='重置确定', ind=ind+1)
            # f5, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_ksyd.png', name='快速移动', ind=ind+1)
            # f6, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_ksyd_qd.png', name='快速移动确定', ind=ind+1)
            # f7, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_ksyd_qd_qd.png', name='快速移动确定确定', ind=ind+1)
            
            f8, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd.png', name='扫荡', ind=ind+1)
            f9, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_-.png', name='-', ind=ind+1)
            f10, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_kssd.png', name='快速扫荡', ind=ind+1)
            time.sleep(90)
            f11, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_kssd_wcsd.png', name='完成扫荡', ind=ind+1)
            f12, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_sd_kssd_wcsd_tcgm.png', name='退出购买', ind=ind+1)
            f13, _, _ = self.find_and_click(img_path='./tasks/rc_mlmx_fh.png', name='退出密林', ind=ind+1)
            att += 1
            finished = f0 and f1 and f2 and f3 and f4 and f5 and f6 and f7 and f8 and f9 and f10 and f11 and f12 and f13
            if finished and not self.test:
                self.record['forest_adventure'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('密林冒险完成', ind=ind)
        else:
            user_print('密林冒险未完成', ind=ind)
    
    def bag(self, ind=0):
        ''' 背包 '''
        user_print('背包开始', ind=ind)
        self.pet()
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
        done = self.record['bag']['pet']['play_with_pet']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/bag.png', name='背包', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/bag_pet.png', name='宠物', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/bag_pet_sun.png', name='太阳', offset=[3.9*DPM,0.2*DPM], ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./tasks/bag_pet_sun_hg.png', name='好感', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/bag_pet_sun_hg_yjwy.png', name='一键喂养', ind=ind+1)
            att += 1
            finished = f0 and f1 and f2 and f3 and f4
            if finished and not self.test:
                self.record['bag']['pet']['play_with_pet'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('好感度完成', ind=ind)
        else:
            user_print('好感度未完成', ind=ind)
    def pet_growing(self, ind=2):
        ''' 升级 updated '''
        user_print('升级开始', ind=ind)
        done = self.record['bag']['pet']['pet_growing']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/bag.png', name='背包', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./tasks/bag_pet.png', name='宠物', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./tasks/bag_pet_penguin.png', name='伽梅尔', offset=[3.9*DPM,0.2*DPM], ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./tasks/bag_pet_penguin_sj.png', name='升级', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/bag_pet_penguin_sj_zdtj.png', name='自动添加', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/bag_pet_penguin_sj_yjsj.png', name='一键升级', ind=ind+1)
            att += 1
            finished = f0 and f1 and f2 and f3 and f4 and f5
            if finished and not self.test:
                self.record['bag']['pet']['pet_growing'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('升级完成', ind=ind)
        else:
            user_print('升级未完成', ind=ind)


    def save_to_json(self):
        ''' 保存 '''
        with open("tmp.json", "w") as jsonFile:
            json.dump(self.record, jsonFile, indent=4)
        if os.name == 'nt':
            if HIGH_LEVEL:
                os.system('del checklist_xl.json')
                time.sleep(3)
                os.system('ren tmp.json checklist_xl.json')
            else:
                os.system('del checklist_xl.json')
                time.sleep(3)
                os.system('ren tmp.json checklist_xl.json')
        else:
            if HIGH_LEVEL:
                os.system('rm checklist_xl.json')
                time.sleep(3)
                os.system('mv tmp.json checklist_xl.json')
            else:
                os.system('rm tmp.json')
                time.sleep(3)
                os.system('mv tmp.json checklist_xl.json')

    def train_boyo(self, ind=1):
        ''' 伙伴培养 updated '''
        user_print('伙伴培养开始', ind=ind)
        done = self.record['daily_tasks']['train_boyo']['done']
        name = self.record['daily_tasks']['train_boyo']['name']
        if self.test:
            done = 0
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./tasks/rw.png', name='任务', ind=ind+1)
            f1, fpx, fpy = self.find_and_click(img_path='./tasks/rw_cjrw.png', name='固定点', n_clicks=0, ind=ind+1)
            f2, _, _ = self.drag_find_and_click(fp=[fpx, fpy + 4 * DPM], dragto=[0, -2*DPM], img_path='./tasks/rw_pyhb.png', name="培养伙伴", offset=[4*DPM,0.5*DPM], ind=ind+1, n_clicks=1)
            char_path = './tasks/rw_pyhb_' + name + '.png'
            f3, _, _ = self.find_and_click(img_path=char_path, name='路飞', offset=[4*DPM, 0], ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./tasks/rw_pyhb_py.png', name='培养', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./tasks/rw_pyhb_py_djpy.png', name='道具培养', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./tasks/rw_pyhb_py_djpy_py.png', name='自动培养培养', ind=ind+1)
            finished_partial = f0 and f1 and f2 and f3 and f4 and f5 and f6
            if finished_partial: 
                time.sleep(60)
            f6, _, _ = self.find_and_click(img_path='./tasks/rw_pyhb_tc.png', name='结束培养', ind=ind+1)
            finished = finished_partial and f6
            if finished and not self.test:
                self.record['daily_tasks']['train_boyo']['done'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('伙伴培养完成', ind=ind)
        else:
            user_print('伙伴培养未完成', ind=ind)

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
            self.back_to_home(ind=ind+1)
            self.find_and_click(img_path='./tasks/rw.png', name='任务', ind=ind+1)
            found, _, _ = self.find_and_click(img_path='./tasks/rw_ljl.png', name='任务领奖', ind=ind+1)
            while found:
                found, _, _ = self.find_and_click(img_path='./tasks/rw_ljl.png', name='任务领奖', ind=ind+1)
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


# import win32gui, win32con

# hwnd = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

ar = AutoRun(to_test=False, to_reset=False)
ar.run()
# ar.bag()

# ar.get_task_reward()
# ar.gumball_machine()
# todo:
'''
add error handling
'''