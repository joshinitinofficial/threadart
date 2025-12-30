# Thread Art – Modular Multiplication Visualizer

This Streamlit app visualizes mathematical thread art using the rule:

end = (i × k) mod N

## Features
- Adjustable total nodes (N)
- Adjustable multiplier (k)
- Node indexing
- Mathematical prediction of focal loops using gcd(N, k−1)

## Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
