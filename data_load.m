tests = cell(4,1);

original = cell(4,1);
recon = cell(4,1);

for i = 1:4
    tests{i} = "test" + num2str(i);
    original{i} = audioread(tests{i} + '.wav');
    recon{i} = audioread(tests{i} + '_reconstructed.wav');
end

clearvars -except original recon

