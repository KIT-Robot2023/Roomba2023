function Y=highspeedmakestraight(t)

l1=0.2;
l2=0.3;

Amp=-20*pi/180;

%%% x は固定 %%%
x=l1*cos(pi/6)+l2*cos(pi/6-pi/6);

theta=Amp*sin(pi*t);

q1=acos((x-l2*cos(theta))/l1);
y=l1*sin(q1)+l2*sin(theta);

Y=[x;y;-1;0;0;theta];
%Y=[x;y;-0.22;0;0;theta];
