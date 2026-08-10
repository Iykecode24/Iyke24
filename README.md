# IYKE CONTENT STUDIO

> AI-Powered Content Production Platform

Create complete movies, children's cartoons, explainer videos, news videos, image-to-video animations, and product advertisements from simple instructions.

![License](https://img.shields.io/badge/license-proprietary-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)

---

## Features

- 🎬 **AI Movie Studio** — Generate complete movies from a title and story idea
- 🧸 **Children's Cartoon Studio** — Create educational cartoons for YouTube
- 📚 **Explainer Video Studio** — Build tutorials and presentations
- 📰 **News Video Studio** — Transform articles into anchor-led news videos
- 🖼️ **Image-to-Video Studio** — Animate photographs with motion controls
- 📢 **Advertisement Studio** — Create product ads from images or links
- 🎭 **Character Consistency** — Maintain character identity across scenes
- 🗣️ **Voice Generation** — ElevenLabs integration with multilingual support
- 👄 **Lip Synchronization** — Match speech to character mouth movements
- 🎞️ **Video Enhancement** — Upscaling, face restoration, frame interpolation
- ☁️ **Cloud Rendering** — RunPod GPU integration with cost controls
- 📱 **Social Publishing** — Publish to YouTube, TikTok, Instagram, and more

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Next.js 15    │────▶│   FastAPI         │────▶│   PostgreSQL    │
│   Frontend      │     │   Backend         │     │   + Redis       │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
              ┌──────────┐ ┌────────┐ ┌──────────┐
              │  RunPod   │ │OpenAI  │ │ElevenLabs│
              │  GPU      │ │  LLM   │ │  Voice   │
              └──────────┘ └────────┘ └──────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15, TypeScript, Tailwind CSS |
| Backend | Python FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Database | PostgreSQL 16 |
| Cache & Queue | Redis 7, Celery |
| GPU Rendering | RunPod (Pods + Serverless) |
| AI Models | OpenAI, FLUX, Stable Diffusion, Wan2.1, HunyuanVideo |
| Voice | ElevenLabs, Open-source TTS |
| Storage | Cloudflare R2 (S3-compatible) |
| Media Processing | FFmpeg |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local frontend development)
- Python 3.12+ (for local backend development)

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd iyke-content-studio
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start with Docker Compose:**
   ```bash
   docker compose up -d
   ```

4. **Run database migrations:**
   ```bash
   docker compose exec backend alembic upgrade head
   ```

5. **Access the application:**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Local Development (without Docker)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Configuration

All configuration is done through environment variables. See `.env.example` for all available options.

### Required API Keys

| Service | Purpose | Required |
|---------|---------|----------|
| OpenAI | Script generation, AI orchestration | Yes |
| ElevenLabs | Voice generation | Optional |
| RunPod | GPU rendering | For video generation |
| Cloud Storage | Media file storage | For production |

API keys are configured through the Admin Settings panel — never stored in code.

## Project Structure

```
iyke-content-studio/
├── frontend/          # Next.js 15 application
├── backend/           # FastAPI application
├── runpod-worker/     # RunPod GPU worker
├── docs/              # Documentation
├── docker-compose.yml # Local development stack
└── .env.example       # Environment template
```

## Security

- All API keys encrypted at rest (Fernet)
- JWT authentication with refresh tokens
- Role-based access control (Admin/Creator/Editor/Viewer)
- MFA support (TOTP)
- Rate limiting
- Input validation and sanitization
- Content safety filtering
- CSRF and XSS protection
- Audit logging

## Documentation

- [Deployment Guide](docs/deployment.md)
- [API Documentation](docs/api-docs.md)
- [Admin Manual](docs/admin-manual.md)
- [User Manual](docs/user-manual.md)
- [Security Checklist](docs/security-checklist.md)
- [Troubleshooting](docs/troubleshooting.md)

## License

Proprietary — All rights reserved.

---

Built with ❤️ by **IYKE CONTENT STUDIO**
