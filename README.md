# local-llm-stack

Tento repozitář obsahuje kompletní Docker Compose konfiguraci pro nasazení lokálního jazykového modelu (LLM) s využitím GPU, webového rozhraní a dalších podpůrných služeb. Cílem je **jednoduché a přenositelné** řešení, které lze rychle zprovoznit v lokálním či cloudovém Home Labu.

---

## Obsah

1. [Přehled kontejnerů](#přehled-kontejnerů)
2. [Požadavky](#požadavky)
3. [Instalace a nastavení](#instalace-a-nastavení)
   - [Struktura projektu](#struktura-projektu)
   - [Environment proměnné](#environment-proměnné)
4. [Spuštění projektu](#spuštění-projektu)
5. [Nastavení SSL](#nastavení-ssl)
6. [Tipy k provozu a zabezpečení](#tipy-k-provozu-a-zabezpečení)
7. [Časté dotazy (FAQ)](#časté-dotazy-faq)
8. [Přispěvatelé](#přispěvatelé)
9. [Licence](#licence)
10. [Shrnutí a odkazy](#shrnutí-a-odkazy)

---

## Přehled kontejnerů

V rámci `docker-compose.yml` se spouští následující služby:

- **openwebui**: Poskytuje webové rozhraní (Open WebUI) pro ovládání a správu lokálního LLM.
- **nginx**: Reverzní proxy s možností nasazení SSL certifikátů.
- **watchtower**: Automatická kontrola a aktualizace Docker kontejnerů.
- **tika**: Služba pro extrahování textu z různých typů dokumentů (např. PDF, DOC).
- **backend**: Vlastní aplikační logika (např. zpracování nahraných souborů, API pro komunikaci s LLM).

> **Poznámka**: Pro správné fungování je potřeba mít na hostitelském stroji nainstalovanou [Ollamu](https://github.com/ollama/ollama/blob/main/docs/linux.md). Ollama není kontejnerizovaná v tomto stacku a přistupuje k GPU přímo z hosta.

---

## Požadavky

- **Nainstalovaný Docker** a **Docker Compose** (doporučena verze `docker compose v2`).
- **NVIDIA GPU** a ovladače + knihovna [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html), pokud chcete používat GPU akceleraci.
- **Ollama** nainstalovaná na hostu dle oficiální dokumentace ([návod pro Linux](https://github.com/ollama/ollama/blob/main/docs/linux.md)).
- Linuxové prostředí (Ubuntu, Debian, CentOS apod.) nebo WSL2 na Windows (také možné nasadit na macOS, ale GPU akcelerace bývá limitovaná).

---

## Instalace a nastavení

1. **Naklonujte repozitář** do lokálního prostředí:
   ```bash
   git clone https://github.com/ZiMi-lab/local-llm-stack.git
   cd local-llm-stack
   ```

2. **Nainstalujte Ollamu**
   - Pokud jste Ollamu ještě neinstalovali, řiďte se oficiálním návodem zde:
     [Ollama Linux Installation Guide](https://github.com/ollama/ollama/blob/main/docs/linux.md)
   - Ujistěte se, že Ollama po instalaci funguje (např. příkazem `ollama help`).

3. **Vytvořte si `.env` soubor** na základě souboru `.env.example`:
   ```bash
   cp .env.example .env
   ```
   Vyplňte potřebné proměnné (např. `WEBUI_URL`, `WEBUI_URL_SCHEME`, atd.).

### Struktura projektu

```
local-llm-stack/
│
├── docker-compose.yml        # Hlavní konfigurační soubor pro Docker Compose
├── .env.example              # Ukázkové hodnoty proměnných
├── .gitignore                # Soubory a adresáře k ignorování
├── nginx/
│   ├── ssl/                  # Místo pro SSL certifikáty (v .gitignore)
│   └── templates/            # Šablony pro Nginx
├── backend/
│   └── Dockerfile            # Definice kontejneru pro backend
└── uploads_data/             # Úložiště nahraných souborů
```

### Environment proměnné

Tento projekt používá jen **vybrané** proměnné z Open WebUI pro potřeby tohoto konkrétního nasazení (např. `ENABLE_SIGNUP`, `ENABLE_LOGIN_FORM`, `WEBUI_URL`, `OLLAMA_BASE_URL`). Kompletní výčet všech dostupných proměnných naleznete v [oficiální dokumentaci OpenWebUI](https://docs.openwebui.com/getting-started/env-configuration).

> **Poznámka**: Citlivé údaje nikdy necommitujte do repozitáře. `.env` soubor je ve výchozím stavu ignorován v `.gitignore`.

---

## Spuštění projektu

1. **Zkontrolujte soubor `.env`**, zda obsahuje validní hodnoty.
2. **Spusťte**:
   ```bash
   docker compose up -d
   ```
3. **Ověřte běh kontejnerů**:
   ```bash
   docker ps
   ```
   Měli byste vidět všechny kontejnerové služby (`openwebui`, `nginx`, `watchtower`, `tika`, `backend`).
4. Aplikace by měla být dostupná na adrese:
   ```
   https://<VAŠE_DOMÉNA> (pokud máte SSL, jinak http://localhost:3000)
   ```

---

## Nastavení SSL a Nginx

Tento stack používá Nginx jako reverzní proxy před OpenWebUI a dalšími službami. Můžete jej konfigurovat pomocí šablon v `./nginx/templates`.

1. **Ve složce `nginx/ssl`** přidejte **vlastní** certifikáty a klíče (např. `cert.crt` a `privkey.key`).  
2. Pro testování můžete využít **self-signed** certifikát (viz níže ukázka).  
3. V produkci použijte ověřený certifikát z **Let's Encrypt** či jiné certifikační autority.  

### Nginx template

> „Před spuštěním je nutné zkopírovat `default.conf.template.example` na `default.conf.template`.
> `cp nginx/templates/default.conf.template.example nginx/templates/default.conf.template`“
- Docker Compose ve svém volume/mountu hledá pouze `default.conf.template`.  
- Pokud tam není, kontejner s Nginx se buď nespustí (hlásí chybu), nebo zůstane v fallback stavu (pokud to tak nastavíte).

Soubor (např.) `default.conf.template` v adresáři `nginx/templates` slouží k nastavení hlavního konfiguračního souboru Nginx:

```nginx
server {
    listen 443 ssl http2;
    server_name ${WEBUI_URL};  # Doména, kterou zadáváte do .env

    ssl_certificate /etc/nginx/ssl/cert.crt;
    ssl_certificate_key /etc/nginx/ssl/privkey.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    client_max_body_size 32M;

    location / {
        proxy_pass http://openwebui:8080;  # Odpovídá nastavení v docker-compose
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;

        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # (Optional) Disable proxy buffering for better streaming response from models
        proxy_cache_bypass $http_upgrade;
        proxy_buffering off;
    }
}
```

> **Poznámka**: Docker obraz `nginx:alpine` umožňuje využívat tzv. [dockerize templating](https://hub.docker.com/_/nginx) nebo environment proměnné v šablonách, které se doplňují při startu kontejneru. Pokud máte jiné požadavky (např. další subdomény nebo různé location bloky), upravte si šablonu podle svého.

---

## Tipy k provozu a zabezpečení

- **Watchtower**
  - Kontroluje aktualizace image a při nalezení novější verze ji automaticky stáhne a nasadí.
  - V produkčním prostředí zvažte, zda chcete automatické aktualizace, nebo raději ruční.

- **Omezení přístupu**
  - Pokud chcete, aby byla aplikace přístupná pouze z lokální sítě, nepovolujte porty do internetu.
  - Použijte firewall pro vybrané porty (např. 3000, 443).

- **Síla hesel a OAuth**
  - Doporučujeme používat silná hesla nebo OAuth (pokud je nakonfigurován).

---

## Časté dotazy (FAQ)

1. **Proč Ollama není v kontejneru?**
   - Ollamu je možné kontejnerizovat, ale v tomto repozitáři vyžadujeme instalaci přímo na hostu. Dosáhneme tak menších problémů s GPU a rychlejšího přímého přístupu k místním zdrojům.
   - Postup instalace Ollamy pro Linux najdete v [oficiálním dokumentu](https://github.com/ollama/ollama/blob/main/docs/linux.md).

2. **Jak aktualizuji na novou verzi?**
   - Stačí spustit `docker compose pull` a poté `docker compose up -d`. Watchtower to případně udělá i automaticky.

3. **Kde najdu logy?**
   - Můžete použít `docker logs jmeno_kontejneru` nebo nainstalovat Portainer, který má uživatelsky přívětivé rozhraní pro prohlížení logů.

---

## Licence

Tento projekt je zveřejněn pod licencí [MIT](LICENSE). Můžete ho tedy volně forknout, upravovat a využívat pro komerční i nekomerční účely – s podmínkou zachování zmínky o původním autorovi.

---

## Shrnutí a odkazy

Tento repozitář si klade za cíl poskytnout snadno rozšiřitelnou šablonu pro **lokální LLM** s využitím Docker Compose a GPU akcelerace. Před použitím v produkci zvažte důkladné zabezpečení a zálohy.