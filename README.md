# renovate-config

Shared [Renovate](https://docs.renovatebot.com/) preset for `dvystrcil/*` repos.

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["local>dvystrcil/renovate-config"]
}
```

New repos get this automatically: Renovate's onboarding looks for a repo named
`renovate-config` under the same owner and suggests its `default.json`.

## What it sets

| | |
|---|---|
| base | `config:recommended` |
| third-party GitHub Actions | pinned to a commit SHA (`helpers:pinGitHubActionDigests`) |
| our own actions (`dvystrcil/**`) | left on their semver tag (`pinDigests: false`), so a fix ships by moving `v1` |
| Dependency Dashboard issue | labelled `dependency-dashboard`, so the project board's auto-add workflows skip it with `-label:dependency-dashboard` (homelab `bin/project-board-tidy.py` removes any that slip on) |

The pinning rule is homelab decision **D-042** (`architecture/ways-of-working.md` in
`dvystrcil/homelab`). Fleet compliance is reported weekly by
`bin/audit-action-pinning.py` there.

A change here applies to every repo that extends it on that repo's next Renovate run.

## License

[MIT](LICENSE)
