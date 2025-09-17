import constants
from magicbot import feedback
import rev


class Roller:
    SPEED = 0.0

    def setup(self) -> None:
        # Set up the roller motor as a brushed motor
        self.roller_motor = rev.SparkMax(
            constants.ROLLER_MOTOR_ID, rev.SparkLowLevel.MotorType.kBrushed
        )

        # Set can timeout. Because this project only sets parameters once on
        # construction, the timeout can be long without blocking robot operation. Code
        # which sets or gets parameters during operation may need a shorter timeout.
        self.roller_motor.setCANTimeout(constants.CAN_TIMEOUT)

        # Create and apply configuration for roller motor. Voltage compensation helps
        # the roller behave the same as the battery voltage dips. The current limit helps
        # prevent breaker trips or burning out the motor in the event the roller stalls.
        self.roller_config = rev.SparkMaxConfig()
        self.roller_config.voltageCompensation(constants.ROLLER_MOTOR_VOLTAGE_COMP)
        self.roller_config.smartCurrentLimit(constants.ROLLER_MOTOR_CURRENT_LIMIT)
        self.roller_motor.configure(
            self.roller_config,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )

    # =========================================================================
    # CONTROL METHODS
    # =========================================================================

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

    # =========================================================================
    # INFORMATIONAL METHODS
    # =========================================================================

    @feedback(key="Speed")
    def speed(self) -> float:
        """Get the speed of the drive."""
        return self.SPEED
