# PAWNSHOP-BACKEND
## AUTHORS:
* Zdeněk Lapeš <lapes.zdenek@gmail.com> (xlapes02)
* Andrej Bínovský <binovsky.andrej@gmail.com> (xbinov00)
* Richard Buban <sisoriso777@gmail.com> (xbuban00)

---

## SYSTEM REQUIREMENTS:

---

### Stručný popis cíle práce, výstupů:
systém musí umět uchovávat a pracovat s těmito daty:

- Zastavených produktech a produktech které již propadli (Zákazník se nedostavil v dohodnuté lhůtě)
- Produktech na prodej
- Zákaznících
- Obsluze
- Pobočkách

a vhodně je zobrazovat uživatelům systému.

Pro pochopení business logic uvádím pár jednoduchých příkladů:

__Příklad 1__: Zákazník přijde do prodejny a chce zastavit něco (cokoli, např.: telefon), obsluha podle OP, zadá do systému info o zákazníkovi a zastavované věci, lhůta pro zaplacení dlužné částky je systémem automaticky nastavena do 4 týdnů, (zákazník do 4 týdnů vyplatí dlužnou částku plus sjednaný úrok (ten je počítán po týdnu)), pokud se blíží konec lhůty, a zákazník má zájem zastavenou věc vyplatit později, muže zaplatit pouze úrok za uplynulé období (bez dlužné částky) a lhůta je znova prodloužena o další 4 týdny.

__Příklad 2__: Přijde zákazník na pobočku a chce si něco koupit. Obsluha zákazníkovi produkt prodá s tím, že v systému se musí produkt označit jako prodaný (to musí být vidět i v historii všech uskutečněných transakcí) a pokud to zakazník vyžaduje, obsluha vystaví zákazníkovi účtenku.

__Příklad 3__: Přijde zákazník na pobočku a chce něco prodat. Obsluha opět vyplní formulář podle OP zákazníka a vyplní popis a výkupní cenu prodávaného zboží. Údaje se uloží do systému a zákazník dostane peníze.

### Cílová skupina uživatelů:
Podnikatelé/Vlastníci maloobchodních poboček Zastaváren a Bazarů

### Popis uživatelských rolí:
__Obsluha:__

- obsluhuje zákazníky a na základě požadavků přidává data do systému (zastava, prodej)
- má k dispozici jen nezbytně nutné informace pro práci (přistup k zastaveným věcem, věcem na prodej a jejich cenám pro danou pobočku)
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
