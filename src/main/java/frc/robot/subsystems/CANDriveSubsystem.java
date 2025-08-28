// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import org.fairportrobotics.frc.posty.TestableSubsystem;
import org.fairportrobotics.frc.posty.test.BitTest;
import org.fairportrobotics.frc.posty.test.PostTest;
import org.fairportrobotics.frc.posty.util.Utilities;
import static org.fairportrobotics.frc.posty.assertions.Assertions.*;

import com.revrobotics.spark.SparkBase.PersistMode;
import com.revrobotics.spark.SparkBase.ResetMode;
import com.revrobotics.spark.SparkLowLevel.MotorType;
import com.revrobotics.spark.SparkMax;
import com.revrobotics.spark.config.SparkMaxConfig;

import edu.wpi.first.wpilibj.drive.DifferentialDrive;
import frc.robot.Constants.DriveConstants;

// Class to drive the robot over CAN
public class CANDriveSubsystem extends TestableSubsystem {
  private final SparkMax leftLeader;
  private final SparkMax leftFollower;
  private final SparkMax rightLeader;
  private final SparkMax rightFollower;

  private final DifferentialDrive drive;

  public CANDriveSubsystem() {
    super();
    // create brushed motors for drive
    leftLeader = new SparkMax(DriveConstants.LEFT_LEADER_ID, MotorType.kBrushed);
    leftFollower = new SparkMax(DriveConstants.LEFT_FOLLOWER_ID, MotorType.kBrushed);
    rightLeader = new SparkMax(DriveConstants.RIGHT_LEADER_ID, MotorType.kBrushed);
    rightFollower = new SparkMax(DriveConstants.RIGHT_FOLLOWER_ID, MotorType.kBrushed);

    // set up differential drive class
    drive = new DifferentialDrive(leftLeader, rightLeader);

    // Set can timeout. Because this project only sets parameters once on
    // construction, the timeout can be long without blocking robot operation. Code
    // which sets or gets parameters during operation may need a shorter timeout.
    leftLeader.setCANTimeout(250);
    rightLeader.setCANTimeout(250);
    leftFollower.setCANTimeout(250);
    rightFollower.setCANTimeout(250);

    // Create the configuration to apply to motors. Voltage compensation
    // helps the robot perform more similarly on different
    // battery voltages (at the cost of a little bit of top speed on a fully charged
    // battery). The current limit helps prevent tripping
    // breakers.
    SparkMaxConfig config = new SparkMaxConfig();
    config.voltageCompensation(12);
    config.smartCurrentLimit(DriveConstants.DRIVE_MOTOR_CURRENT_LIMIT);

    // Set configuration to follow leader and then apply it to corresponding
    // follower. Resetting in case a new controller is swapped
    // in and persisting in case of a controller reset due to breaker trip
    config.follow(leftLeader);
    leftFollower.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
    config.follow(rightLeader);
    rightFollower.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);

    // Remove following, then apply config to right leader
    config.disableFollowerMode();
    rightLeader.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
    // Set conifg to inverted and then apply to left leader. Set Left side inverted
    // so that postive values drive both sides forward
    config.inverted(true);
    leftLeader.configure(config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters);
  }

  @Override
  public void periodic() {
  }

  // sets the speed of the drive motors
  public void driveArcade(double xSpeed, double zRotation) {
    drive.arcadeDrive(xSpeed, zRotation);
  }

  //
  //  Test functions
  //

  private void motor_current_print(String header, double[] data) {
    System.out.println(String.format("%s:", header));
    System.out.println(String.format("\t%-20s: %lf", "left leader",     data[0]));
    System.out.println(String.format("\t%-20s: %lf", "left follower",   data[1]));
    System.out.println(String.format("\t%-20s: %lf", "ritht leader",    data[2]));
    System.out.println(String.format("\t%-20s: %lf", "right follower",  data[3]));
    System.err.println("");
  }

  private double[] get_motor_currents() {
    // Get the currents
    double[] to_ret = {
      this.leftLeader.getOutputCurrent(),
      this.leftFollower.getOutputCurrent(),
      this.rightLeader.getOutputCurrent(),
      this.rightFollower.getOutputCurrent()
    };

    // Return the data
    return to_ret;
  }

  @PostTest
  public void canDevicesConnected(){
    assertThat(rightLeader.getFirmwareVersion()).isGreaterThan(5);
    assertThat(rightFollower.getFirmwareVersion()).isGreaterThan(5);
    assertThat(leftLeader.getFirmwareVersion()).isGreaterThan(5);
    assertThat(leftFollower.getFirmwareVersion()).isGreaterThan(5);
  }

  @BitTest
  public void canDevicesRun() {
    // Stop the motors
    System.out.println("Stopping the motors for one second");
    this.drive.stopMotor();
    Utilities.waitForCondition(() -> false, (float)1);

    double stopped_current[] = this.get_motor_currents();
    this.motor_current_print("Stopped Current", stopped_current);

    // Do CCW Rotation
    System.out.println("Driving counterclockwise for 1 second");
    this.drive.tankDrive(-.5, .5);
    Utilities.waitForCondition(() -> false, (float)1);

    double[] ccw_current = this.get_motor_currents();
    this.motor_current_print("Counter Clockwise Current (abs)", ccw_current);

    double[] ccw_diff = new double[4];
    for(int i = 0; i < 4; ++i){ccw_diff[i] = ccw_current[i] - stopped_current[i];}
    this.motor_current_print("Counter Clockwise Current (diff)", ccw_diff);

    // Stop
    System.out.println("Stopping the motors for one second");
    this.drive.stopMotor();
    Utilities.waitForCondition(() -> false, (float)1);

    // Do CW Rotation
    System.out.println("Driving clockwise for 1 second");
    this.drive.tankDrive(-.5, .5);
    Utilities.waitForCondition(() -> false, (float)1);

    double[] cw_current = this.get_motor_currents();
    this.motor_current_print("Clockwise Current (abs)", cw_current);

    double[] cw_diff = new double[4];
    for(int i = 0; i < 4; ++i){cw_diff[i] = cw_current[i] - stopped_current[i];}
    this.motor_current_print("Clockwise Current (diff)", cw_diff);

    // Stop
    System.out.println("Stopping the motors");
    this.drive.stopMotor();

    // Ensure that current signs on all 4 motors are different between rotation directions
    for (int i = 0; i < 4; ++i) {
      assertThat((ccw_diff[i] < 0) != (cw_diff[i] < 0)).isTrue();
    }

  }

}
