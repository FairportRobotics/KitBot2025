# ============================================================
# CONTROLLER CONSTANTS
# ============================================================
# The port the controller is connected to
CONTROLLER_PORT = 0

# ============================================================
# DRIVETRAIN CONSTANTS
# ============================================================
LEFT_LEADER_ID = 1
LEFT_FOLLOWER_ID = 2
RIGHT_LEADER_ID = 3
RIGHT_FOLLOWER_ID = 4
DRIVE_MOTOR_CURRENT_LIMIT = 60

CAN_TIMEOUT = 250
VOLTAGE_COMPENSATION = 12

DEFAULT_MAX_OUTPUT = 0.8

# ============================================================
# ROLLER CONSTANTS
# ============================================================
ROLLER_MOTOR_ID = 5
ROLLER_MOTOR_CURRENT_LIMIT = 60
ROLLER_MOTOR_VOLTAGE_COMP = 10
ROLLER_EJECT_VALUE = 0.44

# ============================================================
# PID CONSTANTS
# ============================================================
TURN_P = 0.03
TURN_I = 0.0
TURN_D = 0.0
TURN_F = 0.00
TURN_TOLERANCE_DEGREES = 2.0
