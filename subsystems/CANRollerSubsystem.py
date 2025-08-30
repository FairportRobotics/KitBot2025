# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.F

import commands2
import constants
import rev


class CANRollerSubsystem(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()

        self.rollerMotor = rev.SparkMax(
            constants.ROLLER_MOTOR_ID, rev.SparkBase.MotorType.kBrushed
        )

        # set can timeouts. This program only sets parameters on startup and
        # doesn't get any parameters so a long timeout is acceptable. Programs
        # which set or get parameters during runtime likely want a timeout
        # closer or equal to the default.
        self.rollerMotor.setCANTimeout(constants.CAN_TIMEOUT)

        self.sparkConfig = rev.SparkMaxConfig()
        # enable voltage compensation. This makes the performance more consistent
        # at different levels of battery charge at the cost of some peak performance
        # with a fully charged battery. Because the roller never really needs the full
        # speed, the compensation value is set very conservatively
        self.sparkConfig.voltageCompensation(constants.ROLLER_MOTOR_VOLTAGE_COMP)
        self.sparkConfig.smartCurrentLimit(constants.ROLLER_MOTOR_CURRENT_LIMIT)
        self.rollerMotor.configure(
            self.sparkConfig,
            rev.SparkBase.ResetMode.kResetSafeParameters,
            rev.SparkBase.PersistMode.kPersistParameters,
        )

    # function to run the roller with joystick inputs
    def runRoller(self, forward: float, reverse: float) -> None:
        self.rollerMotor.set(forward - reverse)
