# Especificación Técnica: HU47 - Repetición Espaciada Automática

## 1. Visión General
Esta funcionalidad implementa un sistema de repasos automáticos basado en el algoritmo de repetición espaciada (estilo SM-2/Anki). El objetivo es reforzar el aprendizaje de los temas que el estudiante ya domina, programando sesiones de práctica en intervalos crecientes para evitar la curva del olvido.

## 2. Requisitos Funcionales

### 2.1 Modelo de Repaso (`RepasoProgramado`)
Crear un nuevo modelo para persistir el estado de los repasos por estudiante y tema en `AppEvaluar`:
- `estudiante`: Relación con el usuario.
- `tema`: Relación con el tema dominado.
- `fecha_proximo_repaso`: Fecha en la que el tema debe volver a practicarse.
- `intervalo`: Días actuales entre repasos (entero).
- `factor_facilidad` (EF): Multiplicador para ajustar el intervalo según el desempeño (Default: 2.5).
- `estado`: Booleano (Activo/Inactivo).

### 2.2 Lógica de Repetición Espaciada (SM-2 Simplificado)
- **Inicio:** Cuando un tema alcanza el **Umbral de Dominio** (>90% precisión y 10+ ejercicios), se crea el registro inicial con un intervalo de 1 día.
- **Acierto en Repaso:**
    - Nuevo Intervalo = Intervalo anterior * EF.
    - Se suma 0.1 al EF (máximo 3.0).
- **Fallo en Repaso:**
    - Se aplica una **Penalización Suave**: Nuevo Intervalo = Intervalo anterior * 0.5 (mínimo 1 día).
    - Se resta 0.2 al EF (mínimo 1.3).

### 2.3 Integración con Motor de Recomendación
- El motor de recomendación (`calcular_recomendacion`) deberá verificar primero si existen `RepasadosProgramados` cuya `fecha_proximo_repaso` sea menor o igual a la fecha actual.
- **Prioridad Bloqueante (Alta):** Si hay repasos vencidos, el sistema recomendará el tema del repaso más antiguo antes de sugerir nuevos temas basados en debilidades actuales.

## 3. Requisitos No Funcionales
- **Persistencia:** Los intervalos y fechas deben ser consistentes en PostgreSQL.
- **Desempeño:** La consulta de repasos vencidos debe ser eficiente (indexada por fecha y estudiante).
- **Aislamiento:** La lógica de cálculo de intervalos debe estar en un servicio separado.

## 4. Criterios de Aceptación
- [ ] Se crea automáticamente un objeto `RepasoProgramado` cuando un tema supera el 90% de precisión con 10 ejercicios.
- [ ] El motor de recomendación prioriza temas con fecha de repaso vencida.
- [ ] Al resolver correctamente un ejercicio de un tema en repaso, la fecha se posterga según el intervalo * EF.
- [ ] Al fallar un ejercicio de un tema en repaso, el intervalo se reduce a la mitad y el EF disminuye.
- [ ] Si no hay repasos vencidos, el motor de recomendación funciona normalmente sugiriendo debilidades.

## 5. Fuera de Alcance
- Notificaciones externas (Email/Push).
- Configuración manual de intervalos por el docente.
- Vista de calendario de repasos futuros.
