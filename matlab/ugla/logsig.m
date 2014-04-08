function [a] = logsig(n),
%LOGSIG log-sigmoid transfer function
% usage: a = logsig(n)

a = 1./(1+exp(-n));
