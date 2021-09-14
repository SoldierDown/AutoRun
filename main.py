SHORT_PAUSE = 1
MID_PAUSE = 10
LONG_PAUSE = 30
N_CLICKS = 20
N_DRAGS = 10
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
    def __init__(self):
        filename = ''
        filename = 'checklist_xl.json'
        # if HIGH_LEVEL:
        #     filename = 'checklist_xl.json'
        # else:
        #     filename = 'checklist_sl.json'
        with open(filename, 'r') as f:
            self.record = json.load(f)
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
    
    def drag_find_and_click(self, fp=[0, 0], dragto=[0, 0], img_path='', name='', offset=[0, 0],ind=1, n_clicks=1, n_drags=1):
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
                pag.drag(dragto[0], dragto[1])
                cnt_drags += 1
                time.sleep(1)
                pos = pag.locateOnScreen(img_path, confidence=conf)
        if pos is not None:
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
            self.game_assistant()
            self.harbor()
            self.union()
            self.functions()
            self.bag()
            # self.reward_center()
            self.cross_servers()
            self.lineup()
            self.boyos()
            self.get_task_reward()
        else:
            self.normal_activity()
            self.time_limited_activity()
            self.union()
            self.bag()
            self.reward_center()
            self.boyos()
            self.get_task_reward()
    
    def back_to_home(self, ind=0):
        ''' 回到主页 '''
        self.find_and_click(img_path='./img/bth.png', name='主页', n_clicks=N_CLICKS, ind=ind)

    def recruit(self, ind=0):
        ''' 招募 '''

    def normal_activity(self, ind=0):
        ''' 日常任务 '''
        user_print('日常任务开始', ind=ind)
        self.daily_checkin()
        self.buy_bali()
        self.get_vip_gift()
        self.get_daily_gift()
        user_print('日常任务完成', ind=ind)
    def daily_checkin(self, ind=1):
        ''' 每日签到 '''
        user_print('每日签到开始', ind=ind)
        done = self.record['normal_activity']['daily_checkin']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            self.find_and_click(img_path='./img/na.png', name='日常活动', ind=ind+1)
            self.find_and_click(img_path='./img/na_dci.png', name='每日签到', ind=ind+1)
            self.find_and_click(img_path='./img/na_dci_aci.png', name='每日签到格', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/na_dci_aci_lq_o.png', name='每日签到领取', ind=ind+1)
            if not finished:
                finished, _, _ = self.find_and_click(img_path='./img/na_dci_aci_lq_b.png', name='每日签到领取', ind=ind+1)
            att += 1
            if finished:
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
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], img_path='./img/na_bb.png', name='购买贝里', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/na_bb_bo.png', name='购买贝里一次', ind=ind+1)
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
        ''' VIP礼物 '''
        user_print('VIP礼物开始', ind=ind)
        done = self.record['normal_activity']['get_vip_gift']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], img_path='./img/na_vipg.png', name='VIP礼包', ind=ind+1)
            self.find_and_click(img_path='./img/na_vipg_mrg.png', name='VIP每日礼包', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/na_vipg_mrg_lq.png', name='VIP每日礼包领取', ind=ind+1)
            self.find_and_click(img_path='./img/na_vipg_mrg_lq_qd.png', name='VIP每日礼包领取确定', ind=ind+1)
            att += 1
            if finished:
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
        self.get_mz_gift()
        self.get_my_gift()
        user_print('日常礼包完成', ind=ind)
    def get_mr_gift(self, ind=2):
        ''' 每日礼包 '''
        user_print('每日礼包开始', ind=ind)
        done = self.record['normal_activity']['get_daily_gift']['mr']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], n_drags=8, ind=ind+1)
            self.find_and_click(img_path='./img/na_rcg.png', name='日常礼包', ind=ind+1)

            self.find_and_click(img_path='./img/na_rcg_mrg.png', name='日常礼包每日礼包', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/na_rcg_mrg_mf.png', name='日常礼包每日礼包领取', ind=ind+1)
            self.find_and_click(img_path='./img/na_rcg_mrg_mf_qd.png', name='日常礼包每日礼包领取', ind=ind+1)
            time.sleep(3)
            att += 1
            if finished:
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
            self.find_and_click(img_path='./img/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], n_drags=8, ind=ind+1)
            self.find_and_click(img_path='./img/na_rcg.png', name='日常礼包', ind=ind+1)
            self.find_and_click(img_path='./img/na_rcg_mzg.png', name='日常礼包每周礼包', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/na_rcg_mzg_mf.png', name='日常礼包每周礼包领取', ind=ind+1)
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
            self.find_and_click(img_path='./img/na.png', name='日常活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], n_drags=8, ind=ind+1)
            self.find_and_click(img_path='./img/na_rcg.png', name='日常礼包', ind=ind+1)

            self.find_and_click(img_path='./img/na_rcg_myg.png', name='日常礼包每月礼包', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/na_rcg_myg_mf.png', name='日常礼包每月礼包领取', ind=ind+1)
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
        self.consecutive_logins()
        self.sales_items()
        self.dollar_shop()
        user_print('限时活动完成', ind=ind)
    def consecutive_logins(self, ind=1):
        ''' 累计登录 '''
        user_print('累计登录开始', ind=ind)
        done = self.record['time_limited_activity']['consecutive_logins']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/la.png', name='限时活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], img_path='./img/la_lj.png', name='累计登录', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/la_lj_lq.png', name='累计登录领取', n_clicks=1, ind=ind+1)
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
        ''' 福利商店 '''
        user_print('福利商店开始', ind=ind)
        done = self.record['time_limited_activity']['dollar_shop']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/la.png', name='限时活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], img_path='./img/la_fl.png', name='福利商店', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/la_fl_tl.png', name='福利商店购买体力', offset=[6*DPM, 0.5*DPM], n_clicks=5, ind=ind+1)
            att += 1
            if finished:
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
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/la.png', name='限时活动', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/bth.png', name='固定点', n_clicks=0, ind=ind+1)
            fpx, fpy = fpx, fpy - 12 * DPM
            self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], img_path='./img/la_dj.png', name='道具折扣', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/la_dj_tl.png', name='道具折扣购买体力', offset=[6*DPM, 0.5*DPM], n_clicks=5, ind=ind+1)
            att += 1
            if finished:
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
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./img/ga.png', name='游戏助手', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./img/ga_da.png', name='全部执行', pause=LONG_PAUSE, ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./img/ga_da_back.png', name='游戏执行完成', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./img/ga_da_back_back.png', name='退出游戏助手', ind=ind+1)
            att += 1
            finished = f0 and f1 and f2 and f3
            if finished:
                self.record['game_assistant'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('游戏助手完成', ind=ind)
        else:
            user_print('游戏助手未完成', ind=ind)



    def reward_center(self, ind=0):
        ''' 奖励中心 '''
        user_print('奖励中心开始', ind=ind)
        done = self.record['reward_center']
        att = 0
        while done != 1 and att < 1:
            self.find_and_click(img_path='./img/jlzx.png', name='奖励中心', ind=ind+1)
            self.find_and_click(img_path='./img/ljzx_qblq.png', name='奖励中心领取', ind=ind+1)
            self.find_and_click(img_path='./img/ljzx_qblq_qd.png', name='奖励中心领取确定', ind=ind+1)
            att += 1
            self.record['reward_center'] = 1
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
        self.official_pirates()
        user_print('工会活动完成', ind=ind)
    def official_pirates(self, ind=1):
        ''' 七武海 '''
        user_print('七武海开始', ind=ind)
        done = self.record['union']['official_pirates']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./img/gh.png', name='工会', pause=LONG_PAUSE, ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./img/gh_qwh.png', name='七武海', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./img/gh_qwh_jsjl.png', name='击杀奖励', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./img/gh_qwh_jsjl_yjlq.png', name='一键领取', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./img/gh_qwh_jsjl_yjlq_qd.png', name='确定', ind=ind+1)
            time.sleep(5)
            f5, _, _ = self.find_and_click(img_path='./img/gh_qwh_jsjl_yjlq_qd_tc.png', name='退出', ind=ind+1)
            time.sleep(5)
            # f6, _, _ = self.find_and_click(img_path='./img/gh_qwh_sdqb.png', name='扫荡全部', ind=ind+1)
            # time.sleep(30)
            # f7, _, _ = self.find_and_click(img_path='./img/gh_qwh_sdqb_tc.png', name='退出', ind=ind+1)
            f8, _, _ = self.find_and_click(img_path='./img/gh_qwh_fh.png', name='返回', ind=ind+1)
            f9, _, _ = self.find_and_click(img_path='./img/gh_fh.png', name='返回', ind=ind+1)

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
        ''' 工会建设 '''
        user_print('工会建设开始', ind=ind)
        done = self.record['union']['union_construction']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gh.png', name='工会', pause=LONG_PAUSE, ind=ind+1)
            self.find_and_click(img_path='./img/gh_ghdt.png', name='工会大厅', ind=ind+1)
            self.find_and_click(img_path='./img/gh_ghdt_ptjs.png', name='普通建设', offset=[DPM/3, DPM*3.3], ind=ind+1)
            self.find_and_click(img_path='./img/gh_ghdt_ptjs_qwlq.png', name='前往领取奖励', ind=ind+1)
            self.find_and_click(img_path='./img/gh_ghdt_ptjs_qwlq_lq.png', name='领取奖励', ind=ind+1)
            self.find_and_click(img_path='./img/gh_ghdt_ptjs_qwlq_lq_qd.png', name='确定领取', ind=ind+1)
            self.find_and_click(img_path='./img/gh_ghdt_ptjs_qwlq_lq_fh.png', name='返回工会', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/gh_fh.png', name='退出工会', ind=ind+1)
            att += 1
            if finished:
                self.record['union']['union_construction'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('工会建设完成', ind=ind)
        else:
            user_print('工会建设未完成', ind=ind)
    def pirate_wanted(self, ind=1):
        ''' 海盗悬赏 '''
        user_print('海盗悬赏开始', ind=ind)
        done = self.record['union']['pirate_wanted']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gh.png', name='工会', pause=LONG_PAUSE, ind=ind+1)
            self.find_and_click(img_path='./img/gh_hdxs.png', name='海盗悬赏', ind=ind+1)
            _, tzx, tzy = self.find_and_click(img_path='./img/gh_hdxs_tz.png', name='海盗悬赏挑战', ind=ind+1)
            pag.moveTo(tzx, tzy+2*DPM)
            pag.click()
            self.find_and_click(img_path='./img/gh_ghdt_fh.png', name='退出海盗悬赏', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/gh_fh.png', name='退出工会', ind=ind+1)
            att += 1
            if finished:
                self.record['union']['pirate_wanted'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('海盗悬赏完成', ind=ind)
        else:
            user_print('海盗悬赏未完成', ind=ind)



    def harbor(self, ind=0):
        ''' 港口 '''
        user_print('港口开始', ind=ind)
        self.harbor_reward()
        self.harbor_shop()
        user_print('港口完成', ind=ind)
    def harbor_reward(self, ind=1):
        ''' 港口领奖 '''
        user_print('港口领奖开始', ind=ind)
        done = self.record['harbor']['harbor_reward']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gk.png', name='港口', ind=ind+1)
            self.find_and_click(img_path='./img/gk_lj.png', name='港口领奖', ind=ind+1)
            finished, _, _ = self.find_and_click(img_path='./img/gk_lj_qd.png', name='港口领奖确定', ind=ind+1)
            time.sleep(5)
            self.find_and_click(img_path='./img/gk_fh.png', name='退出港口', ind=ind+1)
            att += 1
            if finished:
                self.record['harbor']['harbor_reward'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('港口领奖完成', ind=ind)
        else:
            user_print('港口领奖未完成', ind=ind)
    def harbor_shop(self, ind=1):
        ''' 港口商店 '''
        user_print('港口商店开始', ind=ind)
        self.harbor_shop_orange()
        self.harbor_shop_red()
        self.harbor_shop_tech()
        user_print('港口商店完成', ind=ind)
    def harbor_shop_orange(self, ind=2):
        ''' 橙色饰品碎片 '''
        user_print('港口商店-橙色饰品碎片开始', ind=ind)
        finished = False
        done = self.record['harbor']['harbor_shop']['orange']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gk.png', name='港口', ind=ind+1)
            self.find_and_click(img_path='./img/gk_sd.png', name='港口商店', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/gk_sd_fp.png', name='固定点', n_clicks=0, ind=ind+1)
            finished, _, _ = self.drag_find_and_click(fp=[fpx, fpy+2*DPM], dragto=[0, -DPM], offset=[6*DPM, 0.5*DPM], img_path='./img/gk_sd_o.png', name='橙色饰品碎片', ind=ind+1)
            if finished:
                self.find_and_click(img_path='./img/gk_sd_pt.png', name='+10', ind=ind+1)
                time.sleep(5)
                self.find_and_click(img_path='./img/gk_sd_o_qd.png', name='确定购买橙色饰品碎片', ind=ind+1)
                time.sleep(5)
                self.find_and_click(img_path='./img/gk_sd_o_qd_qd.png', name='返回港口商店', ind=ind+1)
                time.sleep(5)
            att += 1
            if finished:
                self.record['harbor']['harbor_shop']['orange'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('港口商店-橙色饰品碎片完成', ind=ind)
        else:
            user_print('港口商店-橙色饰品碎片未完成', ind=ind)    
    def harbor_shop_red(self, ind=2):
        ''' 红色饰品精华 '''
        user_print('港口商店-红色饰品精华开始', ind=ind)
        done = self.record['harbor']['harbor_shop']['red']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gk.png', name='港口', ind=ind+1)
            self.find_and_click(img_path='./img/gk_sd.png', name='港口商店', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/gk_sd_fp.png', name='固定点', n_clicks=0, ind=ind+1)
            finished, _, _ = self.drag_find_and_click(fp=[fpx, fpy+2*DPM], dragto=[0, -DPM], offset=[6*DPM, 0.5*DPM], img_path='./img/gk_sd_r.png', name='红色饰品精华', ind=ind+1)
            if finished:
                self.find_and_click(img_path='./img/gk_sd_pt.png', name='+10', ind=ind+1)
                time.sleep(5)
                self.find_and_click(img_path='./img/gk_sd_r_qd.png', name='确定购买红色饰品精华', ind=ind+1)
                time.sleep(5)
                self.find_and_click(img_path='./img/gk_sd_r_qd_qd.png', name='返回港口商店', ind=ind+1)
                time.sleep(5)
            # self.find_and_click(img_path='./img/gk_sd_fh.png', name='退出港口商店')
            # self.find_and_click(img_path='./img/gk_fh.png', name='退出港口')
            att += 1
            if finished:
                self.record['harbor']['harbor_shop']['red'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('港口商店-红色饰品精华完成', ind=ind)
        else:
            user_print('港口商店-红色饰品精华未完成', ind=ind)
    def harbor_shop_tech(self, ind=2):
        ''' 科技芯片 '''
        user_print('港口商店-科技芯片开始', ind=ind)
        done = self.record['harbor']['harbor_shop']['tech']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gk.png', name='港口', ind=ind+1)
            self.find_and_click(img_path='./img/gk_sd.png', name='港口商店', ind=ind+1)
            _, fpx, fpy = self.find_and_click(img_path='./img/gk_sd_fp.png', name='固定点', n_clicks=0, ind=ind+1)
            finished, _, _ = self.drag_find_and_click(fp=[fpx, fpy+2*DPM], dragto=[0, -DPM], offset=[6*DPM, 0.5*DPM], img_path='./img/gk_sd_kj.png', name='科技芯片', ind=ind+1)
            if finished:
                self.find_and_click(img_path='./img/gk_sd_pt.png', name='+10', ind=ind+1)
                time.sleep(5)
                self.find_and_click(img_path='./img/gk_sd_kj_qd.png', name='确定购买科技芯片', ind=ind+1)
                time.sleep(5)
                self.find_and_click(img_path='./img/gk_sd_kj_qd_qd.png', name='返回港口商店', ind=ind+1)
                time.sleep(5)
            att += 1
            if finished:
                self.record['harbor']['harbor_shop']['tech'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('港口商店-科技芯片完成', ind=ind)
        else:
            user_print('港口商店-科技芯片未完成', ind=ind)

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
        done = self.record['functions']['adventure_logs']['gumball_machine']
        att = 0
        total_chances = 3
        cnt_tb = 0
        while done != 1 and att < MAX_ATTEMPTS:
            # TODO
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gn.png', name='功能', ind=ind+1)
            self.find_and_click(img_path='./img/gn_mxrz.png', name='冒险日志', ind=ind+1)
            self.find_and_click(img_path='./img/gn_mxrz_ndj.png', name='扭蛋机', ind=ind+1)
            while cnt_tb < total_chances:
                f0, _, _ = self.find_and_click(img_path='./img/gn_mxrz_ndj_tb.png', name='投币一次', ind=ind+1)
                f1, _, _ = self.find_and_click(img_path='./img/gn_mxrz_ndj_tb_qd.png', name='投币确定', ind=ind+1)
                if f0 and f1:
                    cnt_tb += 1
            att += 1
            if cnt_tb == total_chances: 
                self.record['functions']['adventure_logs']['gumball_machine'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('扭蛋机完成', ind=ind)
        else:
            user_print('扭蛋机未完成', ind=ind)
    def adventure_fights(self, ind=2):
        # TODO
        ''' 冒险挑战 '''
        user_print('冒险挑战开始', ind=ind)
        done = self.record['functions']['adventure_logs']['adventure_fights']
        att = 0
        total_changes = 3
        total_fights = 3
        cur_changes = 0
        cur_fights = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            self.find_and_click(img_path='./img/gn.png', name='功能', ind=ind+1)
            self.find_and_click(img_path='./img/gn_mxrz.png', name='冒险日志', ind=ind+1)
            self.find_and_click(img_path='./img/gn_mxrz_mxtz.png', name='冒险挑战', ind=ind+1)
            while cur_fights < total_fights:
                found, _, _ = self.find_and_click(img_path='./img/gn_mxrz_mxtz_jf10.png', name='低分海贼', n_clicks=0, ind=ind+1)
                # 低积分海贼
                if found:
                    user_print('发现低分海贼', ind=ind+1)
                    # 还可免费更改
                    if cur_changes < total_changes:
                        user_print('更换海贼', ind=ind+1)
                        self.find_and_click(img_path='./img/gn_mxrz_mxtz_cxmb.png', name='重选目标', ind=ind+1)
                        cur_changes += 1
                    # 只能打了
                    else:
                        user_print('攻打低分海贼', ind=ind+1)
                        self.find_and_click(img_path='./img/gn_mxrz_mxtz_fqtz.png', name='发起挑战', ind=ind+1)
                        self.find_and_click(img_path='./img/gn_mxrz_mxtz_tg.png', name='跳过', ind=ind+1)
                        pag.click()
                        cur_fights += 1
                # 高积分海贼: 直接打
                else:
                    user_print('发现高分海贼', ind=ind+1)
                    self.find_and_click(img_path='./img/gn_mxrz_mxtz_fqtz.png', name='发起挑战', ind=ind+1)
                    self.find_and_click(img_path='./img/gn_mxrz_mxtz_tg.png', name='跳过', ind=ind+1)
                    pag.click()
                    cur_fights += 1
            att += 1
            if cur_fights == total_fights:
                self.record['functions']['adventure_logs']['adventure_fights'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('冒险挑战完成', ind=ind)
        else:
            user_print('冒险挑战未完成', ind=ind)


    
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
        ''' 好感度 '''
        user_print('好感度开始', ind=ind)
        done = self.record['bag']['pet']['play_with_pet']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./img/bag.png', name='背包', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./img/bag_pet.png', name='宠物', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./img/bag_pet_pick.png', name='选择宠物', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./img/bag_pet_pick_hg.png', name='好感', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./img/bag_pet_pick_hg_yjwy.png', name='一键喂养', ind=ind+1)
            att += 1
            finished = f0 and f1 and f2 and f3 and f4
            if finished:
                self.record['bag']['pet']['play_with_pet'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('好感度完成', ind=ind)
        else:
            user_print('好感度未完成', ind=ind)
    def pet_growing(self, ind=2):
        ''' 升级 '''
        user_print('升级开始', ind=ind)
        done = self.record['bag']['pet']['pet_growing']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _, = self.find_and_click(img_path='./img/bag.png', name='背包', ind=ind+1)
            f1, _, _, = self.find_and_click(img_path='./img/bag_pet.png', name='宠物', ind=ind+1)
            f2, _, _, = self.find_and_click(img_path='./img/bag_pet_pick.png', name='选择宠物', ind=ind+1)
            f3, _, _, = self.find_and_click(img_path='./img/bag_pet_pick_sj.png', name='升级', ind=ind+1)
            f4, _, _, = self.find_and_click(img_path='./img/bag_pet_pick_sj_zdtj.png', name='自动添加', ind=ind+1)
            f5, _, _, = self.find_and_click(img_path='./img/bag_pet_pick_sj_yjsj.png', name='一键升级', ind=ind+1)
            finished = f0 and f1 and f2 and f3 and f4 and f5
            if finished:
                self.record['bag']['pet']['pet_growing'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('升级完成', ind=ind)
        else:
            user_print('升级未完成', ind=ind)



    def save_to_json(self):
        ''' 保存 '''
        with open("latestchecklist.json", "w") as jsonFile:
            json.dump(self.record, jsonFile, indent=4)
        if os.name == 'nt':
            if HIGH_LEVEL:
                os.system('del checklist_xl.json')
                time.sleep(3)
                os.system('ren latestchecklist.json checklist_xl.json')
            else:
                os.system('del checklist_sl.json')
                time.sleep(3)
                os.system('ren latestchecklist.json checklist_sl.json')
        else:
            if HIGH_LEVEL:
                os.system('rm checklist_xl.json')
                time.sleep(3)
                os.system('mv latestchecklist.json checklist_xl.json')
            else:
                os.system('rm checklist_sl.json')
                time.sleep(3)
                os.system('mv latestchecklist.json checklist_sl.json')

    def boyos(self, ind=0):
        ''' 伙伴 '''
        user_print('伙伴开始', ind=ind)
        self.train_boyo()
        user_print('伙伴结束', ind=ind)
    def train_boyo(self, ind=1):
        ''' 伙伴培养 '''
        user_print('伙伴培养开始', ind=ind)
        done = self.record['boyos']['train_boyo']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f0, _, _ = self.find_and_click(img_path='./img/hb.png', name='伙伴', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./img/hb_lf.png', name='路飞', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./img/hb_lf_py.png', name='培养', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./img/hb_lf_py_djpy.png', name='道具培养', offset=[0, DPM], n_clicks=1, ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./img/hb_lf_py_py.png', name='一键培养', ind=ind+1)
            time.sleep(60)
            f5, _, _ = self.find_and_click(img_path='./img/hb_lf_py_py_tc.png', name='退出', ind=ind+1)
            finished = f0 and f1 and f2 and f3 and f4 and f5
            if finished:
                self.record['boyos']['train_boyo'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('伙伴培养完成', ind=ind)
        else:
            user_print('伙伴培养未完成', ind=ind)



    def lineup(self, ind=0):
        ''' 阵容 '''
        user_print('阵容开始', ind=ind)
        self.accessory_strengthen()
        self.equipment_enchant()
        user_print('阵容完成', ind=ind)
    def equipment_enchant(self, ind=1):
        ''' 装备附魔 '''
        user_print('装备附魔开始', ind=ind)
        done = self.record['lineup']['equipment_enchant']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f1, _, _ = self.find_and_click(img_path='./img/zr.png', name='阵容', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./img/zr_xl.png', name='溪流', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./img/zr_xl_lgm.png', name='流光帽', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./img/zr_xl_lgm_fm.png', name='附魔', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./img/zr_xl_lgm_fm_yjfm.png', name='一键附魔', ind=ind+1)
            f6, _, _ = self.find_and_click(img_path='./img/zr_xl_lgm_fm_yjfm_pt.png', name='+10', ind=ind+1)
            f7, _, _ = self.find_and_click(img_path='./img/zr_xl_lgm_fm_yjfm_qd.png', name='确定', ind=ind+1)
            finished = f1 and f2 and f3 and f4 and f5 and f6 and f7
            if finished:
                self.record['lineup']['equipment_enchant'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('装备附魔完成', ind=ind)
        else:
            user_print('装备附魔未完成', ind=ind)
    def accessory_strengthen(self, ind=1):
        ''' 饰品强化 '''
        user_print('饰品强化开始', ind=ind)
        done = self.record['lineup']['accessory_strengthen']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            finished = False
            f1, _, _ = self.find_and_click(img_path='./img/zr.png', name='阵容', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./img/zr_zyj.png', name='紫云晶', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./img/zr_zyj_qh.png', name='强化', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./img/zr_zyj_qh_zdtj.png', name='自动添加', ind=ind+1)
            f5, _, _ = self.find_and_click(img_path='./img/zr_zyj_qh_zdtj_yjqh.png', name='一键强化', ind=ind+1)
            finished = f1 and f2 and f3 and f4 and f5
            if finished:
                self.record['lineup']['accessory_strengthen'] = 1
                done = 1
                self.save_to_json()
        if done == 1:
            user_print('饰品强化完成', ind=ind)
        else:
            user_print('饰品强化未完成', ind=ind)



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
            f0, _, _ = self.find_and_click(img_path='./img/kf.png', name='跨服', ind=ind+1)
            f1, _, _ = self.find_and_click(img_path='./img/kf_bzzd.png', name='宝藏争夺', ind=ind+1)
            f2, _, _ = self.find_and_click(img_path='./img/kf_bzzd_lj.png', name='领取', ind=ind+1)
            f3, _, _ = self.find_and_click(img_path='./img/kf_bzzd_lj_qd.png', name='确定', ind=ind+1)
            f4, _, _ = self.find_and_click(img_path='./img/kf_bzzd_fh.png', name='返回', ind=ind+1)
            finished = f0 and f1 and f2 and f3 and f4
            if finished:
                self.record['cross_servers']['treasures'] = 1
                done = 1
                self.save_to_json()
            else:
                self.find_and_click(img_path='./img/kf_bzzd_fh.png', name='返回', ind=ind+1)
        if done == 1:
            user_print('宝藏争夺完成', ind=ind)
        else:
            user_print('宝藏争夺未完成', ind=ind)



    def get_task_reward(self, ind=0):
        ''' 任务领奖 '''
        user_print('任务领奖开始', ind=ind)
        done = self.record['get_task_reward']
        att = 0
        while done != 1 and att < MAX_ATTEMPTS:
            self.back_to_home(ind=ind+1)
            self.find_and_click(img_path='./img/rw.png', name='任务', ind=ind+1)
            found, _, _ = self.find_and_click(img_path='./img/rw_ljl.png', name='任务领奖', ind=ind+1)
            while found:
                found, _, _ = self.find_and_click(img_path='./img/rw_ljl.png', name='任务领奖', ind=ind+1)
            self.record['get_task_reward'] = 1
            done = 1
            self.save_to_json()
        if done == 1:
            user_print('任务领奖完成', ind=ind)
        else:
            user_print('任务领奖未完成', ind=ind)
    def test(self):
        found, _, _ = self.find_and_click(img_path='./img/gn_mxrz_mxtz_jf10.png', name='低分海贼', n_clicks=0, ind=2)


import win32gui, win32con

# hwnd = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

ar = AutoRun()
# ar.bag()
# ar.run()
# ar.get_task_reward()
# ar.gumball_machine()
# todo:
'''
add error handling
'''