import commands
import components
import constants
import geniebot
import os
import reefscape
import subsystems
# import wpilib

os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"


class MyRobot(geniebot.GenieRobot):
    CHANGE_TARGET_REEF_LEVEL_BY = 0
    CHANGE_TARGET_REEF_SIDE_BY = 0
    DEFAULT_MAX_SPEED = 0.8
    TARGET_REEF_LEVEL = 0
    TARGET_REEF_SIDE = 0

    drivetrain: subsystems.CANDriveSubsystem
    roller: subsystems.CANRollerSubsystem
    xbox_controller: components.XboxController
    xbox_controller_port: int

    def createObjects(self):
        # wpilib.DataLogManager.start()
        # wpilib.DataLogManager.logNetworkTables(True)
        # wpilib.DataLogManager.logConsoleOutput(True)
        self.xbox_controller_port = constants.CONTROLLER_PORT

    def teleopPeriodic(self):
        self.xbox_controller.capture_buton_presses()
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

        if self.xbox_controller.dpad_down_pressed():
            self.CHANGE_TARGET_REEF_LEVEL_BY = -1

        if (
            self.xbox_controller.dpad_up_was_pressed()
            or self.xbox_controller.dpad_down_was_pressed()
        ):
            new_target_reef_level = (
                self.TARGET_REEF_LEVEL + self.CHANGE_TARGET_REEF_LEVEL_BY
            )
            if new_target_reef_level >= 0 and new_target_reef_level <= 4:
                self.TARGET_REEF_LEVEL = new_target_reef_level
                print(f"Reef level set to {self.TARGET_REEF_LEVEL}")

        if self.xbox_controller.dpad_right_pressed():
            self.CHANGE_TARGET_REEF_SIDE_BY = 1

        if self.xbox_controller.dpad_left_pressed():
            self.CHANGE_TARGET_REEF_SIDE_BY = -1

        if (
            self.xbox_controller.dpad_left_was_pressed()
            or self.xbox_controller.dpad_right_was_pressed()
        ):
            new_target_reef_side = (
                self.TARGET_REEF_SIDE + self.CHANGE_TARGET_REEF_SIDE_BY
            )
            if new_target_reef_side >= 0 and new_target_reef_side <= 11:
                self.TARGET_REEF_SIDE = new_target_reef_side
                print(f"Reef side set to {reefscape.REEF_SIDES[self.TARGET_REEF_SIDE]}")

        # ============================================================
        # X BUTTON HANDLING
        # ============================================================
        # The x button is used to execute an autonomous routine based on
        # the selected target reef level and side
        if self.xbox_controller.x_button_was_pressed():
            print(
                f"Starting autonomous to level {self.TARGET_REEF_LEVEL}, side {reefscape.REEF_SIDES[self.TARGET_REEF_SIDE]}"
            )
