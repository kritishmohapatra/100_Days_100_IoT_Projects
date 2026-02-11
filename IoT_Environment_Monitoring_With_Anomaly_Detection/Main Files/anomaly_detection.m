%% =========================================================
%  ThingSpeak IoT Data Anomaly Detection using Z-Score
%  Sensors: LDR, Temperature, Humidity
%  Platform: MATLAB + ThingSpeak
%  Method: Statistical Z-Score Based Anomaly Detection
%% =========================================================

% -------- ThingSpeak Channel Credentials --------
readChannelID = "readchanelid";   % Replace with your ThingSpeak Channel ID
readAPIKey   = 'readkey';         % Replace with your Read API Key


%% ================= LDR ANALYSIS =================
% Field 3 is assumed to contain LDR (Light Intensity) data
ldrField = 3;

% Read last 60 minutes of LDR data from ThingSpeak
ld = thingSpeakRead(readChannelID, ...
    'Fields', ldrField, ...
    'NumMinutes', 60, ...
    'ReadKey', readAPIKey);

disp(ld);   % Display raw LDR data

% Calculate average light intensity
avgldr = mean(ld);
fprintf("Avg Light Intensity = %.2f\n", avgldr);

% Assign data to variable x for processing
x = ld;

% Compute Z-score (standard score)
e  = mean(x);     % Mean of LDR data
si = std(x);      % Standard deviation of LDR data
z  = (x - e) / si;

% Index arrays for normal and anomalous samples
op  = [];   % Normal data indices
op1 = [];   % Anomaly data indices

% Detect anomalies using Z-score threshold
for i = 1:length(z)
    if (z(i) <= 1.4 && z(i) >= -1.4)
        op = [op i];      % Normal sample
    else
        op1 = [op1 i];    % Anomalous sample
    end
end

% Extract normal and anomalous LDR values
w  = x(op);
w1 = x(op1);

fprintf("Normal values (LDR):\n");
disp(w);

fprintf("Anomalies in LDR data:\n");
disp(w1);

fprintf("LDR Anomaly Count = %d\n\n", length(w1));


%% ================= TEMPERATURE ANALYSIS =================
% Field 1 is assumed to contain Temperature data
tempField = 1;

% Read last 60 minutes of Temperature data
temp = thingSpeakRead(readChannelID, ...
    'Fields', tempField, ...
    'NumMinutes', 60, ...
    'ReadKey', readAPIKey);

disp(temp);   % Display raw temperature data

% Calculate average temperature
avgtemp = mean(temp);
fprintf("Avg Temperature = %.2f °C\n", avgtemp);

% Z-score calculation for temperature
xtmp   = temp;
etmp   = mean(xtmp);     % Mean temperature
si_tmp = std(xtmp);      % Standard deviation
ztmp   = (xtmp - etmp) / si_tmp;

% Index arrays for temperature anomaly detection
op_tmp  = [];
op1_tmp = [];

% Detect temperature anomalies (wider threshold)
for i = 1:length(ztmp)
    if (ztmp(i) <= 2.5 && ztmp(i) >= -2.5)
        op_tmp = [op_tmp i];
    else
        op1_tmp = [op1_tmp i];
    end
end

% Extract normal and anomalous temperature values
wtmp   = xtmp(op_tmp);
w1_tmp = xtmp(op1_tmp);

fprintf("Normal Temperature values:\n");
disp(wtmp);

fprintf("Temperature Anomalies:\n");
disp(w1_tmp);

fprintf("Temperature Anomaly Count = %d\n\n", length(w1_tmp));


%% ================= HUMIDITY ANALYSIS =================
% Field 2 is assumed to contain Humidity data
humField = 2;

% Read last 60 minutes of Humidity data
hum = thingSpeakRead(readChannelID, ...
    'Fields', humField, ...
    'NumMinutes', 60, ...
    'ReadKey', readAPIKey);

disp(hum);   % Display raw humidity data

% Calculate average humidity
avgh = mean(hum);
fprintf("Avg Humidity = %.2f %%\n", avgh);

% Z-score calculation for humidity
xh   = hum;
eh   = mean(xh);     % Mean humidity
si_h = std(xh);      % Standard deviation
zh   = (xh - eh) / si_h;

% Index arrays for humidity anomaly detection
op_h  = [];
op1_h = [];

% Detect humidity anomalies
for i = 1:length(zh)
    if (zh(i) <= 2.5 && zh(i) >= -2.5)
        op_h = [op_h i];
    else
        op1_h = [op1_h i];
    end
end

% Extract normal and anomalous humidity values
wh   = xh(op_h);
w1_h = xh(op1_h);

fprintf("Normal Humidity values:\n");
disp(wh);

fprintf("Humidity Anomalies:\n");
disp(w1_h);

fprintf("Humidity Anomaly Count = %d\n\n", length(w1_h));


%% ================= VISUALIZATION =================
% Plot Z-score values for all sensors in a single figure

figure;

subplot(3,1,1);
plot(z, "g");
title("LDR Z-Score");
ylabel("Z");

subplot(3,1,2);
plot(ztmp, "r");
title("Temperature Z-Score");
ylabel("Z");

subplot(3,1,3);
plot(zh);
title("Humidity Z-Score");
ylabel("Z");
xlabel("Samples");
