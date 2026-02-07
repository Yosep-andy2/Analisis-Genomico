# Requisitos del Sistema - Plataforma de Análisis Genómico

## 1. Visión General del Proyecto

### 1.1 Descripción
Plataforma web de bioinformática para análisis genómico completo que permite a estudiantes e investigadores analizar genomas bacterianos de manera automatizada. El sistema se conecta directamente con bases de datos públicas (NCBI GenBank) para descargar genomas y ejecutar análisis computacionales avanzados.

### 1.2 Objetivos del Sistema
- Proporcionar una interfaz web intuitiva para análisis genómico sin necesidad de conocimientos avanzados de programación
- Automatizar el proceso de descarga de genomas desde NCBI GenBank
- Ejecutar análisis bioinformáticos estándar (conteo de codones, análisis de genes, estadísticas genómicas)
- Generar reportes científicos con visualizaciones profesionales
- Validar resultados mediante comparación con literatura científica
- Facilitar el aprendizaje de bioinformática aplicada

### 1.3 Alcance
**Incluye:**
- Búsqueda y descarga de genomas desde NCBI GenBank
- Análisis de codones de inicio (ATG) y terminación (TAA, TAG, TGA)
- Extracción y análisis de genes anotados
- Cálculo de estadísticas genómicas (GC%, densidad génica, tamaño del genoma)
- Generación de gráficos y visualizaciones
- Exportación de resultados en múltiples formatos (JSON, CSV, PDF)
- Sistema de validación de resultados

**No incluye:**
- Sistema de autenticación de usuarios (no requiere login/registro)
- Análisis de genomas eucariotas complejos (enfoque en bacterias)
- Ensamblaje de genomas desde lecturas raw
- Análisis filogenéticos o comparativos entre múltiples genomas
- Predicción de estructura proteica

---

## 2. Requisitos Funcionales

### RF-001: Búsqueda de Genomas
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir buscar genomas en NCBI GenBank mediante diferentes criterios.

**Criterios de aceptación:**
- Búsqueda por nombre de organismo (ej: "Escherichia coli K-12 MG1655")
- Búsqueda por número de acceso (ej: "NC_000913.3")
- Búsqueda por taxonomía (género, especie)
- Mostrar resultados con información básica: nombre, tamaño, fecha de publicación
- Filtros por tamaño de genoma y tipo de molécula (DNA cromosómico, plásmido)

---

### RF-002: Descarga Automatizada de Genomas
**Prioridad:** Alta  
**Descripción:** El sistema debe descargar automáticamente archivos GenBank desde NCBI.

**Criterios de aceptación:**
- Descarga en formato GenBank (.gb, .gbk)
- Validación de integridad del archivo descargado
- Manejo de errores de conectividad con reintentos automáticos
- Verificación de que el organismo descargado corresponde al solicitado
- Almacenamiento temporal seguro del archivo
- Indicador de progreso de descarga

---

### RF-003: Análisis de Codones de Inicio (ATG)
**Prioridad:** Alta  
**Descripción:** Identificar y cuantificar todos los codones ATG en el genoma completo.

**Criterios de aceptación:**
- Conteo total de codones ATG en ambas hebras
- Cálculo de densidad de ATG por kilobase
- Comparación con número de genes anotados
- Identificación de posiciones de cada ATG
- Generación de gráfico de distribución de ATG a lo largo del genoma

---

### RF-004: Análisis de Codones de Terminación
**Prioridad:** Alta  
**Descripción:** Identificar y cuantificar los tres codones de terminación (TAA, TAG, TGA).

**Criterios de aceptación:**
- Conteo individual de cada tipo de codón de terminación
- Cálculo de proporciones relativas (%)
- Comparación con frecuencias reportadas en literatura
- Análisis de preferencia de uso de codones de terminación
- Tabla resumen con estadísticas

---

### RF-005: Extracción de Información de Genes
**Prioridad:** Alta  
**Descripción:** Extraer información de todos los genes anotados en el archivo GenBank.

**Criterios de aceptación:**
- Conteo total de genes
- Extracción de secuencias CDS (Coding DNA Sequences)
- Cálculo de longitud de cada gen
- Cálculo de contenido GC por gen
- Identificación de genes en hebra forward y reverse
- Extracción de metadatos (nombre del gen, producto, función)

---

### RF-006: Estadísticas Genómicas Globales
**Prioridad:** Alta  
**Descripción:** Calcular estadísticas generales del genoma completo.

**Criterios de aceptación:**
- Tamaño total del genoma (pares de bases)
- Contenido GC global (%)
- Densidad génica (% del genoma que codifica proteínas)
- Número total de genes
- Longitud promedio de genes
- Distribución de tamaños de genes (histograma)

---

### RF-007: Validación de Resultados
**Prioridad:** Media  
**Descripción:** Comparar resultados obtenidos con valores de referencia conocidos.

**Criterios de aceptación:**
- Base de datos de valores de referencia para genomas modelo (E. coli K-12, etc.)
- Cálculo de desviaciones porcentuales
- Alertas cuando desviaciones excedan umbrales (±5% para GC, ±10% para longitud génica)
- Sugerencias de posibles causas de discrepancias
- Indicador visual de validación (aprobado/advertencia/error)

---

### RF-008: Visualización de Datos
**Prioridad:** Alta  
**Descripción:** Generar gráficos profesionales de los resultados del análisis.

**Criterios de aceptación:**
- Gráfico de barras: frecuencia de codones de terminación
- Histograma: distribución de longitudes de genes
- Gráfico circular: proporción de codones de terminación
- Gráfico de línea: distribución de GC% a lo largo del genoma
- Mapa genómico simple mostrando ubicación de genes
- Todos los gráficos con títulos, ejes etiquetados y leyendas

---

### RF-009: Exportación de Resultados
**Prioridad:** Media  
**Descripción:** Permitir exportar resultados en múltiples formatos.

**Criterios de aceptación:**
- Exportación en formato JSON (datos estructurados)
- Exportación en formato CSV (tablas de datos)
- Exportación de gráficos en PNG de alta resolución
- Generación de reporte PDF completo con todos los análisis
- Descarga de archivo GenBank original analizado

---

### RF-010: Interfaz de Usuario Intuitiva
**Prioridad:** Alta  
**Descripción:** Proporcionar una interfaz web moderna y fácil de usar.

**Criterios de aceptación:**
- Diseño responsive (funciona en desktop, tablet, móvil)
- Flujo de trabajo claro: Buscar → Seleccionar → Analizar → Resultados
- Indicadores de progreso para operaciones largas
- Mensajes de error claros y accionables
- Ayuda contextual y tooltips explicativos
- Tema visual profesional y científico

---

## 3. Requisitos No Funcionales

### RNF-001: Rendimiento
- Descarga de genomas < 30 segundos para genomas bacterianos típicos (4-6 Mb)
- Análisis completo de E. coli K-12 (4.6 Mb) < 2 minutos
- Tiempo de respuesta de interfaz < 200ms para interacciones
- Generación de gráficos < 5 segundos

### RNF-002: Escalabilidad
- Soporte para genomas de hasta 15 Mb (bacterias grandes)
- Capacidad de procesar 10 análisis concurrentes
- Almacenamiento temporal de hasta 100 genomas

### RNF-003: Disponibilidad
- Disponibilidad del sistema: 95% (excluyendo mantenimiento programado)
- Manejo graceful de caídas de NCBI API
- Sistema de caché para genomas frecuentemente solicitados

### RNF-004: Usabilidad
- Interfaz en español e inglés
- Documentación completa de uso
- Ejemplos pre-cargados para demostración
- Curva de aprendizaje < 15 minutos para usuarios con conocimientos básicos de biología

### RNF-005: Seguridad
- Validación de entrada para prevenir inyección de código
- Límites de tamaño de archivo para prevenir ataques DoS
- Sanitización de nombres de archivo
- Rate limiting en API de NCBI (máximo 3 peticiones/segundo)

### RNF-006: Compatibilidad
- Navegadores: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- No requiere instalación de software adicional
- Compatible con lectores de pantalla (accesibilidad básica)

### RNF-007: Mantenibilidad
- Código modular y bien documentado
- Pruebas unitarias con cobertura > 70%
- Logs detallados de operaciones y errores
- Configuración mediante variables de entorno

### RNF-008: Portabilidad
- Despliegue en AWS, Google Cloud o Azure
- Contenedorización con Docker
- Base de datos portable (SQLite para desarrollo, PostgreSQL para producción)

---

## 4. Casos de Uso Principales

### CU-001: Análisis Completo de E. coli K-12
**Actor:** Estudiante de bioinformática  
**Precondiciones:** Ninguna  
**Flujo principal:**
1. Usuario accede a la plataforma
2. Busca "Escherichia coli K-12 MG1655"
3. Selecciona el genoma de la lista de resultados
4. Hace clic en "Analizar Genoma"
5. Sistema descarga el genoma desde NCBI
6. Sistema ejecuta todos los análisis automáticamente
7. Sistema muestra resultados con gráficos y estadísticas
8. Usuario revisa resultados y los compara con valores esperados
9. Usuario exporta reporte en PDF

**Postcondiciones:** Reporte completo generado y descargado

---

### CU-002: Comparación de Codones de Terminación
**Actor:** Investigador  
**Precondiciones:** Genoma ya descargado  
**Flujo principal:**
1. Usuario selecciona genoma previamente analizado
2. Navega a sección "Análisis de Codones"
3. Visualiza tabla de frecuencias de TAA, TAG, TGA
4. Compara proporciones con valores de referencia
5. Exporta datos en CSV para análisis adicional

**Postcondiciones:** Datos exportados para análisis estadístico externo

---

### CU-003: Validación de Resultados con Valores de Referencia
**Actor:** Profesor verificando trabajo de estudiantes  
**Precondiciones:** Análisis completado  
**Flujo principal:**
1. Usuario revisa sección "Validación"
2. Sistema muestra comparación con E. coli K-12 de referencia
3. Sistema indica desviaciones con códigos de color
4. Usuario identifica discrepancias
5. Sistema sugiere posibles causas

**Postcondiciones:** Validación completada y documentada

---

## 5. Restricciones y Suposiciones

### Restricciones
- Dependencia de disponibilidad de NCBI API
- Límites de rate limiting de NCBI (3 peticiones/segundo)
- Enfoque en genomas bacterianos (procariotas)
- No requiere autenticación de usuarios (sistema abierto)
- Almacenamiento temporal limitado (archivos eliminados después de 24 horas)

### Suposiciones
- Usuarios tienen conocimientos básicos de biología molecular
- Conexión a internet estable
- Genomas en NCBI están correctamente anotados
- Usuarios utilizan navegadores modernos actualizados
- Análisis se realiza en genomas completos, no en borradores (drafts)

---

## 6. Dependencias Externas

### APIs y Servicios
- **NCBI Entrez API:** Búsqueda y descarga de genomas
- **NCBI E-utilities:** Acceso programático a bases de datos

### Librerías y Frameworks
- **BioPython:** Parsing de archivos GenBank, análisis de secuencias
- **Pandas:** Manipulación de datos tabulares
- **Matplotlib/Plotly:** Generación de gráficos
- **Flask/FastAPI:** Backend web
- **React/Vue:** Frontend interactivo

---

## 7. Criterios de Éxito del Proyecto

1. **Funcionalidad Completa:** Todos los análisis requeridos implementados y funcionando
2. **Precisión:** Resultados coinciden con valores de referencia (±2% para E. coli K-12)
3. **Usabilidad:** Estudiantes pueden completar análisis completo en < 10 minutos
4. **Rendimiento:** Análisis de genoma bacteriano típico < 2 minutos
5. **Documentación:** Guía de usuario completa y documentación técnica
6. **Reproducibilidad:** Mismos inputs producen mismos outputs consistentemente
7. **Adopción:** Al menos 20 estudiantes utilizan exitosamente la plataforma

---

## 8. Glosario de Términos

- **ATG:** Codón de inicio de traducción (Metionina)
- **TAA, TAG, TGA:** Codones de terminación (stop codons)
- **CDS:** Coding DNA Sequence (secuencia codificante)
- **GenBank:** Base de datos de secuencias genéticas de NCBI
- **GC%:** Porcentaje de guanina y citosina en el genoma
- **Densidad génica:** Proporción del genoma que codifica genes
- **NCBI:** National Center for Biotechnology Information
- **BioPython:** Librería de Python para bioinformática
- **Número de acceso:** Identificador único de secuencia en GenBank (ej: NC_000913.3)

---

## 9. Priorización de Requisitos

### Fase 1 - MVP (Producto Mínimo Viable)
- RF-001: Búsqueda de genomas
- RF-002: Descarga automatizada
- RF-003: Análisis de codones ATG
- RF-004: Análisis de codones de terminación
- RF-005: Extracción de genes
- RF-006: Estadísticas genómicas
- RF-010: Interfaz básica

### Fase 2 - Mejoras
- RF-007: Validación de resultados
- RF-008: Visualizaciones avanzadas
- RF-009: Exportación múltiples formatos

### Fase 3 - Optimizaciones
- Sistema de caché
- Análisis comparativos
- Optimizaciones de rendimiento
