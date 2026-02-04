# Problemes de seguretat del requirements.txt actual
En revisar el fitxer "requirements.txt" s'observen diversos problemes relacionats amb la seguretat i la reproduïbilitat:
1. Absència de versionat estricte
2. Absència de hashing

## Absència de versionat estricte
Algunes dependències no especifiquen estrictament la versió. Això implica que:
- Es pot instal·lar qualsevol versió parx futura, incloses verisons:
    - No provades
    - Incompatibles 
    - Amb vulnerabilitats noves
- El mateix projecte pot funcionar de manera diferent segons el dia o l'entorn.

Aquest problema té el risc de que les build no siguin reproduïbles i que s'introdueixin vulnerabilitats involuntàriament.

## Absència de hashing
Sense hashes:
- No es verifica que el paquet descarregat sigui exactament el que s'esperava.
- És vulnerable a:
    - supply-chain attacks
    - paquets manipulats
    - mirrors compromesos

# Versió millorada
Per generar la versió millorada de l'arxiu s'ha aplicat la següent estratègia:
- Especificat de verisons estricte de tots els requeriments 
- Generació de signatures hash
- Preparació del fitxer per:
    - CI/CD
    - Producció
    - Escaneig de vulnerabilitats

# Procediment recomanat en producció
El fluxe de producció que faria jo és:
1. Monitoritzar alertes
2. Actualitzar requirements.in
3. Regenerar requirements.txt
4. Executar:
    - tests
    - escaneig de vulnerabilitats
5. Merge controlat
6. Deploy

Aquest fluxe el realitzaria mensualment o immediatament en haver CVEs crítiques.

# Escenaris que es prevenen
Amb el nou fitxers es prevenen:
- Atacs de supply chain
- Paquets manipulats
- Diferències entre entorns
- Trencaments inesperats en producció
- Dependències transitives insegures