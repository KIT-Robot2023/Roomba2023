% PDRDMATRIX 
%   
%    ����  PDRDMATRIX(pd,xi_d,Wcec)
%    ����  u=[pd; xi_d; Wcec]
%          pd     (3,n)   : �ڕW�ʒu
%      �@�@xi_d   (3,n) : �ڕW�p��
% �@�@     Vd     (6,1)   : �ڕW�ʒu�p�����x
%
%   �Q�l  


function y=invAd(u)
    p=u(1:3,1);
    xi=u(4:6,1);
    R=expm(wedge(xi));
    phat=wedge(p);
    invAd=[R' -R'*phat;zeros(3,3) R'];
    y=invAd;
