# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Self-hosted AI Package - A Docker Compose template that bootstraps a local AI and low-code development environment. Combines n8n workflow automation with local LLMs via Ollama, Supabase for database/auth, and supporting services.

## Starting Services

All services run under a single Docker Compose project named "localai".

```bash
# Start with GPU (NVIDIA)
python start_services.py --profile gpu-nvidia

# Start with CPU only
python start_services.py --profile cpu

# Start without Ollama (for Mac users running Ollama natively)
python start_services.py --profile none
```

## Stopping and Upgrading

```bash
# Stop services
docker compose -p localai -f docker-compose.yml --profile <profile> down

# Upgrade containers
docker compose -p localai -f docker-compose.yml --profile <profile> pull
python start_services.py --profile <profile>
```

## Architecture

### Docker Compose Structure
- `docker-compose.yml` - Main compose file that includes Supabase and defines all AI services
- `supabase/docker/docker-compose.yml` - Supabase stack (auto-cloned from GitHub on first run)

### Core Services and Ports
| Service | Port | Purpose |
|---------|------|---------|
| n8n | 5678 | Workflow automation |
| Supabase Kong (API) | 8000 | Supabase API gateway |
| Ollama | 11434 | Local LLM inference |
| Qdrant | 6333 | Vector database |
| Flowise | 3007 | Low-code AI agent builder |
| Neo4j | 7474/7687 | Graph database |

### Key Files
- `start_services.py` - Orchestrates startup: clones Supabase repo, copies .env, starts services

## Environment Configuration

Copy `.env.example` to `.env` and set required secrets:
- N8N: `N8N_ENCRYPTION_KEY`, `N8N_USER_MANAGEMENT_JWT_SECRET`
- Supabase: `POSTGRES_PASSWORD`, `JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY`, `DASHBOARD_USERNAME`, `DASHBOARD_PASSWORD`, `POOLER_TENANT_ID`

**Important**: Don't use `@` character in POSTGRES_PASSWORD (causes connection issues).

## Service Credentials

### n8n Connections
- Ollama: `http://ollama:11434`
- Postgres (Supabase): Host is `db`, use credentials from .env
- Qdrant: `http://qdrant:6333`

### Ollama Model Initialization
On startup, Ollama auto-pulls: `nomic-embed-text`, `snowflake-arctic-embed2:568m`, `qwen3:8b`

Edit the `x-init-ollama` section in `docker-compose.yml` to change default models.

## Volumes and Data

- `n8n/backup/` - n8n workflow/credential backups
- `shared/` - Shared files accessible to n8n at `/data/shared`
- `neo4j/` - Neo4j data, logs, plugins
- `supabase/docker/volumes/` - Supabase persistent data
