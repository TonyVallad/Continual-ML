# Améliorer une solution d’IA en continu

## Préparation – Jour 1

1. **Discord Webhook**

   * Créez un webhook via les paramètres Discord → Intégration → copier l’URL.

2. **Docker‑compose pour Uptime Kuma et une API**

   ```yaml
   version: '3.8'
   services:
     app:
       build: .
       container_name: fastapi_app
       ports:
         - "8000:8000"
       restart: unless-stopped
     uptime-kuma:
       image: louislam/uptime-kuma:latest
       container_name: uptime_kuma
       ports:
         - "3001:3001"
       volumes:
         - uptime-kuma-data:/app/data
       restart: unless-stopped
   volumes:
     uptime-kuma-data:
   ```

3. **Configurez Uptime Kuma**

   * Accédez à [http://localhost:3001](http://localhost:3001)
   * Ajoutez un service ping vers http\://fastapi\_app:8000/health toutes les 30 sec.

4. **Notifications Discord**
   Exemple en Python :

   ```python
   def send_discord_embed(message):
       ...
       response = requests.post(DISCORD_WEBHOOK_URL, json=data)
       ...
   send_discord_embed("Le traitement des données est terminé avec succès.")
   ```

---

## Intro Prefect – Pipeline “random‑check” (Jour 1)

* Créez un pipeline tournant toutes les 30 sec :

  * génère un nombre aléatoire ;
  * si < 0,5 → retraining (avec échec + retries) ; sinon affiche "ok".
* Objectifs : découvrir `@task`, `@flow`, logs, retries, planification.
* Conteneuriser ensuite via Docker‑Compose (sans toucher au code).

### Étapes à suivre

* Initialisation :

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install "prefect>=3.1"
  ```

* Implémentation :

  ```python
  from prefect import flow, task
  from prefect.logging import get_run_logger

  @task(retries=2, retry_delay_seconds=1)
  def check_random(): ...

  @flow
  def periodic_check(): ...
  ```

* Planification :

  ```python
  if __name__ == "__main__":
      periodic_check.serve(name="every-10s", interval=10)
  ```

* Ajoutez des logs pour indiquer drift ou état OK.

* Test puis conteneurisation.

---

## Vérification dans l’UI Prefect (port 4200)

1. Lancez : `prefect server start`
2. Exportez la variable :

   * PowerShell : `$Env:PREFECT_API_URL = "http://127.0.0.1:4200/api"`
   * Bash : `export PREFECT_API_URL=http://127.0.0.1:4200/api`
3. Exécutez `python flow.py`.
4. Conteneurisez avec Dockerfile + Docker‑Compose, incluant un service `prefect-server` et votre service `random-check-with-server`.

---

## Créer l’API – Jour 2

* **Approche agile** : création de groupes, dépôt GitHub, Kanban/US/EPIC.
* **Routes à implémenter** :

  * `predict` : prédiction avec régression logistique sur le dernier dataset.
  * `health` : retourne 200 OK.
  * `generate` : création d’un dataset linéaire à 2 features stocké en DB.
  * `retrain` : réentraînement à chaud, suivi par MLflow.
* **Tests unitaires** pour chaque route.

---

## Monitoring & Application – Jour 3

* Documentation (`README`, journaux journaliers), CI/CD via GitHub Actions.
* Surveillance ressource via **Prometheus + Grafana**.
* Logging avec **Loguru**.
* Avant `retrain`, mesurer la performance : lancer le retrain uniquement si le modèle décroît sous un seuil.
* **Uptime Kuma** ping API chaque minute avec alertes.
* Interface petite via **Streamlit** : boutons pour routes + auth.
* **CI/CD**, **migration Alembic**, **tokens API**.

---

## Première restitution – Jour 4

* Daily, slides + document tech + bilan des difficultés et solutions.
* **Automatisation** : suppression route `retrain`, intégration complète via Prefect.
* **Discord webhook** pour logs/dérives.
* Création d’un **template** à partir du projet.
* Présentation des groupes + analyse réflexive.

---

## Projet IA – Jours 5 à 8

Types de projets possibles (à reprendre depuis le template) :

1. Reconnaissance audio/photo de membres de groupe.
2. Reconnaissance vidéo en continu et fine-tuning YOLOv11.
3. Fine-tuning YOLOv11 pour jeu pierre‑ciseaux‑feuille.
4. Projet libre ou variante.
5. **Bonus** : intégration de **Celery** pour exécuter prédictions et entraînement de façon asynchrone.