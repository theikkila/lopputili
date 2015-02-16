# Lopputili - kirjanpitosovellus

Sovelluksen avulla voidaan pitää pienen yrityksen tai yhdistyksen kirjanpitoa ja luoda laskuja asiakkaille.


Sovellus käyttää Flask-mikroframeworkkiä ja on ohjelmoitu käyttäen Python-kieltä.  

Sovellus rakennetaan Heroku-arkkitehtuurin mukaisesti, mutta varsinainen deploy suoritetaan dokku-ympäristöön omalle viski.me-palvelimelle.

Käyttäjän selaimen on tuettava HTML5-merkkauskieltä ja Javascriptiä.

Sovellus käyttää tietokantanaan *PostgreSQL*-tietokantaa ja kehittäessä kantana on *SQLite*.

Sovellusta varten on itse kirjoitettu ORM käyttäen hyväksi pythonin metaluokkia.

Sovellus on pystytetty [tänne](http://lopputili.viski.me/)
# Käyttö

Sovelluksen voi käynnistää komennolla `make run` jolloin tarvittavat riippuvuudet ladataan automaattisesti ja käynnistetään wsgi-palvelin.

Pelkät riippuvuudet voidaan asentaa komennolla `make install`

Dokumentaatio generoidaan komennolla `make docs` jonka jälkeen `doc/generated`-hakemistoon ilmestyy uusi pdf-muotoinen dokumentaatio.
## Käyttötapaukset

### Käyttäjäryhmät

#### Jokamies
Jokamiehellä tarkoitetaan ketä tahansa, joka internetin välityksellä tulee katsomaan sovellusta.

#### Käyttäjä
Käyttäjällä tarkoitetaan kirjanpitosovelluksen pääasiallisia käyttäjiä

![Käyttötapauskaavio](https://raw.githubusercontent.com/theikkila/lopputili/master/doc/usecase.jpg)


#### Käyttäjä
- Kirjaa menoja ja tuloja
- Tekee laskuja
- Seuraa laskujen maksamista
- Tulostaa raportteja laskuista
- Tulostaa raportteja kirjanpidosta

#### Jokamies
- Ei voi tehdä mitään.


### Käyttötapauskuvaukset

#### Kirjaa menot ja tulot
Käyttäjä voi lisätä ja poistaa kaksinkertaisen kirjanpidon mukaisesti tositteita eri tileiltä.

#### Tekee laskuja
Käyttäjä voi luoda laskuja ja tallentaa ne PDF-muotoisina.

#### Seuraa laskujen maksamista
Käyttäjä voi merkitä laskut maksetuiksi ja seurata vanhojen laskujen tietoja

#### Tulostaa raportteja
Käyttäjä voi tulostaa erilaisia raportteja laskuista ja tileistä. (esim. kuukauden alv:t, maksamattomat laskut, yms.)

# Käyttöliittymä

Käyttöliittymä on luonnosteltu HTML-kielellä lean-tyyliin.

![Käyttöliittymäkaavio](https://raw.githubusercontent.com/theikkila/lopputili/master/doc/guichart.png)
# Järjestelmän tietosisältö

## Käyttäjä (User)

| Attribuutti 	| Arvojoukko                                 	| Kuvaus                                	|
|-------------	|--------------------------------------------	|---------------------------------------	|
| first_name  	| Merkkijono, max 40 merkkiä, voi olla tyhjä 	| Käyttäjän etunimi                     	|
| last_name   	| Merkkijono, max 40 merkkiä, voi olla tyhjä 	| Käyttäjän sukunimi                    	|
| username    	| Merkkijono, max 100 merkkiä, pakollinen    	| Käyttäjän käyttäjätunnus              	|
| password    	| Merkkijono, max 100 merkkiä, pakollinen    	| Käyttäjän salasana bcrypt tiivisteenä 	|

## Asetukset (Setting)

Käyttäjän yhteisön asetukset

| Attribuutti  	| Arvojoukko                                  	| Kuvaus                          	|
|--------------	|---------------------------------------------	|---------------------------------	|
| owner        	| Avain, pakollinen                           	| Omistava käyttäjä               	|
| company_name 	| Merkkijono, max 140 merkkiä, voi olla tyhjä 	| Yhteisön nimi                   	|
| vat_code     	| Merkkijono, max 140 merkkiä, voi olla tyhjä 	| Yhteisön Y-tunnus               	|
| iban         	| Merkkijono, max 140 merkkiä, voi olla tyhjä 	| Yhteisön pankkitilin IBAN-koodi 	|
| bic          	| Merkkijono, max 140 merkkiä, voi olla tyhjä 	| Yhteisön pankkitilin BIC-koodi  	|


## Yhteystieto (Contact)

Käyttäjän asiakkaiden yhteystiedot

| Attribuutti 	| Arvojoukko                                  	| Kuvaus                        	|
|-------------	|---------------------------------------------	|-------------------------------	|
| owner       	| Avain, pakollinen                           	| Omistava käyttäjä             	|
| name        	| Merkkijono, max 400 merkkiä, pakollinen     	| Yhteystiedon nimi             	|
| address     	| Merkkijono, max 400 merkkiä, voi olla tyhjä 	| Yhteystiedon postiosoite      	|
| zip_code    	| Merkkijono, max 40 merkkiä, voi olla tyhjä  	| Yhteystiedon postinumero      	|
| city        	| Merkkijono, max 100 merkkiä, voi olla tyhjä 	| Yhteystiedon postitoimipaikka 	|
| email       	| Merkkijono, max 200 merkkiä, voi olla tyhjä 	| Yhteystiedon sähköpostiosoite 	|


## Tili (Account)

Käyttäjän kirjanpidon tilit

| Attribuutti 	| Arvojoukko                                  	| Kuvaus            	|
|-------------	|---------------------------------------------	|-------------------	|
| owner       	| Avain, pakollinen                           	| Omistava käyttäjä 	|
| name        	| Merkkijono, max 40 merkkiä, pakollinen      	| Tilin nimi        	|
| aid         	| Kokonaisluku                                	| Tilin koodi       	|
| description 	| Merkkijono, max 400 merkkiä, voi olla tyhjä 	| Tilin kuvaus      	|
| side        	| Merkkijono, max 13 merkkiä, pakollinen      	| Tilin puoli       	|


## Tosite (Receipt)

Kirjanpidon tosite

| Attribuutti 	| Arvojoukko                                  	| Kuvaus              	|
|-------------	|---------------------------------------------	|---------------------	|
| owner       	| Avain, pakollinen                           	| Omistava käyttäjä   	|
| commit_date 	| Aikaleima                                   	| Tositteen aikaleima 	|
| rid         	| Kokonaisluku                                	| Tositenumero        	|
| description 	| Merkkijono, max 400 merkkiä, voi olla tyhjä 	| Tositteen kuvaus    	|

## Tapahtuma (Commit)

Tositteeseen liittyvä tapahtuma

| Attribuutti   	| Arvojoukko        	| Kuvaus                            	|
|---------------	|-------------------	|-----------------------------------	|
| owner         	| Avain, pakollinen 	| Omistava käyttäjä                 	|
| receipt       	| Avain, pakollinen 	| Tosite                            	|
| account       	| Avain, pakollinen 	| Tapahtuman tili                   	|
| credit_amount 	| Kokonaisluku      	| Tapahtuman credit määrä sentteinä 	|
| debet_amount  	| Kokonaisluku      	| Tapahtuman debet määrä sentteinä  	|



# Relaatiotietokantakaavio


![Relaatiotietokantakaavio](https://raw.githubusercontent.com/theikkila/lopputili/master/doc/reldiag.png)# Järjestelmän yleisrakenne


Järjestelmä koostuu neljästä osasta. Kaikki tiedostot ovat kirjoitettu pienellä.

## ORM

Tätä projektia varten ohjelmoitu tietokanta-agnostinen SQL ORM sijaitsee `orm/`-hakemistossa.

## Mallit ja kontrollerit

Sovelluksen mallit ja kontrollerit sijaitsevat `app/`-hakemistossa ja sen alihakemistoissa `app/controllers/` ja `app/models

## Sovelluksen runko ja reititin

Sovelluksen runko ja reititykset ovat `lopputili.py`-tiedostossa päähakemistossa.

## Sovelluksen frontend

Sovelluksen Angular-frontend sijaitsee `static/app`-hakemistossa josta se palvellaan staattisina tiedostoina.

## Asetukset

Sovelluksen asetukset konfiguroidaan suurimmaksi osaksi ympäristömuuttujien avulla. Erillistä konfigurointitiedostoa ei ole, mutta osa käyttäjään vaikuttavista asetuksista tallennetaan tietokantaan.

# Asennus

Projektin asentaminen on helppoa esimerkiksi suoraan Herokuun tai heroku-yhteensopivaan järjestelmään (dokku). Asentaminen edellämainittuihin käy suorittamalla `git push <heroku>` kunhan palvelu on lisätty repoon remoteksi.

Tietokanta konfiguroidaan ympäristömuuttujaan `DATABASE_URL`. Tuetut kannat ovat PostgreSQL ja SQLite.

Toinen vaihtoehto on ajaa sovellus käyttäen Dockeria.

Buildaa Docker-image:

```bash
docker build -t lopputili .
```

Luo kontti:
```bash
docker run -d -t lopputili
```

Kolmas vaihtoehto on ajaa projektia "kehitystilassa"

```bash
make run
```

# PDF
PDF-muotoinen dokumentaatio ladattavissa [@ Github](https://github.com/theikkila/lopputili/blob/master/doc/generated/documentation.pdf?raw=true)
