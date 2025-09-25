import components
import magicbot


class Forward(magicbot.AutonomousStateMachine):
    MODE_NAME = "Rev Roller"
    DEFAULT = False

    roller: components.Roller

    @magicbot.state(first=True)
    def start(self):
        self.next_state("rev")

    @magicbot.timed_state(duration=1.0, next_state="finish")
    def rev(self):
        self.roller.go(1, 0)

    @magicbot.state()
    def finish(self):
        self.done()
