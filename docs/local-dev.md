# Local development with Docker Compose

The repo ships three Compose files:

| File | Loaded automatically by `docker compose`? | Purpose |
| --- | --- | --- |
| `docker-compose.yml` | yes | Base services: postgres, redis, minio, backend, celery, frontend. The frontend service here uses the **production standalone build** (multi-stage Dockerfile, served by `node server.js`). |
| `docker-compose.override.yml` | yes | Local-dev overlay. Re-targets the frontend image to the `builder` stage, bind-mounts the source tree, and runs `npm run dev` with hot reload. |
| `docker-compose.prod.yml` / `docker-compose.staging.yml` | no | Loaded only via explicit `-f` for deploys. |

## Day-to-day commands

```bash
# Boot everything for local work.
docker compose up -d

# Tail frontend logs (Next.js dev server output).
docker compose logs -f frontend

# Restart the dev server after a config file change (next.config.ts,
# tailwind config, etc.). Pure source edits do NOT need a restart.
docker compose restart frontend

# Refresh node_modules after a package.json change.
docker compose build frontend
docker compose up -d --force-recreate frontend
```

## Hot reload behavior

With the override active:

- Any edit under `frontend/src/` propagates to the dev server inside
  the container via the `./frontend:/app` bind mount, and Next.js
  recompiles on save. The browser at `localhost:3000` picks the change
  up in a few seconds.
- `node_modules` lives in a named volume populated from the
  `deps` stage of the Dockerfile, so it matches the container's
  architecture. Do NOT delete `/app/node_modules` inside the container.
- `.next` lives in a named volume so the dev compile cache survives
  container restarts.

## When you DO need a rebuild

| Change | Action |
| --- | --- |
| Any file under `frontend/src/` | nothing, hot reload handles it |
| `frontend/package.json` or `package-lock.json` | `docker compose build frontend && docker compose up -d --force-recreate frontend` |
| `frontend/Dockerfile` | same as above |
| `frontend/next.config.ts` | `docker compose restart frontend` |
| `frontend/.dockerignore` | same as above |

## Production-style verification

To boot the frontend the same way prod does, bypass the override:

```bash
docker compose -f docker-compose.yml up -d --build frontend
```

`-f` causes `docker compose` to ignore `docker-compose.override.yml`,
so the production standalone build runs against the base config. Use
this when you want to confirm an image actually ships the latest code,
or when you're debugging an issue that only reproduces in the
production runtime.

## Deploy paths (informational)

- **Staging:** `docker compose -f docker-compose.yml -f docker-compose.staging.yml up -d`
- **Production:** `docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

Both forms pass explicit `-f` flags, so the local-dev override is not
loaded. The override file is therefore safe to keep in the repo and
does not need to be excluded from the deploy image (it is not copied
into the frontend image at all because it lives at the repo root, not
under `frontend/`).

## The bug this layout fixes

Before this change, `docker-compose.yml` bind-mounted
`./frontend/src:/app/src` onto the production runner. The runner serves
from the Next.js standalone bundle (`.next/standalone/server.js`), not
from `/app/src`, so the mount had **no effect on what the browser
saw**, but it created a `/app/src` directory inside the container that
looked like live source to anyone debugging. Combined with the missing
`.dockerignore` (which let host `.next/` leak into the build context)
and the absence of a dev override (which made every edit feel like it
needed `--no-cache`), this regularly produced "I rebuilt and the
browser still shows old code" reports. The current layout splits the
two concerns cleanly: production base file serves prod; override file
serves dev with real hot reload.
