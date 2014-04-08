function [d] = dlogsig(n),
%DLOGSIG derivative of log-sigmoid transfer function
% usage: d = dlogsig(n)

a = logsig(n);
d = a.*(1-a);


