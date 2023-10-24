%gtopxi
%
%	gtopxi(g) returns p and xi
%	g in R^{4 x 4}
%

function y=gtopxi(g);

p=g(1:3,4);
xi=Rtoxi(g(1:3,1:3));

y=[p;xi];
