import components
from magicbot import tunable
from wpimath.controller import PIDController


class TurnTo:
    drivetrain: components.DifferentialDrive
    gyro: components.NavX

    IS_EXECUTING = False
    TARGET_ANGLE = 0
    # Turn PID controler settings
    P = tunable(0.02)
    I = tunable(0.0)
    D = tunable(0.001)
    TOLERANCE = tunable(2.0)  # degrees

    def setup(self) -> None:
        self.pid = PIDController(self.P, self.I, self.D)
        self.pid.setTolerance(self.TOLERANCE)

    def engage(self):
        self.pid.reset()
        self.pid.setSetpoint(self.TARGET_ANGLE)
        self.IS_EXECUTING = True

    def execute(self) -> None:
        if not self.IS_EXECUTING:
            return

        current_angle = self.gyro.get_heading()
        output = self.pid.calculate(current_angle)
        self.drivetrain.go(0, output)

        if self.pid.atSetpoint():
            self.interupt()

    def interupt(self) -> None:
        self.IS_EXECUTING = False

    def set_target_angle(self, angle) -> None:
        self.TARGET_ANGLE = angle
