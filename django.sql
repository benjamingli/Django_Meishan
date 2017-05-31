DROP DATABASE IF EXISTS django;
CREATE DATABASE IF NOT EXISTS django;

CREATE USER django@'localhost' IDENTIFIED BY 'django';
GRANT ALL PRIVILEGES ON django.* TO django@'localhost' WITH GRANT OPTION;
flush privileges;
