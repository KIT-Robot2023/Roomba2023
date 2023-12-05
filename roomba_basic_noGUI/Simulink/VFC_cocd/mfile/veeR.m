%vee
%
%   veeR(R) R : Rotation Matrix (3 x 3)
%
%    || size(R)!=[3 3])
function Y=veeR(R)

ZERO=1e-8;

LogR=logm(R);

if (LogR(1,1)>=-ZERO)*(LogR(1,1)<=ZERO)*(LogR(2,2)>=-ZERO)*(LogR(2,2)<=ZERO)*(LogR(3,3)>=-ZERO)*(LogR(3,3)<=ZERO)==1

    X=[0 LogR(1,2) LogR(1,3);LogR(2,1) 0 LogR(2,3);LogR(3,1) LogR(3,2) 0];
else
    X=LogR
end

if X~=-X'

    fprintf('logm(R) is not a Rotation Matrix');

elseif size(R)~=[3 3]

    fprintf('R is not a 3 x 3 Rotation Matrix');
else

    if  (X(1,2)>=-ZERO)*(X(1,2)<=ZERO)==1
        X(1,2)=0;
    end

    if  (X(1,3)>=-ZERO)*(X(1,3)<=ZERO)==1
        X(1,3)=0;
    end 

    if  (X(2,3)>=-ZERO)*(X(2,3)<=ZERO)==1
        X(2,3)=0;
    end

    Y=[-X(2,3);X(1,3);-X(1,2)];

end
