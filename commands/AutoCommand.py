# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2
import wpilib
from subsystems.CANDriveSubsystem import CANDriveSubsystem


# Command class to run the robot forwards at 1/2 power for 1 second in autonomous.
class AutoCommand(commands2.Command):
    # Constructor for CAN command
    def __init__(self, driveSubsystem: CANDriveSubsystem) -> None:
        self.driveSubsystem = driveSubsystem
        self.timer = wpilib.Timer()
        self.seconds = 1.0
        super().__init__()

    # called when command is initially scheduled
    def initialize(self) -> None:
        self.timer.restart()

    # called every loop cycle (~20 ms) while command is running
    def execute(self) -> None:
        self.driveSubsystem.arcadeDrive(0.5, 0.0)

    # called after every execution to check if command is finished
    def isFinished(self) -> bool:
        return self.timer.get() >= self.seconds

    # called when command ends
    def end(self, interrupted: bool) -> None:
        self.driveSubsystem.arcadeDrive(0.0, 0.0)
