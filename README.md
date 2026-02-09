# 🧬 Plataforma de Análisis Genómico

> Aplicación web de bioinformática para análisis automatizado de genomas bacterianos con integración directa a NCBI GenBank.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)

---

## 📋 Descripción del Proyecto

Esta plataforma web permite a estudiantes e investigadores realizar análisis bioinformáticos completos de genomas bacterianos sin necesidad de conocimientos avanzados de programación. El sistema se conecta directamente con NCBI GenBank para descargar genomas y ejecutar análisis computacionales automatizados.

### Características Principales

✨ **Búsqueda Inteligente**: Busca genomas en NCBI GenBank por nombre de organismo o número de acceso  
🔬 **Análisis Automatizado**: Análisis completo de codones, genes y estadísticas genómicas  
📊 **Visualizaciones Profesionales**: Gráficos interactivos de alta calidad con Plotly  
✅ **Validación de Resultados**: Comparación automática con valores de referencia científicos  
📄 **Exportación Múltiple**: Exporta resultados en JSON, CSV y PDF  
🚀 **Sin Registro**: Acceso directo sin necesidad de crear cuenta  

---

## 🎯 Casos de Uso

### Para Estudiantes
- Aprender bioinformática aplicada con ejemplos reales
- Completar proyectos de análisis genómico
- Validar resultados con literatura científica
- Generar reportes profesionales para entregas

### Para Investigadores
- Análisis rápido de genomas bacterianos
- Comparación de estadísticas genómicas
- Generación de figuras para publicaciones
- Validación de anotaciones genómicas

### Para Profesores
- Herramienta educativa para cursos de bioinformática
- Plataforma para asignaciones prácticas
- Demostración de conceptos de genómica
- Evaluación de comprensión de análisis genómico

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────┐
│   Usuario   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│     Frontend (React + TypeScript)   │
│  - Búsqueda de genomas              │
│  - Visualización de resultados      │
│  - Gráficos interactivos            │
└──────────────┬──────────────────────┘
               │ HTTP/REST
               ▼
┌─────────────────────────────────────┐
│      Backend API (FastAPI)          │
│  - Endpoints REST                   │
│  - Validación de requests           │
│  - Orquestación de servicios        │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌─────────────┐  ┌─────────────┐
│   Celery    │  │    NCBI     │
│   Workers   │  │  Entrez API │
│  - Análisis │  │  - Búsqueda │
│  - Descarga │  │  - Descarga │
└──────┬──────┘  └─────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│         Capa de Datos               │
│  - PostgreSQL (metadatos)           │
│  - Redis (caché)                    │
│  - File Storage (genomas)           │
└─────────────────────────────────────┘
```

**Documentación completa:** Ver [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🔬 Análisis Implementados

### 1. Análisis de Codones de Inicio (ATG)
- Conteo total de codones ATG en el genoma
- Densidad de ATG por kilobase
- Comparación con número de genes anotados
- Distribución a lo largo del genoma

### 2. Análisis de Codones de Terminación
- Conteo de TAA, TAG, TGA
- Proporciones relativas de cada codón
- Comparación con frecuencias reportadas en literatura
- Análisis de preferencia de uso

### 3. Análisis de Genes
- Extracción de genes anotados (CDS)
- Cálculo de longitud de genes
- Contenido GC por gen
- Estadísticas descriptivas (promedio, mediana, min, max)

### 4. Estadísticas Genómicas
- Tamaño total del genoma
- Contenido GC global
- Densidad génica
- Número total de genes
- Distribución de tamaños de genes

### 5. Validación de Resultados
- Comparación con genomas de referencia
- Cálculo de desviaciones porcentuales
- Alertas de discrepancias significativas
- Indicadores visuales de validación

---

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: FastAPI 0.104 (Python 3.11)
- **Base de Datos**: PostgreSQL 15
- **Caché**: Redis 7
- **Task Queue**: Celery 5.3
- **Bioinformática**: BioPython 1.81
- **Análisis de Datos**: Pandas, NumPy
- **Visualización**: Matplotlib, Plotly

### Frontend
- **Framework**: React 18.2 con TypeScript 5.0
- **Estado**: Redux Toolkit
- **UI**: Material-UI 5
- **Gráficos**: Plotly.js
- **HTTP Client**: Axios
- **Build Tool**: Vite 4

### DevOps
- **Contenedores**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoreo**: Prometheus + Grafana
- **Logs**: ELK Stack

---

## 📁 Estructura del Proyecto

```
Analisis-Genomico/
├── backend/              # API FastAPI y servicios de análisis
├── frontend/             # Aplicación React
├── data/                 # Almacenamiento de genomas y resultados
├── tests/                # Suite de tests (unitarios + integración)
├── devops/               # Docker, Kubernetes, Terraform
├── design/               # Wireframes, mockups, diagramas
├── docs/                 # Documentación completa
├── logs/                 # Logs de aplicación
├── config/               # Configuración por entorno
└── scripts/              # Scripts de utilidad
```

**Documentación completa:**
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Estructura de directorios
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guía de despliegue y testing
- [docs/api.md](docs/api.md) - Documentación de API

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker 20.10+ y Docker Compose 2.0+
- Git
- (Opcional) Python 3.11+ y Node.js 18+ para desarrollo local

### Instalación con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/Analisis-Genomico.git
   cd Analisis-Genomico
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tu email de NCBI
   ```

3. **Iniciar servicios**
   ```bash
   cd devops/docker
   docker-compose up -d
   ```

4. **Acceder a la aplicación**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Instalación Local (Desarrollo)

#### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

---

## 📖 Uso de la Plataforma

### 1. Buscar un Genoma

1. Ingresa el nombre del organismo o número de acceso en el buscador
   - Ejemplo: "Escherichia coli K-12 MG1655"
   - Ejemplo: "NC_000913.3"

2. Selecciona el genoma de los resultados

### 2. Iniciar Análisis

1. Haz clic en "Analizar Genoma"
2. El sistema descargará automáticamente el genoma desde NCBI
3. Se ejecutarán todos los análisis en segundo plano
4. Verás una barra de progreso con el estado actual

### 3. Visualizar Resultados

Una vez completado el análisis, verás:

- **Estadísticas Generales**: Tamaño, GC%, número de genes
- **Análisis de Codones**: Gráficos de frecuencias
- **Análisis de Genes**: Distribución de longitudes, contenido GC
- **Validación**: Comparación con valores de referencia

### 4. Exportar Resultados

- **JSON**: Datos estructurados para análisis adicional
- **CSV**: Tablas para Excel/R/Python
- **PDF**: Reporte completo con gráficos

---

## 📊 Ejemplo de Análisis: E. coli K-12 MG1655

### Resultados Esperados

| Métrica | Valor Esperado | Tolerancia |
|---------|----------------|------------|
| Tamaño del genoma | 4,641,652 bp | ±1% |
| Contenido GC | 50.8% | ±0.5% |
| Número de genes | ~4,300 | ±5% |
| Longitud promedio de genes | ~950 bp | ±10% |
| TAA (stop codon) | ~61% | ±5% |
| TAG (stop codon) | ~9% | ±5% |
| TGA (stop codon) | ~30% | ±5% |

### Tiempo de Análisis

- Descarga: ~10-20 segundos
- Análisis completo: ~1-2 minutos
- Generación de gráficos: ~5 segundos

---

## 🧪 Testing

### Ejecutar Tests Backend

```bash
cd backend

# Tests unitarios
pytest tests/unit/ -v

# Tests de integración
pytest tests/integration/ -v

# Cobertura
pytest --cov=app --cov-report=html
```

### Ejecutar Tests Frontend

```bash
cd frontend

# Tests unitarios
npm run test

# Tests E2E
npm run test:e2e
```

---

## 📚 Documentación

- **[REQUIREMENTS.md](REQUIREMENTS.md)**: Requisitos funcionales y no funcionales completos
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Arquitectura del sistema con diagramas
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)**: Estructura de directorios detallada
- **[Implementation Plan](docs/implementation_plan.md)**: Plan de implementación por fases
- **[API Documentation](http://localhost:8000/docs)**: Documentación interactiva de API (cuando el servidor esté corriendo)

---

## 🔧 Configuración

### Variables de Entorno Principales

```bash
# Backend
DATABASE_URL=postgresql://user:pass@localhost:5432/genomics_db
REDIS_URL=redis://localhost:6379/0
NCBI_EMAIL=tu-email@example.com  # Requerido por NCBI
NCBI_API_KEY=tu-api-key           # Opcional, aumenta rate limit

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
```

### Configuración de NCBI

Para usar la API de NCBI necesitas:

1. **Email**: Requerido por las políticas de NCBI
2. **API Key** (opcional): Aumenta el rate limit de 3 a 10 requests/segundo
   - Obtener en: https://www.ncbi.nlm.nih.gov/account/settings/

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Seguir PEP 8 para código Python
- Usar TypeScript strict mode para código frontend
- Escribir tests para nuevas funcionalidades
- Actualizar documentación según sea necesario

---

## 🐛 Reporte de Bugs

Si encuentras un bug, por favor abre un issue con:

- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs. actual
- Screenshots (si aplica)
- Información del entorno (OS, versión de navegador, etc.)

---

## 📝 Roadmap

### Fase 1 - MVP (Actual)
- ✅ Búsqueda y descarga de genomas
- ✅ Análisis de codones y genes
- ✅ Visualizaciones básicas
- ✅ Exportación de resultados

### Fase 2 - Mejoras (Próximo)
- [ ] Análisis comparativo de múltiples genomas
- [ ] Visualización de genomas circulares
- [ ] Anotación automática de genes
- [ ] Integración con UniProt y KEGG

### Fase 3 - Avanzado (Futuro)
- [ ] Machine Learning para predicción de genes
- [ ] Análisis filogenético
- [ ] Colaboración multi-usuario
- [ ] API pública para terceros

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 👥 Autores

- **Equipo de Desarrollo** - Plataforma de Análisis Genómico

---

## 🙏 Agradecimientos

- **NCBI** por proporcionar acceso gratuito a GenBank
- **BioPython** por las herramientas de bioinformática
- **FastAPI** y **React** por los excelentes frameworks
- Comunidad de bioinformática open source

---

## 📞 Contacto

- **Email**: soporte@genomics-platform.com
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/Analisis-Genomico/issues)
- **Documentación**: [Wiki del Proyecto](https://github.com/tu-usuario/Analisis-Genomico/wiki)

---

## 🔗 Enlaces Útiles

- [NCBI GenBank](https://www.ncbi.nlm.nih.gov/genbank/)
- [BioPython Tutorial](https://biopython.org/wiki/Documentation)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Material-UI](https://mui.com/)

---

<div align="center">

**¿Te gusta el proyecto? Dale una ⭐ en GitHub!**

[Reportar Bug](https://github.com/tu-usuario/Analisis-Genomico/issues) · [Solicitar Feature](https://github.com/tu-usuario/Analisis-Genomico/issues) · [Documentación](docs/)

</div>
