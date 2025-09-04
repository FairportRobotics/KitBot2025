from magicbot import feedback
import navx
import time


class NavX:
    IS_CONNECTED = False

    def execute(self):
        self.IS_CONNECTED = self.ahrs.isConnected()

    def setup(self):
        self.ahrs = navx.AHRS.create_spi()

        self.ahrs.enableBoardlevelYawReset(True)

        # Calibrate the gyro. This takes a few seconds, so it's best to
        # do this at the beginning of the match when the robot is stationary.
        while self.ahrs.isCalibrating():
            time.sleep(0.1)

        self.reset()

    def reset(self):
        self.ahrs.reset()

    @feedback(key="Connected")
    def get_is_connected(self) -> bool:
        """Get whether the NavX is connected."""
        return self.IS_CONNECTED

    @feedback(key="Heading")
    def get_heading(self) -> float:
        """Get the fused 9-axis heading."""
        return self.ahrs.getFusedHeading()

    @feedback(key="Angle")
    def get_angle(self) -> float:
        """Get the angle of the robot."""
        return self.ahrs.getAngle()

    @feedback(key="Pitch")
    def get_pitch(self) -> float:
        """Get the pitch of the robot."""
        return self.ahrs.getPitch()

    @feedback(key="Roll")
    def get_roll(self) -> float:
        """Get the roll of the robot."""
        return self.ahrs.getRoll()

    @feedback(key="Z")
    def get_yaw(self) -> float:
        """Get the yaw of the robot."""
        return self.ahrs.getYaw()
