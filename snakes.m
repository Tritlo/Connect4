clear
board = zeros(6,7)

for i=1:70
    x = ceil(rand(1)*5)+1
    y = ceil(rand(1)*4)+1
    ntup(i).snake(1,:) = [x y];
    ntup(i).n = 3; % P = 3 encoding annars 4
    ntup(i).m = 8;
    n = 1;
    while (n<8)
        if ~any(sum(ntup(i).snake == ones(n,1)*[x y],2)==2)
            n = n + 1;
            ntup(i).snake(n,:) = [x y];
        end
        while (1)
            dx = round(rand(1)*2)-1;
            dy = round(rand(1)*2)-1;
            if (((x + dx) >= 1) && ((x+dx)<=7) && ((y + dy) >= 1) && ((y+dy)<=6))
                break;
            end
        end
        x = x + dx;
        y = y + dy;
    end
end

% decoding function, "getfeatures"
%function phi = getfeatures(board,ntup)
N = 0;
for k=1:length(ntup)
    m = ntup(k).m;
    n =  ntup(k).n;
    shift = 0:(m^n):(k*m^n-1);
    triadic = m.^(0:(n-1));
    N = N + m.^n;
    s = zeros(n,1)
    for i=1:n
       x = ntup(k).snake(i,1);
       y = ntup(k).snake(i,2);
       s(i) = board(y,x);
       index(k) = shift(end) + triadic* s + 1;
    end
end
phi = sparse(1,N);
phi(index) = 1;
