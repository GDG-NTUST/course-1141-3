<div align="center">

# 🎓 GDG Course Query & Animation Demo 🎓

[<img src=".github/assets/gdg-logo.png" width="400" alt="GDG | NTUST">](https://gdg-ntust.org/)

<br>[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=ffffff)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.12+-e92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://pydantic.dev/)

**English** | [繁體中文](README_zh-TW.md)

</div>

## Overview

This project is a tutorial demonstration of a course query system, featuring a **FastAPI-based backend** and a **real-time terminal animation client**. It demonstrates how to interact with external APIs, manage data simulation, and create engaging command-line visualizations.

### Technical Highlights

- ⚡ **FastAPI Backend** - High-performance asynchronous API for course data management.
- 🔄 **Real-time Simulation** - Background worker for simulating enrollment changes.
- 🎨 **Terminal Animation** - Dynamic terminal UI with color-coded enrollment tracking.
- 🛠️ **Modern Tooling** - Dependency management with `uv`, type safety with `Pydantic`.
- 🌐 **Async HTTP** - Efficient external API calls using `httpx`.

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (recommended package manager)

### Installation

```bash
# Install uv package manager
pip install uv

# Clone the repository
git clone https://github.com/GDG-NTUST/course-1141-3.git
cd course-1141-3

# Install dependencies
uv sync
```

### Running the Project

The project consists of two main components that should be run in separate terminals.

#### 1. Start the Backend Server

The backend provides the course data API and handles simulations.

```bash
# Using uv script
uv run backend

# Or directly running the module
python src/backend/backend.py
```
The server will be available at `http://localhost:8000`.

#### 2. Start the Animation Client

The client fetches data from the backend and displays it with animations.

```bash
# Using uv script
uv run animate

# Or directly running the file
python src/animate.py
```

## Usage

### Backend API

- **Root:** `GET /` - Welcome message.
- **Health Check:** `GET /healthz` - System status.
- **Course Query:** `POST /QueryCourse/api//courses` - Search for courses using criteria.

### Animation Client

The terminal client provides a live view of courses:
- **Yellow:** Current enrollment count.
- **Red (+):** Enrollment increased since the last update.
- **Green (-):** Enrollment decreased since the last update.
- **Cyan:** Course number and name.

## Project Architecture

```
course-1141-3/
├── src/
│   ├── backend/
│   │   └── backend.py    # FastAPI server & Data logic
│   └── animate.py        # Terminal visualization client
├── pyproject.toml        # Project configuration & dependencies
└── README.md             # Project documentation
```

### Key Components

- **`backend.py`**: 
  - Implements `CourseRepository` for data fetching and in-memory storage.
  - Features a `simulation_worker` that randomly updates course enrollment to demonstrate real-time tracking.
  - Uses FastAPI `lifespan` for managed startup and shutdown.
- **`animate.py`**:
  - Implements a polling loop to fetch data from the backend.
  - Uses `colorama` for cross-platform terminal coloring.
  - Uses `wcwidth` to ensure correct alignment for multi-byte characters (Chinese).

## License

This project is licensed under the [MIT License](LICENSE)

---

<div align="center">

Made with ❤️ by [GDG NTUST](https://gdg-ntust.org/)

</div>
