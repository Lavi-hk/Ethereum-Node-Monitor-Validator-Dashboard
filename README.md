# ⟠ Ethereum Node Monitor & Validator Dashboard

A real-time monitoring dashboard for Ethereum mainnet node health, block tracking, gas analytics, and validator metrics — built with Python, Streamlit, Web3.py, and Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Web3.py](https://img.shields.io/badge/Web3.py-6.15-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 🚀 Features

- **Live block tracking** — latest block number, block time, transaction count
- **Gas price monitoring** — base fee, priority fee, 24h historical chart with alert thresholds
- **Validator metrics** — attestation rates, balances, proposals, rewards
- **Network health** — peer count, finality, active validator count, beacon slot/epoch
- **Auto-refresh** — configurable interval (10–60 seconds)
- **Demo mode** — runs with realistic simulated data even without an API key

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit, custom CSS |
| Blockchain | Web3.py, Ethereum JSON-RPC |
| Data | Pandas, real-time simulation |
| DevOps | Docker, Docker Compose |
| Language | Python 3.11 |

---

## 📦 Quick Start

### Option 1 — Run Locally

```bash
# Clone the repo
git clone https://github.com/Lavi-hk/eth-node-monitor
cd eth-node-monitor

# Install dependencies
pip install -r requirements.txt

# (Optional) Set your RPC URL for live data
cp .env.example .env
# Edit .env and add your Infura/Alchemy key

# Run
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### Option 2 — Docker

```bash
# Build and run
docker compose up --build

# With your RPC URL
ETH_RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY docker compose up --build
```

### Option 3 — Demo Mode (no API key needed)

Just run without setting `ETH_RPC_URL`. The dashboard uses realistic simulated Ethereum mainnet data.

---

## 🔑 Getting a Free RPC Endpoint

1. **Infura** (recommended): [app.infura.io](https://app.infura.io) → Create project → Copy HTTP endpoint
2. **Alchemy**: [alchemy.com](https://www.alchemy.com) → Create app → Copy HTTPS URL

Both offer generous free tiers (100k+ requests/day).

---

## 📁 Project Structure

```
eth-node-monitor/
├── app.py                 # Main Streamlit dashboard
├── src/
│   ├── eth_client.py      # Web3 connection & data fetching
│   ├── metrics.py         # Time-series metrics & history
│   └── utils.py           # Formatting helpers
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 🔮 Roadmap

- [ ] Beacon Chain API integration for real validator data
- [ ] PostgreSQL persistence for historical metrics
- [ ] Telegram/Discord alert bot
- [ ] Multi-chain support (Polygon, Solana)
- [ ] Grafana export

---

## 👩‍💻 Author

**Harpreet Kour** — [github.com/Lavi-hk](https://github.com/Lavi-hk) | [linkedin.com/in/harpreet01kour](https://linkedin.com/in/harpreet01kour)

Built as part of learning blockchain infrastructure and validator node operations.
