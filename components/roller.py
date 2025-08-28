from magicbot import feedback
import rev


class Roller:
    SPEED = 0.0

    roller_motor: rev.SparkMax

    def execute(self) -> None:
        pass

    def run(self, forward: float, reverse: float) -> None:
        """
        Run the roller motor with joystick input.
        :param forward: The speed to run the roller motor at, between -1.0 and 1.0.
        :param reverse: The speed to run the roller motor in reverse, between -1.0 and 1
        """
        self.set_speed(forward - reverse)
        self.roller_motor.set(self.SPEED)

    def set_speed(self, speed: float) -> None:
        """
        Set the speed of the roller motor.
        :param speed: The speed to set the roller motor to, between -1.0 and 1.0.
        """
        self.SPEED = speed

    @feedback(key="Speed")
    def get_speed(self) -> float:
        """Get the speed of the drive."""
        return self.SPEED
