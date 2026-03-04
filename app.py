"""
Ethereum Node Monitor & Validator Dashboard
Author: Harpreet Kour
Description: Real-time monitoring dashboard for Ethereum mainnet node health,
             block data, gas prices, and validator metrics.
"""

import streamlit as st
import time
import random
from datetime import datetime, timedelta
from src.eth_client import EthereumClient
from src.metrics import MetricsCollector
from src.utils import format_wei_to_gwei, format_large_number, time_ago

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ETH Node Monitor",
    page_icon="⟠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2235;
    --border: #1e2d45;
    --accent: #00d4ff;
    --accent2: #7c3aed;
    --green: #00ff88;
    --red: #ff4d6d;
    --yellow: #ffd60a;
    --text: #e2e8f0;
    --muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background-color: var(--bg) !important; }

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.metric-card:hover { border-color: var(--accent); }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 28px;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    color: var(--accent);
    line-height: 1.2;
}
.metric-sub {
    font-size: 12px;
    color: var(--muted);
    margin-top: 4px;
}

.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}
.status-dot.green { background: var(--green); box-shadow: 0 0 8px var(--green); }
.status-dot.red { background: var(--red); }
.status-dot.yellow { background: var(--yellow); }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

.block-row {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    transition: background 0.2s;
}
.block-row:hover { background: var(--surface2); }

.header-title {
    font-family: 'Space Mono', monospace;
    font-size: 24px;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: -0.5px;
}
.header-sub {
    font-size: 13px;
    color: var(--muted);
    margin-top: 4px;
}

.sidebar-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 16px;
}
.sidebar-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
}

.gas-bar {
    height: 6px;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--green), var(--yellow), var(--red));
    margin: 8px 0;
    position: relative;
}
.gas-indicator {
    position: absolute;
    top: -3px;
    width: 12px; height: 12px;
    border-radius: 50%;
    background: white;
    transform: translateX(-50%);
    box-shadow: 0 0 6px rgba(0,212,255,0.8);
}

div[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
div[data-testid="stSidebar"] * { color: var(--text) !important; }

.stSelectbox > div, .stSlider > div { color: var(--text) !important; }

h1, h2, h3 { color: var(--text) !important; }

.alert-box {
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 13px;
    border-left: 3px solid;
}
.alert-warn {
    background: rgba(255, 214, 10, 0.1);
    border-color: var(--yellow);
    color: var(--yellow);
}
.alert-ok {
    background: rgba(0, 255, 136, 0.1);
    border-color: var(--green);
    color: var(--green);
}
.alert-err {
    background: rgba(255, 77, 109, 0.1);
    border-color: var(--red);
    color: var(--red);
}

.validator-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# ── Initialize Clients ────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return EthereumClient()

@st.cache_resource
def get_metrics():
    return MetricsCollector()


client = get_client()
metrics = get_metrics()


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="header-title">⟠ ETH Monitor</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-sub">Node Health Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Connection status
    is_connected = client.is_connected()
    status_color = "green" if is_connected else "red"
    status_text = "Connected" if is_connected else "Disconnected"
    rpc_info = client.get_rpc_info()

    st.markdown(f"""
    <div class="sidebar-section">
        <div class="sidebar-label">Node Status</div>
        <div style="margin-top:10px; font-size:15px; font-weight:600;">
            <span class="status-dot {status_color}"></span>{status_text}
        </div>
        <div style="font-size:12px; color:#64748b; margin-top:6px; font-family:'Space Mono',monospace;">
            {rpc_info['endpoint']}<br/>
            Network: {rpc_info['network']}<br/>
            Chain ID: {rpc_info['chain_id']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Auto-refresh
    st.markdown('<div class="sidebar-label">Refresh Settings</div>', unsafe_allow_html=True)
    auto_refresh = st.toggle("Auto Refresh", value=True)
    refresh_interval = st.slider("Interval (seconds)", 10, 60, 15)

    st.markdown("---")

    # Gas alert threshold
    st.markdown('<div class="sidebar-label">Gas Alert Threshold (Gwei)</div>', unsafe_allow_html=True)
    gas_threshold = st.slider("", 10, 200, 50, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px; color:#64748b; text-align:center; font-family:'Space Mono',monospace;">
        Last updated<br/>{datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)


# ── Fetch Data ────────────────────────────────────────────────────────────────
with st.spinner(""):
    node_data = client.get_node_data()
    gas_data = client.get_gas_data()
    recent_blocks = client.get_recent_blocks(8)
    validator_data = client.get_validator_metrics()
    uptime_history = metrics.get_uptime_history()
    block_time_history = metrics.get_block_time_history()


# ── Main Header ───────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("""
    <div style="margin-bottom:24px;">
        <div style="font-family:'Space Mono',monospace; font-size:22px; font-weight:700; color:#00d4ff;">
            Ethereum Mainnet — Node Monitor
        </div>
        <div style="font-size:13px; color:#64748b; margin-top:4px;">
            Real-time validator node health, block tracking & gas analytics
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    sync_status = node_data.get('sync_status', 'Synced')
    sync_color = "green" if sync_status == "Synced" else "yellow"
    st.markdown(f"""
    <div style="text-align:right; padding-top:8px;">
        <span class="status-dot {sync_color}"></span>
        <span style="font-size:14px; font-weight:600;">{sync_status}</span><br/>
        <span style="font-size:11px; color:#64748b;">Ethereum Mainnet</span>
    </div>
    """, unsafe_allow_html=True)


# ── Top Metrics Row ───────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

metrics_data = [
    (c1, "Latest Block", f"#{format_large_number(node_data['block_number'])}", f"{node_data['block_time']}s avg block time"),
    (c2, "Gas Price", f"{gas_data['base_fee']} Gwei", f"Priority: +{gas_data['priority_fee']} Gwei"),
    (c3, "Peers Connected", str(node_data['peer_count']), "Active P2P connections"),
    (c4, "Node Uptime", f"{node_data['uptime_pct']}%", f"{node_data['uptime_days']}d {node_data['uptime_hrs']}h running"),
    (c5, "Pending Txns", format_large_number(node_data['pending_txns']), "In mempool"),
]

for col, label, value, sub in metrics_data:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)


st.markdown("<br/>", unsafe_allow_html=True)


# ── Gas Price Alert ───────────────────────────────────────────────────────────
current_gas = gas_data['base_fee']
if current_gas > gas_threshold:
    st.markdown(f"""
    <div class="alert-box alert-warn">
        ⚠️  Gas price ({current_gas} Gwei) exceeds your alert threshold ({gas_threshold} Gwei).
        Consider delaying non-urgent transactions.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="alert-box alert-ok">
        ✓  Gas price is healthy at {current_gas} Gwei — below your threshold of {gas_threshold} Gwei.
    </div>
    """, unsafe_allow_html=True)


# ── Charts Row ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("#### 📊 Gas Price History (24h)")
    import pandas as pd
    gas_history = metrics.get_gas_history()
    df_gas = pd.DataFrame(gas_history)
    st.line_chart(df_gas.set_index("time")["gwei"], use_container_width=True, height=200)

with col_right:
    st.markdown("#### ⏱ Block Time History")
    df_blocks = pd.DataFrame(block_time_history)
    st.line_chart(df_blocks.set_index("block")["seconds"], use_container_width=True, height=200)


# ── Recent Blocks & Validator Section ─────────────────────────────────────────
col_bl, col_val = st.columns([3, 2])

with col_bl:
    st.markdown("#### 🧱 Recent Blocks")
    for block in recent_blocks:
        age = time_ago(block['timestamp'])
        st.markdown(f"""
        <div class="block-row">
            <div style="color:#00d4ff; min-width:110px;">#{format_large_number(block['number'])}</div>
            <div style="color:#64748b; min-width:80px; font-size:12px;">{age}</div>
            <div style="min-width:100px;">{block['tx_count']} txns</div>
            <div style="color:#64748b; font-size:12px; min-width:110px;">Gas: {block['gas_used_pct']}%</div>
            <div style="color:#7c3aed; font-size:12px;">{block['miner'][:10]}...</div>
        </div>
        """, unsafe_allow_html=True)

with col_val:
    st.markdown("#### 🔐 Validator Metrics")
    for v in validator_data:
        status_c = "green" if v['status'] == "Active" else "yellow"
        st.markdown(f"""
        <div class="validator-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="font-family:'Space Mono',monospace; font-size:13px; font-weight:700; color:#00d4ff;">
                    Validator #{v['index']}
                </div>
                <div style="font-size:12px;">
                    <span class="status-dot {status_c}"></span>{v['status']}
                </div>
            </div>
            <div style="margin-top:10px; display:grid; grid-template-columns:1fr 1fr; gap:8px;">
                <div>
                    <div style="font-size:10px; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Balance</div>
                    <div style="font-size:14px; font-weight:600;">{v['balance']} ETH</div>
                </div>
                <div>
                    <div style="font-size:10px; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Attestations</div>
                    <div style="font-size:14px; font-weight:600; color:#00ff88;">{v['attestation_rate']}%</div>
                </div>
                <div>
                    <div style="font-size:10px; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Proposals</div>
                    <div style="font-size:14px; font-weight:600;">{v['proposals']}</div>
                </div>
                <div>
                    <div style="font-size:10px; color:#64748b; text-transform:uppercase; letter-spacing:1px;">Rewards</div>
                    <div style="font-size:14px; font-weight:600; color:#00d4ff;">+{v['rewards']} ETH</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Network Health ─────────────────────────────────────────────────────────────
st.markdown("#### 🌐 Network Health Summary")
nh_cols = st.columns(4)
health_items = [
    ("Finality", node_data['finality'], "Epochs since finalized"),
    ("Slot", format_large_number(node_data['slot']), "Current beacon slot"),
    ("Epoch", format_large_number(node_data['epoch']), "Current epoch"),
    ("Active Validators", format_large_number(node_data['active_validators']), "Total active on network"),
]
for col, (label, value, sub) in zip(nh_cols, health_items):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="font-size:22px;">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Auto Refresh ──────────────────────────────────────────────────────────────
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()
