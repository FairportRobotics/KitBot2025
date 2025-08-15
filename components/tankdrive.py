from magicbot import feedback
import wpilib.drive

class TankDrive:
    drive: wpilib.drive.DifferentialDrive
    
    def setup(self):
        self.speed = 0.0
        self.rotation = 0.0
        self.mode = "arcade"  # Default to arcade drive

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
                self.drive.curvatureDrive(self.speed, self.rotation, allowTurnInPlace=True)
            

    def stop(self):
        self.speed = 0.0
        self.drive.stopMotor()

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

    def set_mode(self, mode: str):
        """
        Set the drive mode.

        :param mode: The drive mode to set, either "arcade", "curvature" or "tank".
        """
        if mode not in ["arcade", "curvature", "tank"]:
            raise ValueError("Invalid drive mode. Use 'arcade', 'curvature' or 'tank'.")
        self.mode = mode
