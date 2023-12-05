function Y=highspeedmaketarget(t)

l1=0.2;
l2=0.3;

ox=0.04*cos(12/2.8*t)+0.2*cos(pi/6)+0.26;
oy=-(0.1*sin(24/2.8*t-pi/6)-0.05);

rx=ox;
ry=oy;

k=sqrt((rx^2+ry^2+l1^2+l2^2)^2-2*((rx^2+ry^2)^2+l1^4+l2^4));
q1=atan2(ry,rx)+atan2(k,rx^2+ry^2+l1^2-l2^2);
q2=-atan2(k,rx^2+ry^2-l1^2-l2^2);
theta=q1+q2;

Y=[ox;oy;-1;0;0;theta];
%Y=[ox;oy;-0.22;0;0;theta];
