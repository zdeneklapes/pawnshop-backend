# PAWNSHOP-SYSTEM

## INSTALLATION

### REQUIREMENTS

```
openssl@3
postgresql@14
```

### RUN

All commands are run from the __pawnshop-backend/__ directory.

#### Docker:

```shell
# To build the docker images and RUN the containers in the background
docker-compose -f docker-compose.yml up -d

# To stop pawnshop-backend containers:
docker stop $(docker ps -a | grep "pawnshop\|postgres" | awk "{print \$1}") # WARN: Could stop some other containers
```

#### Local:

```
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
./start.sh --clean-migrations       # Clean all migrations folders
./start.sh --loaddata               # Load data from fixtures
./start.sh --runserver              # Run server
```

### SWAGGER DOCUMENTATION

Could be found on this address after server starts locally:

```shell
http://localhost:8000/swagger/      # List of all endpoints and their usage(expected data, etc...)
```

---

## SYSTÉMOVÉ POŽADAVKY

### Stručný popis cíle práce, výstupů

systém musí umět uchovávat a pracovat s těmito daty:

- Zastavených produktech a produktech které již propadli (Zákazník se nedostavil v dohodnuté lhůtě)
- Produktech na prodej
- Zákaznících
- Obsluze
- Pobočkách

a vhodně je zobrazovat uživatelům systému.

Pro pochopení business logic uvádím pár jednoduchých příkladů:

__Příklad 1 (Zástava)__: Zákazník přijde do prodejny a chce zastavit něco (cokoli, např.: telefon), obsluha podle OP,
zadá do
systému info o zákazníkovi a zastavované věci, lhůta pro zaplacení dlužné částky je systémem automaticky nastavena do 4
týdnů, (zákazník do 4 týdnů vyplatí dlužnou částku plus sjednaný úrok (ten je počítán po týdnu)), pokud se blíží konec
lhůty, a zákazník má zájem zastavenou věc vyplatit později, muže zaplatit pouze úrok za uplynulé období (bez dlužné
částky) a lhůta je znova prodloužena o další 4 týdny.

__Příklad 2 (Prodej)__: Přijde zákazník na pobočku a chce si něco koupit. Obsluha zákazníkovi produkt prodá s tím, že v
systému
se musí produkt označit jako prodaný (to musí být vidět i v historii všech uskutečněných transakcí) a pokud to zakazník
vyžaduje, obsluha vystaví zákazníkovi účtenku.

__Příklad 3 (Nákup)__: Přijde zákazník na pobočku a chce něco prodat. Obsluha opět vyplní formulář podle OP zákazníka a
vyplní
popis a výkupní cenu prodávaného zboží. Údaje se uloží do systému a zákazník dostane peníze.

### Cílová skupina uživatelů:

Podnikatelé/Vlastníci maloobchodních poboček Zastaváren a Bazarů

### Popis uživatelských rolí:

__Obsluha:__

- obsluhuje zákazníky a na základě požadavků přidává data do systému (zastava, prodej)
- má k dispozici jen nezbytně nutné informace pro práci (přistup k zastaveným věcem, věcem na prodej a jejich cenám pro
  danou pobočku)
- spravuje zákazníky

__Admin:__

- má k dispozici stejné akce jako obsluha

_a navíc:_

- vidí statistiky, které obsluha nevídí (tržba, ...)
- vidí možné akce, které obsluha nevidí (editace předmětu smlouvy, ...)
- spravuje obsluhu

### Technologie, které budou použity pro implementaci:

__Backend:__ Python(Django)

__DB:__ PostgresSQL

__Frontend:__ NextJS, Tailwind, ...
