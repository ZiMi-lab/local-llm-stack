# nginx/ssl

Adresář slouží k uložení SSL certifikátů a odpovídajících privátních klíčů, které používá kontejner s Nginx pro šifrovanou komunikaci (HTTPS).

## Jak použít

1. **Vložte sem své certifikáty** (např. `cert.crt`) a **privátní klíče** (např. `privkey.key`).
2. Ujistěte se, že v konfiguračním souboru Nginx (`default.conf.template` nebo jiném) správně odkazujete na tyto soubory.
3. **Nepřidávejte reálné klíče do verzovacího systému** – soubory v této složce jsou ve výchozím nastavení ignorovány (`.gitignore`), aby se nedostaly na GitHub.

## Self-signed certifikát (testování)

Pokud nemáte k dispozici oficiální certifikát, můžete vygenerovat self-signed certifikát například pomocí:

```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.key \
  -out cert.crt \
  -subj "/CN=localhost"
```

Self-signed certifikáty jsou vhodné jen pro **interní testování**. Pro nasazení do ostrého provozu použíte certifikát od důvěryhodné autority (např. Let's Encrypt).
