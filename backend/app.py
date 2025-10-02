from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import redis
import os
app = Flask(__name__)
CORS(app)
# Lire le secret
with open('/run/secrets/db_password', 'r') as f:
DB_PASSWORD = f.read().strip()
# Configuration
DB_CONFIG = {
'host': os.getenv('DB_HOST', 'db'),
'database': os.getenv('DB_NAME', 'flask_db'),
'user': os.getenv('DB_USER', 'postgres'),
'password': DB_PASSWORD
}
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
# Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
def get_db_connection():
return psycopg2.connect(**DB_CONFIG)
@app.route('/health', methods=['GET'])
def health():
"""Healthcheck endpoint"""
try:
# Test DB
conn = get_db_connection()
conn.close()
# Test Redis
redis_client.ping()
return jsonify({'status': 'healthy', 'db': 'ok', 'redis': 'ok'}), 200
except Exception as e:
return jsonify({'status': 'unhealthy', 'error': str(e)}), 503
@app.route('/api/items', methods=['GET'])
def get_items():
"""Get all items"""
# Try cache first
cached = redis_client.get('items')
if cached:
return jsonify({'source': 'cache', 'items': eval(cached)})
# Query DB
conn = get_db_connection()
cur = conn.cursor()
cur.execute('SELECT id, name, description FROM items ORDER BY id')
items = [{'id': row[0], 'name': row[1], 'description': row[2]} for row in
cur.fetchall()]
cur.close()
conn.close()
# Cache for 60 seconds
redis_client.setex('items', 60, str(items))
return jsonify({'source': 'database', 'items': items})
@app.route('/api/items', methods=['POST'])
def create_item():
Étape 4 : Backend - Dockerfile
Étape 5 : Frontend - index.html
"""Create a new item"""
data = request.json
name = data.get('name')
description = data.get('description', '')
conn = get_db_connection()
cur = conn.cursor()
cur.execute(
'INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id',
(name, description)
)
item_id = cur.fetchone()[0]
conn.commit()
cur.close()
conn.close()
# Invalidate cache
redis_client.delete('items')
return jsonify({'id': item_id, 'name': name, 'description': description}), 201
if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)