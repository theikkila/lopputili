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

