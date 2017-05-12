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
ipmi = load('ipmi-data.mat');
snmp =load('snmp-data.mat');
loads = load('loads_stress.mat');
%t = linspace(0,1, 10);
figure(1)
hold on

subplot(6,1,1)
plot(ipmi.u_1_t,ipmi.u_1,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 1 IPMI')
xlim([min(ipmi.u_1_t) max(ipmi.u_1_t)])

subplot(6,1,2)
plot(ipmi.u_2_t,ipmi.u_2,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 2 IPMI')
xlim([min(ipmi.u_2_t) max(ipmi.u_2_t)])

subplot(6,1,3)
plot(ipmi.u_3_t,ipmi.u_3,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 3 IPMI')
xlim([min(ipmi.u_3_t) max(ipmi.u_3_t)])

subplot(6,1,4)
plot(ipmi.u_4_t,ipmi.u_4,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 4 IPMI')
xlim([min(ipmi.u_4_t) max(ipmi.u_4_t)])

subplot(6,1,5)
plot(ipmi.u_5_t,ipmi.u_5,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 5')
xlim([min(ipmi.u_5_t) max(ipmi.u_5_t)])

subplot(6,1,6)
plot(ipmi.u_6_t,ipmi.u_6,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 6 IPMI')
xlim([min(ipmi.u_6_t) max(ipmi.u_6_t)])


x_cpu_max = 75;
x_cpu_min = 20;
x_cpu_plot_max = 80;
x_cpu_plot_min = x_cpu_min;
figure(2)
subplot(4,1,1)
plot([ipmi.x_1_t(1) ipmi.x_1_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
plot(ipmi.x_1_t,ipmi.x_1,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.x_1_t) max(ipmi.x_1_t)])
title('CPU 1 Temp IPMI')


subplot(4,1,2)
plot([ipmi.x_2_t(1) ipmi.x_2_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
stairs(ipmi.x_2_t,ipmi.x_2,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.x_2_t) max(ipmi.x_2_t)])
title('CPU 2 Temp IPMI')

subplot(4,1,3)
plot(ipmi.x_i_t,ipmi.x_i,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_i)-1 max(ipmi.x_i)+1])
xlim([min(ipmi.x_i_t) max(ipmi.x_i_t)])
title('Inlet Temp IPMI')

subplot(4,1,4)
plot(ipmi.x_o_t,ipmi.x_o,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_o)-1 max(ipmi.x_o)+1])
xlim([min(ipmi.x_o_t) max(ipmi.x_o_t)])
title('Exhaust Temp IPMI')

figure(3)
subplot(4,1,1)
hold on
plot(ipmi.l_c_t,ipmi.l_c,'k')
xlabel('Time [sec]')
ylabel(sprintf('Percent [%%]'))
%ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.l_c_t) max(ipmi.l_c_t)])
title('CPU load IPMI')


subplot(4,1,2)
hold on
plot(ipmi.l_io_t,ipmi.l_io,'k')
xlabel('Time [sec]')
ylabel(sprintf('Percent [%%]'))
%ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.l_io_t) max(ipmi.l_io_t)])
title('IO load IPMI')

subplot(4,1,3)
plot(ipmi.l_m_t,ipmi.l_m,'k')
xlabel('Time [sec]')
ylabel(sprintf('Percent [%%]'))
%ylim([min(ipmi.x_i)-1 max(ipmi.x_i)+1])
xlim([min(ipmi.l_m_t) max(ipmi.l_m_t)])
title('Memory load IPMI')

subplot(4,1,4)
plot(ipmi.l_s_t,ipmi.l_s,'k')
xlabel('Time [sec]')
ylabel(sprintf('Percent [%%]'))
%ylim([min(_o)-1 max(ipmi.x_o)+1])
xlim([min(ipmi.l_s_t) max(ipmi.l_s_t)])
title('System load IPMI')

figure(4)
subplot(2,1,1)
hold on
plot(ipmi.c_1_t,ipmi.c_1,'k')
xlabel('Time [sec]')
ylabel('Amps')
%ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.c_1_t) max(ipmi.c_1_t)])
title('Current 1 IPMI')


subplot(2,1,2)
hold on
plot(ipmi.c_2_t,ipmi.c_2,'k')
xlabel('Time [sec]')
ylabel('Amps')
%ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.c_2_t) max(ipmi.c_2_t)])
title('Current 2 IPMI')

figure(5)
subplot(2,1,1)
hold on
plot(ipmi.v_1_t,ipmi.v_1,'k')
xlabel('Time [sec]')
ylabel('Volts')
%ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.v_1_t) max(ipmi.v_1_t)])
title('Voltage 1 IPMI')


subplot(2,1,2)
hold on
plot(ipmi.v_2_t,ipmi.v_2,'k')
xlabel('Time [sec]')
ylabel('Volts')
%ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(ipmi.v_2_t) max(ipmi.v_2_t)])
title('Voltage 2 IPMI')

figure(6)
subplot(1,1,1)
hold on
plot(ipmi.p_c_t,ipmi.p_c,'k')
xlabel('Time [sec]')
ylabel('Watts')
ylim([min(ipmi.p_c)-1 max(ipmi.p_c)+1])
xlim([min(ipmi.p_c_t) max(ipmi.p_c_t)])
title('Power Consumtion IPMI')

figure(7)
hold on

subplot(6,1,1)
plot(snmp.u_1_t,snmp.u_1,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 1 SNMP')
xlim([min(snmp.u_1_t) max(snmp.u_1_t)])

subplot(6,1,2)
plot(snmp.u_2_t,snmp.u_2,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 2 SNMP')
xlim([min(snmp.u_2_t) max(snmp.u_2_t)])

subplot(6,1,3)
plot(snmp.u_3_t,snmp.u_3,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 3 SNMP')
xlim([min(snmp.u_3_t) max(snmp.u_3_t)])

subplot(6,1,4)
plot(snmp.u_4_t,snmp.u_4,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 4 SNMP')
xlim([min(snmp.u_4_t) max(snmp.u_4_t)])

subplot(6,1,5)
plot(snmp.u_5_t,snmp.u_5,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 5 SNMP')
xlim([min(snmp.u_5_t) max(snmp.u_5_t)])

subplot(6,1,6)
plot(snmp.u_6_t,snmp.u_6,'k')
xlabel('Time [sec]')
ylabel('Speed [RPM]')
title('Fan 6 SNMP')
xlim([min(snmp.u_6_t) max(snmp.u_6_t)])


x_cpu_max = 75;
x_cpu_min = 20;
x_cpu_plot_max = 80;
x_cpu_plot_min = x_cpu_min;
figure(8)
subplot(4,1,1)
plot([snmp.x_1_t(1) snmp.x_1_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
plot(snmp.x_1_t,snmp.x_1,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(snmp.x_1_t) max(snmp.x_1_t)])
title('CPU 1 Temp SNMP')


subplot(4,1,2)
plot([snmp.x_2_t(1) snmp.x_2_t(end)], [x_cpu_max x_cpu_max], 'r--')
hold on
plot(snmp.x_2_t,snmp.x_2,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([x_cpu_plot_min x_cpu_plot_max])
xlim([min(snmp.x_2_t) max(snmp.x_2_t)])
title('CPU 2 Temp SNMP')

subplot(4,1,3)
plot(snmp.x_i_t,snmp.x_i,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_i)-1 max(snmp.x_i)+1])
xlim([min(snmp.x_i_t) max(snmp.x_i_t)])
title('Inlet Temp SNMP')

subplot(4,1,4)
plot(snmp.x_o_t,snmp.x_o,'k')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_o)-1 max(snmp.x_o)+1])
xlim([min(snmp.x_o_t) max(snmp.x_o_t)])
title('Exhaust Temp SNMP')

% figure(9)
% subplot(2,1,1)
% hold on
% plot(snmp.c_1_t,snmp.c_1,'k')
% xlabel('Time [sec]')
% ylabel('MHz')
% %ylim([x_cpu_plot_min x_cpu_plot_max])
% xlim([min(snmp.c_1_t) max(snmp.c_1_t)])
% title('CPU 1 Speed SNMP')


% subplot(2,1,2)
% hold on
% plot(snmp.c_2_t,snmp.c_2,'k')
% xlabel('Time [sec]')
% ylabel('MHz')
% %ylim([x_cpu_plot_min x_cpu_plot_max])
% xlim([min(snmp.c_2_t) max(snmp.c_2_t)])
% title('CPU 2 Speed SNMP')
% 
% figure(10)
% subplot(2,1,1)
% hold on
% plot(snmp.v_1_t,snmp.v_1,'k')
% xlabel('Time [sec]')
% ylabel('Volts')
% %ylim([x_cpu_plot_min x_cpu_plot_max])
% xlim([min(snmp.v_1_t) max(snmp.v_1_t)])
% title('Voltage 1 SNMP')
% 
% 
% subplot(2,1,2)
% hold on
% plot(snmp.v_2_t,snmp.v_2,'k')
% xlabel('Time [sec]')
% ylabel('Volts')
% %ylim([x_cpu_plot_min x_cpu_plot_max])
% xlim([min(snmp.v_2_t) max(snmp.v_2_t)])
% title('Voltage 2 SNMP')
% snmp.p_c = snmp.p_c - snmp.p_c(1);
% figure(11)
% subplot(1,1,1)
% hold on
% plot(snmp.p_c_t,snmp.p_c,'k')
% xlabel('Time [sec]')
% ylabel('Wh')
% ylim([min(snmp.p_c)-1 max(snmp.p_c)+1])
% xlim([min(snmp.p_c_t) max(snmp.p_c_t)])
% title('Power Consumtion SNMP')

[xa,ya] = stairs(loads.socket00_time,loads.socket00_values,'k');
[xb,yb] = stairs(loads.socket01_time,loads.socket01_values,'k--');

figure(12)
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

h = figure(13)
stairs(ipmi.x_1_t,ipmi.x_1, 'b')
hold on
stairs(ipmi.x_2_t,ipmi.x_2, 'g')
plot(xa+(loads.s_t-ipmi.s_t),ya*20+40, 'b:')
plot(xb+(loads.s_t-ipmi.s_t),yb*20+40, 'g:')
plot([ipmi.x_1_t(1) ipmi.x_1_t(end)], [x_cpu_max x_cpu_max], 'r--')
ll = legend({'CPU$_1$', 'CPU$_2$'});
set(ll,'Interpreter', 'latex')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(ipmi.x_1)-10 max(ipmi.x_1)+10])
xlim([min(ipmi.x_1_t) max(ipmi.x_1_t)])
title('CPUs temps. vs loads [IPMI]')
set(h,'Units','centimeters');
pos = get(h,'Position');
set(h,'PaperPositionMode','Auto','PaperUnits','centimeters','PaperSize',[pos(3), pos(4)])
print(h,'CPUs_temps_vs_loads.pdf','-dpdf','-r0')

s = figure(14)
stairs(snmp.x_1_t,snmp.x_1, 'b')
hold on
stairs(snmp.x_2_t,snmp.x_2, 'g')
plot(xa+(loads.s_t-snmp.s_t),ya*20+40, 'b:')
plot(xb+(loads.s_t-snmp.s_t),yb*20+40, 'g:')
plot([snmp.x_1_t(1) snmp.x_1_t(end)], [x_cpu_max x_cpu_max], 'r--')
ll = legend({'CPU$_1$', 'CPU$_2$'});
set(ll,'Interpreter', 'latex')
xlabel('Time [sec]')
ylabel(sprintf('Temp [%cC]', char(176)))
ylim([min(snmp.x_1)-10 max(snmp.x_1)+10])
xlim([min(snmp.x_1_t) max(snmp.x_1_t)])
title('CPUs temps. vs loads [SNMP]')
set(h,'Units','centimeters');
pos = get(h,'Position');
set(h,'PaperPositionMode','Auto','PaperUnits','centimeters','PaperSize',[pos(3), pos(4)])
print(h,'CPUs_temps_vs_loads.pdf','-dpdf','-r0')
