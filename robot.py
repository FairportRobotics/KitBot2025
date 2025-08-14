import components
import constants
import magicbot
import wpilib


class Robot(magicbot.MagicRobot):
    controller: components.XboxController

    def createObjects(self):
        wpilib.DataLogManager.start()
        wpilib.DataLogManager.logNetworkTables(True)
        wpilib.DataLogManager.logConsoleOutput(True)
        # =============================================================
        # CONTROLLER
        # =============================================================
        self.xbox_controller = wpilib.XboxController(constants.CONTROLLER_PORT)
        # =============================================================
        # MOTORS
        # =============================================================

    def teleopPeriodic(self):
        # Get the input from the controller
        left_x, left_y, right_x, right_y = self.controller.get_joysticks()

        drivetrain_mode = self.drivetrain.get_mode()
        if drivetrain_mode in ("arcade", "curvature"):
            left_stick = -left_y
            right_stick = -right_x
        else:
            # Using tank drive
            left_stick = -left_y
            right_stick = -right_y
        # Use the controller input to move the robot
        self.drivetrain.go(left_stick, right_stick)