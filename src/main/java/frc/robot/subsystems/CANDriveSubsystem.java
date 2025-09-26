// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package frc.robot.subsystems;

import org.fairportrobotics.frc.posty.TestableSubsystem;
import org.fairportrobotics.frc.posty.test.PostTest;
import static org.fairportrobotics.frc.posty.assertions.Assertions.*;

import com.ctre.phoenix.motorcontrol.can.WPI_VictorSPX;
import com.ctre.phoenix.WPI_CallbackHelper;

import com.revrobotics.spark.SparkBase.PersistMode;
import com.revrobotics.spark.SparkBase.ResetMode;
import com.revrobotics.spark.SparkLowLevel.MotorType;
import com.revrobotics.spark.SparkMax;
import com.revrobotics.spark.config.SparkMaxConfig;

import edu.wpi.first.wpilibj.drive.DifferentialDrive;
import edu.wpi.first.wpilibj.motorcontrol.Victor;
import frc.robot.Constants.DriveConstants;

// Class to drive the robot over CAN
public class CANDriveSubsystem extends TestableSubsystem {
  private final WPI_VictorSPX leftLeader;
  private final WPI_VictorSPX leftFollower;
  private final WPI_VictorSPX rightLeader;
  private final WPI_VictorSPX rightFollower;

  private final DifferentialDrive drive;

  public CANDriveSubsystem() {
    super();
    // create brushed motors for drive
    leftLeader = new WPI_VictorSPX(DriveConstants.LEFT_LEADER_ID);
    leftFollower = new WPI_VictorSPX(DriveConstants.LEFT_FOLLOWER_ID);
    rightLeader = new WPI_VictorSPX(DriveConstants.RIGHT_LEADER_ID);
    rightFollower = new WPI_VictorSPX(DriveConstants.RIGHT_FOLLOWER_ID);
    leftLeader.setInverted(true);
    leftFollower.setInverted(true);

    // set up differential drive class
    drive = new DifferentialDrive(leftLeader, rightLeader);

    // Set can timeout. Because this project only sets parameters once on
    // construction, the timeout can be long without blocking robot operation. Code
    // which sets or gets parameters during operation may need a shorter timeout.
    //leftLeader.setCANTimeout(250);
    //rightLeader.setCANTimeout(250);
    //leftFollower.setCANTimeout(250);
    //rightFollower.setCANTimeout(250);

    // Create the configuration to apply to motors. Voltage compensation
    // helps the robot perform more similarly on different
    // battery voltages (at the cost of a little bit of top speed on a fully charged
    // battery). The current limit helps prevent tripping
    // breakers.
    SparkMaxConfig config = new SparkMaxConfig();
    config.voltageCompensation(12);
    config.smartCurrentLimit(DriveConstants.DRIVE_MOTOR_CURRENT_LIMIT);

    leftFollower.follow(this.leftLeader);
    rightFollower.follow(this.rightLeader);
  }

  @Override
  public void periodic() {
  }

  // sets the speed of the drive motors
  public void driveArcade(double xSpeed, double zRotation) {
    drive.arcadeDrive(xSpeed, zRotation);
  }

  @PostTest
  public void canDevicesConnected(){
    assertThat(rightLeader.getFirmwareVersion()).isGreaterThan(5);
    assertThat(rightFollower.getFirmwareVersion()).isGreaterThan(5);
    assertThat(leftLeader.getFirmwareVersion()).isGreaterThan(5);
    assertThat(leftFollower.getFirmwareVersion()).isGreaterThan(5);
  }

}
