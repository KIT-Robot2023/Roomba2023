%vee
%
%   vee(A) A is a Skew Symmetric Matrix (3 x 3)
%
%   veeR
function Y=vee(A)

% ZERO=1e-3; tau‚Å‚Æ‚Ô‚È‚Ç‚¨‚©‚µ‚È‹““®
ZERO=1e-8;

if (A(1,1)>=-ZERO)*(A(1,1)<=ZERO)*(A(2,2)>=-ZERO)*(A(2,2)<=ZERO)*(A(3,3)>=-ZERO)*(A(3,3)<=ZERO)==1

    X=[0 A(1,2) A(1,3);A(2,1) 0 A(2,3);A(3,1) A(3,2) 0];
else
    X=A;
end



if((norm((X+X'))>=-ZERO)*(norm((X+X'))<=ZERO)~=1)

    fprintf('A is not a Skew Symmetric Matrix\n');
    X

elseif(size(A)~=[3 3])

    fprintf('A is not a 3 x 3 Matrix\n');

else

    if  (X(1,2)>=-ZERO)*(X(1,2)<=ZERO)==1
        X(1,2)=0;
    end

    if  (X(1,3)>=-ZERO)*(X(1,3)<=ZERO)==1
        X(1,3)=0;
    end 

    if  (X(2,3)>=-ZERO)*(X(2,3)<=ZERO)==1
        X(2,3)=0;
    end

    Y=[-X(2,3);X(1,3);-X(1,2)];

end
