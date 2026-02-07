# Estructura del Proyecto - Plataforma de Análisis Genómico

## Organización de Directorios

```
Analisis-Genomico/
│
├── backend/                          # Backend API y servicios
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # Entry point FastAPI
│   │   │
│   │   ├── api/                      # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py       # Dependencias compartidas
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py         # Router principal v1
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── genomes.py    # Endpoints de búsqueda/descarga
│   │   │           ├── analysis.py   # Endpoints de análisis
│   │   │           ├── results.py    # Endpoints de resultados
│   │   │           ├── validation.py # Endpoints de validación
│   │   │           └── health.py     # Health checks
│   │   │
│   │   ├── core/                     # Configuración central
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # Settings y configuración
│   │   │   ├── security.py           # Rate limiting, CORS
│   │   │   ├── logging.py            # Configuración de logs
│   │   │   └── exceptions.py         # Excepciones personalizadas
│   │   │
│   │   ├── models/                   # Modelos SQLAlchemy
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # Base model
│   │   │   ├── genome.py             # Modelo Genome
│   │   │   ├── analysis.py           # Modelo Analysis
│   │   │   ├── result.py             # Modelo Result
│   │   │   └── validation.py         # Modelo Validation
│   │   │
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── genome.py             # Schemas de genoma
│   │   │   ├── analysis.py           # Schemas de análisis
│   │   │   ├── result.py             # Schemas de resultados
│   │   │   └── validation.py         # Schemas de validación
│   │   │
│   │   ├── services/                 # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── ncbi_service.py       # Interacción con NCBI
│   │   │   ├── analysis_service.py   # Orquestación de análisis
│   │   │   ├── validation_service.py # Validación de resultados
│   │   │   └── export_service.py     # Exportación de datos
│   │   │
│   │   ├── analyzers/                # Módulos de análisis bioinformático
│   │   │   ├── __init__.py
│   │   │   ├── base_analyzer.py      # Clase base
│   │   │   ├── codon_analyzer.py     # Análisis de codones
│   │   │   ├── gene_analyzer.py      # Análisis de genes
│   │   │   ├── genome_analyzer.py    # Estadísticas genómicas
│   │   │   └── visualization.py      # Generación de gráficos
│   │   │
│   │   ├── tasks/                    # Tareas Celery
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py         # Configuración Celery
│   │   │   ├── download_tasks.py     # Tareas de descarga
│   │   │   └── analysis_tasks.py     # Tareas de análisis
│   │   │
│   │   ├── db/                       # Database setup
│   │   │   ├── __init__.py
│   │   │   ├── session.py            # Database session
│   │   │   └── base.py               # Base declarativa
│   │   │
│   │   └── utils/                    # Utilidades
│   │       ├── __init__.py
│   │       ├── file_utils.py         # Manejo de archivos
│   │       ├── validators.py         # Validadores
│   │       └── formatters.py         # Formateadores
│   │
│   ├── alembic/                      # Migraciones de BD
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   │
│   ├── requirements.txt              # Dependencias Python
│   ├── requirements-dev.txt          # Dependencias de desarrollo
│   ├── Dockerfile                    # Docker para backend
│   └── .env.example                  # Variables de entorno ejemplo
│
├── frontend/                         # Frontend React
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── assets/
│   │       └── images/
│   │
│   ├── src/
│   │   ├── main.tsx                  # Entry point
│   │   ├── App.tsx                   # Componente principal
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── components/               # Componentes React
│   │   │   ├── common/               # Componentes comunes
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Footer.tsx
│   │   │   │   ├── LoadingSpinner.tsx
│   │   │   │   ├── ErrorBoundary.tsx
│   │   │   │   └── Notification.tsx
│   │   │   │
│   │   │   ├── search/               # Búsqueda de genomas
│   │   │   │   ├── GenomeSearch.tsx
│   │   │   │   ├── SearchResults.tsx
│   │   │   │   ├── SearchFilters.tsx
│   │   │   │   └── GenomeCard.tsx
│   │   │   │
│   │   │   ├── analysis/             # Control de análisis
│   │   │   │   ├── AnalysisPanel.tsx
│   │   │   │   ├── ProgressIndicator.tsx
│   │   │   │   ├── AnalysisControls.tsx
│   │   │   │   └── AnalysisHistory.tsx
│   │   │   │
│   │   │   ├── results/              # Visualización de resultados
│   │   │   │   ├── ResultsDashboard.tsx
│   │   │   │   ├── CodonAnalysis.tsx
│   │   │   │   ├── GeneStatistics.tsx
│   │   │   │   ├── GenomeStats.tsx
│   │   │   │   └── ValidationPanel.tsx
│   │   │   │
│   │   │   └── visualization/        # Gráficos y visualizaciones
│   │   │       ├── CodonChart.tsx
│   │   │       ├── GeneLengthHistogram.tsx
│   │   │       ├── GCContentPlot.tsx
│   │   │       ├── GenomeMap.tsx
│   │   │       └── ExportControls.tsx
│   │   │
│   │   ├── pages/                    # Páginas principales
│   │   │   ├── HomePage.tsx
│   │   │   ├── SearchPage.tsx
│   │   │   ├── AnalysisPage.tsx
│   │   │   ├── ResultsPage.tsx
│   │   │   └── NotFoundPage.tsx
│   │   │
│   │   ├── services/                 # Servicios API
│   │   │   ├── api.ts                # Cliente Axios configurado
│   │   │   ├── genomeService.ts      # Servicios de genoma
│   │   │   ├── analysisService.ts    # Servicios de análisis
│   │   │   └── exportService.ts      # Servicios de exportación
│   │   │
│   │   ├── store/                    # Redux store
│   │   │   ├── store.ts              # Configuración store
│   │   │   └── slices/
│   │   │       ├── genomeSlice.ts
│   │   │       ├── analysisSlice.ts
│   │   │       └── uiSlice.ts
│   │   │
│   │   ├── types/                    # TypeScript types
│   │   │   ├── genome.types.ts
│   │   │   ├── analysis.types.ts
│   │   │   ├── result.types.ts
│   │   │   └── api.types.ts
│   │   │
│   │   ├── hooks/                    # Custom hooks
│   │   │   ├── useGenomeSearch.ts
│   │   │   ├── useAnalysis.ts
│   │   │   └── usePolling.ts
│   │   │
│   │   ├── utils/                    # Utilidades
│   │   │   ├── formatters.ts
│   │   │   ├── validators.ts
│   │   │   └── constants.ts
│   │   │
│   │   └── styles/                   # Estilos globales
│   │       ├── theme.ts              # Tema MUI
│   │       ├── global.css
│   │       └── variables.css
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .env.example
│
├── data/                             # Datos y almacenamiento
│   ├── genomes/                      # Genomas descargados
│   │   └── .gitkeep
│   ├── results/                      # Resultados de análisis
│   │   └── .gitkeep
│   ├── exports/                      # Exportaciones (PDF, CSV)
│   │   └── .gitkeep
│   ├── cache/                        # Caché temporal
│   │   └── .gitkeep
│   └── reference/                    # Datos de referencia
│       └── reference_genomes.json    # Valores de referencia
│
├── tests/                            # Tests
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── conftest.py               # Fixtures pytest
│   │   │
│   │   ├── unit/                     # Tests unitarios
│   │   │   ├── test_analyzers/
│   │   │   │   ├── test_codon_analyzer.py
│   │   │   │   ├── test_gene_analyzer.py
│   │   │   │   └── test_genome_analyzer.py
│   │   │   ├── test_services/
│   │   │   │   ├── test_ncbi_service.py
│   │   │   │   ├── test_analysis_service.py
│   │   │   │   └── test_validation_service.py
│   │   │   └── test_utils/
│   │   │       └── test_validators.py
│   │   │
│   │   ├── integration/              # Tests de integración
│   │   │   ├── test_api/
│   │   │   │   ├── test_genomes_endpoints.py
│   │   │   │   ├── test_analysis_endpoints.py
│   │   │   │   └── test_results_endpoints.py
│   │   │   └── test_workflows/
│   │   │       └── test_full_analysis_workflow.py
│   │   │
│   │   └── fixtures/                 # Datos de prueba
│   │       ├── sample_genbank.gb
│   │       └── expected_results.json
│   │
│   └── frontend/
│       ├── setup.ts                  # Setup Vitest
│       ├── unit/
│       │   ├── components/
│       │   │   └── GenomeSearch.test.tsx
│       │   └── services/
│       │       └── genomeService.test.ts
│       └── e2e/
│           └── analysis-workflow.spec.ts
│
├── devops/                           # DevOps y deployment
│   ├── docker/
│   │   ├── docker-compose.yml        # Compose para desarrollo
│   │   ├── docker-compose.prod.yml   # Compose para producción
│   │   └── nginx/
│   │       └── nginx.conf            # Configuración Nginx
│   │
│   ├── kubernetes/                   # Manifiestos K8s (futuro)
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   │
│   ├── terraform/                    # Infrastructure as Code
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── scripts/
│       ├── deploy.sh                 # Script de deployment
│       ├── backup.sh                 # Backup de BD
│       └── restore.sh                # Restore de BD
│
├── design/                           # Diseño y assets
│   ├── wireframes/
│   │   ├── home-page.png
│   │   ├── search-page.png
│   │   └── results-page.png
│   │
│   ├── mockups/
│   │   └── ui-design.fig             # Archivo Figma
│   │
│   └── diagrams/
│       ├── architecture-diagram.png
│       ├── data-flow-diagram.png
│       └── er-diagram.png
│
├── docs/                             # Documentación del sistema
│   ├── README.md                     # Documentación principal
│   ├── REQUIREMENTS.md               # Requisitos del sistema
│   ├── ARCHITECTURE.md               # Arquitectura del sistema
│   ├── API.md                        # Documentación de API
│   ├── DEPLOYMENT.md                 # Guía de deployment
│   ├── DEVELOPMENT.md                # Guía de desarrollo
│   ├── USER_GUIDE.md                 # Guía de usuario
│   │
│   ├── api/                          # Documentación API detallada
│   │   ├── endpoints.md
│   │   ├── schemas.md
│   │   └── examples.md
│   │
│   └── tutorials/                    # Tutoriales
│       ├── getting-started.md
│       ├── running-analysis.md
│       └── interpreting-results.md
│
├── logs/                             # Logs de aplicación
│   ├── backend/
│   │   ├── app.log
│   │   ├── celery.log
│   │   └── error.log
│   ├── frontend/
│   │   └── access.log
│   └── .gitkeep
│
├── config/                           # Archivos de configuración
│   ├── development/
│   │   ├── backend.env
│   │   └── frontend.env
│   ├── production/
│   │   ├── backend.env.example
│   │   └── frontend.env.example
│   └── reference_data/
│       └── known_genomes.json        # Genomas de referencia
│
├── scripts/                          # Scripts de utilidad
│   ├── setup/
│   │   ├── init_db.py                # Inicializar base de datos
│   │   ├── seed_reference_data.py    # Cargar datos de referencia
│   │   └── check_dependencies.sh     # Verificar dependencias
│   │
│   ├── maintenance/
│   │   ├── cleanup_old_files.py      # Limpiar archivos antiguos
│   │   └── update_reference_data.py  # Actualizar referencias
│   │
│   └── development/
│       ├── run_dev.sh                # Iniciar entorno desarrollo
│       └── run_tests.sh              # Ejecutar todos los tests
│
├── .github/                          # GitHub workflows
│   └── workflows/
│       ├── ci.yml                    # Continuous Integration
│       ├── cd.yml                    # Continuous Deployment
│       └── tests.yml                 # Tests automatizados
│
├── .gitignore                        # Git ignore
├── .env.example                      # Variables de entorno ejemplo
├── README.md                         # README principal del proyecto
├── LICENSE                           # Licencia del proyecto
└── CHANGELOG.md                      # Registro de cambios

```

## Descripción de Directorios Principales

### `/backend` - Backend API
Contiene toda la lógica del servidor, API REST, servicios de análisis bioinformático, y tareas asíncronas. Organizado siguiendo principios de Clean Architecture.

### `/frontend` - Frontend Web
Aplicación React con TypeScript para la interfaz de usuario. Incluye componentes, páginas, servicios API, y gestión de estado.

### `/data` - Almacenamiento de Datos
Directorio para almacenar genomas descargados, resultados de análisis, exportaciones, y datos de referencia. No versionado en Git (excepto .gitkeep).

### `/tests` - Suite de Tests
Tests unitarios, de integración, y end-to-end para backend y frontend. Incluye fixtures y datos de prueba.

### `/devops` - DevOps y Deployment
Configuraciones de Docker, Kubernetes, Terraform, y scripts de deployment. Infraestructura como código.

### `/design` - Diseño y Assets
Wireframes, mockups, diagramas de arquitectura, y otros assets de diseño.

### `/docs` - Documentación
Documentación completa del sistema: requisitos, arquitectura, API, guías de usuario y desarrollo.

### `/logs` - Logs de Aplicación
Archivos de log generados por la aplicación. No versionados en Git.

### `/config` - Configuración
Archivos de configuración para diferentes entornos (desarrollo, producción) y datos de referencia.

### `/scripts` - Scripts de Utilidad
Scripts para setup inicial, mantenimiento, y desarrollo.

## Archivos de Configuración Clave

### Backend
- `backend/requirements.txt` - Dependencias Python
- `backend/Dockerfile` - Imagen Docker del backend
- `backend/.env.example` - Variables de entorno

### Frontend
- `frontend/package.json` - Dependencias Node.js
- `frontend/vite.config.ts` - Configuración Vite
- `frontend/tsconfig.json` - Configuración TypeScript

### DevOps
- `devops/docker/docker-compose.yml` - Orquestación de contenedores
- `.github/workflows/ci.yml` - Pipeline CI/CD

## Convenciones de Nombres

- **Archivos Python:** snake_case (ej: `codon_analyzer.py`)
- **Archivos TypeScript/React:** PascalCase para componentes (ej: `GenomeSearch.tsx`), camelCase para utilidades (ej: `formatters.ts`)
- **Directorios:** lowercase con guiones (ej: `reference-data/`) o snake_case
- **Variables de entorno:** UPPER_SNAKE_CASE (ej: `DATABASE_URL`)
- **Constantes:** UPPER_SNAKE_CASE
- **Funciones/métodos:** snake_case (Python), camelCase (TypeScript)
- **Clases:** PascalCase

## Gestión de Versiones

- **Backend API:** Versionado en URL (`/api/v1/`)
- **Frontend:** Versionado semántico en `package.json`
- **Base de datos:** Migraciones con Alembic
- **Docker images:** Tags semánticos (ej: `1.0.0`, `1.0.0-beta`)

## Seguridad

- **Secretos:** Nunca en código, usar variables de entorno
- **`.env` files:** No versionados, solo `.env.example`
- **Datos sensibles:** En `/data` (no versionado)
- **Logs:** En `/logs` (no versionado)

## Próximos Pasos

1. Crear estructura de directorios
2. Configurar entornos de desarrollo
3. Implementar backend API básico
4. Desarrollar frontend inicial
5. Integrar servicios NCBI
6. Implementar análisis bioinformáticos
7. Crear suite de tests
8. Configurar CI/CD
9. Deployment inicial
