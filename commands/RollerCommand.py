# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.

import commands2

from subsystems.CANRollerSubsystem import CANRollerSubsystem


# Command class to run the roller based on joystick input
class RollerCommand(commands2.Command):
    def __init__(
        self,
        forward: lambda forward: forward,
        reverse: lambda reverse: reverse,
        rollerSubsystem: CANRollerSubsystem,
    ) -> None:
        self.rollerSubsystem = rollerSubsystem
        self.forward = forward
        self.reverse = reverse
        self.addRequirements(rollerSubsystem)
        super().__init__()

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self.rollerSubsystem.runRoller(self.forward, self.reverse)

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        return False
