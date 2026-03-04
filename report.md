# Desplegament Segur en Producció amb Docker Compose

## Respostes i justificacions

### Enduriment del Contenidor
En primer lloc, pel que fa a l'enduriment del contenidor, la necessitat principal va ser evitar l'execució de l'aplicació com a usuari root. Executar processos com a root dins d'un contenidor és una mala pràctica, ja que si un atacant compromet l'aplicació, podria obtenir privilegis elevats dins del contenidor. Per mitigar aquest risc, es va modificar el Dockerfile per crear un ususari específic no privilegiat (appuser) mitjançant la instrucció `RUN userdd`, es van ajustar la propietat del directori de treball amb `chown`, i finalment es va canviar l'usuari de l'aplicació al no privilegiat amb `USER appuser`. Aquesta decisió segueix el principi de mínim privilegi, reduint l'impacte potencial d'una intrusió.

### Configuració de Producció
En segon lloc, per a la configuració de producció, es va utilitzar el patró d'override de Docker Compose mitjançant un fitxer `docker-compose.production.yml`. Aquesta decisió permet mantenir intacte el fitxer original de desenvolupament, garantint separació clara entre entorns i evitant errors humans. En aquest fitxer només es van incloure les modificacions necessàries:
* Política de reinici automàtic `restart: unless-stopped`
* Eliminació de l'exposició de ports per a Django i PostgreSQL `ports:[]`
* Exposició exclusiva del port 80 per a NGINX.
Aquesta configuració assegura que la base de dades i l'aplicació només siguin accessibles dins de la xarxa interna de Docker, minimitzant la superfície d'atac.

### Gestió de Secrets
Pel que fa a la gestió de secrets, es va crear un fitxer `.env.production` que no es versiona al repositori i que està inclòs al `.gitignore`. Aquesta decisió evita la filtració accidental de claus secretes o credencials en GitHub. Els valors de `SECRET_KEY` i `POSTGRES_PASSWORD` es van generar aleatòriament mitjançant eines criptogràfiques segures, evitant contrasenyes febles o predeterminades. La tranferència del fitxer al servidor es faria mitjançant `scp` sobre SSH, garantint xifrat punt a punt. També es van restringir els permisos del fitxer amb `chmod 600`, limitant-ne l'accés únicament a l'usuari propietari. En aquest cas, per transferir el fitxer al servidor l'he generat de nou en lloc de pasar-lo.

### Desplegament i verificació
En el desplegament, es va adoptar el model "pull". Atès que el servidor es troba sense accés des de GitHub, el desplegament s'ha d'iniciar des del propi servidor. Aquesta decisió és coherent amb entorns on els servidors no exposen serveis SSH a Internet. El procés consistí a clonar el repositori, crear el fitxer `.env.production`, i executar `docker compose` amb ambdós fitxers. Es van verificar tres aspectes clau:
* Accés correcte a l'aplicació
* Comprovació que `DEBUG=False`
* Confirmació que el port 5432 no és accessible des de l'exterior.
Aquestes proves validen que la configuració és segura i no exposa informació sensible.

### Construcció i Publicació
Finalment, a la fase de construcció i publicació d'imatges, es va automatitzar la creació de l'artefacte mitjançant GitHub Actions. En lloc de construir la imatge en el servidor de producció, es va configurar un workflow que es dispara només quan el pipeline de tests finalitza amb èxit. Aquesta decisió garanteix que només es publiquin imatges que han superat les proves automatitzades. Es va utilitzar `docker/login-action` i `docker-build-push-action` amb credencials emmagatzemades com a secrets del respositori. Això evita exposar el token de Docker Hub al codi. Posteriorment, es va modificar el fitxer de producció per sobreescriure `build: .` per `image: username/sportsclub:latest`, convertint el desplegament en un procés basat en imatges immutables. Aquesta pràctica assegura traçabilitat, reproductibilitat i coherència entre entorns.

## Transferència Segura
Per transferir l'arxiu `.env.production` de forma segura he emprat un canal encriptat basat en SSH, concretament l'eina `scp`(Secure Copy Protocol). Aquesta eina permet copiar fitxers entre màquines a través d'una connexió SSH xifrada, garantint la confidencialitat i integritat de les dades durant la transmissió.

Primer, he generat el fitxer localment, assegurant-me d'incloïr-lo al `.gitignore` per evitar que s'hagi pujat accidentalment al repositori. Aquest fitxer conté valors sensibles com claus secretes i credencials d'accés que no s'han de versionar mai.

Un cop preparat, he executat la comanda:
```bash
scp .env.production user@IP_SERVER:/route
```
Aquesta operació transfereix el fitxer directament al directori de desplegament del servidor. A més, els permisos del fitxer han estat restingits amb:
```bash
chmod 600 .env.production
```
D'aquesta manera, només l'usuari propietari podrà llegir-lo. Aquest mètode és segur perquè evita l'exposició de secrets en repositoris, correus electrònics o canals no xifrats, i s'ajusta a bones pràctiques de gestió de secrets en entorns de producció.
