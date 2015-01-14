# Lopputili - kirjanpitosovellus

Sovellus käyttää Flask-mikroframeworkkiä ja on ohjelmoitu käyttäen Python-kieltä.  

Sovellus käyttää tietokantanaan *PostgreSQL*-tietokantaa ja kehittäessä kantana on *SQLite*.

Sovellus on pystytetty [tänne](http://lopputili.viski.me/)# Käyttö

Sovelluksen voi käynnistää komennolla `make run` jolloin tarvittavat riippuvuudet ladataan automaattisesti ja käynnistetään wsgi-palvelin.

Pelkät riippuvuudet voidaan asentaa komennolla `make install`

Dokumentaatio generoidaan komennolla `make docs` jonka jälkeen `doc/generated`-hakemistoon ilmestyy uusi pdf-muotoinen dokumentaatio.
# Käyttötapaukset


### Käyttäjä
- Kirjaa menoja ja tuloja
- Tekee laskuja
- Seuraa laskujen maksamista
- Tulostaa raportteja laskuista
- Tulostaa raportteja kirjanpidosta