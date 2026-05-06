---
titre: 05 Terrain Mouvement
sujet: Règles de terrain et de mouvement : escalader, se laisser tomber, sauter. Types de terrain : Lourd, Léger, Accessible, Bloquant, Insignifiant, Exposé, Promontoire.
mots_cles: terrain, mouvement, escalader, tomber, sauter, lourd, léger, accessible, bloquant, insignifiant, exposé, promontoire, rempart, garde-corps
---

# TERRAIN ET MOUVEMENT  

Un agent ne peut pas se déplacer à travers le terrain. Il peut le contourner, l’escalader, se laisser tomber ou sauter depuis celui-ci.
*Un agent doit finir un mouvement à un endroit où il peut être placé. S’il n’y a pas d’endroit où il peut être placé à la fin de son mouvement, celui-ci est impossible.*

## ESCALADER

Un agent doit être à 1” horizontalement et à 3” verticalement d’un terrain qu’il voit pour l’escalader. Escalader compte pour un minimum de 2” verticalement (par exemple, une distance de 1” compte pour 2”).

## SE LAISSER TOMBER

Un agent peut se laisser tomber quand il sort d’un terrain ou après avoir sauté. Ignorez 2” de la distance verticale sur laquelle l’agent se laisse tomber à chaque action. Si un agent se laisse tomber plusieurs fois pendant une action, seul un total de 2” est ignoré.

## SAUTER

Un agent peut sauter d’un terrain de type Promontoire et plus haut de 2” que le sol de la killzone quand il le quitte. Il peut parcourir jusqu’à 4” horizontalement à partir du bord d’où il saute, comme un mouvement normal, mais en une seule ligne droite. L’agent doit ensuite se laisser tomber ou escalader depuis le point qu’il atteint. Quand il saute depuis un élément de terrain, s’il y a un rempart sur le bord d’où l’agent saute, il doit d’abord l’escalader, mais saute tout de même depuis le niveau du terrain de type Promontoire. Quand il saute vers un élément de terrain, vous pouvez ignorer une différence de hauteur de 1” ou moins, y compris un rempart le cas échéant.
*Sauter signifie qu’un agent peut négocier des vides jusqu’à 4” de large, et qu’il peut sauter de jusqu’à 4” par-dessus des obstacles situés plus bas que lui.*
> Ci-contre, l’agent escalade de 4” jusqu'à ce qu’il dépasse le point le plus haut du mur.
> Il se déplace ensuite de 2” jusqu’à ce que son socle passe totalement le garde-corps, puis se laisse tomber pour 0” (car cette chute fait moins de 2”).
*Souvenez-vous qu’un segment de droite est toujours arrondi au supérieur, donc si un agent se déplace de 3,5”, cela compte comme 4”.*

> L’agent se déplace de 2” jusqu'à ce qu’il dépasse totalement le bord, puis se laisse tomber de 2” (la distance de chute réelle est 4”, mais il peut ignorer 2”).
> L’agent pourrait aussi sauter à partir de l’élément de terrain, et se déplacerait alors de 4” à partir du bord avant de se laisser tomber.
> L’agent se déplace verticalement de 2” (en réalité une distance de 1”, mais qui compte pour 2” car il s’agit du minimum) jusqu’à ce qu’il soit au-dessus du point le plus haut qu’il doit escalader. Il se déplace ensuite de 3”, jusqu’à ce que son socle dépasse totalement l’élément de terrain, puis se laisse tomber de 0” (car cette chute fait moins de 2”).
