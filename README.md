# Ombyggnad av program: orderrapporter

När ett python-program har all sin funktionalitet i samma .py fil finns nackdelar i felsökning, kodförändring och tester. Med målet bättre robusthet görs programet om till en modulär struktur.

## Nya strukturen
Genom att isärhålla konfigurering och beräkningskod samt skapa en source-mapp (bibliotek) kan vi läsa in och testa bitar av programmet.

**1. Mapp: src**

**1.1 mapp: orderreport**
* `__main__.py`: programkörning (main guard)
* `__init__.py`: publikt API framhäver main och dataklass ReportConfig
* `configure.py`: inställningar och relativ path genom dataclass
* `logger_config.py`: setup för loggern
* `filing.py`: läser och skriver filer
* `calculations.py`: dataintegritet (såsom format) och kalkyler

**2. mapp: data** plats för excelfil .csv.

**3. mapp: output** plats där programmets rapporter hamnar.

**4. mapp: tests** plats för pytest automatiserade filer.

**5. ``pyproject.toml``** namnger och version, och biblioteksberoenden.

## Projektets installering
Kommandot installeras i editable mode genom terminal med
* ``pip install -e .``

## Projektets körning
Aktivera programet i terminal med
* ``python -m order_report``.
CSV i data-mapp tas då till validering, kalkyler och output, medan logger och terminalmeddelanden sparas/visas (se ``order_report.log``).

## Pytest
Kör test med ``pytest``



## Reflektion
1. *Vilka var de viktigaste problemen i originalkoden?*

Bristen på robust struktur gjorde kod svår att ändra och felsöka, även ineffektivitet i att hela programet körs med importering och brist på relativ pathing.

2. *Vilka förändringar tycker du förbättrade programmet mest?*

Det går fortare att ändra kalkyl-funktioner i och med modulära approachen, och det blir mindre klutter av att ha en konfigurerad logger.

3. *Varför valde du den projektstruktur du använde?*

Source-mapp gör programmet tydligare i vart data, kalkyler, testning och resultat befinner sig.

4. *Var använde du OOP/dataclass och varför passade det där?* 

I ``configure.py`` passade dataklass då pathing hör till och ingångsdata ska vara åtkomlig genomut programet förändringslåst, i motverkan av fel.

5. *Vilka viktiga beteenden skyddar dina automatiska tester, och vilken nytta ger testerna om programmet förändras i framtiden?*

Det som skyddas är resultaten, och om tex. prestandan behövs bättras kan detta prövas medan resultaten ska bli desamma.

6. *Vad var svårast?*

Utmaningarna var i projektstrukturering. Att en funktion inte ska ha mer än ett syfte var tydligt, men konfigurering var centralt för samstämmigt program.

7. *Vad hade du velat förbättra ytterligare om du haft mer tid?*

Testning för edge-cases såsom orimliga negativa siffror och filformat försäkran.
