-- phpMyAdmin SQL Dump
-- version 4.9.4
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 08-09-2020 a las 12:57:54
-- Versión del servidor: 10.3.24-MariaDB-log-cll-lve
-- Versión de PHP: 7.3.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `admin_banco_pichincha`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `superintendencia_accionistas_estructura`
--

CREATE TABLE `superintendencia_accionistas_estructura` (
  `id` int(11) NOT NULL,
  `identificacion` varchar(15) DEFAULT NULL,
  `nombre` varchar(200) DEFAULT NULL,
  `identificacion_socio` varchar(20) DEFAULT NULL,
  `nombre_socio` varchar(100) DEFAULT NULL,
  `nacionalidad` varchar(50) DEFAULT NULL,
  `tipo_inversion` varchar(50) DEFAULT NULL,
  `capital` varchar(50) DEFAULT NULL,
  `restriccion` varchar(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `superintendencia_accionistas_estructura`
--
ALTER TABLE `superintendencia_accionistas_estructura`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `superintendencia_accionistas_estructura`
--
ALTER TABLE `superintendencia_accionistas_estructura`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
