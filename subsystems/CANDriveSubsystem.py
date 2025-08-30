# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2
import constants
import rev
import wpilib
import wpilib.drive
from magicbot import feedback


class CANDriveSubsystem(commands2.Subsystem):
    # The next three lines were added for the genie bot
    MAX_OUTPUT = 0.0
    ROTATION = 0.0
    SPEED = 0.0

    def __init__(self) -> None:
        super().__init__()

        # spark max motor controllers in brushed mode
        self.leftLeader = rev.SparkMax(
            constants.LEFT_LEADER_ID, rev.SparkBase.MotorType.kBrushed
        )
        self.leftFollower = rev.SparkMax(
            constants.LEFT_FOLLOWER_ID, rev.SparkBase.MotorType.kBrushed
        )
        self.rightLeader = rev.SparkMax(
            constants.RIGHT_LEADER_ID, rev.SparkBase.MotorType.kBrushed
        )
        self.rightFollower = rev.SparkMax(
            constants.RIGHT_FOLLOWER_ID, rev.SparkBase.MotorType.kBrushed
        )

        # this is the differential drive instance which allows us to control
        # the drive with joysticks
        self.drive = wpilib.drive.DifferentialDrive(self.leftLeader, self.rightLeader)

        # set can timeouts. This program only sets parameters on startup and
        # doesn't get any parameters so a long timeout is acceptable. Programs
        # which set or get parameters during runtime likely want a timeout
        # closer or equal to the default.
        self.leftLeader.setCANTimeout(constants.CAN_TIMEOUT)
        self.rightLeader.setCANTimeout(constants.CAN_TIMEOUT)
        self.leftFollower.setCANTimeout(constants.CAN_TIMEOUT)
        self.rightFollower.setCANTimeout(constants.CAN_TIMEOUT)

        self.sparkConfig = rev.SparkMaxConfig()

        # enable voltage compensation. This makes the performance more consistent
        # at different levels of battery charge at the cost of some peak performance
        # with a fully charged battery
        self.sparkConfig.voltageCompensation(constants.VOLTAGE_COMPENSATION)

        # set current limit. This helps prevent tripping breakers
        self.sparkConfig.smartCurrentLimit(constants.DRIVE_MOTOR_CURRENT_LIMIT)

        # set to follow leader and then use to configure corresponding follower
        self.sparkConfig.follow(self.leftLeader)
        self.leftFollower.configure(
            self.sparkConfig,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )
        self.sparkConfig.follow(self.rightLeader)
        self.rightFollower.configure(
            self.sparkConfig,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )

        # disable following and use to configure leader. Invert before configuring
        # left side so that postive values drive both sides forward
        self.sparkConfig.disableFollowerMode()
        self.rightLeader.configure(
            self.sparkConfig,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )
        self.sparkConfig.inverted(True)
        self.leftLeader.configure(
            self.sparkConfig,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )

    # function to drive with joystick inputs
    def arcadeDrive(self, xSpeed: float, zRotation: float) -> None:
        # self.drive.arcadeDrive(xSpeed, zRotation)

        # =====================================================================
        # ALL LINES BELOW THIS COMMENT WERE ADDED FOR THE GENIE BOT
        # =====================================================================

        self.SPEED = self.MAX_OUTPUT * xSpeed
        self.ROTATION = self.MAX_OUTPUT * zRotation
        self.drive.arcadeDrive(self.SPEED, self.ROTATION, squareInputs=True)

    def execute(self):
        pass

    def set_max_output(self, max_output: float) -> None:
        """
        Set the maximum output of the drive.

        :param max_output: The maximum output to set, between 0.0 and 1.0.
        """
        if not 0.0 <= max_output <= 1.0:
            raise ValueError("Max output must be between 0.0 and 1.0")
        self.MAX_OUTPUT = max_output

    def get_drive_type(self) -> str:
        """Get the current drive type."""
        return "arcade"

    def stop(self) -> None:
        """Stop the drivetrain."""
        self.drive.stopMotor()

    @feedback(key="Max Output")
    def get_max_output(self) -> float:
        """Get the maximum output of the drive."""
        return self.MAX_OUTPUT

    @feedback(key="Speed")
    def get_speed(self) -> float:
        """Get the speed passed into the drive."""
        return self.SPEED

    @feedback(key="Rotation")
    def get_rotation(self) -> float:
        """Get the rotation passed into the drive."""
        return self.ROTATION
