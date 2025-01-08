# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 13:34:29 2025

@author: Mustafa Yasir
-Prepared by neuronauts group.
-This code converts your selected mono or avg. referencing '.edf' file to 
    bipolar referencing.
-Input monopolar 'dataname.edf' file -> Output bipolar 'dataname_bipolar.edf' 
    file at same location.
-Require the os,mne and edfio libraries
"""

import os
import mne

# Insert the file locations 
file_path = r'C:\Users\Mustafa Yasir\Desktop\Merve_Zaim_after.edf'

if not os.path.exists(file_path):
    print("The selected file does not exist!")
else:
    print(f"Selected file: {file_path}")

    # Reading the .edf file
    raw = mne.io.read_raw_edf(file_path, preload=True)

    # channel labels for index
    chl = raw.info['ch_names']

    # Bipolar correspondings of electrode for indexing
    # Channel naming may vary, so before running the code, set the names of the 
    # channel pairs to the names in your .edf file. The standard 10-20 channel 
    # names are given below.
    bc = [
        ('Fp1', 'F3'), ('F3', 'C3'), ('C3', 'P3'), ('P3', 'O1'),
        ('Fp2', 'F4'), ('F4', 'C4'), ('C4', 'P4'), ('P4', 'O2'),
        ('Fp1', 'F7'), ('F7', 'T7'), ('T7', 'P7'), ('P7', 'O1'),
        ('Fp2', 'F8'), ('F8', 'T8'), ('T8', 'P8'), ('P8', 'O2'),
        ('Fz', 'Cz'), ('Cz', 'Pz')
    ]

    bc2 = [
        ('Fp1', 'F3'), ('F3', 'C3'), ('C3', 'P3'), ('P3', 'O1'),
        ('Fp2', 'F4'), ('F4', 'C4'), ('C4', 'P4'), ('P4', 'O2'),
        ('Fp1', 'F7'), ('F7', 'T3'), ('T3', 'T5'), ('T5', 'O1'),
        ('Fp2', 'F8'), ('F8', 'T4'), ('T4', 'T6'), ('T6', 'O2'),
        ('Fz', 'Cz'), ('Cz', 'Pz')
    ]

    # Referential index corresponding to bipolar
    datanew = []
    for i in range(len(bc)):
        bi_ch = [idx for idx, ch in enumerate(chl) if bc[i][0] in ch]
        bi_ref = [idx for idx, ch in enumerate(chl) if bc[i][1] in ch]
        
        if not bi_ch or not bi_ref:
            # Eğer bu kanal bulunmazsa, bc2'yi dene
            bi_ch = [idx for idx, ch in enumerate(chl) if bc2[i][0] in ch]
            bi_ref = [idx for idx, ch in enumerate(chl) if bc2[i][1] in ch]
            if not bi_ch or not bi_ref:
                print(f"Given monopolar channel locations are not found for {bc[i]} or {bc2[i]}. Adjust the code or change the channel names.")
                continue
        
        # Compute the bipolar channels values
        datanew.append(raw.get_data(picks=bi_ch[0])[0] - raw.get_data(picks=bi_ref[0])[0])

    # Arrange the new channels indeks
    labels = [
        "Fp1-F3", "F3-C3", "C3-P3", "P3-O1", "Fp2-F4", "F4-C4", "C4-P4", "P4-O2",
        "Fp1-F7", "F7-T7", "T7-P7", "P7-O1", "Fp2-F8", "F8-T8", "T8-P8", "P8-O2", 
        "Fz-Cz", "Cz-Pz"
    ]
    


    info = mne.create_info(ch_names=labels, sfreq=raw.info['sfreq'], ch_types='eeg')
    bipolar_raw = mne.io.RawArray(datanew, info)
    # Retrieves the recording date and time data. Update the meas_date and meas_id values
    bipolar_raw.set_meas_date(raw.info['meas_date'])
    bipolar_raw.set_annotations(raw.annotations)
    
    
    # Write the new bipolar referential data as '.edf' at the same location as the source
    output_path = file_path.replace('.edf', '_bipolar2.edf')
    bipolar_raw.export(output_path, fmt='edf')

    print(f"Bipolar referenced .edf file saved: {output_path}")
    
