drop database if exists stocks;

CREATE DATABASE IF NOT EXISTS stocks CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON stocks.* TO stock@localhost IDENTIFIED BY 'stock';
