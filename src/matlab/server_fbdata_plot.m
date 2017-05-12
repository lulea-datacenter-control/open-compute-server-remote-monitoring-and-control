%
% Copyright (c) 2017 Martin Eriksson
% 
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program. If not, see <http://www.gnu.org/licenses/>.
%

close all hidden
clear all
clc
ipmi = load('fb-data.mat');
snmp = load('fb-data.mat');
loads = load('loads_fbstress.mat');

subplot(2,1,1)
plot(ipmi.u_1_t,ipmi.u_1,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 1 IPMI')
xlim([min(ipmi.u_1_t) max(ipmi.u_1_t)])
ylim([min(ipmi.u_1)-100 max(ipmi.u_1)+100])

subplot(2,1,2)
plot(ipmi.u_2_t,ipmi.u_2,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 2 IPMI')
xlim([min(ipmi.u_2_t) max(ipmi.u_2_t)])
ylim([min(ipmi.u_2)-100 max(ipmi.u_2)+100])

x_cpu_max = 100;
x_cpu_min = 20;
x_cpu_plot_max = 80;
x_cpu_plot_min = x_cpu_min;
figure(2)
subplot(2,1,1)
plot([ipmi.x_1_t(1) ipmi.x_1_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
plot(ipmi.x_s0_t,ipmi.x_s0,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_s0)-5 max(ipmi.x_s0)+5])
xlim([min(ipmi.x_s0_t) max(ipmi.x_s0_t)])
title('CPU 1 Temp IPMI')


subplot(2,1,2)
plot([ipmi.x_s1_t(1) ipmi.x_s1_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
plot(ipmi.x_s1_t,ipmi.x_s1,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_s1)-5 max(ipmi.x_s1)+5])
xlim([min(ipmi.x_s1_t) max(ipmi.x_s1_t)])
title('CPU 2 Temp IPMI')

figure(3)
subplot(2,1,1)
plot([ipmi.x_d0_t(1) ipmi.x_d0_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
plot(ipmi.x_d0_t,ipmi.x_d0,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_d0)-5 max(ipmi.x_d0)+5])
xlim([min(ipmi.x_d0_t) max(ipmi.x_d0_t)])
title('CPU 1 DIMM Temp IPMI')


subplot(2,1,2)
plot([ipmi.x_d1_t(1) ipmi.x_d1_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
stairs(ipmi.x_d1_t,ipmi.x_d1,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_d1)-5 max(ipmi.x_d1)+5])
xlim([min(ipmi.x_d1_t) max(ipmi.x_d1_t)])
title('CPU 2 DIMM Temp IPMI')

figure(4)

subplot(2,1,1)
plot(ipmi.x_i_t,ipmi.x_i,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_i)-1 max(ipmi.x_i)+1])
xlim([min(ipmi.x_i_t) max(ipmi.x_i_t)])
title('Inlet Temp IPMI')

subplot(2,1,2)
plot(ipmi.x_o_t,ipmi.x_o,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_o)-1 max(ipmi.x_o)+1])
xlim([min(ipmi.x_o_t) max(ipmi.x_o_t)])
title('Exhaust Temp IPMI')

[xa,ya] = stairs(loads.socket00_time,loads.socket00_values,'k');
[xb,yb] = stairs(loads.socket01_time,loads.socket01_values,'k--');

figure(5)
hold on
subplot(2,1,1);
plot(xa,ya,'k')
xlabel('Time [sec]')
ylabel('Loads')
title('Socket 0 loads')
xlim([min(loads.socket00_time) max(loads.socket00_time)])
ylim([-0.5 1.5])

subplot(2,1,2);
plot(xb,yb,'k')
xlabel('Time [sec]')
ylabel('Loads')
title('Socket 1 loads')
xlim([min(loads.socket01_time) max(loads.socket01_time)])
ylim([-0.5 1.5])

h = figure(6)
stairs(ipmi.x_1_t,ipmi.x_1+100, 'b')
hold on
stairs(ipmi.x_2_t,ipmi.x_2+100, 'g')
stairs(ipmi.u_1_t,(ipmi.u_1+ipmi.u_2)/200,'k')
plot([ipmi.x_1_t(1) ipmi.x_1_t(end)], [x_cpu_max x_cpu_max], 'r--')
plot(xa+(loads.s_t-ipmi.s_t),ya*(max(ipmi.x_1+100)-min(ipmi.x_1+100))+min(ipmi.x_1+100), 'b:')
plot(xb+(loads.s_t-ipmi.s_t),yb*(max(ipmi.x_2+100)-min(ipmi.x_2+100))+min(ipmi.x_2+100), 'g:')
ll = legend({'CPU$_1$', 'CPU$_2$','Average fan speed','CPU MAX Temp'});
set(ll,'Interpreter', 'latex')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_1+100)-20 max(ipmi.x_1+100)+20])
xlim([min(ipmi.x_1_t) max(ipmi.x_1_t)])
title('CPUs temps. vs loads [IPMI]')
set(h,'Units','centimeters');
pos = get(h,'Position');
set(h,'PaperPositionMode','Auto','PaperUnits','centimeters','PaperSize',[pos(3), pos(4)])
print(h,'CPUs_temps_vs_loads[FB].pdf','-dpdf','-r0')

x_cpu_max = 75;
x_cpu_min = 20;
x_cpu_plot_max = 80;
x_cpu_plot_min = x_cpu_min;
figure(7)
subplot(3,1,1)
plot(snmp.x_0_t,snmp.x_0,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_0)-1 max(snmp.x_0)+1])
xlim([min(snmp.x_0_t) max(snmp.x_0_t)])
title('Core 0 Temp SNMP')

subplot(3,1,2)
plot(snmp.x_1_t,snmp.x_1,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_1)-1 max(snmp.x_1)+1])
xlim([min(snmp.x_1_t) max(snmp.x_1_t)])
title('Core 1 Temp SNMP')

subplot(3,1,3)
plot(snmp.x_2_t,snmp.x_2,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_2)-1 max(snmp.x_2)+1])
xlim([min(snmp.x_2_t) max(snmp.x_2_t)])
title('Core 2 Temp SNMP')

figure(8)

subplot(3,1,1)
plot(snmp.x_3_t,snmp.x_3,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_3)-1 max(snmp.x_3)+1])
xlim([min(snmp.x_3_t) max(snmp.x_3_t)])
title('Core 3 Temp SNMP')


subplot(3,1,2)
plot(snmp.x_4_t,snmp.x_4,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_4)-1 max(snmp.x_4)+1])
xlim([min(snmp.x_4_t) max(snmp.x_4_t)])
title('Core 4 Temp SNMP')

subplot(3,1,3)
plot(snmp.x_5_t,snmp.x_5,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_5)-1 max(snmp.x_5)+1])
xlim([min(snmp.x_5_t) max(snmp.x_5_t)])
title('Core 5 Temp SNMP')

figure(9)

subplot(3,1,1)
plot(snmp.x_6_t,snmp.x_6,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_6)-1 max(snmp.x_6)+1])
xlim([min(snmp.x_6_t) max(snmp.x_6_t)])
title('Core 6 Temp SNMP')

subplot(3,1,2)
plot(snmp.x_7_t,snmp.x_7,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_7)-1 max(snmp.x_7)+1])
xlim([min(snmp.x_7_t) max(snmp.x_7_t)])
title('Core 7 Temp SNMP')

subplot(3,1,3)
plot(snmp.x_8_t,snmp.x_8,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_8)-1 max(snmp.x_8)+1])
xlim([min(snmp.x_8_t) max(snmp.x_8_t)])
title('Core 8 Temp SNMP')

figure(10)

subplot(3,1,1)
plot(snmp.x_9_t,snmp.x_9,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_9)-1 max(snmp.x_9)+1])
xlim([min(snmp.x_9_t) max(snmp.x_9_t)])
title('Core 9 Temp SNMP')

subplot(3,1,2)
plot(snmp.x_10_t,snmp.x_10,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_10)-1 max(snmp.x_10)+1])
xlim([min(snmp.x_10_t) max(snmp.x_10_t)])
title('Core 10 Temp SNMP')

subplot(3,1,3)
plot(snmp.x_11_t,snmp.x_11,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_11)-1 max(snmp.x_11)+1])
xlim([min(snmp.x_11_t) max(snmp.x_11_t)])
title('Core 11 Temp SNMP')

figure(11)

subplot(3,1,1)
plot(snmp.x_12_t,snmp.x_12,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_12)-1 max(snmp.x_12)+1])
xlim([min(snmp.x_12_t) max(snmp.x_12_t)])
title('Core 12 Temp SNMP')

subplot(3,1,2)
plot(snmp.x_13_t,snmp.x_13,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_13)-1 max(snmp.x_13)+1])
xlim([min(snmp.x_13_t) max(snmp.x_13_t)])
title('Core 13 Temp SNMP')

subplot(3,1,3)
plot(snmp.x_14_t,snmp.x_14,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_14)-1 max(snmp.x_14)+1])
xlim([min(snmp.x_14_t) max(snmp.x_14_t)])
title('Core 14 Temp SNMP')

figure(12)

subplot(3,1,1)
plot(snmp.x_15_t,snmp.x_15,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_15)-1 max(snmp.x_15)+1])
xlim([min(snmp.x_15_t) max(snmp.x_15_t)])
title('Core 15 Temp SNMP')

subplot(3,1,2)
plot(snmp.x_16_t,snmp.x_16,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_16)-1 max(snmp.x_16)+1])
xlim([min(snmp.x_16_t) max(snmp.x_16_t)])
title('Core 16 Temp SNMP')


subplot(3,1,3)
plot(snmp.x_17_t,snmp.x_17,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_17)-1 max(snmp.x_17)+1])
xlim([min(snmp.x_17_t) max(snmp.x_17_t)])
title('Core 17 Temp SNMP')

figure(13)

subplot(4,1,1)
plot(snmp.l_0_t,snmp.l_0,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_0)-5 max(snmp.l_0)+5])
xlim([min(snmp.l_0_t) max(snmp.l_0_t)])
title('Core 0 Load SNMP')

subplot(4,1,2)
plot(snmp.l_1_t,snmp.l_1,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_1)-5 max(snmp.l_1)+5])
xlim([min(snmp.l_1_t) max(snmp.l_1_t)])
title('Core 1 Load SNMP')

subplot(4,1,3)
plot(snmp.l_2_t,snmp.l_2,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_2)-5 max(snmp.l_2)+5])
xlim([min(snmp.l_2_t) max(snmp.l_2_t)])
title('Core 2 Load SNMP')

subplot(4,1,4)
plot(snmp.l_3_t,snmp.l_3,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_3)-5 max(snmp.l_3)+5])
xlim([min(snmp.l_3_t) max(snmp.l_3_t)])
title('Core 3 Load SNMP')

figure(14)

subplot(4,1,1)
plot(snmp.l_4_t,snmp.l_4,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_4)-5 max(snmp.l_4)+5])
xlim([min(snmp.l_4_t) max(snmp.l_4_t)])
title('Core 4 Load SNMP')

subplot(4,1,2)
plot(snmp.l_5_t,snmp.l_5,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_5)-5 max(snmp.l_5)+5])
xlim([min(snmp.l_5_t) max(snmp.l_5_t)])
title('Core 5 Load SNMP')

subplot(4,1,3)
plot(snmp.l_6_t,snmp.l_6,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_6)-5 max(snmp.l_6)+5])
xlim([min(snmp.l_6_t) max(snmp.l_6_t)])
title('Core 6 Load SNMP')

subplot(4,1,4)
plot(snmp.l_7_t,snmp.l_7,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_7)-5 max(snmp.l_7)+5])
xlim([min(snmp.l_7_t) max(snmp.l_7_t)])
title('Core 7 Load SNMP')

figure(15)

subplot(4,1,1)
plot(snmp.l_8_t,snmp.l_8,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_8)-5 max(snmp.l_8)+5])
xlim([min(snmp.l_8_t) max(snmp.l_8_t)])
title('Core 8 Load SNMP')

subplot(4,1,2)
plot(snmp.l_9_t,snmp.l_9,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_9)-5 max(snmp.l_9)+5])
xlim([min(snmp.l_9_t) max(snmp.l_9_t)])
title('Core 9 Load SNMP')

subplot(4,1,3)
plot(snmp.l_10_t,snmp.l_10,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_10)-5 max(snmp.l_10)+5])
xlim([min(snmp.l_10_t) max(snmp.l_10_t)])
title('Core 10 Load SNMP')

subplot(4,1,4)
plot(snmp.l_11_t,snmp.l_11,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_11)-5 max(snmp.l_11)+5])
xlim([min(snmp.l_11_t) max(snmp.l_11_t)])
title('Core 11 Load SNMP')

figure(16)

subplot(4,1,1)
plot(snmp.l_12_t,snmp.l_12,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_12)-5 max(snmp.l_12)+5])
xlim([min(snmp.l_12_t) max(snmp.l_12_t)])
title('Core 12 Load SNMP')

subplot(4,1,2)
plot(snmp.l_13_t,snmp.l_13,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_13)-5 max(snmp.l_13)+5])
xlim([min(snmp.l_13_t) max(snmp.l_13_t)])
title('Core 13 Load SNMP')

subplot(4,1,3)
plot(snmp.l_14_t,snmp.l_14,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_14)-5 max(snmp.l_14)+5])
xlim([min(snmp.l_14_t) max(snmp.l_14_t)])
title('Core 14 Load SNMP')

subplot(4,1,4)
plot(snmp.l_15_t,snmp.l_15,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_15)-5 max(snmp.l_15)+5])
xlim([min(snmp.l_15_t) max(snmp.l_15_t)])
title('Core 15 Load SNMP')

figure(17)

subplot(4,1,1)
plot(snmp.l_16_t,snmp.l_16,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_16)-5 max(snmp.l_16)+5])
xlim([min(snmp.l_16_t) max(snmp.l_16_t)])
title('Core 16 Load SNMP')

subplot(4,1,2)
plot(snmp.l_17_t,snmp.l_17,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_17)-5 max(snmp.l_17)+5])
xlim([min(snmp.l_17_t) max(snmp.l_17_t)])
title('Core 17 Load SNMP')

subplot(4,1,3)
plot(snmp.l_18_t,snmp.l_18,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_18)-5 max(snmp.l_18)+5])
xlim([min(snmp.l_18_t) max(snmp.l_18_t)])
title('Core 18 Load SNMP')

subplot(4,1,4)
plot(snmp.l_19_t,snmp.l_19,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_19)-5 max(snmp.l_19)+5])
xlim([min(snmp.l_19_t) max(snmp.l_19_t)])
title('Core 19 Load SNMP')

figure(18)

subplot(4,1,1)
plot(snmp.l_20_t,snmp.l_20,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_20)-5 max(snmp.l_20)+5])
xlim([min(snmp.l_20_t) max(snmp.l_20_t)])
title('Core 20 Load SNMP')

subplot(4,1,2)
plot(snmp.l_21_t,snmp.l_21,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_21)-5 max(snmp.l_21)+5])
xlim([min(snmp.l_21_t) max(snmp.l_21_t)])
title('Core 21 Load SNMP')

subplot(4,1,3)
plot(snmp.l_22_t,snmp.l_22,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_22)-5 max(snmp.l_22)+5])
xlim([min(snmp.l_22_t) max(snmp.l_22_t)])
title('Core 22 Load SNMP')


subplot(4,1,4)
plot(snmp.l_23_t,snmp.l_23,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_23)-5 max(snmp.l_23)+5])
xlim([min(snmp.l_23_t) max(snmp.l_23_t)])
title('Core 23 Load SNMP')

figure(19)

subplot(4,1,1)
plot(snmp.l_24_t,snmp.l_24,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_24)-5 max(snmp.l_24)+5])
xlim([min(snmp.l_24_t) max(snmp.l_24_t)])
title('Core 24 Load SNMP')

subplot(4,1,2)
plot(snmp.l_25_t,snmp.l_25,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_25)-5 max(snmp.l_25)+5])
xlim([min(snmp.l_25_t) max(snmp.l_25_t)])
title('Core 25 Load SNMP')


subplot(4,1,3)
plot(snmp.l_26_t,snmp.l_26,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_26)-5 max(snmp.l_26)+5])
xlim([min(snmp.l_26_t) max(snmp.l_26_t)])
title('Core 26 Load SNMP')

subplot(4,1,4)
plot(snmp.l_27_t,snmp.l_27,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_27)-5 max(snmp.l_27)+5])
xlim([min(snmp.l_27_t) max(snmp.l_27_t)])
title('Core 27 Load SNMP')

figure(20)

subplot(4,1,1)
plot(snmp.l_28_t,snmp.l_28,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_28)-5 max(snmp.l_28)+5])
xlim([min(snmp.l_28_t) max(snmp.l_28_t)])
title('Core 28 Load SNMP')


subplot(4,1,2)
plot(snmp.l_29_t,snmp.l_29,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_29)-5 max(snmp.l_29)+5])
xlim([min(snmp.l_29_t) max(snmp.l_29_t)])
title('Core 29 Load SNMP')

subplot(4,1,3)
plot(snmp.l_30_t,snmp.l_30,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_30)-5 max(snmp.l_30)+5])
xlim([min(snmp.l_30_t) max(snmp.l_30_t)])
title('Core 30 Load SNMP')

subplot(4,1,4)
plot(snmp.l_31_t,snmp.l_31,'k')
xlabel('Time [sec]')
ylabel('Percent [%%]')
ylim([min(snmp.l_31)-5 max(snmp.l_31)+5])
xlim([min(snmp.l_31_t) max(snmp.l_31_t)])
title('Core 31 Load SNMP')

figure(21)

subplot(2,1,1)
plot(ipmi.u_1_t,(ipmi.u_1+ipmi.u_2)/2,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Average fan speed IPMI')
xlim([min(ipmi.u_1_t) max(ipmi.u_1_t)])
ylim([min((ipmi.u_1+ipmi.u_2)/2)-100 max((ipmi.u_1+ipmi.u_2)/2)+100])

subplot(2,1,2)
plot(ipmi.u_2_t,abs(ipmi.u_1-ipmi.u_2),'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Difference Fan 1 vs Fan 2 IPMI')
xlim([min(ipmi.u_2_t) max(ipmi.u_2_t)])
%ylim([min(ipmi.u_2)-100 max(ipmi.u_2)+100])
