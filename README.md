# ImmunoMimic

A personalized web platform predicting autoimmune risk through pathogen-human molecular mimicry, based on published immunology research.

## Run locally
```bash
pip install streamlit pandas plotly
streamlit run app.py
```

## Deploy live (free, ~5 minutes)
1. Create a GitHub repo and push this folder (`app.py`, `data/`, `requirements.txt`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub → "New app" → select your repo → main file: `app.py`
4. Click Deploy — you get a live public link (e.g. `yourapp.streamlit.app`)

## Files
- `app.py` — the full website (5 pages: Home, Personalized Risk Check, Pathogen Comparison, Leaderboard, About)
- `data/mimicry_database.csv` — 6 literature-sourced pathogen-human mimicry cases (Strep/rheumatic fever, Campylobacter/GBS, EBV/MS, Coxsackievirus/T1D, H. pylori/gastritis, Mycoplasma/cold agglutinin disease)

## Extending for your full 3-month submission
Replace/expand `mimicry_database.csv` with results from your own BLASTp runs (Module 1) once you've done the sequence alignment work — the app already reads any CSV with the same column structure, so no code changes needed downstream.
