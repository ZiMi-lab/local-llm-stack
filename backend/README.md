# Backend

Tato složka obsahuje zdrojový kód a konfigurační soubory pro **backend** (FastAPI aplikaci), který v tomto projektu zajišťuje:

1. **Zpracování nahraných souborů** a jejich ukládání do cílového adresáře (např. `/uploads`).
2. **Autorizaci pomocí tokenů** (definovaných v `.env` proměnné `BACKEND_UPLOAD_TOKENS`).

## Struktura

- **`main.py`** – hlavní aplikační logika, definice endpointů.
- **`Dockerfile`** – pokyny pro sestavení Docker image (využívá se v `docker-compose.yml`).
- Volitelné podadresáře pro další moduly, knihovny, šablony apod.

## Spuštění v Dockeru

1. Ujistěte se, že máte v hlavním adresáři projektu `.env` s proměnnou `BACKEND_UPLOAD_TOKENS`.
2. Spusťte docker-compose (z kořenové složky):
   ```bash
   docker compose up -d
   ```
3. Kontejner `backend` se sestaví a poběží jako součást stacku.

## Konfigurace tokenů (BACKEND_UPLOAD_TOKENS)

- V `.env` definujte proměnnou `BACKEND_UPLOAD_TOKENS` – například:
  ```
  BACKEND_UPLOAD_TOKENS="token1, token2"
  ```
- Backend při nahrávání souborů vyžaduje, aby uživatel poslal jeden z povolených tokenů (pole `token` ve formuláři).
- Správný token je kontrolován v `main.py` (pseudokód):
  ```python
  if token not in VALID_TOKENS:
      raise HTTPException(status_code=401, detail="Invalid token")
  ```

## Bezpečnostní poznámky

- `BACKEND_UPLOAD_TOKENS` by měly být vždy uloženy v `.env`, který je **ignorován** v `.gitignore` (tj. netrackovat v repozitáři).
- Soubory nahrané uživatelem ukládejte do odděleného adresáře (např. `/uploads`), a pečlivě zvažte přístupová práva a oddělení tak, abyste předešli nechtěnému přímému zpřístupnění nebo přepsání existujících souborů.
