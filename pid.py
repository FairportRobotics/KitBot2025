import time
import random


class PIDController:
    def __init__(self, p, i, d, setpoint=0, tolerance=0) -> None:
        self.p = p
        self.i = i
        self.d = d
        self.setpoint = setpoint
        self.tolerance = tolerance
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()
        self.current_value = 0

    def at_setpoint(self) -> bool:
        return abs(self.current_value - self.setpoint) <= self.tolerance

    def atSetpoint(self):
        return self.at_setpoint()

    def calculate(self, process_variable) -> float:
        current_time = time.time()
        self.current_value = process_variable
        change_in_time = current_time - self.last_time
        self.last_time = current_time
        error = self.setpoint - process_variable
        self.integral += error * change_in_time
        derivative = (error - self.previous_error) / change_in_time
        self.previous_error = error
        output = self.p * error + self.i * self.integral + self.d * derivative
        return output

    def reset(self) -> None:
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()

    def set_setpoint(self, setpoint) -> None:
        self.setpoint = setpoint

    def setSetpoint(self, setpoint) -> None:
        self.set_setpoint(setpoint)

    def set_tolerance(self, tolerance) -> None:
        self.tolerance = tolerance

    def setTolerance(self, tolerance) -> None:
        self.set_tolerance(tolerance)


class SelfTuningPID:
    def __init__(self, p, i, d, setpoint) -> None:
        self.pid = PIDController(p, i, d, setpoint)
        self.setpoint = setpoint

    def tune(self, process_simulator, iterations=100, step=0.1):
        best_performance = float("inf")
        best_params = (self.pid.p, self.pid.i, self.pid.d)

        for _ in range(iterations):
            trial_p = max(0, best_params[0], +(random.random() - 0.5) * step)
            trial_i = max(0, best_params[1], +(random.random() - 0.5) * step)
            trial_d = max(0, best_params[2], +(random.random() - 0.5) * step)

            self.pid.p = trial_p
            self.pid.i = trial_i
            self.pid.d = trial_d
            self.pid.reset()

            trial_performance = self._simulate_performance(process_simulator)

            if trial_performance < best_performance:
                best_performance = trial_performance
                best_params = (trial_p, trial_i, trial_d)

        print(
            f"Tuning complete. Optimal P={best_params[0]}, I={best_params[1]}, D={best_params[2]}"
        )

    def _simulate_performance(self, process_simulator, steps=50):
        total_error_squared = 0
        current_process_variable = 0
        for _ in range(steps):
            output = self.pid.calculate(current_process_variable)
            current_process_variable = process_simulator(
                current_process_variable, output
            )
            error = self.setpoint - current_process_variable
            total_error_squared += error**2
        return total_error_squared
