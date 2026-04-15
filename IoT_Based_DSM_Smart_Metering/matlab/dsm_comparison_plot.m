% ============================================================
%  DSM Smart Meter — MATLAB Comparison Plot
%  Code 1 (Without DSM) vs Code 2 (With DSM Peak Shifting)
%  Author : Kritish Mohapatra
% ============================================================

clc; clear; close all;

%% ── Load Data ───────────────────────────────────────────────
d1 = readtable('check1.csv');
d2 = readtable('check2.csv');

% Parse time to minutes from 18:00
function mins = parse_time(times)
    mins = zeros(length(times), 1);
    for i = 1:length(times)
        t = char(times{i});
        h = str2double(t(1:2));
        m = str2double(t(4:5));
        mins(i) = (h * 60 + m) - (18 * 60);
    end
end

t1 = parse_time(d1.Time);
t2 = parse_time(d2.Time);

tp1 = d1.TotalPower;
tp2 = d2.TotalPower;

%% ── Figure 1: Side by Side Comparison ───────────────────────
figure('Name', 'DSM Comparison', 'Position', [50 50 1200 500]);

% Plot 1 — Without DSM
subplot(1,2,1);
area(t1, tp1, 'FaceColor', [1 0.6 0.6], 'EdgeColor', 'r', 'LineWidth', 1.5);
hold on;
xregion(17, 49, 'FaceColor', 'red', 'FaceAlpha', 0.15);
xlabel('Time (min from 6:00 PM)');
ylabel('Total Power (W)');
title('Without DSM (Phase 1)');
grid on;
xlim([0 65]); ylim([0 130]);
xticks(0:5:65);
xticklabels(arrayfun(@(x) sprintf('%02d:%02d', ...
    floor((18*60+x)/60), mod(18*60+x,60)), 0:5:65, 'UniformOutput', false));
xtickangle(45);
text(28, 115, 'PEAK ZONE', 'Color', 'red', 'FontWeight', 'bold', ...
     'HorizontalAlignment', 'center', 'FontSize', 10);
legend('Total Power', 'Peak Zone', 'Location', 'northwest');

% Plot 2 — With DSM
subplot(1,2,2);
area(t2, tp2, 'FaceColor', [0.6 1 0.6], 'EdgeColor', [0 0.6 0], 'LineWidth', 1.5);
hold on;
xregion(17, 49, 'FaceColor', 'red', 'FaceAlpha', 0.15);
xlabel('Time (min from 6:00 PM)');
ylabel('Total Power (W)');
title('With DSM Peak Shifting (Phase 2)');
grid on;
xlim([0 65]); ylim([0 130]);
xticks(0:5:65);
xticklabels(arrayfun(@(x) sprintf('%02d:%02d', ...
    floor((18*60+x)/60), mod(18*60+x,60)), 0:5:65, 'UniformOutput', false));
xtickangle(45);
text(28, 115, 'PEAK ZONE', 'Color', 'red', 'FontWeight', 'bold', ...
     'HorizontalAlignment', 'center', 'FontSize', 10);
text(28, 30, 'Iron AUTO OFF', 'Color', [0 0.5 0], 'FontWeight', 'bold', ...
     'HorizontalAlignment', 'center', 'FontSize', 10);
legend('Total Power', 'Peak Zone', 'Location', 'northwest');

sgtitle('DSM Smart Meter — Peak Shifting Comparison', ...
        'FontSize', 14, 'FontWeight', 'bold');

%% ── Figure 2: Overlay Comparison ────────────────────────────
figure('Name', 'Overlay Comparison', 'Position', [50 600 900 450]);

plot(t1, tp1, 'r-', 'LineWidth', 2.5); hold on;
plot(t2, tp2, 'g-', 'LineWidth', 2.5);
xregion(17, 49, 'FaceColor', 'red', 'FaceAlpha', 0.1);

xlabel('Time (min from 6:00 PM)');
ylabel('Total Power (W)');
title('Without DSM vs With DSM — Overlay');
legend('Without DSM', 'With DSM (Peak Shifted)', 'Peak Zone', ...
       'Location', 'northwest');
grid on;
xlim([0 65]); ylim([0 130]);
xticks(0:5:65);
xticklabels(arrayfun(@(x) sprintf('%02d:%02d', ...
    floor((18*60+x)/60), mod(18*60+x,60)), 0:5:65, 'UniformOutput', false));
xtickangle(45);

% Peak reduction annotation
peak_idx1 = t1 >= 17 & t1 < 49;
peak_idx2 = t2 >= 17 & t2 < 49;
avg1 = mean(tp1(peak_idx1));
avg2 = mean(tp2(peak_idx2));
reduction = ((avg1 - avg2) / avg1) * 100;
text(33, 110, sprintf('Peak reduced by %.1f%%', reduction), ...
     'Color', 'blue', 'FontWeight', 'bold', ...
     'HorizontalAlignment', 'center', 'FontSize', 11, ...
     'BackgroundColor', 'white');

%% ── Figure 3: Energy Saved ───────────────────────────────────
figure('Name', 'Energy Comparison', 'Position', [500 600 600 400]);

% Calculate energy (Wh) using trapezoidal integration
dt = 1/60;  % 1 minute intervals in hours
energy1 = trapz(t1, tp1) * dt;
energy2 = trapz(t2, tp2) * dt;
energy_saved = energy1 - energy2;

bar_data = [energy1, energy2];
b = bar(bar_data, 0.5);
b.FaceColor = 'flat';
b.CData(1,:) = [1 0.4 0.4];
b.CData(2,:) = [0.4 0.8 0.4];

xticklabels({'Without DSM', 'With DSM'});
ylabel('Energy Consumed (Wh)');
title('Total Energy Comparison');
grid on;

text(1, energy1 + 0.3, sprintf('%.2f Wh', energy1), ...
     'HorizontalAlignment', 'center', 'FontWeight', 'bold');
text(2, energy2 + 0.3, sprintf('%.2f Wh', energy2), ...
     'HorizontalAlignment', 'center', 'FontWeight', 'bold');
text(1.5, max(bar_data)*0.6, sprintf('Saved: %.2f Wh\n(%.1f%% reduction)', ...
     energy_saved, (energy_saved/energy1)*100), ...
     'HorizontalAlignment', 'center', 'FontSize', 11, ...
     'Color', 'blue', 'FontWeight', 'bold', 'BackgroundColor', 'white');

fprintf('\n===== DSM RESULTS =====\n');
fprintf('Avg peak power WITHOUT DSM : %.1f W\n', avg1);
fprintf('Avg peak power WITH DSM    : %.1f W\n', avg2);
fprintf('Peak reduction             : %.1f%%\n', reduction);
fprintf('Energy WITHOUT DSM         : %.2f Wh\n', energy1);
fprintf('Energy WITH DSM            : %.2f Wh\n', energy2);
fprintf('Energy saved               : %.2f Wh (%.1f%%)\n', energy_saved, (energy_saved/energy1)*100);
fprintf('=======================\n');