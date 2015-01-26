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
# PDF
PDF-muotoinen dokumentaatio ladattavissa [@ Github](https://github.com/theikkila/lopputili/blob/master/doc/generated/documentation.pdf?raw=true)
