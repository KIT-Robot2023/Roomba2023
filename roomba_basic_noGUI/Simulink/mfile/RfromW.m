%RfromW   
%
%	RfromW(R) returns an axis of rotatoin and a rotation angle
%
%

function y=RfromW(x);

%ZERO=1e-5;
ZERO=1e-8;

if (max(abs(x))<=ZERO)
  y=eye(3);
else

if max(size(x))==3
        w=x/norm(x);
        v=norm(x);
        y=expm(v*wedge(w));
elseif max(size(x))==4
    w=[x(1);x(2);x(3)];
    w=w/norm(w);
    v=x(4);
    y=expm(v*wedge(w));
elseif max(size(x))==5
    w=[x(1);x(2);x(3)];
    w=w/norm(w);
    v=x(4);
    sptime=x(5);
    y=expm(v*wedge(w)*sptime);
else
    fprintf('size error')
    y=eye(3);
end

end

