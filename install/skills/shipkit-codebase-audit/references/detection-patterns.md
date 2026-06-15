# Detection Patterns

Detection runs on every tier, before anything else. Detect-before-install: never duplicate tooling/config that already exists.

## 1. Package manager + runner

| Signal (in priority order) | Package manager | Ephemeral runner |
|----------------------------|-----------------|------------------|
| `bun.lockb` | bun | `bunx` |
| `pnpm-lock.yaml` / `pnpm-workspace.yaml` | pnpm | `pnpm dlx` |
| `yarn.lock` | yarn | `yarn dlx` |
| `package-lock.json` / none | npm | `npx --yes` |

If multiple lockfiles exist, prefer the one matching `packageManager` in `package.json`; else the most recently modified.

### Monorepo layout
- `package.json` `workspaces` array (npm/yarn), or `pnpm-workspace.yaml`.
- Each workspace package has its own `package.json` and may have its own dead-code config.
- knip supports workspaces natively; run from the repo root and let it resolve members. For other tools, run per-package and aggregate.

## 2. Existing dead-code tooling / config (reuse, don't duplicate)

| Tool | Config / signal | Notes |
|------|-----------------|-------|
| **knip** (primary) | `knip.json`, `knip.jsonc`, `.knip.{js,ts}`, `knip` key in `package.json`, `knip` in devDependencies | Most comprehensive: unused files/exports/deps/devDeps + unresolved imports in one pass |
| depcheck | `.depcheckrc*`, depcheck in devDeps | Dependencies only |
| ts-prune | ts-prune in devDeps/scripts | Unused exports only (TS) |
| unimported | `.unimportedrc*` | Unused files/deps |

**If a tool is already installed, prefer it** (runs offline, matches the repo's expectations). Only reach for ephemeral `npx knip` when nothing is wired in.

### Detecting an existing `lint:dead`-style script
Scan `package.json` `scripts` for `knip`, `depcheck`, `ts-prune`, `unimported`, or a `lint:dead` / `dead`/`deadcode` entry. If present, the repo is already wired — skip the persistence offer.

## 3. Running the sweep

Preferred (knip), ephemeral:
```
<runner> knip --no-progress --reporter json
```
- `--reporter json` for parseable output; fall back to default reporter + text parse if json unsupported by the resolved version.
- For TS repos without knip config, knip auto-detects `tsconfig.json` and entry points.

Installed-tool path (no network):
```
<pm> run lint:dead          # if a script exists
<pm> exec knip --reporter json   # if knip is a devDep
```

## 4. Non-JS / unsupported languages

| Ecosystem | Possible tool | If absent |
|-----------|---------------|-----------|
| Python | `vulture`, `deptry` | Report "no dead-code tooling available for Python"; offer Mode B only |
| Go | `staticcheck` (U1000), `deadcode` | As above |
| Rust | `cargo +nightly udeps`, dead_code lint | As above |
| Other | — | Clean exit, no fabricated findings |

**Rule**: never invent findings for a language whose tooling isn't available. Report the gap honestly and, for `deep`/`exhaustive`, proceed with Mode B (reasoning) only — which is language-agnostic.

## 5. Failure handling

- Network blocked / offline sandbox → ephemeral `npx`/`dlx` will fail. Report it explicitly; suggest the installed-tool path or opt-in persistence. Never silently treat a failed run as "clean".
- Tool exits non-zero because it *found* issues (some tools do) vs. because it *errored* — distinguish via output shape, not exit code alone.
