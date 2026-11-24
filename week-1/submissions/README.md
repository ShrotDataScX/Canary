# Submissions

Each mentee creates their own folder here via a pull request:

```
week-1/submissions/
└── <your-github-username>/
    ├── notes.md              <- copy of _template.md, filled in
    ├── question_bank.md      <- 10 questions (Exercise 7), seeds our Week 5 golden set
    └── exercises/
        ├── ex1_kev.py
        ├── ex1_kev_chart.png
        ├── ex2_nvd.md
        ├── ex3_filings.md
        ├── ex4_event_study.py
        ├── ex5_toy_rag.py
        ├── ex5_report.md
        └── ex6_test_plan.md
```

## Checklist before opening your PR

- [ ] Folder is named after your GitHub username
- [ ] `git status` shows **no** `.env`, `.csv`, data dumps or API keys
- [ ] Code runs from the repo root with a fresh venv (`pip install -r requirements.txt`)
- [ ] Every factual claim links to a source you opened
- [ ] You wrote down at least one question for the sync in `notes.md`
- [ ] PR title: `Week 1: <username> submission`; a teammate is requested as reviewer

## Peer review (required)

Review **one teammate's** PR: run their code, then leave at least two comments: one thing that was clear and well done, one suggestion or question. Reviewing is how we learn each other's parts of the system.
