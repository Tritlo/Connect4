function [state, reward] = connect4simulate(state, action, colour)
%CONNECT4SIMULATE 
% usage: [state, reward] = connect4simulate(state, action, colour)

  reward = [];
  I = find(0 == state(:,action)); % find all empties in vertical line
  endofline = I(end);
  state(endofline,action) = colour; % drop the disc to the end of this line

% now examine if the game is over and return a reward
% the code is brute force and can most probably be optimized further

% check for vertical win
  for i = 1:3
    if all(colour == state(i:(i+3),action))
       reward = colour;
       return;
    end
  end
% check for horizontal win
   for i = 1:4
     if all(colour == state(endofline,i:(i+3)))
        reward = colour;
        return;
     end
   end
% check for diagonal win (top/left)
   col = action - min(action,endofline);
   row = endofline - min(action,endofline);
   col = col + (1:4);
   row = row + (1:4);
   while ((col(end) < 8) && (row(end) < 7))
     if all(colour == state(row+(col-1)*6))
       reward = colour;
       return;
     end
     row = [row(2:end) (row(end)+1)];
     col = [col(2:end) (col(end)+1)];
   end
% check for diagonal win (bottom/left)
   col = action - min(action,6-endofline+1);
   row = endofline + min(action,6-endofline+1);
   col = col + (1:4);
   row = row - (1:4);
   while ((col(end) < 8) && (row(end) > 0))
     if all(colour == state(row+(col-1)*6))
       reward = colour;
       return;
     end
     row = [row(2:end) (row(end)-1)];
     col = [col(2:end) (col(end)+1)];
   end
   
 % check for a draw:
  if all(state(1,:)) 
    reward = 0; 
  end