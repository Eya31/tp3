# Changelog

## v1.2 (comparé à v0.2)

### Ajouts
- `POST /multiply` et `GET /multiply?a=..&b=..` : multiplication de deux nombres.
- `POST /divide` et `GET /divide?a=..&b=..` : division, avec erreur 400
  « Division par zéro impossible » si b = 0.
- Classe `Operands` (Pydantic) pour valider le corps JSON des requêtes POST.
- Fonctions `compute_multiply` et `compute_divide`, partagées par les versions GET et POST.

### Corrections
- `GET /` renvoie `{"message": "it works !"}` (au lieu de `"Hello World"`).
- Suppression d'un `return` inutile, resté en double dans `/addition`.

### Statistiques (`git diff v0.2 v1.2 --stat`)
```
main.py | 42 +++++++++++++++++++++++++++++++++++++++---
1 file changed, 39 insertions(+), 3 deletions(-)
```

### Tests réalisés
| Test | Résultat |
|---|---|
| `/divide?a=8&b=2` depuis un autre PC (IP du leader) | 200, 4.0 |
| `/divide?a=8&b=0` | 400, « Division par zéro impossible » |
| `/`, `/addition`, `/greeting` | sans régression |