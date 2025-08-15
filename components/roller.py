from magicbot import feedback
import rev

class Roller:
    roller_motor: rev.SparkMax

    def setup(self):
        self.speed = 0.0

    def execute(self):
        pass

    def run(self, forward: float, reverse: float):
        """
        Run the roller motor with joystick input.
        :param forward: The speed to run the roller motor at, between -1.0 and 1.0.
        :param reverse: The speed to run the roller motor in reverse, between -1.0 and 1
        """
        self.set_speed(forward - reverse)
        self.roller_motor.set(self.speed)

    def set_speed(self, speed: float):
        """
        Set the speed of the roller motor.
        :param speed: The speed to set the roller motor to, between -1.0 and 1.0.
        """
        self.speed = speed

    @feedback(key="Speed")
    def get_speed(self) -> float:
        """Get the speed passed into the drive."""
        return self.speed