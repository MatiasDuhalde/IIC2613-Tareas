% Dos celdas son vecinas si se encuentran adjacentes en el mapa. En otras palabras,
% son vecinas si los valores de sus coordenadas se diferencian en uno.
neigh(X,Y,Xp,Yp) :- cell(X,Y), cell(Xp,Yp), |Xp-X|+|Yp-Y|=1.


% Si para una celda se cumple safe(X,Y), entonces es seguro moverse a esta.
% En otras palabras, no hay posibilidad de que esta celda contenga un wumpus o un pozo (pit).
% Todas las celdas ya visitadas (alive) son safe
safe(X,Y) :- alive(X,Y), cell(X,Y).
% Las celdas donde hay un pozo o un wumpus no son safe
not safe(X,Y) :- wumpus(X,Y), cell(X,Y).
not safe(X,Y) :- pit(X,Y), cell(X,Y).
% Las celdas donde hay una celda vecina alive que no tiene ningún sense son safe
safe(X,Y) :- cell(X,Y), cell(A,B), neigh(X,Y,A,B), alive(A,B), not sense_stench(A,B), not sense_breeze(A,B).

% Lo de abajo debería ser disyuntivo !! !! !! !!

% Si una celda tiene la regla sense_breeze, entonces existe la posibilidad de que la celda adyacente
% tenga un pozo (pit).
pit(X,Y); safe(X,Y) :- cell(X,Y), cell(A,B), sense_breeze(A,B), neigh(X,Y,A,B), alive(A,B), not alive(X,Y), not wumpus(X,Y).

% Si una celda tiene la regla sense_stench, entonces existe la posibilidad de que la celda adyacente
% tenga un wumpus.
wumpus(X,Y); safe(X,Y) :- cell(X,Y), cell(A,B), sense_stench(A,B), neigh(X,Y,A,B), alive(A,B), not alive(X,Y), not pit(X,Y).

% Si una celda tiene otra celda adyacente que no tiene la regla sense_breeze, entonces es imposible
% que esta celda tenga un pozo.
not pit(X,Y) :- cell(X,Y), cell(A,B), not sense_breeze(A,B), neigh(X,Y,A,B), alive(A,B), not alive(X,Y), not wumpus(X,Y).

% Si una celda tiene otra celda adyacente que no tiene la regla sense_stench, entonces es imposible
% que esta celda tenga un wumpus.
not wumpus(X,Y) :- cell(X,Y), cell(A,B), not sense_stench(A,B), neigh(X,Y,A,B), alive(A,B), not alive(X,Y), not pit(X,Y).


% Una celda con la regla sense_breeze debe tener por lo menos una celda vecina que no es safe.
:- cell(X,Y), sense_breeze(X,Y), K = #count{A,B : cell(A,B), neigh(X,Y,A,B), not safe(A,B)}, K==0.
% Una celda con la regla sense_stench debe tener por lo menos una celda vecina que no es safe.
:- cell(X,Y), sense_stench(X,Y), K = #count{A,B : cell(A,B), neigh(X,Y,A,B), not safe(A,B)}, K==0.

#show pit/2.
#show wumpus/2.
#show safe/2.
#show sense_breeze/2.
#show sense_stench/2.
#show alive/2.
