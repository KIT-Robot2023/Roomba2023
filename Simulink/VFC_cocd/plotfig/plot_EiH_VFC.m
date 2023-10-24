% Plot Version
version = 1; 

% Plot Flag
ea_flag = 1;
eeo_flag = 1;
ad_ao_flag = 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(version==1)
    %======================================================%
        if(ea_flag==1)

        figure(1)
        subplot(3,2,1)
        %hold on
        plot(time,ea1,'b-')
        title('x ea')

        figure(1)
        subplot(3,2,3)
        %hold on
        plot(time,ea2,'b-')
        title('y ea')

        figure(1)
        subplot(3,2,5)
        %hold on
        plot(time,ea3,'b-')
        title('z ea')

        figure(1)
        subplot(3,2,2)
        %hold on
        plot(time,ea4,'b-')
        title('zeta x ea')

        figure(1)
        subplot(3,2,4)
        %hold on
        plot(time,ea5,'b-')
        title('zeta y ea')

        figure(1)
        subplot(3,2,6)
        %hold on
        plot(time,ea6,'b-')
        title('zeta z ea')

    end
    %======================================================%

    %======================================================%
    if(eeo_flag==1)

        figure(2)
        subplot(3,2,1)
        %hold on
        plot(time,eeo1,'r-')
        title('x ee')

        figure(2)
        subplot(3,2,3)
        %hold on
        plot(time,eeo2,'r-')
        title('y ee')

        figure(2)
        subplot(3,2,5)
        %hold on
        plot(time,eeo3,'r-')
        title('z ee')

        figure(2)
        subplot(3,2,2)
        %hold on
        plot(time,eeo4,'r-')
        title('zeta x ee')

        figure(2)
        subplot(3,2,4)
        %hold on
        plot(time,eeo5,'r-')
        title('zeta y ee')

        figure(2)
        subplot(3,2,6)
        %hold on
        plot(time,eeo6,'r-')
        title('zeta z ee')

    end
	%======================================================%
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(version ~= 1)
    %======================================================%
        if(ea_flag==1)

        figure
        %hold on
        plot(time,ea1,'b-')
        title('x ea')

        figure
        %hold on
        plot(time,ea2,'b-')
        title('y ea')

        figure
        %hold on
        plot(time,ea3,'b-')
        title('z ea')

        figure
        %hold on
        plot(time,ea4,'b-')
        title('zeta x ea')

        figure
        %hold on
        plot(time,ea5,'b-')
        title('zeta y ea')

        figure
        %hold on
        plot(time,ea6,'b-')
        title('zeta z ea')

    end
    %======================================================%

    %======================================================%
    if(eeo_flag==1)

        figure
        %hold on
        plot(time,eeo1,'r-')
        title('x ee')

        figure
        %hold on
        plot(time,eeo2,'r-')
        title('y ee')

        figure
        %hold on
        plot(time,eeo3,'r-')
        title('z ee')

        figure
        %hold on
        plot(time,eeo4,'r-')
        title('zeta x ee')

        figure
        %hold on
        plot(time,eeo5,'r-')
        title('zeta y ee')

        figure
        %hold on
        plot(time,eeo6,'r-')
        title('zeta z ee')

    end
    %======================================================%
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if(ad_ao_flag == 1)
    figure(3)
    subplot(3,2,1)
    plot(time,paox,'r')
    hold on
    plot(time,padx,'b')
    title('ad ao x')

    figure(3)
    subplot(3,2,3)
    plot(time,paoy,'r')
    hold on
    plot(time,pady,'b')
    title('ad ao y')

    figure(3)
    subplot(3,2,5)
    plot(time,paoz,'r')
    hold on
    plot(time,padz,'b')
    title('ad ao z')

    figure(3)
    subplot(3,2,2)
    plot(time,zetaaox,'r')
    hold on
    plot(time,zetaadx,'b')
    title('ad ao zeta_x')

    figure(3)
    subplot(3,2,4)
    plot(time,zetaaoy,'r')
    hold on
    plot(time,zetaady,'b')
    title('ad ao zeta_y')

    figure(3)
    subplot(3,2,6)
    plot(time,zetaaoz,'r')
    hold on
    plot(time,zetaadz,'b')
    title('ad ao zeta_z')
end