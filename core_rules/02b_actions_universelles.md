---
titre: 02B Actions Universelles
sujet: Liste complète et détaillée de toutes les actions universelles disponibles pour tous les agents avec leur coût en PA : Repositionnement (1PA), Sprinter (1PA), Battre en retraite (2PA), Charger (1PA), Ramasser un marqueur (1PA), Placer un marqueur (1PA), Contre-attaquer (0PA), Tirer (1PA), Combattre (1PA), Garde (1PA).
mots_cles: repositionnement, sprinter, battre en retraite, charger, ramasser marqueur, placer marqueur, contre-attaquer, tirer, combattre, garde, PA, coût, action universelle, séquence tir, séquence combat, dés attaque, dés défense
---

# ACTIONS_UNIVERSELLES_DETAIL

## REPOSITIONNEMENT — 1 PA

- → Déplacez l’agent actif, sans dépasser sa caractéristique de Mouvement, jusqu’à un endroit où il peut être placé. Vous devez procéder à un ou plusieurs déplacements en segments de ligne droite, en arrondissant la longueur de chaque segment à l’entier supérieur le plus proche.
- → Il ne peut pas se déplacer à portée de contrôle d’un agent ennemi, sauf si au moins un agent ami est déjà à portée de contrôle de cet agent ennemi, auquel cas il peut se déplacer à portée de contrôle de cet agent ennemi, mais ne peut pas y terminer son mouvement.
- ⚠ Un agent ne peut pas faire cette action tant qu’il est à portée de contrôle d’un agent ennemi, ou pendant la même activation ou il à fait l’action Battre en retraite ou Charger.
*Se déplacer par segments de droite rend les choses plus précises et plus claires.*

## SPRINTER — 1 PA

- → Comme l’action Repositionnement, sauf que vous n’utilisez pas la caractéristique de Mouvement de l’agent, car à
la place, il peut se déplacer au maximum de 3”. De plus, il ne peut pas escalader pendant ce mouvement, mais il
peut se laisser tomber et sauter.
- ⚠ Un agent ne peut pas faire cette action tant qu’il est à portée de contrôle d’un agent ennemi, ou pendant la même
activation ou il à fait l’action Charger.
***Sprinter*** *permet de compléter une action ***Repositionnement*** pour se déplacer un peu plus loin.* 

## BATTRE EN RETRAITE — 2 PA

- → Comme l’action Repositionnement, sauf que l’agent actif peut se déplacer à portée de contrôle d’un agent ennemi, mais ne peut pas y terminer son mouvement.
- ⚠ Un agent ne peut pas faire cette action sauf si un agent ennemi est dans sa portée de contrôle. Il ne peut pas faire cette action pendant la même activation ou il à fait l’action **Repositionnement** ou **Charger**.
*Si un agent est activé à portée de contrôle d’un agent ennemi, ***Battre en retraite*** est une façon de se replier.*

## CHARGER - 1PA

- → Comme l’action Repositionnement, sauf que l’agent actif peut se déplacer de 2” supplémentaires. Il peut se déplacer, et doit finir son déplacement, à portée de contrôle d’un agent ennemi. S’il se déplace à portée de contrôle d’un agent ennemi qui n’est pas dans la portée de contrôle d’aucun autre agent ennemi, il ne peut pas quitter la portée de contrôle de cet agent ennemi.
- ⚠ Un agent ne peut pas faire cette action tant qu’il à un ordre de Dissimulation. s’il est déjà à portée de contrôle d’un agent ennemi, ou pendant la même activation ou il à fait l’action **Repositionnement**, **Sprinter** ou **Battre en retraite**.
*L’action ***Charger*** permet à un agent d’engager un ennemi, mais pour ce faire, il faut un ordre d’Engagement.*

## RAMASSER UN MARQUEUR — 1 PA

- → Retirez un marqueur que l’agent actif contrôle et qui peut être la cible de l’action **Ramasser un Marqueur**. Désormais, cet agent porte, conteste et contrôle le marqueur.
- ⚠ Un agent ne peut pas faire cette action tant qu’il est à portée de contrôle d’un agent ennemi, ou s’il porte déjà un marqueur.
*S’il existe des marqueurs pouvant être la cible de l’action ***Ramasser un marqueur***, cela sera précisé.*

## PLACER UN MARQUEUR — 1 PA

- → Placez à portée de contrôle de l’agent actif un marqueur qu’il portait. Si un agent portant un marqueur est neutralisé, il doit faire cette action pour 0PA avant d’être retiré de la killzone. Cela l’emporte sur les règles qui l’en empêcherait.
- ⚠ Un agent ne peut pas faire cette action pendant la même activation où il a fait l’action **Ramasser un marqueur** (sauf s’il est neutralisé).
*Comme ci-dessus, si l’agent porte un ou des marqueurs, cela sera indiqué.*

## CONTRE-ATTAQUER — 0 PA

Quand vous devriez activer un agent préparé, si la totalité de vos agents sont indisponibles alors que votre adversaire à toujours des agents préparés, vous pouvez choisir un de vos agents indisponibles avec l’ordre d’Engagement pour effectuer une action à 1PA (sauf **Garde**) gratuitement. Chaque agent ne peut contre-attaquer qu’une fois par tournant, et ne peut pas se déplacer de plus de 2” (ou être retiré et replacé à plus de 2”) en contre-attaquant (cela l’emporte sur toutes les autres règles). Contre-attaquer est optionnel. Quel que soit votre choix, c’est ensuite à l’adversaire d’activer un agent.
*Contre-attaquer n’est pas une activation, cela remplace une activation, ce qui signifie que les restrictions qui concernent les actions ne s’appliquent donc pas.*

## TIRER - 1 PA

- → Tirez avec l’agent actif en suivant la séquence ci-dessous. Le joueur de l’agent actif est l’attaquant. Le joueur de l’agent ennemi choisi est le défenseur.
- ⚠ Un agent ne peut pas faire cette action tant qu’il à un ordre de Dissimulation, ou tant qu’il est à portée de contrôle d’un agent ennemi.

1. **Choisir une arme** : L’attaquant choisit une arme de tir de son agent et prend ses dés d’attaque, c.à.d autant de D6 que la caractéristique d’Attaques (A) de l’arme.
2. **Choisir une cible éligible** :
    - L’attaquant choisit un agent ennemi éligible et n’ayant aucun agent ami à portée de contrôle.
    - Si la cible désignée a un ordre d’Engagement, elle est éligible si elle est visible de l’agent actif.
    - Si la cible désignée a un ordre de Dissimulation, elle est éligible si elle est visible de l’agent actif et si elle n’est pas à couvert.
    - Un agent est visible si l’agent actif le voit. Un agent est à couvert s’il y a un terrain interposé dans sa portée de contrôle. Il ne peut pas être à couvert tant qu’il est à 2” de l’agent actif.
    - Un agent ne peut pas être à couvert et masqué par le même élément de terrain. Si c’est le cas, le défenseur choisit (à couvert ou masqué) pour cette séquence quand son agent est choisi comme cible éligible.
*Dans de rares cas, vous serez à la fois l’attaquant et le défenseur, comme lorsqu’on tire sur un agent ami à cause de la règle d’arme Déflagration. Dans ce cas, vous jetez vos propres dés d’attaque et de défense.*
3. **Jeter les Dés d’Attaque** : L’attaquant jette ses dés. Chaque résultat supérieur ou égal à sa caractéristique de Touche de l’arme est un réussite, conservez le dé. Tout autre résultat est un échec, défaussez le dé. Chaque résultat de 6 est toujours une réussite critique. Chaque autre réussite est une réussite normale. Chaque résultat de 1 est toujours un échec. Un agent est masqué s’il y a du **Terrain Lourd interposé**. Cependant, il ne peut pas être masqué par du terrain lourd interposé à 1” de lui ou de l’autre agent. Si l’agent ciblé est masqué :
    - L’attaquant doit défausser une réussite de son choix au lieu de la conserver.
    - Toutes les réussites critiques de l’attaquant compte comme des réussites normales et ne peuvent pas être changées en réussites critiques (cela l’emporte sur toutes les autres règles).
*Un agent est masqué s’il y a de gros objets qui gênent la ligne de tir. On ignorera cette règle quand les agents sont proches de tels objets, on imagine qu’ils se penchent au coin d’un bâtiment ou regardent par une fenêtre.*
4. **Jeter les Dés de Défense** : Le défenseur prend trois dés de défense. Si l’agent ciblé est à couvert, il peut conserver une réussite normale sans jeter un des dés, cela s’appelle une **sauvegarde de couvert**. Les autres dés sont jetés normalement.
*Ce sont les agents avec un ordre d’Engagement qui sont à couvert, car un ordre de Dissimulation permet de ne pas être une cible éligible.*
5. **Résoudre les Dés de Défense** : Le défenseur alloue ses dés de défense réussis afin de bloquer des dés d’attaque réussis.
    - Une réussite normale peut bloquer une réussite normale.
    - Deux réussites normales peuvent bloquer une réussite critique.
    - Une réussite critique peut bloquer une réussite normale ou une réussite critique.
6. **Résoudre les Dés d’attaque** : Les dés réussis qui ne sont pas bloqués infligent des dégâts à l'agent ciblé.
    - Une réussite normale inflige les Dégâts Normaux de l’arme.
    - Une réussite critique inflige les Dégâts Critiques de l’arme.
    - Tout agent qui est neutralisé est retiré une fois que l’agent actif a terminé l’entièreté de son action.
*Certaines armes tirent plusieurs fois par action, comme celle avec les règles Déflagration ou Torrent. Par conséquent, les agents ne sont pas retirés avant que l’action entière ait été accomplie.*

## COMBATTRE - 1 PA

- → Faites combattre l’agent actif en suivant la séquence ci-dessous. Le joueur de l’agent actif est l’attaquant. Le joueur de l’agent ennemi est le défenseur.
- ⚠ Un agent ne peut pas faire cette action sauf si un agent ennemi est dans sa portée de contrôle.

*Contrairement au tir, le combat est à double sens. Choisissez avec soin l’adversaire que vous affrontez, car il pourra riposter.*

1. **Choisir un Agent Ennemi** : L’attaquant choisit un agent ennemi à portée de contrôle de l’agent actif afin de le combattre. Cet agent ennemi pourra riposter lors de cette action.
*La différence entre un agent qui combat et un agent qui riposte est importante. L'agent qui combat est l'agent actif, tandis que l'agent qui riposte est l'agent ennemi choisi.*
2. **Choisir des Armes** : Chaque joueur choisit une arme de mêlée de son agent et prend ses dés d’attaque, c.à.d autant de D6 que la caractéristique d’Attaques (A) de l’arme.
*Si une règle dit qu’un agent ne peut pas riposter, il peut quand même être combattu, mais lui-même ne peut alors pas prendre des dés d’attaque et les résoudre.*
3. **Jeter les Dés d’attaque** : Les deux joueurs jettent leurs dés d’attaque simultanément. Chaque résultat supérieur ou égal à la caractéristique de Touche de l’arme choisie est une réussite : conserver le dé. Tout autre résultat est un échec : défaussez-le. Chaque résultat de 6 est toujours une réussite critique. Chaque autre réussite est une réussite normale. Chaque résultat de 1 est toujours un échec.
Tant qu’un agent ami est assisté par d’autres agents amis, améliorez de 1 la caractéristique de Touche de ses armes de mêlée pour chaque agent ami qui l’assiste. Pour assister en combat, un agent doit être à portée de contrôle de l’agent ennemi impliqué dans le combat, sans être à portée de contrôle d’un autre agent ennemi.
*Avoir plusieurs agents amis à portée de contrôle d'un agent ennemi ne leur permet pas de se battre tous en même temps, mais cela facilite les réussites des dés d'attaque.*
4. **Résoudre les Dés d’Attaque** : En commençant par l’attaquant, les joueurs résolvent tour à tour un de leurs dés d’attaque réussi et n’ayant pas été bloqué, jusqu’à ce que l’un deux ait résolu tous ses dés (auquel cas l’adversaire résout tous ses dés restants), ou jusqu’à ce qu’un agent impliqué soit neutralisé. Quand un joueur résout un dé, il doit l’utiliser pour frapper ou bloquer.
S’il frappe, infligez les dégâts à l’agent ennemi, puis défaussez le dé.
- Une réussite normale inflige les Dégâts Normaux de l’arme.
- Une réussite critique inflige les Dégâts Critiques de l’arme.
*Bloquer n’empêche pas une frappe qui s’est déjà produite, mais permet d’annuler une réussite qui n’a pas encore été résolue. La première frappe de l’attaquant permet d’assurer une certaine quantité de dégâts.*
S’il bloque, il peut allouer un dé pour bloquer une des réussites **non résolues** de l’adversaire.
- Une réussite normale peut bloquer une réussite normale.
- Une réussite critique peut bloquer une réussite normale ou une réussite critique.
*Vous pouvez choisir de bloquer même si votre adversaire n’a plus de réussite non résolue. Cela peut être pratique si vous ne voulez pas le neutraliser tout de suite.*
