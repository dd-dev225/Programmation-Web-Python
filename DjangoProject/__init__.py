# DjangoProject/__init__.py
# Ce fichier doit être au même niveau que settings.py, urls.py, etc.

import pymysql

# FAKE une version récente de mysqlclient (suffisamment haute pour 2025-2026)
pymysql.version_info = (2, 2, 4, 'final', 0)   # ← change ici : 2.2.4 ou plus

# Remplace MySQLdb par PyMySQL
pymysql.install_as_MySQLdb()