-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-06-2026 a las 01:00:06
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
-- Base de datos: `control_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre`) VALUES
(1, 'Laptop'),
(2, 'Proyector'),
(3, 'Tablet'),
(4, 'Impresora'),
(5, 'Camara'),
(6, 'Monitor'),
(7, 'Teclado'),
(8, 'Mouse'),
(9, 'Parlante'),
(10, 'Microfono');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `equipos`
--

CREATE TABLE `equipos` (
  `id_equipo` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `marca` varchar(50) DEFAULT NULL,
  `modelo` varchar(50) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` enum('Disponible','Prestado','Mantenimiento') DEFAULT 'Disponible',
  `id_categoria` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `equipos`
--

INSERT INTO `equipos` (`id_equipo`, `nombre`, `marca`, `modelo`, `descripcion`, `estado`, `id_categoria`) VALUES
(1, 'Laptop', 'HP', 'ProBook 450', 'Laptop institucional', 'Disponible', 1),
(2, 'Laptop', 'Dell', 'Latitude 5520', 'Laptop para docentes', 'Disponible', 1),
(3, 'Proyector', 'Epson', 'X39', 'Proyector multimedia', 'Disponible', 2),
(4, 'Tablet', 'Samsung', 'Galaxy Tab A', 'Tablet educativa', 'Disponible', 3),
(5, 'Impresora', 'Canon', 'PIXMA G3110', 'Impresora multifuncional', 'Disponible', 4),
(6, 'Laptop', 'Lenovo', 'ThinkPad E14', 'Laptop administrativa', 'Disponible', 1),
(7, 'Camara', 'Canon', 'EOS 2000D', 'Camara para eventos', 'Disponible', 5),
(8, 'Proyector', 'BenQ', 'MS550', 'Proyector para aulas', 'Disponible', 2),
(9, 'Tablet', 'Lenovo', 'Tab M10', 'Tablet institucional', 'Disponible', 3),
(10, 'Laptop', 'Asus', 'VivoBook 15', 'Laptop de apoyo academico', 'Disponible', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

CREATE TABLE `prestamos` (
  `id_prestamo` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `fecha_prestamo` date NOT NULL,
  `fecha_devolucion_prevista` date NOT NULL,
  `fecha_devolucion_real` date DEFAULT NULL,
  `estado` enum('Activo','Devuelto') DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `prestamos`
--

INSERT INTO `prestamos` (`id_prestamo`, `id_usuario`, `id_equipo`, `fecha_prestamo`, `fecha_devolucion_prevista`, `fecha_devolucion_real`, `estado`) VALUES
(1, 1, 1, '2026-06-01', '2026-06-08', '2026-06-07', 'Devuelto'),
(2, 2, 2, '2026-06-02', '2026-06-09', NULL, 'Activo'),
(3, 3, 3, '2026-06-03', '2026-06-10', '2026-06-09', 'Devuelto'),
(4, 4, 4, '2026-06-04', '2026-06-11', NULL, 'Activo'),
(5, 5, 5, '2026-06-05', '2026-06-12', '2026-06-10', 'Devuelto'),
(6, 6, 6, '2026-06-06', '2026-06-13', NULL, 'Activo'),
(7, 7, 7, '2026-06-07', '2026-06-14', '2026-06-12', 'Devuelto'),
(8, 8, 8, '2026-06-08', '2026-06-15', NULL, 'Activo'),
(9, 9, 9, '2026-06-09', '2026-06-16', '2026-06-15', 'Devuelto'),
(10, 10, 10, '2026-06-10', '2026-06-17', NULL, 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitudes`
--

CREATE TABLE `solicitudes` (
  `id_solicitud` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_equipo` int(11) NOT NULL,
  `fecha_solicitud` date NOT NULL,
  `estado` enum('Pendiente','Aprobada','Rechazada') DEFAULT 'Pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `solicitudes`
--

INSERT INTO `solicitudes` (`id_solicitud`, `id_usuario`, `id_equipo`, `fecha_solicitud`, `estado`) VALUES
(1, 1, 1, '2026-06-01', 'Aprobada'),
(2, 2, 2, '2026-06-02', 'Pendiente'),
(3, 3, 3, '2026-06-03', 'Aprobada'),
(4, 4, 4, '2026-06-04', 'Rechazada'),
(5, 5, 5, '2026-06-05', 'Aprobada'),
(6, 6, 6, '2026-06-06', 'Pendiente'),
(7, 7, 7, '2026-06-07', 'Aprobada'),
(8, 8, 8, '2026-06-08', 'Pendiente'),
(9, 9, 9, '2026-06-09', 'Rechazada'),
(10, 10, 10, '2026-06-10', 'Aprobada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo` enum('Docente','Estudiante','Administrativo') NOT NULL,
  `correo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `tipo`, `correo`) VALUES
(1, 'Juan Perez', 'Docente', 'juan@gmail.com'),
(2, 'Maria Lopez', 'Estudiante', 'maria@gmail.com'),
(3, 'Carlos Rojas', 'Administrativo', 'carlos@gmail.com'),
(4, 'Ana Flores', 'Docente', 'ana@gmail.com'),
(5, 'Luis Vargas', 'Estudiante', 'luis@gmail.com'),
(6, 'Sofia Herrera', 'Administrativo', 'sofia@gmail.com'),
(7, 'Pedro Gutierrez', 'Docente', 'pedro@gmail.com'),
(8, 'Valeria Mendoza', 'Estudiante', 'valeria@gmail.com'),
(9, 'Miguel Torres', 'Administrativo', 'miguel@gmail.com'),
(10, 'Camila Rios', 'Estudiante', 'camila@gmail.com');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id_categoria`);

--
-- Indices de la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD PRIMARY KEY (`id_equipo`),
  ADD KEY `fk_categoria` (`id_categoria`);

--
-- Indices de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id_prestamo`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_equipo` (`id_equipo`);

--
-- Indices de la tabla `solicitudes`
--
ALTER TABLE `solicitudes`
  ADD PRIMARY KEY (`id_solicitud`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_equipo` (`id_equipo`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `equipos`
--
ALTER TABLE `equipos`
  MODIFY `id_equipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  MODIFY `id_prestamo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `solicitudes`
--
ALTER TABLE `solicitudes`
  MODIFY `id_solicitud` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `equipos`
--
ALTER TABLE `equipos`
  ADD CONSTRAINT `fk_categoria` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`);

--
-- Filtros para la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`id_equipo`) REFERENCES `equipos` (`id_equipo`);

--
-- Filtros para la tabla `solicitudes`
--
ALTER TABLE `solicitudes`
  ADD CONSTRAINT `solicitudes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `solicitudes_ibfk_2` FOREIGN KEY (`id_equipo`) REFERENCES `equipos` (`id_equipo`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
