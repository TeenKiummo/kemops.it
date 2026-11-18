# KemOps ORBIT

Sito statico KemOps in HTML, CSS e JavaScript. L'esperienza ORBIT riprende il prototipo originale KemOps e i suoi loghi. Non richiede build, librerie JavaScript esterne o backend su GitHub Pages.

## Anteprima del branch

Il branch `feature/kemops-orbit-b2b` non modifica il sito pubblico. Il workflow `.github/workflows/preview.yml` verifica i file e pubblica un artefatto `kemops-orbit-preview` nella pagina Actions del run. Scarica e decomprimi l'artefatto, poi apri `index.html` nel browser. Per testare le pagine con un server locale, dalla cartella estratta esegui `python -m http.server 8000` e apri `http://localhost:8000/`.

La copia di lavoro può essere aperta direttamente in VS Code. Dalla root del progetto, `python scripts/check_site.py` verifica link locali, SEO essenziale e configurazione dei workflow. Il test visivo va fatto su desktop e smartphone prima del merge.

## Pubblicazione

Il workflow `.github/workflows/pages.yml` distribuisce solo i push a `main` su GitHub Pages. Il file `CNAME` rimane `kemops.it`. Il workflow di anteprima non usa `deploy-pages` e non modifica la configurazione Pages.

Il modulo contatti usa l'endpoint Formspree `https://formspree.io/f/meaaoydw`, già presente nel `main` alla creazione di questo branch. Prima del merge, verificare nell'account Formspree del titolare che il form sia attivo e che le richieste arrivino alla casella corretta; il codice da solo non può provarne la consegna. L'indirizzo email e il numero di telefono provengono dal sito esistente.

Prima di pubblicare le nuove pagine, completare e far rivedere i dati del titolare e il testo dell'informativa privacy esistenti. Non sono stati inventati case study, clienti, metriche o risultati garantiti; gli scenari dimostrativi sono indicati come tali.
