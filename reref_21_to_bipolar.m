% Prepared by neuronauts group.
% This code converts your selected mono or avg. referencing '.edf' file to bipolar referencing.
% Input monopolar 'dataname.edf' file -> Output bipolar 'dataname_bipolar.edf' file at same location
% Require the eeglab, biosig
% Events and annotations are not imported!

clear all

[file, path] = uigetfile('*.edf', 'Select an EDF file');
if isequal(file, 0)
    disp('There is no selected file!');
    return;
else
    source_path = fullfile(path, file);
    disp(['Selected file: ', source_path]);
end

EEG = pop_biosig(source_path, 'importevent', 'off', 'importannot', 'off'); %Some new version of the .edf files give the error when importing the events and annotations.

newEEG = EEG;

chl = {EEG.chanlocs.labels}; %channel labels for index
%bipolar correspondings of electrode for indexing
%Channel naming may vary, so before running the code, set the names of the 
%channel pairs to the names in your .edf file. The standard 10-20 channel 
%names are given below.
bc = {'Fp1', 'F3'; 'F3', 'C3'; 'C3', 'P3'; 'P3', 'O1'; 
      'Fp2', 'F4'; 'F4', 'C4'; 'C4', 'P4'; 'P4', 'O2'; 
      'Fp1', 'F7'; 'F7', 'T7'; 'T7', 'P7'; 'P7', 'O1'; 
      'Fp2', 'F8'; 'F8', 'T8'; 'T8', 'P8'; 'P8', 'O2'; 
      'Fz', 'Cz'; 'Cz', 'Pz'};
  
bc2 = {'Fp1', 'F3'; 'F3', 'C3'; 'C3', 'P3'; 'P3', 'O1'; 
      'Fp2', 'F4'; 'F4', 'C4'; 'C4', 'P4'; 'P4', 'O2'; 
      'Fp1', 'F7'; 'F7', 'T3'; 'T3', 'T5'; 'T5', 'O1'; 
      'Fp2', 'F8'; 'F8', 'T4'; 'T4', 'T6'; 'T6', 'O2'; 
      'Fz', 'Cz'; 'Cz', 'Pz'};

for i = 1:18
    %referential index corresponding to bipolar
    bi_ch = find(contains(chl, bc{i,1}));
    bi_ref = find(contains(chl, bc{i,2}));
    if isempty(bi_ch) || isempty(bi_ref)
        bi_ch = find(contains(chl, bc2{i,1}));
        bi_ref = find(contains(chl, bc2{i,2}));
        if isempty(bi_ch) || isempty(bi_ref)
            fprintf('Given monopolar channe locations are not found in available. Your can change the bc, bc2 or, add new one and adjust the code.');
            return;
        end
    end
    ibc(i,:) = [bi_ch bi_ref];
    datanew(i,:) = EEG.data(ibc(i,1),:) - EEG.data(ibc(i,2),:);
end

%changing the channels name and number
labels = ["Fp1-F3", "F3-C3", "C3-P3", "P3-O1", "Fp2-F4", "F4-C4", "C4-P4", "P4-O2","Fp1-F7", "F7-T7", "T7-P7", "P7-O1", "Fp2-F8", "F8-T8", "T8-P8", "P8-O2", "Fz-Cz", "Cz-Pz"];
[newEEG.chanlocs(1:18).labels] = deal(labels{:});
newEEG.chanlocs(19:end) = [];

newEEG.data = datanew;
newEEG.nbchan = 18;
newEEG.ref = 'bipolar';

for i = 1:length(newEEG.chanlocs)
    if ~ischar(newEEG.chanlocs(i).labels)
        newEEG.chanlocs(i).labels = char(newEEG.chanlocs(i).labels); % Kanal adını karakter dizisine çevir
    end
end

[namen, locn] = regexp(source_path, '.edf', 'match', 'once');
save_loc = [source_path(1:locn-1) '_bipolar' source_path(locn:end)];
pop_writeeeg(newEEG, save_loc, 'TYPE', 'EDF');
