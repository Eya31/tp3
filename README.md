## Lancer l'application

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

L'application est disponible sur http://127.0.0.1:8000

## Tester l'application

- Navigateur : ouvrir http://127.0.0.1:8000
- Terminal : `curl http://127.0.0.1:8000`
- Documentation interactive (Swagger) : http://127.0.0.1:8000/docs

Réponse attendue de `GET /` :

```json
{"message": "it works !"}
```
