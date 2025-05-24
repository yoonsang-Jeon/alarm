import time
import datetime
import threading

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
        # 실제 소리 재생 기능은 OS 의존적이므로 생략
        # SoundOutput().play_sound()

class AlarmApp:
    def __init__(self):
        self.scheduler = AlarmScheduler()
        self.next_alarm_id = 1

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

# --- 사용자 인터페이스 (간단한 콘솔 기반) ---
if __name__ == "__main__":
    app = AlarmApp()
    alarm1_id = app.set_alarm(11, 35, [0, 1, 2, 3, 4]) # 평일 알람
    time.sleep(5) # 잠시 대기
    app.dismiss_alarm(alarm1_id)