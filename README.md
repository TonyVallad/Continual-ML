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

### ✅ Jour 2 - API Complète (TERMINÉ)

**Objectifs :** Développement API ML avec routes prédiction et gestion données

**Réalisations :**
- [x] **Routes API Complètes** :
  - `POST /predict` : Prédiction avec régression logistique ✅
  - `GET /health` : Check santé ✅
  - `POST /generate` : Génération dataset linéaire → DB ✅
  - `POST /retrain` : Réentraînement avec tracking MLflow ✅
- [x] **Tests Unitaires** : Coverage complète des routes
- [x] **Base de Données** : SQLite avec SQLAlchemy pour stockage datasets
- [x] **MLflow Integration** : Suivi expérimentations et métriques modèles

**Technologies utilisées :**
- FastAPI, SQLAlchemy, MLflow, scikit-learn
- Pydantic pour validation, pytest pour tests

**Fonctionnalités :**
- Génération datasets linéaires 2 features
- Entraînement régression logistique
- Prédictions avec probabilités
- Tracking automatique MLflow
- Stockage persistant SQLite

### ✅ Jour 3 - Monitoring & Surveillance (TERMINÉ)

**Objectifs :** Monitoring avancé, logging et interface utilisateur

**Réalisations :**
- [x] **Documentation** : README détaillé, guides utilisation
- [x] **CI/CD** : GitHub Actions pipeline avec tests automatisés
- [x] **Monitoring & Logging** :
  - Loguru : Logging structuré remplaçant print/logging basique ✅
  - Performance-based retraining : Mesure performance avant retrain ✅
  - Uptime Kuma : Monitoring API health (déjà configuré) ✅
- [x] **Interface Streamlit** : Dashboard web avec authentification
- [x] **API Tokens** : Sécurité authentification Bearer token
- [x] **Docker Integration** : Services Streamlit dans compose

**Technologies utilisées :**
- Loguru, Streamlit, GitHub Actions
- FastAPI Security, Bearer authentication
- Docker multi-services

**Fonctionnalités :**
- Dashboard web interactif (port 8501)
- Authentification par mot de passe Streamlit
- API sécurisée par tokens Bearer
- Logging structuré avec niveaux
- Retraining intelligent basé performance
- Pipeline CI/CD automatisé

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
├── app.py                      # FastAPI application (Day 2-3)
├── flow.py                     # Prefect pipeline (Day 1)
├── streamlit_app.py           # Streamlit dashboard (Day 3)
├── test_app.py                # Tests unitaires (Day 2-3)
├── docker-compose.yml         # Multi-services container (Day 1-3)
├── Dockerfile                 # Application container
├── requirements.txt           # Dependencies Python (Day 1-3)
├── env.example               # Environment template (Day 1-3)
├── README.md                 # Documentation complète
├── IMPLEMENTATION_SUMMARY.md # Résumé implémentation Day 3
├── .github/workflows/ci.yml  # CI/CD Pipeline (Day 3)
└── docs/
    └── Enonce.md             # Spécifications projet
```

## 🔧 Configuration

### Variables d'Environnement (.env)

```bash
# API Security (Jour 3)
API_KEY=your-secure-api-key-here
PERFORMANCE_THRESHOLD=0.8

# Streamlit Interface (Jour 3)
STREAMLIT_PASSWORD=admin123
API_BASE_URL=http://localhost:8000

# Discord Integration
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/REPLACE_WITH_YOUR_WEBHOOK_URL

# Prefect Flow Configuration
CHECK_INTERVAL_SECONDS=30
TASK_RETRIES=2
RETRY_DELAY_SECONDS=1

# FastAPI Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
```

## 📈 Monitoring

### Services Opérationnels
- **FastAPI API** : Port 8000 (avec authentification Bearer token)
- **Streamlit Dashboard** : Port 8501 (interface web avec auth)
- **Uptime Kuma** : Port 3001 (monitoring santé API)
- **Prefect Server** : Port 4200 (workflows et pipelines)

### Fonctionnalités Monitoring
- **Loguru Logging** : Logs structurés avec niveaux (INFO, WARNING, ERROR)
- **Performance Tracking** : Suivi automatique performance modèles
- **Health Checks** : Monitoring continu via Uptime Kuma
- **Discord Alerts** : Notifications automatiques drift/erreurs
- **CI/CD Pipeline** : Tests automatisés GitHub Actions

## 🔔 Notifications

Le système envoie automatiquement des notifications Discord pour :
- ✅ Modèle performance OK
- 🔄 Détection drift + retraining
- ❌ Échecs pipeline

## 🧪 Tests

```bash
# Tests unitaires complets (Day 2-3)
pip install -r requirements.txt
pytest test_app.py -v

# Tests avec authentification
export API_KEY=your-api-key  # ou $Env:API_KEY = "..." sur Windows
pytest test_app.py -v

# Tests API manuels
curl http://localhost:8000/health
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/model-status
```

## 📊 Progrès Global

### ✅ Jours Complétés : 3/8

- **Jour 1** ✅ : Infrastructure base (Prefect, FastAPI, Docker, Monitoring)  
- **Jour 2** ✅ : API ML complète (Prédictions, MLflow, Tests, Base données)
- **Jour 3** ✅ : Monitoring avancé (Streamlit, Auth, CI/CD, Loguru)
- **Jour 4** 🟡 : Restitution et automatisation (À venir)
- **Jours 5-8** 🟡 : Projet IA spécialisé (À venir)

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

## Day 3 Features

This implementation includes all Day 3 requirements:

### ✅ Implemented Features

- **🔒 API Authentication**: Bearer token authentication for all endpoints
- **📊 Performance-based Retraining**: Models only retrain if performance drops below threshold
- **📝 Loguru Logging**: Structured logging throughout the application
- **🌐 Streamlit Interface**: Web dashboard with authentication for API interaction
- **🔄 CI/CD Pipeline**: GitHub Actions workflow for automated testing
- **📈 Uptime Monitoring**: Integration with Uptime Kuma for API health checks

## Quick Start

### 1. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit .env with your configuration
# Set API_KEY, STREAMLIT_PASSWORD, etc.
```

### 2. Run with Docker Compose

```bash
docker-compose up -d
```

This starts:
- **FastAPI**: http://localhost:8000 (API)
- **Streamlit**: http://localhost:8501 (Web Interface)
- **Uptime Kuma**: http://localhost:3001 (Monitoring)

### 3. Access the Web Interface

1. Go to http://localhost:8501
2. Enter the password (default: `admin123`)
3. Use the dashboard to interact with the API

## API Endpoints

All protected endpoints require `Authorization: Bearer <API_KEY>` header.

- `GET /health` - Health check (no auth required)
- `GET /model-status` - Model status and performance (no auth required)
- `POST /generate` - Generate training dataset 🔒
- `POST /retrain` - Retrain model (with performance check) 🔒
- `POST /predict` - Make predictions 🔒

## Configuration

Key environment variables:

- `API_KEY`: Authentication key for API access
- `PERFORMANCE_THRESHOLD`: Minimum model performance (default: 0.8)
- `STREAMLIT_PASSWORD`: Web interface password
- `DISCORD_WEBHOOK_URL`: Optional Discord notifications

## Development

### Run Tests

```bash
pip install -r requirements.txt
pytest test_app.py -v
```

### Local Development

```bash
# Start API
python app.py

# Start Streamlit (in another terminal)
streamlit run streamlit_app.py

# Start Prefect flow (in another terminal)
python flow.py
```

## Monitoring & Alerting

- **Uptime Kuma**: Configure to monitor `http://fastapi_app:8000/health` every minute
- **Discord**: Set webhook URL for drift notifications
- **Loguru**: Structured logs with different levels (INFO, WARNING, ERROR)

## CI/CD

GitHub Actions automatically:
- Runs tests on push/PR
- Validates app startup
- Caches dependencies for faster builds