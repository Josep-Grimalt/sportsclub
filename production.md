# Desplegament Segur en Producció amb Docker Compose

## Introducció
A continuació es presenten les respostes a les diferents qüesitons de les tasques, així com la justificació tècnica i de seguretat de les decisions preses durant tot el procés de desplegament en entorn de producció.

## Task 1
En primer lloc, pel que fa a l'enduriment del contenidor, la decisió principal va ser evitar l'execució de l'aplicació com a usuari root. Executar processos com a root dins d'un contenidor és una mala pràctica, ja que si un atacant compromet l'aplicació, podria obtenir privilegis elevats dins del contenidor. Per mitigar aquest risc, es va modificar el Dockerfile per crear un ususari específic no privilegiat (appuser) mitjançant la instrucció `RUN userdd`, es van ajustar els permisos del directori de treball amb `chown`, i finalment es va definir `USER appuser`. Aquesta decisió segueix el principi de mínim privilegi, reduint l'impacte potencial d'una intrusió.

## Task 2
En segon lloc, per a la configuració de producció, es va utilitzar el patró d'override de Docker Compose mitjançant un fitxer `docker-compose.production.yml`. Aquesta decisió permet mantenir intacte el fitxer original de desenvolupament, garantint separació clara entre entorns i evitant errors humans. En aquest fitxer només es van incloure les modificacions necessàries:
* Política de reinici automàtic `restart: unless-stopped`
* Eliminació de l'exposició de ports per a Django i PostgreSQL `ports:[]`
* Exposició explusiva del port 80 per a NGINX.
Aquesta configuració assegura que la base de dades i l'aplicació només siguin accessibles dins de la xarxa interna de Docker, minimitzant la superfície d'atac.

## Task 3
Pel que fa a la gestió de secrets, es va crear un fitxer `.env.production` que no es versiona al repositori i que està inclòs al `.gitignore`. Aquesta decisió evita la filtració accidental de claus secretes o credencials en GitHub. Els valors de `SECRET_KEY` i `POSTGRES_PASSWORD` es van generar aleatòriament mitjançant eines criptogràfiques segures, evitant contrasenyes febles o predeterminades. La tranferència del fitxer al servidor es faria mitjançant `scp` sobre SSH, garantint xifrat punt a punt. També es van restringir els permisos del fitxer amb `chmod 600`, limitant-ne l'accés únicament a l'usuari propietari. En aquest cas, per transferir el fitxer al servidor l'he generat de nou en lloc de pasar-lo.

## Task 4
En el desplegament, es va adoptar el model "pull". Atès que el servidor es troba sense accés des de GitHub, el desplegament s'ha d'iniciar des del propi servidor. Aquesta decisió és coherent amb entorns on els servidors no exposen serveis SSH a Internet. El procés consistí a clonar el repositori, crear el fitxer `.env.production`, i executar `docker compose` amb ambdós fitxers. Es van verificar tres aspectes clau:
* Accés correcte a l'aplicació
* Comprovació que `DEBUG=False`
* Confirmació que el port 5432 no és accessible des de l'exterior.
Aquestes proves validen que la configuració és segura i no exposa informacióo sensible.

## Task 5
Finalment, a la fase de construcció i publicació d'imatges, es va automatitzar la creació de l'artefacte mitjançant GitHub Actions. En lloc de construir la imatge en el servidor de producció, es va configurar un workflow que es dispara només quan el pipeline de tests finalitza amb èxit. Aquesta decisió garanteix que només es publiquin imatges que han superat les proves automatitzades. Es va utilitzar `docker/login-action` i `docker-build-push-action` amb credencials emmagatzemades com a secrets del respositori. Això evita exposar el token de Dcker Hub al codi. Posteriorment, es va modificar el fitxer de producció per sobreescriure `build: .` per `image: username/sportsclub:latest`, convertint el desplegament en un procés basat en imatges immutables. Aquesta pràctica assegura traçabilitat, reproductibilitat i coherència entre entorns.

## Conclusió
En conjunt, les decisions preses responen a principis de seguretat fonamentals: mínim privilegi, separació d'entorns, no exposició de secrets, aïllament de serveis, automatització controlada i ús d'artefactes immutables. El resultat final és una arquitectura molt més robusta que l'entorn inicial de desenvolupament, preparada per funcionar en producció amb garanties de seguretat i bones pràctiques.