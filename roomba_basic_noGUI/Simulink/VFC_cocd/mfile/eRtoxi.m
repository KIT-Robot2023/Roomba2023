% ReoTmatrix
%
%
%    書式  eRtozeta(u)
%    入力  u=[eR]
%          eR        (3,1) : 
%
%   参考  


function Y=eRtoxi(u)

ZERO=1e-8;

eR=u(1:3,1);

if norm(eR)<=ZERO
     Y=[0; 0; 0];

else 
     neR=norm(eR); 
     Y=asin(neR)/neR*eR;
end
