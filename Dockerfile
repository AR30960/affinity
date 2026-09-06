# Image de base Python légère
FROM python:3.11-slim

# Répertoire de travail
WORKDIR /app

# Copie des fichiers de l'application
COPY . /app

# Port d'écoute par défaut
EXPOSE 8765
ENV PORT=8765

# Démarrage du serveur
CMD ["python", "server.py"]
