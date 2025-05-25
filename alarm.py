import time
import datetime
import threading
import platform
import os

def play_alarm_sound():
    if platform.system() == "Darwin": # macOS
        try:
            os.system("afplay /System/Library/Sounds/Ping.aiff") 
        except Exception as e:
            print(f"사운드 재생 오류 (macOS): {e}")
    else:
        print(f"macOS 환경이 아닙니다. 사운드 재생은 macOS에서만 지원됩니다.")

class AlarmSetting:
    def __init__(self, hour, minute, days):
        self.hour = hour
        self.minute = minute
        self.days = days
        self.is_active = True

class AlarmScheduler:
    def __init__(self):
        self.alarms = {}
        self.running = True
        self.alarm_app = None # AlarmApp 인스턴스를 저장하기 위한 변수

    def set_alarm_app(self, alarm_app):
        self.alarm_app = alarm_app

    def add_alarm(self, alarm_id, setting):
        self.alarms[alarm_id] = setting
        threading.Thread(target=self._check_alarm, args=(alarm_id,)).start()

    def remove_alarm(self, alarm_id):
        if alarm_id in self.alarms:
            self.alarms[alarm_id].is_active = False
            del self.alarms[alarm_id]

    def _check_alarm(self, alarm_id):
        while self.running and alarm_id in self.alarms and self.alarms[alarm_id].is_active:
            now = datetime.datetime.now()
            setting = self.alarms[alarm_id]
            if now.hour == setting.hour and now.minute == setting.minute and now.weekday() in setting.days:
                self._trigger_alarm(alarm_id)
                break # 한 번 울리면 종료 (필요에 따라 반복 로직 추가 가능)
            time.sleep(1)

    def _trigger_alarm(self, alarm_id):
        print(f"알람 {alarm_id} 울립니다!")
        play_alarm_sound() 
        if self.alarm_app:
            self.alarm_app.handle_alarm_triggered(alarm_id)

class AlarmApp:
    def __init__(self):
        self.scheduler = AlarmScheduler()
        self.scheduler.set_alarm_app(self) # AlarmScheduler에 AlarmApp 인스턴스 전달
        self.next_alarm_id = 1
        self.triggered_alarm_id = None

    def set_alarm(self, hour, minute, days):
        setting = AlarmSetting(hour, minute, days)
        alarm_id = self.next_alarm_id
        self.scheduler.add_alarm(alarm_id, setting)
        print(f"알람 {alarm_id} 설정: {hour:02d}:{minute:02d} ({days})")
        self.next_alarm_id += 1
        return alarm_id

    def dismiss_alarm(self, alarm_id):
        self.scheduler.remove_alarm(alarm_id)
        print(f"알람 {alarm_id} 해제")
        self.triggered_alarm_id = None

    def handle_alarm_triggered(self, alarm_id):
        self.triggered_alarm_id = alarm_id
        

#시간, 분, 요일, 해제
if __name__ == "__main__":
    app = AlarmApp()
    alarm_id = None

    while True:
        try:
            hour_str = input("알람 시간을 설정하세요 (시): ")
            minute_str = input("알람 시간을 설정하세요 (분): ")
            days_str = input("알람 요일을 설정하세요 (쉼표로 구분, 0=월, 1=화, ..., 6=일): ")

            hour = int(hour_str)
            minute = int(minute_str)
            days = [int(d.strip()) for d in days_str.split(',')]

            if 0 <= hour <= 23 and 0 <= minute <= 59 and all(0 <= d <= 6 for d in days):
                alarm_id = app.set_alarm(hour, minute, days)
                print(f"알람이 {hour:02d}:{minute:02d} ({days}) 에 설정되었습니다. 해제 ID는 {alarm_id} 입니다.")
                break
            else:
                print("잘못된 입력입니다. 시간을 0-23, 분을 0-59, 요일을 0-6 사이의 숫자로 입력해주세요.")
        except ValueError:
            print("잘못된 입력 형식입니다. 숫자로 입력해주세요.")

    print("알람이 울릴 때까지 기다립니다...")
    while app.triggered_alarm_id is None:
        time.sleep(1)

    # 알람 울린 후 사용자에게 해제 요청
    dismiss = input(f"알람 {app.triggered_alarm_id} 를 해제하시겠습니까? (y/n): ")
    if dismiss.lower() == 'y':
        app.dismiss_alarm(app.triggered_alarm_id)
    else:
        print(f"알람 {app.triggered_alarm_id}는 계속 울립니다. (현재는 콘솔에만 출력)")
