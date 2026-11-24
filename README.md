# Lab5 – Środowisko CI/CD z Jenkinsem

Aplikacja: prosty kalkulator REST API (Python, Flask) – `/`, `/health`, `/api/<add|subtract|multiply|divide>?a=..&b=..`.

## Środowisko CI/CD (folder `jenkins/`)
| Usługa | Opis | Adres |
|---|---|---|
| Jenkins | konfiguracja jako kod (JCasC + Job DSL), Docker CLI, Python | http://localhost:8080 |
| MailHog | serwer SMTP do testów – powiadomienia e-mail z pipeline | http://localhost:8025 |
| smee-client | przekazuje webhooki z GitHuba do lokalnego Jenkinsa | – |

Uruchomienie:
```
cd jenkins
copy .env.example .env   (uzupełnić SMEE_URL)
docker compose up -d --build
```

## Zadania w Jenkinsie
- **lab5-pipeline** (typ Pipeline) – gałąź `main`, Jenkinsfile z repozytorium,
- **lab5-multibranch** (Multibranch Pipeline) – gałęzie `feature/*`, `develop`, `release/*`.

Oba zadania uruchamiają się automatycznie po pushu (webhook GitHub → smee.io → `/git/notifyCommit`).

## Etapy pipeline (Jenkinsfile)
1. Checkout – pobranie kodu z repozytorium,
2. Lint – analiza statyczna (flake8),
3. Testy jednostkowe – pytest + raport JUnit,
4. Build – obraz Docker,
5. Deploy: test – kontener `lab5-test` (port 8081) dla `develop`, `release/*`, `main`,
6. Akceptacja – ręczne zatwierdzenie wdrożenia na produkcję (tylko `main`),
7. Deploy: produkcja – kontener `lab5-prod` (port 8082),
8. Powiadomienie e-mail o statusie (MailHog).

## Strategia gałęzi
`feature/*` → `develop` → `release/x.y.z` → `main`
- feature: lint, testy, build,
- develop / release: + wdrożenie na środowisko testowe,
- main: + wdrożenie na produkcję po ręcznej akceptacji.
