import subprocess


class StepRunner:

    def __init__(self, logger):

        self.logger = logger

    def run(self, command):

        self.logger.log("RUN: " + command)

        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            self.logger.log(line.strip())

        process.wait()

        return process.returncode