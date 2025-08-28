from magicbot import feedback
import wpilib.drive


class DifferentialDrive:
    DRIVE_TYPE = "arcade"
    MAX_OUTPUT = 0.0
    ROTATION = 0.0
    SPEED = 0.0

    drive: wpilib.drive.DifferentialDrive

    def execute(self):
        pass

    def go(self, left_stick: float, right_stick: float):
        if self.DRIVE_TYPE == "tank":
            self.drive.tankDrive(left_stick, right_stick)
        else:
            self.SPEED = left_stick * self.MAX_OUTPUT
            self.ROTATION = right_stick * self.MAX_OUTPUT
            if self.DRIVE_TYPE == "arcade":
                self.drive.arcadeDrive(self.SPEED, self.ROTATION, squareInputs=True)
            else:
                self.drive.curvatureDrive(
                    self.SPEED, self.ROTATION, allowTurnInPlace=True
                )

    def stop(self):
        self.SPEED = 0.0
        self.drive.stopMotor()

    @feedback(key="Drive Type")
    def get_drive_type(self) -> str:
        """Get the current drive type."""
        return self.DRIVE_TYPE

    @feedback(key="Max Output")
    def get_max_output(self) -> float:
        """Get the maximum output of the drive."""
        return self.MAX_OUTPUT

    @feedback(key="Speed")
    def get_speed(self) -> float:
        """Get the speed passed into the drive."""
        return self.SPEED

    @feedback(key="Rotation")
    def get_rotation(self) -> float:
        """Get the rotation passed into the drive."""
        return self.ROTATION

    def set_drive_type(self, drive_type: str):
        """
        Set the drive type.

        :param drive_type: The drive type to set, either "arcade", "curvature" or "tank".
        """
        if drive_type not in ["arcade", "curvature", "tank"]:
            raise ValueError("Invalid drive type. Use 'arcade', 'curvature' or 'tank'.")
        self.DRIVE_TYPE = drive_type

    def set_max_output(self, max_output: float) -> None:
        """
        Set the maximum output of the drive.

        :param max_output: The maximum output to set, between 0.0 and 1.0.
        """
        if max_output < 0.0 or max_output > 1.0:
            raise ValueError("Max output must be between 0.0 and 1.0")
        self.MAX_OUTPUT = max_output
