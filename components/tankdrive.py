from magicbot import feedback
import wpilib.drive


class TankDrive:
    drive: wpilib.drive.DifferentialDrive

    def setup(self):
        self.max_output = 0.0
        self.mode = "arcade"  # Default to arcade drive
        self.rotation = 0.0
        self.speed = 0.0

    def execute(self):
        pass

    def go(self, left_stick: float, right_stick: float):
        if self.mode == "tank":
            self.drive.tankDrive(left_stick, right_stick)
        else:
            self.speed = left_stick * self.max_output
            self.rotation = right_stick * self.max_output
            if self.mode == "arcade":
                self.drive.arcadeDrive(self.speed, self.rotation, squareInputs=True)
            else:
                self.drive.curvatureDrive(
                    self.speed, self.rotation, allowTurnInPlace=True
                )

    def stop(self):
        self.speed = 0.0
        self.drive.stopMotor()

    @feedback(key="Max Output")
    def get_max_output(self) -> float:
        """Get the maximum speed of the drive."""
        return self.max_output

    @feedback(key="Mode")
    def get_mode(self) -> str:
        """Get the current drive mode."""
        return self.mode

    @feedback(key="Speed")
    def get_speed(self) -> float:
        """Get the speed passed into the drive."""
        return self.speed

    @feedback(key="Rotation")
    def get_rotation(self) -> float:
        """Get the rotation passed into the drive."""
        return self.rotation

    def set_max_output(self, max_output: float) -> None:
        """
        Set the maximum output of the drive.

        :param max_output: The maximum output to set, between 0.0 and 1.0.
        """
        if max_output < 0.0 or max_output > 1.0:
            raise ValueError("Max output must be between 0.0 and 1.0")
        self.max_output = max_output
        #self.drive.setMaxOutput(self.max_output)

    def set_mode(self, mode: str):
        """
        Set the drive mode.

        :param mode: The drive mode to set, either "arcade", "curvature" or "tank".
        """
        if mode not in ["arcade", "curvature", "tank"]:
            raise ValueError("Invalid drive mode. Use 'arcade', 'curvature' or 'tank'.")
        self.mode = mode
