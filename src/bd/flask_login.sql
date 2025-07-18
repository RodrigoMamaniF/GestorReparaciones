-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-07-2025 a las 17:13:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `flask_login`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_clientes` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `existe` tinyint(1) NOT NULL DEFAULT 1,
  `id_usuario` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_clientes`, `nombre`, `email`, `telefono`, `existe`, `id_usuario`) VALUES
(1, 'Mauricio', 'mauri00@gmail.com', '1144663372', 1, 1),
(2, 'Mauricio', 'mauri00@gmail.com', '1144663372', 0, NULL),
(3, 'Federico', 'fede_25@outlook.com', '1144467324', 1, 5),
(4, 'Maxi', 'maxi22@gmail.com', '1156748624', 1, 5),
(5, 'Cliente3usuario', 'cliente3@hotmail.com', '1154435674', 1, 5),
(6, 'Cliente1pablo', 'cliente1pablo@gmail.com', '1133625478', 1, 2),
(7, 'Cliente2pablo', 'cliente2pablo@hotmail.com', '1145738634', 1, 2),
(8, 'ClientedeUsuario3prueba', 'clienteu3@outlook.com', '', 1, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reparaciones`
--

CREATE TABLE `reparaciones` (
  `id_reparaciones` int(11) NOT NULL,
  `fecha_reparacion` date NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `costo` varchar(20) DEFAULT NULL,
  `existe` tinyint(1) DEFAULT 1,
  `estado` text NOT NULL DEFAULT 'pendiente',
  `id_clientes` int(11) NOT NULL,
  `id_usuarios` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reparaciones`
--

INSERT INTO `reparaciones` (`id_reparaciones`, `fecha_reparacion`, `descripcion`, `costo`, `existe`, `estado`, `id_clientes`, `id_usuarios`) VALUES
(2, '2025-02-24', 'Reparación  de flex de netbook.', '50000', 1, 'pendiente', 1, 1),
(4, '2025-06-01', 'Cambio placa madre de Notebook (quemada).', '120000', 1, 'finalizado', 3, 5),
(5, '2025-06-02', 'Cambio de procesador y ram mas limpieza.', '90000', 1, 'pendiente', 4, 5),
(6, '2025-06-10', 'Limpieza completa, cambio de pasta cpu y gpu.', '90000', 1, 'Cancelado', 5, 5),
(7, '2025-07-17', 'A cliente1pablo se le hizo una clonación de disco, de hdd a ssd.', '80000', 1, 'Pendiente', 6, 2),
(8, '2025-07-17', 'Estado de prueba para verificar Existencia y select Estado.', '10000', 1, 'Finalizado', 6, 2),
(9, '2025-07-17', 'Prueba3', '90000', 1, 'Pendiente', 8, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuarios` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `admin` tinyint(1) NOT NULL DEFAULT 0,
  `existe` tinyint(1) NOT NULL DEFAULT 1,
  `email` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuarios`, `nombre`, `contrasena`, `admin`, `existe`, `email`) VALUES
(1, 'rodris', 'admin', 1, 1, NULL),
(2, 'Pablo', 'pablo', 0, 1, 'pablo2025@gmail.com'),
(3, 'Pablo', 'pablo', 0, 0, 'pablo2025@gmail.com'),
(4, 'Rodrigo', 'df', 0, 1, 'mmf@gmail.com'),
(5, 'usuario', 'usuario', 0, 1, NULL),
(6, 'Usuario3prueba', 'usuario3prueba', 0, 1, 'usuario3@hotmail.com'),
(7, 'asd', 'asdasda', 0, 1, 'asdasd@gmail.com');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_clientes`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `reparaciones`
--
ALTER TABLE `reparaciones`
  ADD PRIMARY KEY (`id_reparaciones`),
  ADD KEY `FKClientes` (`id_clientes`),
  ADD KEY `FKUsuarios` (`id_usuarios`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuarios`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_clientes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `reparaciones`
--
ALTER TABLE `reparaciones`
  MODIFY `id_reparaciones` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuarios`);

--
-- Filtros para la tabla `reparaciones`
--
ALTER TABLE `reparaciones`
  ADD CONSTRAINT `reparaciones_ibfk_1` FOREIGN KEY (`id_clientes`) REFERENCES `clientes` (`id_clientes`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `reparaciones_ibfk_2` FOREIGN KEY (`id_usuarios`) REFERENCES `usuarios` (`id_usuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
