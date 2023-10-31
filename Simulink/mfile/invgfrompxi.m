%invgfrompxi
%
%	invgfrompxi(pxi) returns inverse g
%	pxi in R^{6}
%

function y=invgtopxi(pxi);

p=pxi(1:3);
xi=pxi(4:6);
invg=[(RfromW(xi))' -(RfromW(xi))'*p;0 0 0 1];

y=invg;
