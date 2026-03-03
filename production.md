A continuació es presenten les respostes a les diferents qüesitons de les tasques, així com la justificació tècnica i de seguretat de les decisions preses durant tot el procés de desplegament en entorn de producció.

# Task 1
En primer lloc, pel que fa a l'enduriment del contenidor, la decisió principal va ser evitar l'execució de l'aplicació com a usuari root. Executar processos com a root dins d'un contenidor és una mala pràctica, ja que si un atacant compromet l'aplicació, podria obtenir privilegis elevats dins del contenidor. Per mitigar aquest risc, es va modificar el Dockerfile per crear un ususari específic no privilegiat (appuser) mitjançant la instrucció `RUN userdd`, es van ajustar els permisos del directori de treball amb `chown`, i finalment es va definir `USER appuser`. Aquesta decisió segueix el principi de mínim privilegi, reduint l'impacte potencial d'una intrusió.

# Task 2

# Task 3

# Task 4

# Task 5
