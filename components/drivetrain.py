import constants
from magicbot import feedback
import wpilib
import wpilib.drive
import phoenix5 as ctre


class DriveTrain:
    LEFT_LEADER: ctre.TalonFX
    LEFT_FOLLOWER: ctre.TalonFX
    RIGHT_LEADER: ctre.TalonFX
    RIGHT_FOLLOWER: ctre.TalonFX

    THROTTLE: float = 0.0
    ROTATION: float = 0.0

    def setup(self):
        # Set up differential drive class
        self.drive = wpilib.drive.DifferentialDrive(self.LEFT_LEADER, self.RIGHT_LEADER)

    # =========================================================================
    # CONTROL METHODS
    # =========================================================================

    def execute(self):
        pass

    def go(self, throttle: float, rotation: float, square_inputs: bool = True) -> None:
        self.set_throttle(throttle)
        self.set_rotation(rotation)
        self.drive.arcadeDrive(self.THROTTLE, self.ROTATION, squareInputs=square_inputs)

    def stop(self) -> None:
        self.set_throttle(0.0)
        self.set_rotation(0.0)
        self.drive.stopMotor()

    @feedback(key="Throttle")
    def throttle(self) -> float:
        return self.THROTTLE

    @feedback(key="Rotation")
    def rotation(self) -> float:
        return self.ROTATION

    def set_throttle(self, throttle):
        self.THROTTLE = throttle

    def set_rotation(self, rotation):
        self.ROTATION = rotation
