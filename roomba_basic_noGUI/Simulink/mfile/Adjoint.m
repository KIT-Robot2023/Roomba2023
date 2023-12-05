% PDRDMATRIX 
%   
%    書式  PDRDMATRIX(pd,xi_d,Wcec)
%    入力  u=[pd; xi_d; Wcec]
%          pd     (3,n)   : 目標位置
%      　　xi_d   (3,n) : 目標姿勢
% 　　     Vd     (6,1)   : 目標位置姿勢速度
%
%   参考  


function y=Adjoint(u)
    p=u(1:3,1);
    xi=u(4:6,1);
    R=expm(wedge(xi));
    phat=wedge(p);
    Adjoint=[R phat*R;zeros(3,3) R];
    y=Adjoint;
