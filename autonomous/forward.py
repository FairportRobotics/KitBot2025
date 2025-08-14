import components
import magicbot
import json


class Forward(magicbot.AutonomousStateMachine):
    MODE_NAME = "Roll Forward"
    DEFAULT = True

    drivetrain: components.TankDrive

    @magicbot.state(first=True)
    def start(self):
        #self.drivetrain.set_mode("curvature")
        self.next_state("drive_forward")

    @magicbot.timed_state(duration=1.0, next_state="fin")
    def drive_forward(self):
        self.drivetrain.go(1, 0)

    @magicbot.state()
    def fin(self):
        self.drivetrain.stop()
        self.done()