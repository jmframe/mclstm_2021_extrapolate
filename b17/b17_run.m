% Specify the folder where the files live.
myFolderIn = '/Users/jf/Box Sync/r/frequency-analysis/usgs-peak/';
myFolderOut = '/Users/jf/Box Sync/r/frequency-analysis/usgs-peak-fq/';

% Check to make sure that folder actually exists.  Warn user if it doesn't.
if ~isfolder(myFolderIn)
    errorMessage = sprintf('Error: The following folder does not exist:\n%s\nPlease specify a new folder.', myFolder);
    uiwait(warndlg(errorMessage));
    myFolderIn = uigetdir(); % Ask for a new one.
    if myFolderIn == 0
         % User clicked Cancel
         return;
    end
end

% Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(myFolderIn, '*.csv'); % Change to whatever pattern you need.
theFiles = dir(filePattern);
for k = 1 : length(theFiles)
    gaugeName = theFiles(k).name(1:8);
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);
    fprintf(1, 'Now reading %s\n', fullFileName);
    
    filename = strcat(myFolderOut,'out/',gaugeName,'.txt');
    if isfile(filename)
         continue
    end

    pf = load(fullFileName);
    pf(any(isnan(pf),2),:) = [];
    for d = 1:size(pf)[1]
        if pf(d,2) == 0
            pf(d,2) = 1;
        end
    end
    datain = pf;
    gg = 0;
    imgfile = strcat(myFolderOut,'out/',gaugeName,'.png');
    plotref = 1;
    plottype = 1;
    [dataout, skews, pp, XS, SS, hp] = b17(datain, 0, imgfile, gaugeName, plotref, plottype);
    
    fid = fopen(filename,'wt');
    for ii = 1:size(dataout,1)
        fprintf(fid,'%g\t',dataout(ii,:));
        fprintf(fid,'\n');
    end
    fclose(fid);
       
%    break
end