
# Järjestelmän yleisrakenne


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

