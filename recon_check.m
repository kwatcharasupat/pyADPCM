load data.mat

% rho = zeros(4,1);
original_spec = cell(4,1);
recon_spec = cell(4,1);

nfft = 256;
diff_spec = zeros(nfft/2+1,0);
rel_diff = zeros(nfft/2+1,0);

for i = 1:4
%     rho(i) = corr(original{i}, recon{i});
    
    original_spec{i} = spectrogram(original{i}, hamming(nfft), 0.75*nfft);
    recon_spec{i} = spectrogram(recon{i}, hamming(nfft), 0.75*nfft);
    
    len = size(original_spec{i}, 2);
    
    diff_spec(:, end+1:end+len) = abs(recon_spec{i}).^2 - abs(original_spec{i}).^2;
    rel_diff(:, end+1:end+len) = diff_spec(:, end-len+1:end)./abs(original_spec{i}).^2;
    
    figure;
    subplot(2,1,1);
    spectrogram(original{i}, hamming(256), 128, 'yaxis');
    ylabel('original')
    subplot(2,1,2);
    spectrogram(recon{i}, hamming(256), 128, 'yaxis');
    ylabel('reconstructed')
end

