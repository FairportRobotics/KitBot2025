from magicbot import feedback
import wpilib.drive


class TankDrive:
    drive: wpilib.drive.DifferentialDrive

    def setup(self):
        self.max_speed = 0.0
        self.mode = "arcade"  # Default to arcade drive
        self.rotation = 0.0
        self.speed = 0.0

    def execute(self):
        pass

    def go(self, left_stick: float, right_stick: float):
        if self.mode == "tank":
            self.drive.tankDrive(left_stick, right_stick)
        else:
            self.speed = left_stick
            self.rotation = right_stick
            if self.mode == "arcade":
                self.drive.arcadeDrive(self.speed, self.rotation, squareInputs=True)
            else:
                self.drive.curvatureDrive(
                    self.speed, self.rotation, allowTurnInPlace=True
                )

    def stop(self):
        self.speed = 0.0
        self.drive.stopMotor()

    @feedback(key="Max Speed")
    def get_max_speed(self) -> float:
        """Get the maximum speed of the drive."""
        return self.max_speed

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

    def set_max_speed(self, max_speed: float) -> None:
        """
        Set the maximum speed of the drive.

        :param max_speed: The maximum speed to set, between 0.0 and 1.0.
        """
        if max_speed < 0.0 or max_speed > 1.0:
            raise ValueError("Max speed must be between 0.0 and 1.0")
        self.max_speed = max_speed
        self.drive.setMaxOutput(self.max_speed)

    def set_mode(self, mode: str):
        """
        Set the drive mode.

        :param mode: The drive mode to set, either "arcade", "curvature" or "tank".
        """
        if mode not in ["arcade", "curvature", "tank"]:
            raise ValueError("Invalid drive mode. Use 'arcade', 'curvature' or 'tank'.")
        self.mode = mode
