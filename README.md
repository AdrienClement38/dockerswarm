Membres du groupe

    Lika Lobodzinskaya
    Adrien Clement
    Nicolas Massai
    Abdelghani Hamaz
    Yassin Ait Mansour



Déploiement de la stack Flask + Postgres + Redis + Nginx avec Docker Swarm
1. Initialiser Docker Swarm (si ce n’est pas déjà fait)

docker swarm init

2. Créer le secret pour Postgres

echo "flask_secret_password" | docker secret create db_password -

3. Builder les images (depuis la racine du projet)

docker build -t flask-api:latest ./backend
docker build -t flask-frontend:latest ./frontend

4. Déployer la stack

docker stack deploy -c stack.yml flaskapp

5. Vérifier que tout tourne

docker stack services flaskapp

Tu dois voir :

flaskapp_backend → 3/3

flaskapp_db → 1/1

flaskapp_redis → 2/2

flaskapp_frontend → 2/2

6. Initialiser la base de données (si besoin)

docker exec -it $(docker ps -q -f name=flaskapp_db) psql -U postgres -d flask_db

Dans psql :
CREATE TABLE IF NOT EXISTS items (
id SERIAL PRIMARY KEY,
name VARCHAR(255) NOT NULL,
description TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO items (name, description) VALUES
('Sample Item 1', 'This is a sample item'),
('Sample Item 2', 'Another sample item'),
('Sample Item 3', 'Yet another sample item');

Vérifier avec :
SELECT * FROM items;

Quitter avec :
\q

7. Tester

API Healthcheck → http://localhost:5000/health
API Items → http://localhost:5000/api/items
Frontend → http://localhost:8080

8. Commandes utiles

Vérifier les tâches :
docker stack ps flaskapp

Voir les logs du backend :
docker service logs flaskapp_backend

Scaler le backend :
docker service scale flaskapp_backend=5

Rolling update (après rebuild du backend) :
docker build -t flask-api:latest ./backend
docker service update --image flask-api:latest flaskapp_backend

Supprimer la stack :
docker stack rm flaskapp