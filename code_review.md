# Kodgenomgång
Från en överblandad .py fil till bättre separerat projekt, görs ändringar som följer.

## Utspridning av kod

1. Observation - Filhantering, felmeddelanden, databearbetning och läsning finns på samma ställe.
2. Konsekvens - Det är svårt att ändra eller pröva koden.
3. Förslag - Sprid ut funktioner som hör ihop gruppvis.

## Körning

1. Observation - Vid filens start eller inhämtning körs helheten.
2. Konsekvens - När koden inte importeras del för del låter detta en inte testa delar av koden.
3. Förslag - gör en tydligare `main()`.  

## Föredra logging över print

1. Observation - Använd hierarkierna med logging.
2. Konsekvens - Vanlig programdrift, debugging och loggfiler blir överpopulerade.
3. Förslag - Låt logger spara info som är mer relevant i respektive aktivitet.

## Förenkla nästlad kod

1. Observation - Koden sammanfattar kategorier och regioner nästlat.
2. Konsekvens - Metoderna är komplicerade att göra enkla ändringar till.
3. Förslag - Dedikera istället funktioner som stegvis utför metodiken.

## Bättre felrapporter

1. Observation - Terminal eller notebook svarar "Fel data".
2. Konsekvens - Felen blir det otydliga för att korrigera.
3. Förslag - Vi inkluderar mer specifika felmeddelanden samt feltyp.

## Relativ path

1. Observation - `main()` behövs ändras ifall projektet ska testas från andra mappar.
2. Konsekvens - Inställningsändringar är för centralt placerade.
3. Förslag - Det är bättre låta `config` hantera settings och path.