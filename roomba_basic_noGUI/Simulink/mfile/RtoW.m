%RtoW   
%
%	RtoW(R) returns an axis of rotatoin and a rotation angle
%


function y=RtoW(R);

%ZERO=1e-6;
ZERO=1e-8;

v=vee(logm(R));

if(sqrt(v(1)^2+v(2)^2+v(3)^2)<=0.000001)
 omega=[0;0;0];
 theta=0;
else
 omega=v/sqrt(v(1)^2+v(2)^2+v(3)^2);
 theta=sqrt(v(1)^2+v(2)^2+v(3)^2);
end


y=[omega;theta];

