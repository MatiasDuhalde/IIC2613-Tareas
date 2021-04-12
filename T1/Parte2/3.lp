% -----------------------
%         PARTE 2
% -----------------------

% Definición del grafo
calle(a,b).
calle(b,c).
calle(b,e).
calle(e,f).

% Se asume que los componentes de un arco siempre son nodos
esquina(X) :- calle(X,Y).
esquina(Y) :- calle(X,Y).

% El grafo es no dirigido
calle(X,Y) :- calle(Y,X).

% iluminado(X) -> nodo/esquina X está iluminado
iluminado(e).

% iluminada(X,Y) -> arco/calle X,Y está iluminada
iluminada(X,Y) :- iluminado(X), calle(X,Y).
iluminada(X,Y) :- iluminado(Y), calle(X,Y).

% Definición alternativa de camino, basada en la modificación propuesta en la pregunta 1,
% para revisar la cantidad de calles iluminadas entre dos puntos.
camino_ilum(X,Y,Largo,Ilum) :- calle(X,Y), Largo=1, iluminada(X,Y), Ilum=1.
camino_ilum(X,Y,Largo,Ilum) :- calle(X,Y), Largo=1, not iluminada(X,Y), Ilum=0.
camino_ilum(X,Y,Largo,Ilum) :- camino_ilum(X,Z,L1,I1), camino_ilum(Z,Y,L2,I2), Largo=L1+L2, Ilum=I1+I2, Largo <= #count{A,B : calle(A,B)}.

% conectado_k(X,Y,K) -> hay un camino entre X e Y, con exactamente K arcos no iluminados.
conectado_k(X,Y,K) :- camino_ilum(X,Y,L,I), K=L-I.

% -----------------------
%         PARTE 3
% -----------------------

% camino_minimo(X,Y,K) corresponde al camino entre las esquinas X,Y tal que K es la menor cantidad
% de calles no iluminadas entre ambos puntos
camino_minimo(X,Y,K) :- conectado_k(X,Y,_), K = #min{I : conectado_k(A,B,I), A==X, B==Y}.

#show iluminado/1.
#show iluminada/2.
#show camino_minimo/3.
