%% Food Pairing facts

pairs(apple, walnut).
pairs(apple, honey).
pairs(apple, banana).
pairs(walnut, avocado).
pairs(walnut, banana).
pairs(banana, ginger).
pairs(banana, cloves).
pairs(banana, strawberry).
% pairs(banana, coriander).
pairs(strawberry, honey).
pairs(strawberry, ginger).
pairs(strawberry, tea).
pairs(tea, walnut).
pairs(tea, tomato).
pairs(tea, milk).

pairs(X,X).
pairs(_, coconut).

yummy_triple(X,Y,Z) :- pairs(X,Y),
                       X \== Y,
                       pairs(Y,Z),
                       Y \== Z,
                       pairs(X,Z),
                       X \== Z.
