function connect4animate(state,action,colour)
%CONNECT4ANIMATE
%  usage: connect4animate(state,action,colour)

set(gca,'ylim',[0 6],'xlim',[0 7])
k = 1;
if all(state(:)==0),clf,shg, else, hold on, grid on, end
h = [];
while (state(k,action) == 0)
  delete(h);
  if (colour == 1)
    h = plot(action-.5,6-k+.5,'ko','markersize',30,'MarkerFaceColor','r');
  elseif (colour == -1)
    h = plot(action-.5,6-k+.5,'ko','markersize',30,'MarkerFaceColor','y'); 
  end
  k = k + 1;
  if (k == 7), break, end
  pause(0.05),drawnow
end   