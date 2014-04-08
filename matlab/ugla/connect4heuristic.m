function move = connect4heuristic(state, colour, w)
% CONNECT4HEURISTIC this function uses board inversion 
%                                      and calls getfeatures
% usage: move = connect4heuristic(state, colour, w);

A = find(state(1,:) == 0); % find legal moves
phi = zeros(length(w),length(A)); % initialize memory
for i=1:length(A) % evaluate all after-states
  newstate = connect4simulate(state, A(i), colour);
  phi(:,i) = getfeatures(colour*newstate); % your getfeatures may require more inputs?
end
[dummy, i] = max(colour*tansig(w*phi)); % unlikely to have ties
move = A(i);
