%gfrompxi
%
%	gfrompxi(pxi) returns g
%	pxi in R^{6}
%

function y=gtopxi(pxi);

p=pxi(1:3);
xi=pxi(4:6);
g=[RfromW(xi) p;0 0 0 1];

y=g;
