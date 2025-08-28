import components
import magicbot


class Forward(magicbot.AutonomousStateMachine):
    MODE_NAME = "Roll Forward"
    DEFAULT = True

    drivetrain: components.DifferentialDrive

    @magicbot.state(first=True)
    def start(self):
        self.next_state("drive_forward")

    @magicbot.timed_state(duration=1.0, next_state="finish")
    def drive_forward(self):
        self.drivetrain.go(1, 0)

    @magicbot.state()
    def finish(self):
        self.drivetrain.stop()
        self.done()
