function metaD = metaDprimeSubject (subjectNumber)
%subjectNumber = int2str(subjectNumber);
file = strcat('Subject', subjectNumber, '/Generalization/responses.csv');
fid = fopen(file);
subjData = textscan(fid, '%d%d%d', 'delimiter', ',', 'HeaderLines', 1);
fclose(fid);
[nR_S1, nR_S2] = trials2counts(subjData{1},subjData{3}, subjData{2}, 4);
metaD = type2_SDT_SSE(nR_S1, nR_S2)