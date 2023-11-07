function getRigidBody(RigidBodyBlock)
  % getting position and attitude from Motion Capture(motive)
  % necessary : Natnet SDK
  setup(RigidBodyBlock);
end

function setup(RigidBodyBlock)
  RigidBodyBlock.NumInputPorts = 0;
  RigidBodyBlock.NumOutputPorts = 1;
  RigidBodyBlock.NumDialogPrms  = 1;
  
  RigidBodyBlock.OutputPort(1).Dimensions = [7]
  RigidBodyBlock.OutputPort(1).SamplingMode = 'Sample';
  RigidBodyBlock.OutputPort(1).DatatypeID  = 0;
  %RigidBodyBlock.SetPreCompInpPortInfoToDynamic;
  
  SampleTime = -1;
  RigidBodyBlock.SampleTimes = [SampleTime, 0];
  
  RigidBodyBlock.RegBlockMethod('InitializeConditions',    @InitConditions);  
  RigidBodyBlock.RegBlockMethod('Update',                  @Update);  
  
end


function InitConditions(RigidBodyBlock)
  %% Initialize Dwork
  global natnetclient;
  global data;
  global start_time;

  data = natnetclient.getFrame;
  start_time = data.Timestamp;
  
end

function Update(RigidBodyBlock)
  global natnetclient;
  global data;
  global start_time;
  
  data = natnetclient.getFrame;
  if (data.Timestamp ~= start_time) 
  % Position (right-handed system)
    RigidBodyBlock.OutputPort(1).Data(1) = double(data.RigidBody( RigidBodyBlock.DialogPrm(1).Data ).x); % x axis : width
    RigidBodyBlock.OutputPort(1).Data(2) = double(data.RigidBody( RigidBodyBlock.DialogPrm(1).Data ).y); % z axis : length
    RigidBodyBlock.OutputPort(1).Data(3) = double(data.RigidBody( RigidBodyBlock.DialogPrm(1).Data ).z); % y axis : height
    
  % Attitude(Quatanion)
    RigidBodyBlock.OutputPort(1).Data(4) = double(data.RigidBody( RigidBodyBlock.DialogPrm(1).Data ).qw);
    RigidBodyBlock.OutputPort(1).Data(5) = double(data.RigidBody( RigidBodyBlock.DialogPrm(1).Data ).qx);
    RigidBodyBlock.OutputPort(1).Data(6) = double(data.RigidBody( RigidBodyBlock.DialogPrm(1).Data ).qy);
    RigidBodyBlock.OutputPort(1).Data(7) = double(data.RigidBody( RigidBodyBlock.DialogPrm(1).Data ).qz);     
%     fprintf( 'Frame:%6d  ' , data.Frame );
%     fprintf( 'Time:%0.2f\n' , data.Timestamp );
  end
  
end