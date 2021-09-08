SHORT_PAUSE = 1
MID_PAUSE = 10
LONG_PAUSE = 30
N_CLICKS = 20
MAX_CONF = 0.95
MIN_CONF = 0.8
DCONF = -0.05
DPM = 100
import pyautogui as pag
from pynput import mouse
import time

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
            output=''
            for iter in range(ind):
                output +='\t'
            output+=name
            output+='未找到'
            print(output)
            time.sleep(3)
            return False, 0, 0
    
    def drag_find_and_click(self, fp=[0, 0], dragto=[0, 0], img_path='', name='', offset=[0, 0],ind=1, n_clicks=1, n_drags=1):
        if img_path == '':
            for iter in range(n_drags):
                pag.moveTo(fp[0], fp[1])
                pag.drag(dragto[0], dragto[1])
            return True, 0, 0
        pag.moveTo(fp[0], fp[1])
        conf = MAX_CONF
        pos = pag.locateOnScreen(img_path, confidence=conf)
        while pos is None and conf > MIN_CONF:
            pag.drag(dragto[0], dragto[1])
            conf += DCONF
            pos = pag.locateOnScreen(img_path, confidence=conf)
            pag.moveTo(fp[0], fp[1])
        if pos is not None:
            pag.moveTo(pos.left + offset[0], pos.top + offset[1])
            for iter in range(n_clicks):
                pag.click()
            time.sleep(3)
            return True, pos.left, pos.top
        else:
            output=''
            for iter in range(ind):
                output +='\t'
            output+=name
            output+='未找到'
            print(output)
            time.sleep(3)
            return False, 0, 0

    def run(self):
        ''''''
        # self.normal_activity()
        self.time_limited_activity()
        self.game_assistant()
        self.harbor()
        self.union()
        self.functions()
        self.get_task_reward()
    
    def back_to_home(self):
        ''' 回到主页 '''
        self.find_and_click(img_path='./img/bth.png', name='主页', n_clicks=N_CLICKS)

    def normal_activity(self):
        ''' 日常任务 '''
        print('日常任务开始')
        self.daily_checkin()
        # self.buy_bali()
        self.get_vip_gift()
        self.get_daily_gift()
        print('日常任务完成')
    def daily_checkin(self):
        ''' 每日签到 '''
        self.back_to_home()
        finished = False
        print('    每日签到开始')
        self.find_and_click(img_path='./img/na.png', name='日常活动')
        self.find_and_click(img_path='./img/na_dci.png', name='每日签到')
        self.find_and_click(img_path='./img/na_dci_aci.png', name='每日签到格')
        finished, _, _=self.find_and_click(img_path='./img/na_dci_aci_lq.png.bak', name='每日签到领取')
        if finished:
            print('    每日签到完成')
    def buy_bali(self):
        ''' 购买贝里 '''
        self.back_to_home()
        finished = False
        print('    购买贝里开始')
        self.find_and_click(img_path='./img/na.png', name='日常活动')
        _, fpx, fpy = self.find_and_click(img_path='./img/na_fp.png', name='固定点', n_clicks=0)
        self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], img_path='./img/na_bb.png', name='购买贝里')
        finished, _, _ = self.find_and_click(img_path='./img/na_bb_bo.png', name='购买贝里一次')
        if finished:
            print('    购买贝里完成')
    def get_vip_gift(self):
        ''' VIP礼物 '''
        self.back_to_home()
        finished = False
        print('    VIP礼物开始')
        self.find_and_click(img_path='./img/na.png', name='日常活动')
        _, fpx, fpy = self.find_and_click(img_path='./img/na_fp.png', name='固定点', n_clicks=0)
        self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], img_path='./img/na_vipg.png', name='VIP礼包')
        self.find_and_click(img_path='./img/na_vipg_mrg.png', name='VIP每日礼包')
        finished, _, _ = self.find_and_click(img_path='./img/na_vipg_mrg_lq.png', name='VIP每日礼包领取')
        if finished:
            print('    VIP每日礼包完成')
    def get_daily_gift(self):
        ''' 日常礼包 '''
        self.back_to_home()
        finished = False
        print('    日常礼包开始')
        self.find_and_click(img_path='./img/na.png', name='日常活动')
        _, fpx, fpy = self.find_and_click(img_path='./img/na_fp.png', name='固定点', n_clicks=0)
        self.drag_find_and_click(fp=[fpx + 2 * DPM, fpy], dragto=[-DPM, 0], n_drags=8)
        self.find_and_click(img_path='./img/na_rcg.png', name='日常礼包')
        
        self.find_and_click(img_path='./img/na_rcg_mrg.png', name='日常礼包每日礼包', ind=2)
        finished, _, _ = self.find_and_click(img_path='./img/na_rcg_mrg_mf.png', name='日常礼包每日礼包领取', ind=2)
        time.sleep(3)

        self.find_and_click(img_path='./img/na_rcg_mzg.png', name='日常礼包每周礼包', ind=2)
        finished, _, _ = self.find_and_click(img_path='./img/na_rcg_mzg_mf.png', name='日常礼包每周礼包领取', ind=2)
        time.sleep(3)

        self.find_and_click(img_path='./img/na_rcg_myg.png', name='日常礼包每月礼包', ind=2)
        finished, _, _ = self.find_and_click(img_path='./img/na_rcg_myg_mf.png', name='日常礼包每月礼包领取', ind=2)
        time.sleep(3)

        if finished:
            print('    日常礼包完成')



    def time_limited_activity(self):
        ''' 限时活动 '''
        print('限时活动开始')
        self.consecutive_logins()
        self.sales_items()
        self.dollar_shop()
        print('限时活动完成')
    def consecutive_logins(self):
        ''' 累计登录 '''
        self.back_to_home()
        finished = False
        print('    累计登录开始')
        self.find_and_click(img_path='./img/la.png', name='限时活动')
        self.find_and_click(img_path='./img/la_lj.png', name='累计登录')
        finished, _, _ = self.find_and_click(img_path='./img/la_lj_lq.png', name='累计登录领取', n_clicks=5)
        # todo: add offset
        if finished:
            print('    累计登录完成')
    def dollar_shop(self):
        ''' 福利商店 '''
        self.back_to_home()
        finished = False
        print('    福利商店开始')
        self.find_and_click(img_path='./img/la.png', name='限时活动')
        self.find_and_click(img_path='./img/la_fl.png', name='福利商店')
        finished, _, _ = self.find_and_click(img_path='./img/la_fl_tl.png', name='福利商店购买体力', offset=[6*DPM, 0.5*DPM], n_clicks=5)
        if finished:
            print('    福利商店完成')
    def sales_items(self):
        ''' 道具折扣 '''
        self.back_to_home()
        finished = False
        print('    道具折扣开始')
        self.find_and_click(img_path='./img/la.png', name='限时活动')
        self.find_and_click(img_path='./img/la_dj.png', name='道具折扣')
        finished, _, _ = self.find_and_click(img_path='./img/la_dj_tl.png', name='道具折扣购买体力', offset=[6*DPM, 0.5*DPM], n_clicks=5)
        if finished:
            print('    道具折扣完成')



    def game_assistant(self):
        ''' 游戏助手 '''
        self.back_to_home()
        finished = False
        print('游戏助手开始')
        self.find_and_click(img_path='./img/ga.png', name='游戏助手')
        self.find_and_click(img_path='./img/ga_da.png', name='全部执行', pause=LONG_PAUSE)
        self.find_and_click(img_path='./img/ga_da_back.png', name='游戏执行完成')
        self.find_and_click(img_path='./img/ga_da_back_back.png', name='退出游戏助手')
        print('游戏助手完成')

    

    def union(self):
        ''' 工会活动 '''
        print('工会活动开始')
        self.union_construction()
        self.pirate_wanted()
        print('工会活动完成')

    def union_construction(self):
        ''' 工会建设 '''
        self.back_to_home()
        finished = False
        print('    工会建设开始')
        self.find_and_click(img_path='./img/gh.png', name='工会', pause=LONG_PAUSE)
        self.find_and_click(img_path='./img/gh_ghdt.png', name='工会大厅')
        self.find_and_click(img_path='./img/gh_ghdt_ptjs.png', name='普通建设', offset=[DPM/3, DPM*3.3])
        self.find_and_click(img_path='./img/gh_ghdt_fh.png', name='退出工会大厅')
        finished, _, _ = self.find_and_click(img_path='./img/gh_fh.png', name='退出工会')
        if finished:
            print('    道具折扣完成')
    def pirate_wanted(self):
        ''' 海盗悬赏 '''
        self.back_to_home()
        finished = False
        print('    海盗悬赏开始')
        self.find_and_click(img_path='./img/gh.png', name='工会', pause=LONG_PAUSE)
        self.find_and_click(img_path='./img/gh_hdxs.png', name='海盗悬赏')
        _, tzx, tzy = self.find_and_click(img_path='./img/gh_hdxs_tz.png', name='海盗悬赏挑战')
        pag.moveTo(tzx, tzy+2*DPM)
        pag.click()
        self.find_and_click(img_path='./img/gh_ghdt_fh.png', name='退出海盗悬赏')
        finished, _, _ = self.find_and_click(img_path='./img/gh_fh.png', name='退出工会')
        if finished:
            print('    海盗悬赏完成')



    def harbor(self):
        ''' 港口 '''
        print('港口开始')
        self.harbor_reward()
        self.harbor_shop()
        print('港口完成')
    def harbor_reward(self):
        ''' 港口领奖 '''
        self.back_to_home()
        finished = False
        print('    港口领奖开始')
        self.find_and_click(img_path='./img/gk.png', name='港口')
        self.find_and_click(img_path='./img/gk_lj.png', name='港口领奖')
        finished, _, _ = self.find_and_click(img_path='./img/gk_lj_qd.png', name='港口领奖确定')
        time.sleep(5)
        self.find_and_click(img_path='./img/gk_fh.png', name='退出港口')
        if finished:
            print('    港口领奖完成')
    def harbor_shop(self):
        ''' 港口商店 '''
        self.back_to_home()
        finished = False
        print('    港口商店开始')
        self.find_and_click(img_path='./img/gk.png', name='港口')
        self.find_and_click(img_path='./img/gk_sd.png', name='港口商店')
        _, fpx, fpy = self.find_and_click(img_path='./img/gk_sd_fp.png', name='固定点', n_clicks=0)
        finished, _, _ = self.drag_find_and_click(fp=[fpx, fpy+2*DPM], dragto=[0, -2*DPM], offset=[6*DPM, 0.5*DPM], img_path='./img/gk_sd_r.png', name='红色饰品精华')
        if finished:
            self.find_and_click(img_path='./img/gk_sd_pt.png', name='+10')
            time.sleep(5)
            self.find_and_click(img_path='./img/gk_sd_r_qd.png', name='确定购买红色饰品精华')
            time.sleep(5)
            self.find_and_click(img_path='./img/gk_sd_r_qd_qd.png', name='返回港口商店')
            time.sleep(5)
        for iter in range(5):
            pag.moveTo(fpx, fpy)
            pag.drag(DPM*2)

        finished, _, _ = self.drag_find_and_click(fp=[fpx, fpy+2*DPM], dragto=[0, -2*DPM], offset=[6*DPM, 0.5*DPM], img_path='./img/gk_sd_o.png', name='橙色饰品碎片')
        if finished:
            self.find_and_click(img_path='./img/gk_sd_pt.png', name='+10')
            time.sleep(5)
            self.find_and_click(img_path='./img/gk_sd_o_qd.png', name='确定购买橙色饰品碎片')
            time.sleep(5)
            self.find_and_click(img_path='./img/gk_sd_o_qd_qd.png', name='返回港口商店')
            time.sleep(5)
        for iter in range(5):
            pag.moveTo(fpx, fpy)
            pag.drag(DPM*2)

        finished, _, _ = self.drag_find_and_click(fp=[fpx, fpy+2*DPM], dragto=[0, -2*DPM], offset=[6*DPM, 0.5*DPM], img_path='./img/gk_sd_kj.png', name='科技芯片')
        if finished:
            self.find_and_click(img_path='./img/gk_sd_pt.png', name='+10')
            time.sleep(5)
            self.find_and_click(img_path='./img/gk_sd_kj_qd.png', name='确定购买科技芯片')
            time.sleep(5)
            self.find_and_click(img_path='./img/gk_sd_kj_qd_qd.png', name='返回港口商店')
            time.sleep(5)

        self.find_and_click(img_path='./img/gk_sd_fh.png', name='退出港口商店')
        self.find_and_click(img_path='./img/gk_fh.png', name='退出港口')
        if finished:
            print('    港口商店完成')

    

    def functions(self):
        ''' 功能 '''
        print('功能开始')
        self.adventure_logs()
        print('功能完成')
    def adventure_logs(self):
        ''' 冒险日志 '''
        print('    冒险日志开始')
        self.gumball_machine()
        self.adventure_fights()
        print('    冒险日志完成')
    def gumball_machine(self):
        ''' 扭蛋机 '''
        total_chances = 3
        self.back_to_home()
        finished = False
        print('        扭蛋机开始')
        self.find_and_click(img_path='./img/gn.png', name='功能')
        self.find_and_click(img_path='./img/gn_mxrz.png', name='冒险日志')
        self.find_and_click(img_path='./img/gn_mxrz_ndj.png', name='扭蛋机')
        for iter in range(total_chances):
            self.find_and_click(img_path='./img/gn_mxrz_ndj_tb.png', name='投币一次')
        print('        扭蛋机完成')
    def adventure_fights(self):
        ''' 冒险挑战 '''
        total_changes = 3
        total_fights = 3
        cur_changes = 0
        cur_fights = 0
        self.back_to_home()
        finished = False
        print('        冒险挑战开始')
        self.find_and_click(img_path='./img/gn.png', name='功能', ind=2)
        self.find_and_click(img_path='./img/gn_mxrz.png', name='冒险日志', ind=2)
        self.find_and_click(img_path='./img/gn_mxrz_mxtz.png', name='冒险挑战', ind=2)
        while cur_fights < total_fights:
            found, _, _ = self.find_and_click(img_path='./img/gn_mxrz_mxtz_mxjf.png', name='冒险积分', n_clicks=0, ind=2)
            # 低积分海贼
            if found:
                # 还可免费更改
                if cur_changes < total_changes:
                    self.find_and_click(img_path='./img/gn_mxrz_mxtz_cxmb.png', name='重选目标', ind=2)
                    cur_changes += 1
                # 只能打了
                else:
                    self.find_and_click(img_path='./img/gn_mxrz_mxtz_fqtz.png', name='发起挑战', ind=2)
                    self.find_and_click(img_path='./img/gn_mxrz_mxtz_tg.png', name='跳过', ind=2)
                    cur_fights += 1
            # 高积分海贼: 直接打
            else:
                self.find_and_click(img_path='./img/gn_mxrz_mxtz_fqtz.png', name='发起挑战', ind=2)
                self.find_and_click(img_path='./img/gn_mxrz_mxtz_tg.png', name='跳过', ind=2)
                cur_fights += 1
        print('        冒险挑战完成')
    
    
    def get_task_reward(self):
        ''' 任务领奖 '''
        self.back_to_home()
        print('任务领奖开始')
        self.find_and_click(img_path='./img/rw.png', name='任务')
        found, _, _ = self.find_and_click(img_path='./img/rw_ljl.png', name='任务领奖')
        while found:
            found, _, _ = self.find_and_click(img_path='./img/rw_ljl.png', name='任务领奖')
        print('任务领奖完成')
ar = AutoRun()
# ar.run()
ar.get_vip_gift()
