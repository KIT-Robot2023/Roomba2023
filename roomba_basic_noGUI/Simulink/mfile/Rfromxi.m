%Rfromxi   
%
%	Rfromx(xi) returns a rotatoin matrix
%


function y=Rfromxi(xi);


y=expm(wedge(xi));

