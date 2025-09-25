import components
import constants
import magicbot


class MyRobot(magicbot.MagicRobot):
    controller: components.XboxController
    drivetrain: components.DriveTrain
    roller: components.Roller
    # gyro: components.NavX

    def createObjects(self):
        self.controller_port = constants.CONTROLLER_PORT
        self.controller_mode = "drive"
        self.max_output = constants.DEFAULT_MAX_OUTPUT

    def teleopPeriodic(self):
        # ============================================================
        # BUMPER HANDLING
        # ============================================================
        # Switch controller between driver and operator modes when the bumpers are pressed
        if self.controller.x_button_was_pressed():
            self.controller.set_mode("roller")

        if self.controller.y_button_was_pressed():
            self.controller.set_mode("drive")

        # =============================================================
        # B BUTTON HANDLING
        # =============================================================
        # Give a boost of speed when the B button is pressed
        if self.controller.b_button_pressed():
            self.max_output = 1  # Full output
        else:
            self.max_output = constants.DEFAULT_MAX_OUTPUT

        # =============================================================
        # JOYSTICK HANDLING
        # =============================================================
        # Get the input from the controller
        left_x, left_y, right_x, right_y = self.controller.get_joysticks()

        # Handle the controller input based on the controller mode
        if self.controller.get_mode() == "roller":
            # Controller is in operator mode
            self.roller.go(-left_y, -right_y)
        else:
            # Controller is in driver mode
            self.drivetrain.go(-left_y * self.max_output, -right_x * self.max_output)
