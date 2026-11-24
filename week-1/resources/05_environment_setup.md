# 05 · Environment Setup & Team Workflow

Do this first. Budget ~1 hour. If anything fails, ask early.

## 1. Prerequisites

- **Python 3.10+** (`python --version`)
- **Git** (`git --version`) and a **GitHub account**. The mentor will invite you to the private `ShrotDataScX/Canary` repo; accept the invitation (check your email).
- An editor (VS Code recommended).

## 2. Clone and install

```bash
git clone https://github.com/ShrotDataScX/Canary.git
cd Canary

python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
```

If GitHub asks for a password, use a **Personal Access Token** or the GitHub CLI (`gh auth login`). Passwords no longer work for git over HTTPS.

## 3. Configure secrets safely

```bash
cp .env.example .env        # Windows: copy .env.example .env
```

Edit `.env` and set:

- `SEC_USER_AGENT="Your Name your.email@example.com"`: **required** for EDGAR. Use your real name and email, as the SEC's fair-access policy asks.
- `NVD_API_KEY`: optional; request one at <https://nvd.nist.gov/developers/request-an-api-key>.

Load them in a shell session:

```bash
# macOS/Linux
set -a; source .env; set +a
# Windows PowerShell
Get-Content .env | ForEach-Object { if ($_ -match '^\s*([^#=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim('"'), 'Process') } }
```

> 🔒 **`.env` is git-ignored. Never paste keys into code, notebooks, issues, PRs or chat.** If you ever commit a key by accident, tell the mentor immediately; the key must be revoked, since deleting the commit isn't enough.

## 4. Smoke test

```bash
python week-1/scripts/04_toy_rag.py            # no network or keys needed
python week-1/scripts/01_explore_cisa_kev.py   # needs internet
python week-1/scripts/02_explore_nvd.py
python week-1/scripts/03_explore_edgar.py AAPL # needs SEC_USER_AGENT
```

Expected: tables printed, no tracebacks. Common errors:

| Error | Fix |
|---|---|
| `403 Forbidden` from sec.gov | `SEC_USER_AGENT` missing/invalid; set it as shown above |
| `403`/`429` from NVD | You hit the rate limit: wait ~30 s, or use an API key |
| `ModuleNotFoundError` | venv not activated, or `pip install -r requirements.txt` not run |
| SSL / proxy errors | Try a different network; ask the mentor |

## 5. Git workflow (we all use this)

**Never push directly to `main`.** Every change goes through a pull request.

```bash
git checkout main && git pull                     # start fresh
git checkout -b week1/<your-username>-submission  # one branch per piece of work

# ... do work ...

git add week-1/submissions/<your-username>/       # add specific paths, not `git add .`
git status                                        # CHECK: no .env, no data files!
git commit -m "Week 1: add <your-username> submission"
git push -u origin week1/<your-username>-submission
```

Then open a **Pull Request** on GitHub (base: `main`) and request a review from a teammate.

### Branch names
`week<N>/<short-description>`, e.g. `week2/edgar-loader`, `week5/injection-tests`.

### Commit messages
Imperative, specific: ✅ `Add KEV loader with schema validation`, ❌ `update stuff`.

### Pull request etiquette
- Small, focused PRs (a few hundred lines at most).
- Describe *what* and *why*; link the exercise or issue.
- Reviewer: run the code, comment on clarity and correctness, be kind, and approve only if you'd be comfortable maintaining it.
- Resolve merge conflicts by pulling `main` into your branch, not by force-pushing to shared branches.

## 6. Handy habits

- Keep downloaded data in git-ignored `data/` folders. Re-download is cheap; a polluted repo isn't.
- Always work inside the venv: don't `pip install` globally.
- Print less, log more (we'll set up `logging` in Week 2).
- When something runs, **commit**. Small commits are easy to revert.

## 7. Jupyter (optional)

```bash
jupyter lab
```

Notebooks are great for exploration. Before committing one, **clear all outputs** (Cell → All Output → Clear) to avoid leaking data or secrets and to keep diffs readable.
