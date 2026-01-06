# cpp-challenge

A trivial cross-platform C++ library with a fully automated CI/CD pipeline. The library exposes a
single function `int sum(int a, int b)` and is packaged with Conan 2, built with CMake, and
validated with GoogleTest. GitHub Actions orchestrates pull-request checks, label-driven
verification/publishing, and release automation.

## Library layout
- `include/mylib/sum.h` / `src/sum.cpp`: Library implementation.
- `tests/`: GoogleTest unit coverage.
- `consumer/`: Tiny consumer that installs the package from Conan and links via `find_package`.
- `conan/profiles/`: Conan 2 host profiles for Linux, macOS, and Windows.
- `VERSION`: Canonical semantic version for both CMake and Conan recipes.

## Build & test locally
```bash
conan install . --build=missing
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
ctest --test-dir build --output-on-failure --config Release
```

## Conan package (manual)
```bash
conan create . --profile:host=conan/profiles/linux-gcc --build=missing
```

## CI/CD workflows (GitHub Actions)
| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `pr` | `pull_request` | Format check, configure, build, and test for every PR. |
| `label-verify` | `pull_request_target` with `verify` label | Builds consumer against the RC package reference `mylib/<VERSION>-dev-<short-sha>` from the RC remote. |
| `publish-rc` | `pull_request_target` with `publish` label | Blocks if a release already exists in `conan-stable`, then builds/upload RC packages (`<VERSION>-dev-<short-sha>`) to `conan-rc` for Linux/macOS/Windows. |
| `release` | PR merged with `publish` label | Builds and uploads final packages to `conan-stable`, tags the repo (`vX.Y.Z`), and opens a GitHub Release. |
| `branch-protection` | push to `main` or manual | Applies branch protection: up-to-date with `main`, linear history, and required `pr / check` status. |

## Versioning & package references
- Semantic version kept in `VERSION` and mirrored in CMake/Conan.
- Pre-merge artifacts use `mylib/<X.Y.Z>-dev-<short-sha>` uploaded to `conan-rc`.
- Releases use `mylib/<X.Y.Z>` uploaded to `conan-stable` and tagged `vX.Y.Z`.

## Label-driven flow
- Add `verify` label: runs consumer integration via Conan install + `find_package`.
- Add `publish` label: builds RC packages on all platforms and uploads to `conan-rc`; merge is blocked if `conan-stable` already has `<VERSION>`.
- Merge a PR with `publish` label: triggers release workflow, publishes stable packages, tags, and creates GitHub Release.

## Shared reusable workflows
Reusable actions are defined in the companion repository `my-org/cpp-shared-workflows` (mirrored in
`shared-workflows/.github/workflows` for reference). The main workflows call:
- `.github/workflows/build-test.yml`: standard format/build/test.
- `.github/workflows/publish-conan.yml`: matrix package build/upload.
- `.github/workflows/integration-test.yml`: consumer validation against a package reference.

Push the `shared-workflows` directory to a dedicated repo (e.g., `github.com/my-org/cpp-shared-workflows`)
and update the `uses:` references if your org differs.

## Secrets & remotes
Set the following secrets in the GitHub repository:
- `CONAN_USERNAME` / `CONAN_PASSWORD`: Conan credentials for both remotes.
- `CONAN_RC_URL` / `CONAN_STABLE_URL`: Remote URLs for RC and stable remotes.
- `ADMIN_TOKEN`: Token with admin rights for applying branch protection.

## Deliverables checklist
- Git tags/releases and Conan packages are produced automatically—no manual post-approval steps.
- Branch protection enforces up-to-date branches and linear history.
- Version bumps must be included in the PR by editing `VERSION`.
