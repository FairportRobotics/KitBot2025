import components
import constants
import magicbot
import phoenix5 as ctre


class MyRobot(magicbot.MagicRobot):
    CONTROLLER: components.XboxController
    DRIVETRAIN: components.DriveTrain
    ROLLER: components.Roller
    # GYRO: components.NavX

    def createObjects(self):
        self.CONTROLLER_PORT = constants.CONTROLLER_PORT
        self.CONTROLLER_MODE = "drive"
        self.MAX_OUTPUT = constants.DEFAULT_MAX_OUTPUT

        # create brushed motors for drive
        self.DRIVETRAIN_LEFT_LEADER = ctre.TalonSRX(
            constants.CAN_BUS_IDS["LEFT LEADER MOTOR"]
        )
        self.DRIVETRAIN_LEFT_FOLLOWER = ctre.TalonSRX(
            constants.CAN_BUS_IDS["LEFT FOLLOWER MOTOR"]
        )
        self.DRIVETRAIN_RIGHT_LEADER = ctre.TalonSRX(
            constants.CAN_BUS_IDS["RIGHT LEADER MOTOR"]
        )
        self.DRIVETRAIN_RIGHT_FOLLOWER = ctre.TalonSRX(
            constants.CAN_BUS_IDS["RIGHT FOLLOWER MOTOR"]
        )

        self.DRIVETRAIN_LEFT_LEADER.setInverted(True)
        self.DRIVETRAIN_LEFT_FOLLOWER.setInverted(True)

        self.ROLLER_MOTOR = ctre.TalonSRX(constants.CAN_BUS_IDS["ROLLER MOTOR"])

    def teleopPeriodic(self):
        self.CONTROLLER.capture_button_presses()

        # ============================================================
        # BUTTON HANDLING
        # ============================================================
        # Switch controller between driver and operator modes when buttons are pressed
        if self.CONTROLLER.x_button_was_pressed():
            self.CONTROLLER_MODE = "roller"

        if self.CONTROLLER.y_button_was_pressed():
            self.CONTROLLER_MODE = "drive"

        # =============================================================
        # B BUTTON HANDLING
        # =============================================================
        # Give a boost of speed when the B button is pressed
        if self.CONTROLLER.b_button_pressed():
            self.MAX_OUTPUT = 1  # Full output
        else:
            self.MAX_OUTPUT = constants.DEFAULT_MAX_OUTPUT

        # =============================================================
        # JOYSTICK HANDLING
        # =============================================================
        # Get the input from the controller
        left_x, left_y, right_x, right_y = self.CONTROLLER.get_joysticks()

        # Handle the controller input based on the controller mode
        if self.CONTROLLER_MODE == "roller":
            # Controller is in operator mode
            self.ROLLER.go(-left_y, -right_y)
        else:
            # Controller is in driver mode
            self.DRIVETRAIN.go(-left_y * self.MAX_OUTPUT, -right_x * self.MAX_OUTPUT)
