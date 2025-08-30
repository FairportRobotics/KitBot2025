import components
import commands
import constants
import geniebot
import reefscape
import subsystems
import wpilib
import rev
import os

os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"


class MyRobot(geniebot.GenieRobot):
    xbox_controller: components.XboxController
    drivetrain: subsystems.CANDriveSubsystem
    roller: subsystems.CANRollerSubsystem

    CHANGE_TARGET_REEF_LEVEL_BY = 0
    CHANGE_TARGET_REEF_SIDE_BY = 0
    DEFAULT_MAX_SPEED = 0.8
    DPAD_UP_OR_DOWN_WAS_PRESSED = False
    DPAD_LEFT_OR_RIGHT_WAS_PRESSED = False
    TARGET_REEF_LEVEL = 0
    TARGET_REEF_SIDE = 0
    X_BUTTON_WAS_PRESSED = False

    def createObjects(self):
        # wpilib.DataLogManager.start()
        # wpilib.DataLogManager.logNetworkTables(True)
        # wpilib.DataLogManager.logConsoleOutput(True)

        # =============================================================
        # CONTROLLER
        # =============================================================
        self.controller = wpilib.XboxController(constants.CONTROLLER_PORT)

    def teleopPeriodic(self):
        # ============================================================
        # BUMPER HANDLING
        # ============================================================
        # Switch controller between driver and operator modes when the bumpers are pressed
        if self.xbox_controller.right_bumper_pressed():
            self.xbox_controller.set_mode("operator")

        if self.xbox_controller.left_bumper_pressed():
            self.xbox_controller.set_mode("driver")

        # =============================================================
        # BUTTON HANDLING
        # =============================================================
        if self.xbox_controller.b_button_pressed():
            self.drivetrain.set_max_output(1.0)  # Full speed
        else:
            self.drivetrain.set_max_output(self.DEFAULT_MAX_SPEED)  # Default speed

        # =============================================================
        # JOYSTICK HANDLING
        # =============================================================
        # Get the input from the controller
        left_x, left_y, right_x, right_y = self.xbox_controller.get_joysticks()

        # Handle the controller input based on the controller mode
        if self.xbox_controller.get_mode() == "operator":
            # Controller is in operator mode
            commands.RollerCommand(-left_y, -right_y, self.roller).execute()
        else:
            # Controller is in driver mode
            drivetrain_type = self.drivetrain.get_drive_type()
            if drivetrain_type in ("arcade", "curvature"):
                left_stick = -left_y
                right_stick = -right_x
            else:
                # Using tank drive
                left_stick = -left_y
                right_stick = -right_y
            # Use the controller input to move the robot
            # self.drivetrain.go(left_stick, right_stick)
            commands.DriveCommand(left_stick, right_stick, self.drivetrain).execute()

        # ============================================================
        # D-PAD HANDLING
        # ============================================================
        # The d-pad is used to select the target reef level and side
        if self.xbox_controller.dpad_up_pressed():
            self.CHANGE_TARGET_REEF_LEVEL_BY = 1
            self.DPAD_UP_OR_DOWN_WAS_PRESSED = True

        if self.xbox_controller.dpad_down_pressed():
            self.CHANGE_TARGET_REEF_LEVEL_BY = -1
            self.DPAD_UP_OR_DOWN_WAS_PRESSED = True

        if (
            not (
                self.xbox_controller.dpad_up_pressed()
                or self.xbox_controller.dpad_down_pressed()
            )
            and self.DPAD_UP_OR_DOWN_WAS_PRESSED
        ):
            new_target_reef_level = (
                self.TARGET_REEF_LEVEL + self.CHANGE_TARGET_REEF_LEVEL_BY
            )
            if new_target_reef_level >= 0 and new_target_reef_level <= 4:
                self.TARGET_REEF_LEVEL = new_target_reef_level
                print(f"Reef level set to {self.TARGET_REEF_LEVEL}")
            self.DPAD_UP_OR_DOWN_WAS_PRESSED = False

        if self.xbox_controller.dpad_right_pressed():
            self.CHANGE_TARGET_REEF_SIDE_BY = 1
            self.DPAD_LEFT_OR_RIGHT_WAS_PRESSED = True

        if self.xbox_controller.dpad_left_pressed():
            self.CHANGE_TARGET_REEF_SIDE_BY = -1
            self.DPAD_LEFT_OR_RIGHT_WAS_PRESSED = True

        if (
            not (
                self.xbox_controller.dpad_left_pressed()
                or self.xbox_controller.dpad_right_pressed()
            )
            and self.DPAD_LEFT_OR_RIGHT_WAS_PRESSED
        ):
            new_target_reef_side = (
                self.TARGET_REEF_SIDE + self.CHANGE_TARGET_REEF_SIDE_BY
            )
            if new_target_reef_side >= 0 and new_target_reef_side <= 12:
                self.TARGET_REEF_SIDE = new_target_reef_side
                print(f"Reef side set to {reefscape.REEF_SIDES[self.TARGET_REEF_SIDE]}")
            self.DPAD_LEFT_OR_RIGHT_WAS_PRESSED = False

        # ============================================================
        # X BUTTON HANDLING
        # ============================================================
        # The x button is used to execute an autonomous routine based on
        # the selected target reef level and side
        if self.xbox_controller.x_button_pressed():
            self.X_BUTTON_WAS_PRESSED = True

        if not self.xbox_controller.x_button_pressed() and self.X_BUTTON_WAS_PRESSED:
            print(
                f"Starting autonomous to level {self.TARGET_REEF_LEVEL}, side {reefscape.REEF_SIDES[self.TARGET_REEF_SIDE]}"
            )
            self.X_BUTTON_WAS_PRESSED = False
