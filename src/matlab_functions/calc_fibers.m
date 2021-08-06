
% NODES_FILE = "C:\Users\IgorNobrega\University of South Florida\Mao, Wenbin - Myocardium (organized)\Active\Hex_mesh_study\geometry_data\myo_tet_4_study_1_nodes.csv"
% ELEMENTS_FILE = "C:\Users\IgorNobrega\University of South Florida\Mao, Wenbin - Myocardium (organized)\Active\Hex_mesh_study\geometry_data\myo_tet_4_study_1_elems.csv"
% NODES_FILE_HEX = "C:\Users\IgorNobrega\University of South Florida\Mao, Wenbin - Myocardium (organized)\Active\Hex_mesh_study\geometry_data\myo_hex_1_study_1_nodes.csv"
% ELEMENTS_FILE_HEX = "C:\Users\IgorNobrega\University of South Florida\Mao, Wenbin - Myocardium (organized)\Active\Hex_mesh_study\geometry_data\myo_hex_1_study_1_elems.csv"
% THETA_ENDO = -60
% THETA_EPI = 60
% OUTPUT_FOLDER_FILENAME = "C:\Users\IgorNobrega\University of South Florida\Mao, Wenbin - Myocardium (organized)\Active\Hex_mesh_study\fibers_data"

% calculate_fibers_orientation(NODES_FILE, ELEMENTS_FILE, NODES_FILE_HEX, ELEMENTS_FILE_HEX, THETA_ENDO, THETA_EPI, OUTPUT_FOLDER_FILENAME)

function calculate_fibers_orientation(NODES_FILE, ELEMENTS_FILE, NODES_FILE_HEX, ELEMENTS_FILE_HEX, THETA_ENDO, THETA_EPI, OUTPUT_FOLDER_FILENAME)
%% Define Macros

apex = [-0.367668, -0.551779, 0.0815987];
base = [0, 0 , 83.5];
k = base - apex;

%THETA_ENDO = 75;
%THETA_EPI = -45;


%% Load Model

%load nodes and elements info, must be tetrahedral elements
[nodes, elements] = load_data(NODES_FILE,ELEMENTS_FILE);

% create mesh, meshes must be triangular and tetrahedral elements
[model, mesh] = create_model(nodes,elements,false);

%% Apply boundary conditions

% Get faces Ids (MATLAB creates IDs for each face. It does not depend on
% input values and the order they are assigned can be random. Therefore, we
% must find what faces corresponds to the 'Base', 'endocardio' and
% epicardio') 
% ***** 
% NOTE: the current implementation only works for ideal cases,
% if we want to explore non-ideal cases, we must come up with a better
% logic...
% *****
[baseFace, endoFace, epicFace] = getFacesIds(model,mesh,apex,base);

baseFace = 3
endoFace = 1
epicFace = 2

apply_bcs(model,baseFace,endoFace,epicFace); %base, endocardio, epicardio
% apply_bcs(model,2,4,3) %base, endocardio, epicardio <-- work for
% quarter models

% Create the mesh with target maximum element size 5: 'Hmax',5
generateMesh(model);

% % Plot mesh
% plot_mesh(model);

% Call the appropriate solver
result = solve_model(model,false);

%% Plot the Solution as Contour Slices

plot_contour(result,-35:35,-75:0,-35:35,'y',-55:10:0, OUTPUT_FOLDER_FILENAME, THETA_EPI,THETA_ENDO)


%% interpolate back to the original meshes and nodes

[nodes_hex, elements_hex] = load_data(NODES_FILE_HEX,ELEMENTS_FILE_HEX);

elem_c = calculate_centers(nodes_hex, elements_hex);

[u_interp, u_gradient] = interp_data(elem_c, result);

%% Sheet field direction

% Normal direction of the sheet based on interpolated gradient
s0 = sheet_normal_direction(u_gradient); 

% Fiber angles at the endocardium and epicardium
f0 = fiber_direction(s0,k,u_interp,THETA_ENDO,THETA_EPI);

%% Plot fiber orientation on a coarse mes
% 
figure
pdegplot(model,'FaceLabels','on','FaceAlpha',0.2)
hold on
%plot fiber direction close to the epicardium
index = find(u_interp > 0.8);
quiver3(elem_c(index,1),elem_c(index,2),elem_c(index,3),f0(index,1),f0(index,2),f0(index,3),'color','b')
ax = gca;
ax.Clipping = 'off';  %do not clip when zoom in
title('fiber directions on the epicardium')
savefig(OUTPUT_FOLDER_FILENAME+"_o_"+THETA_EPI+"_endo-"+THETA_ENDO+"_MATLABFIG-FIBERS-EPICARDIO.fig")
close

%% Plot fiber direction close to the endocardium

figure
pdegplot(model,'FaceLabels','on','FaceAlpha',0.2)
hold on
index = find(u_interp < 0.2);
quiver3(elem_c(index,1),elem_c(index,2),elem_c(index,3),f0(index,1),f0(index,2),f0(index,3),'color','b')
ax = gca;
ax.Clipping = 'off';  %do not clip when zoom in
axis equal
title('fiber directions on the endocardium')
savefig(OUTPUT_FOLDER_FILENAME+"_o_"+THETA_EPI+"_endo-"+THETA_ENDO+"_MATLABFIG-FIBERS-ENDOCARDIO.fig")
close

%% Save orientation table to csv

filename = OUTPUT_FOLDER_FILENAME+"_o_epi_"+THETA_EPI+"_endo_"+THETA_ENDO+".csv";
write_fiber_orientations_table(s0,f0,elements_hex,filename);



%% Functions

function [nodes, elements] = load_data(nodes_file, elem_file)
	fprintf('Loading Data...\n')
    nodes = csvread(nodes_file,0,1)';
    elements = csvread(elem_file,0,1)';
    fprintf('Data loaded.\n\n')
end

function [model, mesh] = create_model(nodes,elements,view_geometry)
    fprintf('Creating Model...\n')
    model = createpde();
    [G, mesh] = geometryFromMesh(model,nodes,elements);
    if view_geometry
        %View the geometry and face numbers.
        pdegplot(model,'FaceLabels','on','FaceAlpha',0.5)
    end  
    fprintf('Model created.\n\n')
end

function apply_bcs(model,base,f1,f2)
    fprintf('Applying BCs...\n')
    %Neumann bc on the base
    applyBoundaryCondition(model,'neumann','Face',base,'q',0,'g',0);
    %Create the boundary conditions
    applyBoundaryCondition(model,'dirichlet','Face',f1,'u',0); %endocardium, f1
    applyBoundaryCondition(model,'dirichlet','Face',f2,'u',1); %epicardium, f2
    %Create the PDE coefficients.
    specifyCoefficients(model,'m',0,'d',0,'c',1,'a',0,'f',0);
    
    fprintf('BCs applied\n\n')
end

function plot_mesh(model)
    figure
    pdeplot3D(model)
end

function [result] = solve_model(model,plotSol)
    fprintf('Solving model...\n')
    result = solvepde(model);
    
    %plot the solution
    if plotSol
        u = result.NodalSolution;
        figure
        pdeplot3D(model,'ColorMapData',u)
    end
    fprintf('Model solved\n\n')
end

function plot_contour(model,x,y,z,loc,slices, OUTPUT_FOLDER_FILENAME, THETA_EPI,THETA_ENDO)
    %Plot the Solution as Contour Slices
    fprintf('Creating countours...\n')
    [X,Y,Z] = meshgrid(x,y,z);
    V = interpolateSolution(model,X,Y,Z);
    V = reshape(V,size(X));
    %Plot contour slices for various values of Z.
    figure
    colormap jet
    if loc == 'x'
        contourslice(X,Y,Z,V,slices,[],[])
    elseif loc == 'y'
        contourslice(X,Y,Z,V,[],slices,[])
    else
        contourslice(X,Y,Z,V,[],[],slices)
    end
    xlabel('x')
    ylabel('y')
    zlabel('z')
    colorbar
    view(-62,34)
    axis equal
    fprintf('Countours created.\n\n')
    savefig(OUTPUT_FOLDER_FILENAME+"_o_"+THETA_EPI+"_endo-"+THETA_ENDO+"_MATLABFIG-COUNTOURS.fig")
    close
end

function [elem_c] = calculate_centers(nodes_hex,elems_hex)
    fprintf('Calculating centers...\n')
    nodes_hex = nodes_hex';
    elems_hex = elems_hex';
    
    L = length(elems_hex);
    elem_c=zeros(L,3);
    for i=1:L
        non_zero_elems = [];
        elems_line =(elems_hex(i,:));
        for j=1:length(elems_line), if elems_line(j) > 0, non_zero_elems(j) = elems_line(j); end; end        
        elem_c(i,:) = mean(nodes_hex(non_zero_elems,:),1);
    end
    
    fprintf('Centers calculated.\n\n')
end

function [u_interp, u_gradient] = interp_data(elem_c, model)
    fprintf('Interpolating data...\n')
    u_interp = interpolateSolution(model, elem_c(:,1),elem_c(:,2),elem_c(:,3));
    [gradx,grady,gradz] = evaluateGradient(model, elem_c(:,1),elem_c(:,2),elem_c(:,3));
    u_gradient = [gradx,grady,gradz];
    fprintf('Data interpolated.\n\n')
end

function [s0] = sheet_normal_direction(u_gradient)
    fprintf('Calculating s0...\n')
    s0 = u_gradient./sqrt(u_gradient(:,1).^2 +u_gradient(:,2).^2+u_gradient(:,3).^2); 
    fprintf('s0 calculated.\n\n')
end

function [f0] = fiber_direction(s0,k,u_interp,theta_endo,theta_epi)
    fprintf('Calculating fibers directions...\n')
    L = length(s0);
    kp=zeros(L,3);
    for i=1:length(s0)
        kp(i,:) = k - dot(k,s0(i,:))*s0(i,:);
    end

    kp = kp./sqrt(kp(:,1).^2 + kp(:,2).^2+kp(:,3).^2);

    f0_t = cross(s0,kp,2);
    theta = (theta_epi - theta_endo)*u_interp + theta_endo; 
    f0=[];
    for i=1:length(s0)
        s0_cross = [0,-s0(i,3),s0(i,2); s0(i,3),0,-s0(i,1); -s0(i,2),s0(i,1),0];
        rot = eye(3) + sin(theta(i)*pi/180)*s0_cross + 2*sin(theta(i)*pi/180/2)^2*(s0(i,:)'*s0(i,:)-eye(3));
        f0(i,:) = rot*f0_t(i,:)';
    end
    fprintf('Fibers directions calculated.\n\n')
end

function write_fiber_orientations_table(s0,f0,elements_hex,filename)
    fprintf("Writing fiber orientation table to file: '"+filename+"'...\n");
    %sheet direction/cross-fiber direction
    ss0 = cross(s0, f0, 2); 
    % transpose of elements hex
    elements_hex_t = elements_hex';
    % create indexes
    idxs = 1:1:length(elements_hex_t);
    % temporary array
    temp = [idxs',elements_hex_t(:,1), f0, ss0];

    dlmwrite(filename,temp, 'delimiter', ',', 'precision', 9);
    fprintf('File written.\n\n')
end

function [baseFace, endoFace, epicFace] = getFacesIds(model,mesh,apex,base)
    n_faces = model.Geometry.NumFaces;
    baseFace = -1;
    endoFace = -1;
    epicFace = -1;
    face_options = [1,2,3];
    chan_len = 0;
    for i=1:1:n_faces
    %     disp(i)
       node_numbers = findNodes(mesh,'region','Face',i);

       if baseFace == -1
           bazeZ = base(1,3);
           total = sum(mesh.Nodes(3,node_numbers) >= bazeZ*0.95);
           if total > 0.95*length(node_numbers)
              baseFace = i;
              face_options(i - chan_len) = [];
              chan_len = chan_len + 1;
           end
       end

       if epicFace == -1
          apexZ = apex(1,3)
          total = sum(mesh.Nodes(3,node_numbers) <= apexZ*0.90)
          if total > 0 && total <= 0.1*length(node_numbers)
             epicFace = i;
             face_options(i - chan_len) = [];
             chan_len = chan_len + 1;
          end
       end   
    end

    endoFace = face_options(1);
end

end