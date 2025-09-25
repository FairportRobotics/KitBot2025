import constants
from magicbot import feedback
import wpilib
import wpilib.drive


class DriveTrain:
    THROTTLE = 0
    ROTATION = 0

    def setup(self):
        # create brushed motors for drive
        self.left_leader = wpilib.PWMVictorSPX(constants.LEFT_LEADER_ID)
        self.left_follower = wpilib.PWMVictorSPX(constants.LEFT_FOLLOWER_ID)
        self.right_leader = wpilib.PWMVictorSPX(constants.RIGHT_LEADER_ID)
        self.right_follower = wpilib.PWMVictorSPX(constants.RIGHT_FOLLOWER_ID)

        self.left_leader.setInverted(True)

        # Set up differential drive class
        self.drive = wpilib.drive.DifferentialDrive(self.left_leader, self.right_leader)

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
        self.set_throttle(0)
        self.set_rotation(0)
        self.drive.stopMotor()

    @feedback(key="Throttle")
    def throttle(self):
        return self.THROTTLE

    @feedback(key="Rotation")
    def rotation(self):
        return self.ROTATION

    def set_throttle(self, throttle):
        self.THROTTLE = throttle

    def set_rotation(self, rotation):
        self.ROTATION = rotation
