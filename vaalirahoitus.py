# Ladataan pandas-kirjasto aliaksella 'pd' sekä decimal-moduuli.
import pandas as pd
from decimal import Decimal

# Url-osoite, josta laskuissa käytettävä data haetaan.
url="https://gist.githubusercontent.com/rikukissa/0b76ef26b9977289f36fe4c3bbedd993/raw/41c86aadc1d6634bd2ae51bfb08c228fadba81d2/election-funding.csv"

# Luodaan pandasia hyödyntäen dataframe, johon säilötään csv-tiedostosta haettu tieto (erottimena ';').
dfCsv = pd.read_csv(url, sep=';')

# Kopioidaan csv-dataframesta vain laskelmiin tarvittavat sarakkeet väliaikaiseen dataframeen.
dfTemp = dfCsv[['Puolue', 'Vaalikampanjan kulut yhteensä']].copy()

# Korjataan laskettavasta datasta string-muodossa olevat luvut sopivaan muotoon (pilkut pisteiksi) ja muunnetaan ne float-tyyppisiksi.
dfTemp['Vaalikampanjan kulut yhteensä'] = dfTemp['Vaalikampanjan kulut yhteensä'].str.replace(",",".").astype(float)

# Luodaan uusi dataframe, johon lasketaan vaalirahoituskulujen keskiarvot puolueittain. Samalla myös karsitaan duplikaattirivit taulukosta.
dfMean = dfTemp.groupby(['Puolue']).mean()
# Nimetään sarake kuvaamaan sisältöä paremmin.
dfMean.rename(columns={'Vaalikampanjan kulut yhteensä':'Ehdokkaiden keskiarvo'}, inplace=True)

# Luodaan dataframe, johon lasketaan ehdokkaiden vaalirahoituskulut yhteensä puolueittain.
dfSum = dfTemp.groupby(['Puolue']).sum()
# Nimetään sarake kuvaamaan sisältöä paremmin.
dfSum.rename(columns={'Vaalikampanjan kulut yhteensä':'Puoluekohtainen vaalirahoitus'}, inplace=True)

# Luodaan myös dataframe, johon lasketaan ehdokkaiden määrät puolueittain ja nimetään tämä sarake.
dfCount = dfTemp.groupby(['Puolue']).count()
dfCount.rename(columns={'Vaalikampanjan kulut yhteensä':'Ehdokkaita'}, inplace=True)

# Funktio, joka pyöristää annetut arvot valuuttamuotoon kahden desimaalin tarkkuudella.
def floatToCurrency(value):
    return Decimal(value).quantize(Decimal('0.01'))

dfMean['Ehdokkaiden keskiarvo'] = dfMean['Ehdokkaiden keskiarvo'].map(floatToCurrency)
dfSum['Puoluekohtainen vaalirahoitus'] = dfSum['Puoluekohtainen vaalirahoitus'].map(floatToCurrency)

# Yhdistetään keskiarvon, vaalirahoituskulut sekä ehdokkaiden määrän sisältävät dataframet lopulliseksi dataframeksi.
dfTemp = dfSum.merge(dfMean, on='Puolue')
dfFinal = dfTemp.merge(dfCount, on='Puolue')

print(dfFinal)

# Tallennetaan käsitelty data csv-tiedostoon.
dfFinal.to_csv('vaalirahoitus.csv', sep=';', encoding="utf-8-sig")
