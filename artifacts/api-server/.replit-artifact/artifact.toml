kind = "api"
previewPath = "/api" # TODO - should be excluded from preview in the first place
title = "API Server"
version = "1.0.0"
id = "3B4_FFSkEVBkAeYMFRJ2e"

[[services]]
localPort = 8080
name = "API Server"
paths = ["/api"]

[services.development]
run = "pnpm --filter @workspace/api-server run dev"

[services.production]

[services.production.build]
args = ["pnpm", "--filter", "@workspace/api-server", "run", "build"]

[services.production.build.env]
NODE_ENV = "production"

[services.production.run]
# we don't run through pnpm to make startup faster in production
args = ["node", "--enable-source-maps", "artifacts/api-server/dist/index.mjs"]

[services.production.run.env]
PORT = "8080"
NODE_ENV = "production"

[services.production.health.startup]
path = "/api/healthz"
