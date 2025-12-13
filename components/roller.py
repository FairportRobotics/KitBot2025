import constants
from magicbot import feedback
import phoenix5 as ctre


class Roller:
    MOTOR: ctre.TalonSRX
    SPEED: float = 0.0

    # =========================================================================
    # CONTROL METHODS
    # =========================================================================

    def execute(self) -> None:
        pass

    def go(self, forward: float, reverse: float) -> None:
        """
        Run the roller motor with joystick input.
        :param forward: The speed to run the roller motor at, between -1.0 and 1.0.
        :param reverse: The speed to run the roller motor in reverse, between -1.0 and 1
        """
        self.set_speed(forward - reverse)
        self.MOTOR.set(ctre.ControlMode.PercentOutput, self.SPEED)

    def stop(self) -> None:
        """
        Stop the roller motor
        """
        self.MOTOR.set(ctre.ControlMode.PercentOutput, 0.0)

    def set_speed(self, speed: float) -> None:
        """
        Set the speed of the roller motor.
        :param speed: The speed to set the roller motor to, between -1.0 and 1.0.
        """
        self.SPEED = speed

    # =========================================================================
    # INFORMATIONAL METHODS
    # =========================================================================

    @feedback(key="Speed")
    def speed(self) -> float:
        """Get the speed of the drive."""
        return self.SPEED
