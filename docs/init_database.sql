-- ============================================
-- Script de Inicialización - MovieLand
-- Autor: Nicole Beeckmans Barrientos
-- ============================================

DROP DATABASE IF EXISTS movieland_db;
CREATE DATABASE movieland_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE movieland_db;

CREATE TABLE peliculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    año INT NOT NULL,
    director VARCHAR(150) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    duracion INT NULL,
    sinopsis TEXT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Datos de ejemplo
INSERT INTO peliculas (titulo, genero, año, director, precio, duracion, sinopsis) VALUES
('El Padrino', 'Drama', 1972, 'Francis Ford Coppola', 12.99, 175, 'La historia de la familia Corleone en Nueva York.'),
('Pulp Fiction', 'Crimen', 1994, 'Quentin Tarantino', 9.99, 154, 'Historias entrelazadas de crimen en Los Ángeles.'),
('El Caballero Oscuro', 'Acción', 2008, 'Christopher Nolan', 14.99, 152, 'Batman debe enfrentarse al enigmático Joker.'),
('Forrest Gump', 'Drama', 1994, 'Robert Zemeckis', 11.99, 142, 'La vida extraordinaria de un hombre simple.'),
('Inception', 'Ciencia Ficción', 2010, 'Christopher Nolan', 13.99, 148, 'Un ladrón roba secretos a través de sueños.'),
('Matrix', 'Ciencia Ficción', 1999, 'Lana y Lilly Wachowski', 10.99, 136, 'Un hacker descubre la verdad sobre su realidad.'),
('Interstellar', 'Ciencia Ficción', 2014, 'Christopher Nolan', 15.99, 169, 'Exploradores buscan un nuevo hogar para la humanidad.'),
('Gladiador', 'Acción', 2000, 'Ridley Scott', 11.99, 155, 'Un general romano busca venganza tras perder a su familia.'),
('Titanic', 'Romance', 1997, 'James Cameron', 12.99, 194, 'Una historia de amor en el fatídico viaje del Titanic.'),
('Avatar', 'Ciencia Ficción', 2009, 'James Cameron', 14.99, 162, 'Un marine es enviado a la luna Pandora.');