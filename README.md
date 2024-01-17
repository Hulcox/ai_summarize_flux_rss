# Projet IA Veille Technologique

Ce projet est un projet python qui permet de récupérer des articles via un flux RSS et qui via un model LLM d'intelligence artificiel permet de nous faire un résumé de chaque article .

## Configuration

1. Assurez-vous d'avoir Python 3 et pip d'installé.

   ```bash
    python --version
   ```

   ```bash
    pip --version
   ```

2. Créez un environnement virtuel (si vous le souhaiter) et activez-le en vous assurant d'être dans le dossier du projet :

   ```bash
   python -m venv venv
   ```

   ou

   ```bash
   python3 -m venv venv
   ```

   ***

   ```bash
   source venv/bin/activate
   ```

3. Assurez-vous aussi d'avoir le modèle `openchat` d'installé avec [Ollama](https://ollama.ai/) :

   ```bash
   ollama pull openchat
   ```

4. Installez les dépendances nécessaires :

   ```bash
   pip install -r requirements.txt
   ```

   ou

   ```bash
   pip3 install -r requirements.txt
   ```

5. Lancez le script `main.py` :

   ```bash
   python main.py
   ```

   ou

   ```bash
   python main.py
   ```

## Execution du script

Une fois que vous aurez lancer le script main.py vous aurez des information dans la console avec le titre des article, la date de sortie (qui correspond a la date d'aujourd'hui), puis le résumé de l'article fourni par le model d'IA choisi.
A la fin de l'execution, tous les résumés des articles sont sauvegardé dans le dossier **summary** du projet (/summary/{nom_du_flux}/{date}/nom_de_l'article).

**Si vous le souhaiter vous pouvez modifié deux paramètre dans le fichier main.py :**
changer le nombre maximum d'articles pris en considération dans le résumé en changeant la variable :

```bash
   max_limit = default(4)
```

vous pouvez aussi changer de model LLM en changeant la variable :

```bash
model = default("openchat")
```

Bidault Romain MSI 5 - DEV A
