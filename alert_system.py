import time
import threading

class AlertSystem:
    def __init__(self, buzzer):
        self.buzzer = buzzer
        self.alert_thread = None
        self.is_alerting = False

    def trigger_alert(self):
        """Initial warning - short beeps"""
        if not self.is_alerting:
            self.is_alerting = True
            self.alert_thread = threading.Thread(target=self._alert_sequence)
            self.alert_thread.start()

    def trigger_emergency_alert(self):
        """Emergency warning - continuous beep"""
        if not self.is_alerting:
            self.is_alerting = True
            self.alert_thread = threading.Thread(target=self._emergency_sequence)
            self.alert_thread.start()

    def _alert_sequence(self):
        """Pattern for initial warning"""
        for _ in range(3):
            self.buzzer.on()
            time.sleep(0.2)
            self.buzzer.off()
            time.sleep(0.2)
        self.is_alerting = False

    def _emergency_sequence(self):
        """Pattern for emergency alert"""
        self.buzzer.on()
        time.sleep(2.0)
        self.buzzer.off()
        self.is_alerting = False 