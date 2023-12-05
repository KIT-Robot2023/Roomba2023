%RtoW   
%
%	RtoW(R) returns an axis of rotatoin and a rotation angle
%


function y=Rtoxi(R);

v=vee(logm(R));

%omega=v/sqrt(v(1)^2+v(2)^2+v(3)^2);
%theta=sqrt(v(1)^2+v(2)^2+v(3)^2);

y=[v];

