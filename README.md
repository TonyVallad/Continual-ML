# Continual ML - Améliorer une solution d'IA en continu

Un projet de développement d'une solution d'IA avec amélioration continue, monitoring et automatisation sur 8 jours.

## 📋 Aperçu du Projet

Ce projet implémente une architecture complète pour une solution d'IA en production avec :
- Pipeline de données automatisé avec Prefect
- API FastAPI pour les prédictions
- Monitoring avec Uptime Kuma, Prometheus & Grafana
- Notifications Discord automatiques
- Interface utilisateur Streamlit
- CI/CD avec GitHub Actions

## 🚀 Installation Rapide

```bash
# 1. Cloner le projet
git clone <repository-url>
cd Continual-ML

# 2. Configuration environnement
cp env.example .env
# Modifier .env avec vos paramètres

# 3. Option Docker (Recommandée)
docker-compose up --build

# 4. Option Locale
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📅 Développement par Jour

### ✅ Jour 1 - Infrastructure de Base (TERMINÉ)

**Objectifs :** Mise en place de l'infrastructure de monitoring et pipeline basique

**Réalisations :**
- [x] **Discord Webhook** : Notifications automatiques configurées
- [x] **FastAPI Application** : API avec endpoint `/health`
- [x] **Prefect Pipeline** : Flow "random-check" toutes les 30 secondes
- [x] **Docker Compose** : Conteneurisation FastAPI + Uptime Kuma
- [x] **Configuration .env** : Variables d'environnement sécurisées

**Technologies utilisées :**
- FastAPI, Prefect 3.1+, Docker, Uptime Kuma
- Discord Webhooks, python-dotenv

**Fonctionnalités :**
- Pipeline génère nombre aléatoire
- Si < 0.5 → simulation retraining (avec échecs + retries)
- Si ≥ 0.5 → affiche "OK"
- Notifications Discord pour chaque état
- Monitoring santé API via Uptime Kuma

**Comment tester :**
```bash
# Démarrer Prefect server
prefect server start

# Dans un autre terminal
export PREFECT_API_URL=http://127.0.0.1:4200/api  # ou PowerShell: $Env:PREFECT_API_URL = "..."
python flow.py

# Accès interfaces
# - API: http://localhost:8000
# - Prefect UI: http://localhost:4200
# - Uptime Kuma: http://localhost:3001
```

### 🔄 Jour 2 - API Complète (À VENIR)

**Objectifs :** Développement API ML avec routes prédiction et gestion données

**Prévisions :**
- [ ] **Approche Agile** : Organisation équipes, GitHub, Kanban
- [ ] **Routes API** :
  - `POST /predict` : Prédiction avec régression logistique
  - `GET /health` : Check santé (✅ déjà fait)
  - `POST /generate` : Génération dataset linéaire → DB
  - `POST /retrain` : Réentraînement avec tracking MLflow
- [ ] **Tests Unitaires** : Coverage complète des routes
- [ ] **Base de Données** : Stockage datasets et modèles
- [ ] **MLflow Integration** : Suivi expérimentations

### 📊 Jour 3 - Monitoring & Surveillance (À VENIR)

**Objectifs :** Monitoring avancé, logging et interface utilisateur

**Prévisions :**
- [ ] **Documentation** : README détaillé, journaux dev
- [ ] **CI/CD** : GitHub Actions pipeline
- [ ] **Monitoring Stack** :
  - Prometheus : Métriques système
  - Grafana : Dashboards visualisation
  - Loguru : Logging structuré
- [ ] **Intelligence** : Mesure performance avant retrain
- [ ] **Interface Streamlit** : Boutons routes + authentification
- [ ] **Migration Alembic** : Gestion schéma DB
- [ ] **API Tokens** : Sécurité authentification

### 🎯 Jour 4 - Première Restitution (À VENIR)

**Objectifs :** Présentation, automatisation complète

**Prévisions :**
- [ ] **Daily & Slides** : Présentation progrès
- [ ] **Document Technique** : Architecture détaillée
- [ ] **Automatisation Prefect** : Suppression route manuelle retrain
- [ ] **Discord Integration** : Logs/dérives automatiques
- [ ] **Template Création** : Réutilisabilité projet
- [ ] **Analyse Réflexive** : Difficultés et solutions

### 🤖 Jours 5-8 - Projet IA Spécialisé (À VENIR)

**Options projets :**
1. **Reconnaissance Audio/Photo** : Identification membres équipe
2. **Reconnaissance Vidéo** : Fine-tuning YOLOv11 temps réel
3. **Pierre-Ciseaux-Feuille** : YOLOv11 pour jeu gestuel
4. **Projet Libre** : Innovation équipe
5. **Bonus Celery** : Exécution asynchrone prédictions

---

## 🏗️ Architecture Actuelle

```
Continual-ML/
├── app.py                 # FastAPI application
├── flow.py               # Prefect pipeline
├── docker-compose.yml    # Services containerization
├── Dockerfile           # FastAPI container
├── requirements.txt     # Python dependencies
├── env.example         # Environment template
├── setup_day1.md       # Day 1 setup guide
└── docs/
    └── Enonce.md       # Project specifications
```

## 🔧 Configuration

### Variables d'Environnement (.env)

```bash
# Discord
DISCORD_WEBHOOK_URL=your_webhook_url

# Prefect
PREFECT_API_URL=http://127.0.0.1:4200/api

# FastAPI
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000

# Pipeline
CHECK_INTERVAL_SECONDS=30
TASK_RETRIES=2
RETRY_DELAY_SECONDS=1
```

## 📈 Monitoring

### Services Actuels
- **FastAPI** : Port 8000
- **Uptime Kuma** : Port 3001 (monitoring)
- **Prefect Server** : Port 4200 (workflows)

### À Venir (Jour 3)
- **Prometheus** : Métriques
- **Grafana** : Dashboards
- **Streamlit** : Interface utilisateur

## 🔔 Notifications

Le système envoie automatiquement des notifications Discord pour :
- ✅ Modèle performance OK
- 🔄 Détection drift + retraining
- ❌ Échecs pipeline

## 🧪 Tests

```bash
# Tests unitaires (à implémenter Jour 2)
pytest tests/

# Test santé API
curl http://localhost:8000/health
```

## 📚 Documentation

- [Setup Jour 1](setup_day1.md) : Guide installation détaillé
- [Spécifications](docs/Enonce.md) : Cahier charges complet

## 🤝 Contribution

1. Fork le projet
2. Créer branche feature (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branche (`git push origin feature/amazing-feature`)
5. Ouvrir Pull Request

## 📝 Licence

Ce projet est sous licence [MIT](LICENSE).

## 🏷️ Statut Développement

- 🟢 **Jour 1** : Infrastructure de base - TERMINÉ
- 🟡 **Jour 2** : API ML complète - EN ATTENTE
- 🟡 **Jour 3** : Monitoring avancé - EN ATTENTE
- 🟡 **Jour 4** : Restitution - EN ATTENTE
- 🟡 **Jours 5-8** : Projet IA spécialisé - EN ATTENTE