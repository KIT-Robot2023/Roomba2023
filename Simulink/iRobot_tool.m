COM = 5
mode = 'full'
[serPort] = RoombaInit(COM, mode)
tic

while(true)
    if toc > 10
        break
    end
    [Left, Right] = EncoderSensorsRoomba(serPort)
    SetFwdVelRadiusRoomba(serPort, 0.1, 0)
end

SetFwdVelRadiusRoomba(serPort, 0, 0)
PowerOffRoomba(serPort)