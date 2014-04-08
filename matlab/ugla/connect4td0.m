n = 42; % the number of features, depends on you "getfeatures" function
w = zeros(1,n); % initialize weights for linear value function
epsilon = 0.1; % epsilon-greedy policy, 0.1 is a good value to use here
alpha = 0.01;  % step size alpha, will need to tune this or decrease with episodes
for episodes = 1:10000 % the more the better ...
% initialize the game connect-four
  state = zeros(6,7); % the grid is empty with all zeros 6x7
  winner = []; % the reward is empty, i.e. game is not over
  colour = 1; % player with the first move has colour 1, other colour is -1
% player take turns dropping a disc in their respective colour
  phi = zeros(n,2); % previous feature vectors for both players
  counter = 0; % once both players have made a move we can start updating
  while isempty(winner) % while empty then game not over
    counter = counter + 1; % increment move counter
  % get all feasible actions, A(s)
    A = find(0 == state(1,:)); % when zero there is no disk in the top row
  % use a policy to select a move or action from A, for players 1 and -1 
    if (rand(1) < epsilon) % random move
      move = A(ceil(length(A)*rand(1))); % random move
    else % greedy move, uses board inversion
      move = connect4heuristic(state, colour, w);
    end
  % now simulate the move and observe resulting state and reward
    [state, winner] = connect4simulate(state, move, colour);
  % TD update
    i = (colour+1)/2+1; % get index to player colour
    phinew = getfeatures(colour*state); % use board inversion
    if (counter > 2) % update using TD(0) and logsig squashing function
      w = w + alpha*(logsig(w*phinew)-logsig(w*phi(:,i)))*dlogsig(w*phi(:,i))*phi(:,i)';
    end
    phi(:,i) = phinew; % store feature to be used later
  % now its the other player's turn
    colour = -colour;
  end
  % let the reward reflect the probability of winning
  if (1 == winner)
    reward = 1;
  elseif (-1 == winner)
    reward = 0;
  else
    reward = 0.5;
  end
  % now the first player is +1 in colour and actually owns the "w" heuristic
  % so we update the first player with:
  w = w + alpha*(reward - logsig(w*phi(:,1)))*dlogsig(w*phi(:,1))*phi(:,1)';
  % however, since we are using board inversion the second player will be
  % updated with the reverse reward which will be (1-reward):
  w = w + alpha*((1-reward) - logsig(w*phi(:,2)))*dlogsig(w*phi(:,2))*phi(:,2)';
end % episode