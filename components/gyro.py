from magicbot import feedback
import navx
import time


class NavX:
    IS_CONNECTED = False

    def setup(self):
        self.ahrs = navx.AHRS.create_spi()

        self.ahrs.enableBoardlevelYawReset(True)

        # Calibrate the gyro. This takes a few seconds, so it's best to
        # do this at the beginning of the match when the robot is stationary.
        while self.ahrs.isCalibrating():
            time.sleep(0.1)

        self.reset()

    # =========================================================================
    # CONTROL METHODS
    # =========================================================================

    def execute(self):
        self.IS_CONNECTED = self.ahrs.isConnected()

    def reset(self):
        self.ahrs.reset()

    # =========================================================================
    # INFORMATIONAL METHODS
    # =========================================================================

    @feedback(key="Connected")
    def is_connected(self) -> bool:
        """Get whether the NavX is connected."""
        return self.IS_CONNECTED

    @feedback(key="Heading")
    def heading(self) -> float:
        """Get the fused 9-axis heading."""
        return self.ahrs.getFusedHeading()

    @feedback(key="Angle")
    def angle(self) -> float:
        """Get the angle of the robot."""
        return self.ahrs.getAngle()

    @feedback(key="Y")
    def pitch(self) -> float:
        """Get the pitch of the robot."""
        return self.ahrs.getPitch()

    @feedback(key="X")
    def roll(self) -> float:
        """Get the roll of the robot."""
        return self.ahrs.getRoll()

    @feedback(key="Z")
    def yaw(self) -> float:
        """Get the yaw of the robot."""
        return self.ahrs.getYaw()
