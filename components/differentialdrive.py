import constants
from magicbot import feedback
import rev
import wpilib.drive


class DifferentialDrive:
    DRIVE_TYPE = "arcade"
    ROTATION = 0.0
    SPEED = 0.0

    def execute(self):
        pass

    def setup(self):
        # create brushed motors for drive
        self.left_leader = rev.SparkMax(
            constants.LEFT_LEADER_ID, rev.SparkLowLevel.MotorType.kBrushed
        )
        self.left_follower = rev.SparkMax(
            constants.LEFT_FOLLOWER_ID, rev.SparkLowLevel.MotorType.kBrushed
        )
        self.right_leader = rev.SparkMax(
            constants.RIGHT_LEADER_ID, rev.SparkLowLevel.MotorType.kBrushed
        )
        self.right_follower = rev.SparkMax(
            constants.RIGHT_FOLLOWER_ID, rev.SparkLowLevel.MotorType.kBrushed
        )

        # Set up differential drive class
        self.drive = wpilib.drive.DifferentialDrive(self.left_leader, self.right_leader)

        # Set can timeout. Because this project only sets parameters once on
        # construction, the timeout can be long without blocking robot operation. Code
        # which sets or gets parameters during operation may need a shorter timeout.
        self.left_follower.setCANTimeout(constants.CAN_TIMEOUT)
        self.right_follower.setCANTimeout(constants.CAN_TIMEOUT)
        self.left_leader.setCANTimeout(constants.CAN_TIMEOUT)
        self.right_leader.setCANTimeout(constants.CAN_TIMEOUT)

        # Create the configuration to apply to motors. Voltage compensation
        # helps the robot perform more similarly on different
        # battery voltages (at the cost of a little bit of top speed on a fully charged
        # battery). The current limit helps prevent tripping
        # breakers.
        self.spark_max_config = rev.SparkMaxConfig()
        self.spark_max_config.voltageCompensation(constants.VOLTAGE_COMPENSATION)
        self.spark_max_config.smartCurrentLimit(constants.DRIVE_MOTOR_CURRENT_LIMIT)

        # Set configuration to follow leader and then apply it to corresponding
        # follower. Resetting in case a new controller is swapped
        # in and persisting in case of a controller reset due to breaker trip
        self.spark_max_config.follow(self.left_leader)

        self.left_follower.configure(
            self.spark_max_config,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )
        self.spark_max_config.follow(self.right_leader)
        self.right_follower.configure(
            self.spark_max_config,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )

        # Remove following, then apply config to right leader
        self.spark_max_config.disableFollowerMode()
        self.right_leader.configure(
            self.spark_max_config,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )

        # Set config to inverted and then apply to left leader. Set Left side inverted
        #  so that postive values drive both sides forward
        self.spark_max_config.inverted(True)
        self.left_leader.configure(
            self.spark_max_config,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )

    def go(self, left_stick: float, right_stick: float):
        if self.DRIVE_TYPE == "tank":
            self.drive.tankDrive(left_stick, right_stick)
        else:
            self.SPEED = left_stick
            self.ROTATION = right_stick
            if self.DRIVE_TYPE == "arcade":
                self.drive.arcadeDrive(self.SPEED, self.ROTATION, squareInputs=True)
            else:
                self.drive.curvatureDrive(
                    self.SPEED, self.ROTATION, allowTurnInPlace=True
                )

    def stop(self):
        self.SPEED = 0.0
        self.ROTATION = 0.0
        self.drive.stopMotor()

    @feedback(key="Drive Type")
    def get_drive_type(self) -> str:
        """Get the current drive type."""
        return self.DRIVE_TYPE

    @feedback(key="Speed")
    def get_speed(self) -> float:
        """Get the speed passed into the drive."""
        return self.SPEED

    @feedback(key="Rotation")
    def get_rotation(self) -> float:
        """Get the rotation passed into the drive."""
        return self.ROTATION

    def set_drive_type(self, drive_type: str):
        """
        Set the drive type.

        :param drive_type: The drive type to set, either "arcade", "curvature" or "tank".
        """
        if drive_type not in ["arcade", "curvature", "tank"]:
            raise ValueError("Invalid drive type. Use 'arcade', 'curvature' or 'tank'.")
        self.DRIVE_TYPE = drive_type
