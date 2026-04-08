# ⟠ Ethereum Node Monitor & Validator Dashboard
A real-time monitoring dashboard for Ethereum mainnet node health, block tracking, gas analytics, and validator metrics — built with Python, Streamlit, Web3.py, and Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)
![Web3.py](https://img.shields.io/badge/Web3.py-6.15-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

---

## 🌐 Live Demo

👉 **[ethereum-node-monitor-validator-dashboard.streamlit.app](https://ethereum-node-monitor-validator-dashboard.streamlit.app/)**

---

## 🚀 Features
- **Live block tracking** — latest block number, block time, transaction count
- **Gas price monitoring** — base fee, priority fee, 24h historical chart with alert thresholds
- **Validator metrics** — attestation rates, balances, proposals, rewards
- **Network health** — peer count, finality, active validator count, beacon slot/epoch
- **Gemini AI Chat** — Ask questions about Ethereum, blockchain, or get help with your node
- **Auto-refresh** — configurable interval (10–60 seconds)
- **Demo mode** — runs with realistic simulated data even without an API key

---

## 🛠 Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Streamlit, custom CSS |
| AI | Google Gemini AI |
| Blockchain | Web3.py, Ethereum JSON-RPC |
| Data | Pandas, real-time simulation |
| DevOps | Docker, Docker Compose, Vercel |
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

### Option 4 — Deploy to Vercel
1. Push your code to GitHub (see above)
2. Go to [Vercel](https://vercel.com) and import your GitHub repo
3. Set environment variables in Vercel dashboard:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `ETH_RPC_URL`: Your Ethereum RPC endpoint (optional for demo mode)
4. In Vercel project settings, set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT --server.headless true --server.enableCORS false`
5. Deploy!

**Note**: Vercel support for Streamlit is experimental. If issues arise, consider Streamlit Cloud below.

### Option 5 — Deploy to Streamlit Cloud (Recommended for Streamlit apps)
1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set secrets in the app settings:
   - `GEMINI_API_KEY`
   - `ETH_RPC_URL` (optional)
5. Deploy — it's free and optimized for Streamlit!

---

## 🤖 Gemini AI Chat
The dashboard includes an integrated Gemini AI chat box powered by Google's Gemini Pro model. You can:
- Ask questions about Ethereum and blockchain technology
- Get help troubleshooting your node
- Learn about gas prices, validators, and network health
- General AI assistance related to crypto

**Setup**: Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey) and add it to your `.env` file as `GEMINI_API_KEY`.

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
