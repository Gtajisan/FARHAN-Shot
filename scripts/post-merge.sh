#!/bin/bash
set -e
pnpm install --frozen-lockfile
pnpm --filter db push
