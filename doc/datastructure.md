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



