clear
close all

%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%   Setting   %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
Simulation_flag = 1;
Analysis_flag = 1;
%%%%%%%%%%%%%%%%%%%%%%%%%

param_EiH_VFC

%===============================%
if(Simulation_flag == 1)
    cd simfile
    sim('EiH_VFC_Renew_R2020a')
    cd ..
    makedata_EiH_VFC
    Output_aoad
    save data/output_data.mat
    %save data/B_thesis_aoad.mat
    %===============================%
    if(Analysis_flag == 1)
        cd plotfig
        % plot_EiH_VFC
        plot_aoad
        plot_3D
        cd ..
    end
    %===============================%
end
%===============================%