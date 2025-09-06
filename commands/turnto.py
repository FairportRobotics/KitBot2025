import components
from magicbot import tunable
from wpimath.controller import PIDController


class TurnTo:
    drivetrain: components.DifferentialDrive
    gyro: components.NavX

    P = tunable(0.02)
    I = tunable(0.0)
    D = tunable(0.001)

    def setup(self) -> None:
        self.pid = PIDController(self.P, self.I, self.D)
        self.pid.setTolerance(2.0)  # degrees
        self.target_angle = 0
        self.is_executing = False

    def set_target_angle(self, angle) -> None:
        self.target_angle = angle

    def engage(self):
        self.pid.setSetpoint(self.target_angle)
        # self.pid.reset()
        self.is_executing = True

    def interupt(self) -> None:
        self.is_executing = False

    def execute(self) -> None:
        if not self.is_executing:
            return

        current_angle = self.gyro.get_heading()
        output = self.pid.calculate(current_angle)
        self.drivetrain.go(0, output)

        if self.pid.atSetpoint():
            self.is_executing = False
            self.drivetrain.stop()
