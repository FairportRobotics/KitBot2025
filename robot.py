import components
import constants
import reefscape
import magicbot
import os

os.environ["HALSIMXRP_HOST"] = "192.168.42.1"
os.environ["HALSIMXRP_PORT"] = "3540"


class MyRobot(magicbot.MagicRobot):
    controller: components.XboxController
    drivetrain: components.DifferentialDrive
    roller: components.Roller

    CHANGE_TARGET_REEF_LEVEL_BY = 0
    CHANGE_TARGET_REEF_SIDE_BY = 0
    TARGET_REEF_LEVEL = 0
    TARGET_REEF_SIDE = 0

    def createObjects(self):
        self.controller_port = constants.CONTROLLER_PORT
        # wpilib.DataLogManager.start()
        # wpilib.DataLogManager.logNetworkTables(True)
        # wpilib.DataLogManager.logConsoleOutput(True)

    def teleopPeriodic(self):
        # ============================================================
        # BUMPER HANDLING
        # ============================================================
        # Switch controller between driver and operator modes when the bumpers are pressed
        if self.controller.right_bumper_pressed():
            self.controller.set_mode("operator")

        if self.controller.left_bumper_pressed():
            self.controller.set_mode("driver")

        # =============================================================
        # BUTTON HANDLING
        # =============================================================
        if self.controller.b_button_pressed():
            self.drivetrain.set_max_output(1.0)  # Full output
        else:
            self.drivetrain.set_max_output(constants.DEFAULT_MAX_OUTPUT)

        # =============================================================
        # JOYSTICK HANDLING
        # =============================================================
        # Get the input from the controller
        left_x, left_y, right_x, right_y = self.controller.get_joysticks()

        # Handle the controller input based on the controller mode
        if self.controller.get_mode() == "operator":
            # Controller is in operator mode
            self.roller.run(-left_y, -right_y)
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
            self.drivetrain.go(left_stick, right_stick)

        # ============================================================
        # D-PAD HANDLING
        # ============================================================
        # The d-pad is used to select the target reef level and side
        if self.controller.dpad_up_pressed():
            self.CHANGE_TARGET_REEF_LEVEL_BY = 1

        if self.controller.dpad_down_pressed():
            self.CHANGE_TARGET_REEF_LEVEL_BY = -1

        if (
            self.controller.dpad_up_was_pressed()
            or self.controller.dpad_down_was_pressed()
        ):
            new_target_reef_level = (
                self.TARGET_REEF_LEVEL + self.CHANGE_TARGET_REEF_LEVEL_BY
            )
            if new_target_reef_level >= 0 and new_target_reef_level <= 4:
                self.TARGET_REEF_LEVEL = new_target_reef_level
                print(f"Reef level set to {self.TARGET_REEF_LEVEL}")

        if self.controller.dpad_right_pressed():
            self.CHANGE_TARGET_REEF_SIDE_BY = 1

        if self.controller.dpad_left_pressed():
            self.CHANGE_TARGET_REEF_SIDE_BY = -1

        if (
            self.controller.dpad_left_was_pressed()
            or self.controller.dpad_right_was_pressed()
        ):
            new_target_reef_side = (
                self.TARGET_REEF_SIDE + self.CHANGE_TARGET_REEF_SIDE_BY
            )
            if new_target_reef_side >= 0 and new_target_reef_side <= 12:
                self.TARGET_REEF_SIDE = new_target_reef_side
                print(f"Reef side set to {reefscape.REEF_SIDES[self.TARGET_REEF_SIDE]}")

        # ============================================================
        # X BUTTON HANDLING
        # ============================================================
        # The x button is used to execute an autonomous routine based on
        # the selected target reef level and side
        if self.controller.x_button_was_pressed():
            print(
                f"Starting autonomous to level {self.TARGET_REEF_LEVEL}, side {reefscape.REEF_SIDES[self.TARGET_REEF_SIDE]}"
            )
