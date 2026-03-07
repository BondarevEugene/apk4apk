from kivy.clock import Clock

from core.step_runner import StepRunner
from core.logger import Logger


class BuildManager:

    def __init__(self, app):

        self.app = app

        self.logger = Logger(app)

        self.runner = StepRunner(self.logger)

        self.steps = [

            ("Clean build", "buildozer android clean"),

            ("Build APK", "buildozer android debug"),

            ("Install APK", "adb install -r bin/*.apk"),

            ("Run App", "adb shell monkey -p org.example.demobook 1")

        ]

    def start(self):

        Clock.schedule_once(lambda dt: self.run())

    def run(self):

        total = len(self.steps)

        for i, (name, cmd) in enumerate(self.steps):

            self.logger.log("")
            self.logger.log("STEP: " + name)

            self.app.set_step(i, "working")

            code = self.runner.run(cmd)

            if code != 0:

                self.logger.log("FAILED")

                self.app.set_step(i, "error")

                return

            self.app.set_step(i, "ok")

            progress = (i + 1) / total * 100

            self.app.update_progress(progress)

        self.logger.log("BUILD SUCCESS")