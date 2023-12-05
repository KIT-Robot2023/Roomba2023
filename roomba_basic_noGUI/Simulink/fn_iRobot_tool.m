function [EncL, EncR] = get_encoder_count(mode, clock)
    Ctrl_Mode = mode;

    if clock == 0
        Port = setup;
    end

    if (Ctrl_Mode == 2)
        move;

    elseif(Ctrl_Mode == 0)
        stop;
    end
    
    if Port == None
        passthrough
    else
        [EncL, EncR] = EncoderSensorsRoomba(Port)
    end

end

function serPort = setup
    COM = 5
    mode = 'full'
    [serPort] = RoombaInit(COM, mode)
end

function move
    SetFwdVelRadiusRoomba(serPort, 0.1, 0)
end

function stop
    SetFwdVelRadiusRoomba(serPort, 0, 0)
end