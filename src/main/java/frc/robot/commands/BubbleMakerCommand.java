package frc.robot.commands;

import edu.wpi.first.wpilibj2.command.Command;
import frc.robot.subsystems.CANRollerSubsystem;

public class BubbleMakerCommand extends Command {
    private CANRollerSubsystem rollersubsystem;
    public BubbleMakerCommand(CANRollerSubsystem rollersubsystem){
        this.rollersubsystem = rollersubsystem;
    }
    
    public void initialize(){
        rollersubsystem.runRoller(1, 0);
    }

    public void end(boolean interrupt){
        rollersubsystem.runRoller(0, 0);
    }
}
