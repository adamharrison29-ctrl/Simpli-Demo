import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Simplí – Investing, Made Simple",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

_FONT_LINK = (
    '<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700'
    '&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">'
)
st.markdown(_FONT_LINK, unsafe_allow_html=True)

_CSS = """
html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
    background-color: #0B0F0E;
    color: #F0F5F2;
}
.stApp { background-color: #0B0F0E; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 2rem 2.5rem; max-width: 1400px; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1510 0%, #0B0F0E 100%);
    border-right: 1px solid rgba(46,204,113,0.15);
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1.2rem; }
div[data-testid="stSidebar"] .stRadio > div { gap: 0.35rem; flex-direction: column; }
div[data-testid="stSidebar"] .stRadio label {
    background: rgba(20,30,25,0.5);
    border: 1px solid rgba(46,204,113,0.12);
    border-radius: 10px;
    padding: 0.65rem 1rem;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #8A9B90 !important;
    font-size: 0.88rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}
div[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(46,204,113,0.1);
    border-color: rgba(46,204,113,0.4);
    color: #F0F5F2 !important;
}
div[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] { display: none; }
.stSlider [data-baseweb="slider"] { margin-top: 0.5rem; }
.stButton > button {
    background: linear-gradient(135deg, #2ECC71, #27ae60);
    color: #0B0F0E;
    font-family: 'Sora', sans-serif;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.8rem;
    font-size: 0.95rem;
    letter-spacing: 0.03em;
    transition: all 0.25s ease;
    box-shadow: 0 4px 15px rgba(46,204,113,0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(46,204,113,0.4);
    background: linear-gradient(135deg, #34d979, #2ECC71);
}
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: rgba(20,30,25,0.8) !important;
    border: 1px solid rgba(46,204,113,0.2) !important;
    border-radius: 10px !important;
    color: #F0F5F2 !important;
}
[data-testid="stMetric"] {
    background: rgba(20,30,25,0.7);
    border: 1px solid rgba(46,204,113,0.15);
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricValue"] { color: #2ECC71 !important; font-family: 'DM Serif Display', serif; }
hr { border-color: rgba(46,204,113,0.12) !important; margin: 1.5rem 0; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0B0F0E; }
::-webkit-scrollbar-thumb { background: rgba(46,204,113,0.3); border-radius: 3px; }
"""
st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
INVESTMENTS = [
    {
        "name": "ETFs",
        "icon": "📊",
        "desc": "Baskets of stocks tracking an index — low-cost, diversified, autopilot investing.",
        "gross": 8.0, "net": 4.7,
        "tax": "Exit Tax 41% + Deemed Disposal",
        "tax_short": "Exit Tax 41%",
        "risk": 3, "liquidity": "High", "min": 100,
        "colour": "#2ECC71",
        "pros": ["Very low fees", "Instant diversification", "Easy to start"],
        "cons": ["Deemed Disposal every 8 years", "41% Exit Tax hurts returns"],
        "steps": [
            ("Open a broker account", "Visit Degiro.ie or Trading212.com and click 'Open Account'."),
            ("Verify your identity", "Upload your passport/driving licence and proof of address. Usually takes under 24 hours."),
            ("Deposit funds", "Bank transfer from your Irish account. Minimum €100 on most platforms."),
            ("Search for your ETF", "Look for VWCE (Vanguard All-World) or CSPX (S&P 500). Filter by 'accumulating' to auto-reinvest dividends."),
            ("Place your order", "Enter your amount, review the fee, and confirm. You're now an investor."),
        ],
    },
    {
        "name": "Index Funds",
        "icon": "📈",
        "desc": "Mutual funds that mirror the market — similar to ETFs but through a fund manager.",
        "gross": 7.5, "net": 4.4,
        "tax": "Exit Tax 41% + Deemed Disposal",
        "tax_short": "Exit Tax 41%",
        "risk": 3, "liquidity": "Medium", "min": 500,
        "colour": "#27ae60",
        "pros": ["Professionally managed", "Broad market exposure"],
        "cons": ["Higher minimum investment", "Less flexible than ETFs"],
        "steps": [
            ("Choose a provider", "Look at Irish-friendly providers like Zurich Life, Irish Life, or Standard Life."),
            ("Pick an index fund", "Select a global equity fund tracking MSCI World or similar."),
            ("Complete KYC", "Submit identity documents to the provider."),
            ("Set up a direct debit", "Most Irish providers allow regular monthly contributions from €100+."),
            ("Review annually", "Check performance vs. index benchmark once a year."),
        ],
    },
    {
        "name": "Individual Stocks",
        "icon": "🏢",
        "desc": "Own a slice of real companies — higher potential, higher risk.",
        "gross": 10.0, "net": 6.7,
        "tax": "CGT 33%",
        "tax_short": "CGT 33%",
        "risk": 4, "liquidity": "High", "min": 50,
        "colour": "#3498db",
        "pros": ["Best gross returns", "CGT is fairer than Exit Tax", "Annual €1,270 CGT exemption"],
        "cons": ["Stock-picking is hard", "Concentration risk", "Time-intensive to research"],
        "steps": [
            ("Open a stock broker", "Degiro.ie has the lowest fees for Irish investors. Create an account online."),
            ("Complete verification", "Upload ID + proof of address. Approved within 1 business day."),
            ("Fund your account", "Transfer from your bank. As little as €50 gets you started."),
            ("Research a company", "Read the annual report. Check P/E ratio, revenue growth, and debt levels."),
            ("Buy shares", "Search the ticker (e.g. AAPL), enter your amount, and place a market order."),
        ],
    },
    {
        "name": "Gold & Silver",
        "icon": "🥇",
        "desc": "Physical precious metals or ETCs — a classic inflation hedge.",
        "gross": 5.5, "net": 3.7,
        "tax": "CGT 33%",
        "tax_short": "CGT 33%",
        "risk": 3, "liquidity": "Medium", "min": 100,
        "colour": "#F5C842",
        "pros": ["Safe-haven asset", "Inflation hedge", "Portfolio diversifier"],
        "cons": ["No income yield", "Storage costs for physical", "Volatile short-term"],
        "steps": [
            ("Decide: physical or ETC", "Physical gold from GoldCore.ie, or a Gold ETC like IGLN on your broker."),
            ("Check the spot price", "Use goldprice.org to see live gold prices in EUR."),
            ("Purchase your allocation", "Keep gold under 10% of your portfolio as a hedge, not a core holding."),
            ("Store safely", "Physical gold: use insured allocated storage or a home safe. ETCs: stay in your broker account."),
            ("Track CGT events", "Record purchase price. You'll owe 33% CGT on gains when you sell."),
        ],
    },
    {
        "name": "Bank Deposits",
        "icon": "🏦",
        "desc": "Standard savings accounts — safe, boring, and slowly losing to inflation.",
        "gross": 1.5, "net": 1.0,
        "tax": "DIRT 33%",
        "tax_short": "DIRT 33%",
        "risk": 1, "liquidity": "Very High", "min": 1,
        "colour": "#95a5a6",
        "pros": ["FSCS/DGS protected up to €100k", "Zero effort", "Instant access"],
        "cons": ["Returns rarely beat inflation", "DIRT automatically deducted"],
        "steps": [
            ("Compare rates", "Check raisin.ie or your existing bank's savings rates."),
            ("Open a savings account", "In-branch or online — takes 10 minutes."),
            ("Transfer funds", "Move money from your current account."),
            ("DIRT is automatic", "Your bank deducts 33% tax on interest at source. Nothing to file."),
        ],
    },
    {
        "name": "Credit Union Savings",
        "icon": "🤝",
        "desc": "Member-owned co-ops offering slightly better rates than banks.",
        "gross": 2.0, "net": 1.3,
        "tax": "DIRT 33%",
        "tax_short": "DIRT 33%",
        "risk": 1, "liquidity": "High", "min": 5,
        "colour": "#8e44ad",
        "pros": ["Community-owned", "Dividend history", "Some offer loan access"],
        "cons": ["Returns still low", "Must be a member"],
        "steps": [
            ("Find your local credit union", "Use creditunion.ie to find one by county or workplace."),
            ("Become a member", "Pay a small share (€5–€10). You're now a co-owner."),
            ("Open a savings account", "Deposit regularly. Some pay an annual dividend."),
            ("DIRT deducted", "Tax is handled automatically on any dividend/interest paid."),
        ],
    },
    {
        "name": "Government Bonds",
        "icon": "📜",
        "desc": "Lend money to Ireland or the EU — predictable, low-risk returns.",
        "gross": 3.0, "net": 2.0,
        "tax": "CGT 33%",
        "tax_short": "CGT 33%",
        "risk": 1, "liquidity": "Medium", "min": 100,
        "colour": "#1abc9c",
        "pros": ["Very low risk", "Predictable income", "Portfolio stability"],
        "cons": ["Low returns", "Inflation risk on long bonds"],
        "steps": [
            ("Access via a broker", "Irish government bonds trade on Euronext Dublin. Buy via Degiro or Davy."),
            ("Choose a maturity", "Short (1–3yr) for safety, longer for slightly higher yield."),
            ("Place a limit order", "Bonds trade at a price; set a limit to avoid overpaying."),
            ("Collect coupon payments", "Interest paid semi-annually directly to your broker account."),
            ("Record CGT on sale", "If you sell above purchase price, 33% CGT applies to the gain."),
        ],
    },
    {
        "name": "An Post State Savings",
        "icon": "🟢",
        "desc": "Irish government savings — completely tax-free and backed by the State.",
        "gross": 3.0, "net": 3.0,
        "tax": "Tax-Free",
        "tax_short": "Tax-Free ✓",
        "risk": 1, "liquidity": "Low", "min": 50,
        "colour": "#2ECC71",
        "pros": ["100% tax-free", "State-guaranteed", "No fees ever"],
        "cons": ["Fixed term — early withdrawal loses interest", "Lower gross return"],
        "steps": [
            ("Visit anpost.com/savings", "Browse the products: Savings Certs, Savings Bonds, or Prize Bonds."),
            ("Choose your product", "Savings Certificates (5.5yr) offer the best after-tax return. Zero tax."),
            ("Create an An Post Money account", "Online or at any post office. Bring your PPSN and ID."),
            ("Transfer funds", "Minimum €50. Your money is guaranteed by the Irish State."),
            ("Wait and earn", "Interest is paid at maturity. No tax return needed — it's already tax-free."),
        ],
    },
    {
        "name": "Prize Bonds",
        "icon": "🎟️",
        "desc": "Government savings where your interest is entered into weekly prize draws.",
        "gross": 1.0, "net": 1.0,
        "tax": "Tax-Free",
        "tax_short": "Tax-Free ✓",
        "risk": 1, "liquidity": "Medium", "min": 25,
        "colour": "#e67e22",
        "pros": ["Tax-free prizes", "State-backed capital", "Weekly draw"],
        "cons": ["Expected return is only 1%", "Variable/lottery-style"],
        "steps": [
            ("Visit prizebonds.ie", "Or your local post office."),
            ("Buy bonds", "Minimum €25. Each €25 unit = one entry per weekly draw."),
            ("Verify identity", "Bring PPSN and photo ID."),
            ("Check weekly draws", "Results published every Friday on prizebonds.ie."),
            ("Redeem anytime", "Sell back at face value within 7 working days. No loss of capital."),
        ],
    },
    {
        "name": "REITs",
        "icon": "🏘️",
        "desc": "Own a share of commercial property portfolios without being a landlord.",
        "gross": 6.5, "net": 4.4,
        "tax": "CGT 33%",
        "tax_short": "CGT 33%",
        "risk": 3, "liquidity": "High", "min": 200,
        "colour": "#e74c3c",
        "pros": ["Property exposure without hassle", "Dividend income", "Liquid (stock exchange)"],
        "cons": ["Irish REIT market is small", "Property market exposure"],
        "steps": [
            ("Open a broker account", "Degiro or Davy Stockbrokers are suitable for Irish investors."),
            ("Find a REIT", "Search for Irish (e.g. Hibernia, IRES) or European REITs on your broker."),
            ("Review dividend yield", "REITs must distribute 85%+ of profits. Check the historical dividend."),
            ("Buy shares", "Place a market or limit order on the exchange."),
            ("Track distributions", "Dividends taxed as income; capital gains at 33% CGT on sale."),
        ],
    },
    {
        "name": "Peer-to-Peer Lending",
        "icon": "🔗",
        "desc": "Lend directly to borrowers online — higher returns, higher default risk.",
        "gross": 7.0, "net": 4.7,
        "tax": "Income Tax (up to 40%)",
        "tax_short": "Income Tax",
        "risk": 4, "liquidity": "Low", "min": 50,
        "colour": "#fd79a8",
        "pros": ["Attractive gross yields", "Portfolio diversification"],
        "cons": ["Default risk is real", "Illiquid — locked in for loan term", "High earners pay 40%+"],
        "steps": [
            ("Choose a platform", "Linked Finance (Ireland) is the main Irish P2P lender."),
            ("Register and verify", "ID verification required. Process takes 1–2 days."),
            ("Deposit funds", "Minimum varies; €50 per loan is typical."),
            ("Spread across loans", "Diversify across 20+ loans to reduce default impact."),
            ("Declare on your tax return", "P2P interest is taxable income. File Form 12 or Form 11 annually."),
        ],
    },
    {
        "name": "Pension / AVCs",
        "icon": "🏖️",
        "desc": "Tax-relieved retirement savings — your employer's scheme or a personal pension.",
        "gross": 6.0, "net": 6.0,
        "tax": "Tax-Free at Contribution",
        "tax_short": "Tax Relief + Growth",
        "risk": 2, "liquidity": "Very Low", "min": 100,
        "colour": "#74b9ff",
        "pros": ["Up to 40% tax relief on contributions", "Tax-free growth", "Employer matching"],
        "cons": ["Locked until age 60", "Drawdown taxed as income"],
        "steps": [
            ("Check your employer scheme", "Ask HR if your employer offers a pension with matching contributions."),
            ("Set contribution %", "Even 5% of salary, matched by employer, is a 100% instant return."),
            ("Choose your fund", "Pick a 'lifestyling' or equity-heavy fund if you're under 45."),
            ("Set up AVCs", "Additional Voluntary Contributions top up your pension with full tax relief."),
            ("Review annually", "Increase contribution by 1% each year. Your future self will thank you."),
        ],
    },
    {
        "name": "Cryptocurrency",
        "icon": "₿",
        "desc": "Digital assets — extreme upside, extreme volatility, CGT applies.",
        "gross": 15.0, "net": 10.1,
        "tax": "CGT 33%",
        "tax_short": "CGT 33%",
        "risk": 5, "liquidity": "Very High", "min": 10,
        "colour": "#fdcb6e",
        "pros": ["Highest potential returns", "CGT (not Exit Tax) applies", "24/7 liquid"],
        "cons": ["Extreme volatility", "No regulatory protection", "Complex tax tracking"],
        "steps": [
            ("Choose an exchange", "Coinbase or Kraken are regulated and Irish-friendly."),
            ("Complete KYC", "ID + proof of address required. Usually verified within hours."),
            ("Start small", "Invest only what you can afford to lose entirely. €10–€100 to learn."),
            ("Use a hardware wallet", "For amounts over €500, move crypto off the exchange to a Ledger wallet."),
            ("Track every transaction", "Use Koinly.io for Irish CGT reporting. Every swap is a taxable event."),
        ],
    },
]

INV_MAP = {inv["name"]: inv for inv in INVESTMENTS}

RISK_LABELS = {1: "Very Low", 2: "Low", 3: "Medium", 4: "High", 5: "Very High"}
RISK_COLOURS = {1: "#2ECC71", 2: "#27ae60", 3: "#F5C842", 4: "#e67e22", 5: "#e74c3c"}

# ── Helpers ───────────────────────────────────────────────────────────────────
def risk_dots(level):
    dots = ""
    for i in range(1, 6):
        colour = RISK_COLOURS[level] if i <= level else "rgba(255,255,255,0.1)"
        dots += f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{colour};margin-right:3px;"></span>'
    return dots

def card(inv, clickable=False, selected=False):
    border = "rgba(46,204,113,0.6)" if selected else "rgba(46,204,113,0.18)"
    glow = "box-shadow: 0 0 20px rgba(46,204,113,0.25);" if selected else ""
    tax_color = "#2ECC71" if "Tax-Free" in inv["tax"] else "#F5C842"
    return f"""
    <div style="
        background: rgba(20,30,25,0.7);
        border: 1px solid {border};
        border-radius: 16px;
        padding: 1.4rem 1.3rem;
        margin-bottom: 0.6rem;
        transition: all 0.3s ease;
        {glow}
        backdrop-filter: blur(8px);
    ">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6rem;">
            <div style="display:flex;align-items:center;gap:0.5rem;">
                <span style="font-size:1.4rem;">{inv['icon']}</span>
                <span style="font-family:'DM Serif Display',serif;font-size:1.15rem;color:#F0F5F2;">{inv['name']}</span>
            </div>
            <span style="
                background:rgba(46,204,113,0.12);
                border:1px solid rgba(46,204,113,0.25);
                border-radius:20px;
                padding:2px 10px;
                font-size:0.72rem;
                color:#2ECC71;
                font-weight:600;
                letter-spacing:0.04em;
            ">{inv['liquidity']} Liquidity</span>
        </div>
        <p style="color:#8A9B90;font-size:0.82rem;margin:0 0 0.9rem;line-height:1.5;">{inv['desc']}</p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-bottom:0.9rem;">
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:0.6rem 0.8rem;">
                <div style="color:#8A9B90;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;">Gross Return</div>
                <div style="color:#F0F5F2;font-size:1.1rem;font-weight:700;">{inv['gross']}%</div>
            </div>
            <div style="background:rgba(46,204,113,0.08);border-radius:10px;padding:0.6rem 0.8rem;border:1px solid rgba(46,204,113,0.2);">
                <div style="color:#8A9B90;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;">After-Tax ⚡</div>
                <div style="color:#2ECC71;font-size:1.1rem;font-weight:700;">{inv['net']}%</div>
            </div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.4rem;">
            <span style="color:{tax_color};font-size:0.75rem;font-weight:600;background:rgba(245,200,66,0.08);padding:3px 9px;border-radius:20px;border:1px solid rgba(245,200,66,0.15);">{inv['tax_short']}</span>
            <div style="display:flex;align-items:center;gap:6px;">
                {risk_dots(inv['risk'])}
                <span style="color:#8A9B90;font-size:0.72rem;">{RISK_LABELS[inv['risk']]}</span>
            </div>
            <span style="color:#8A9B90;font-size:0.75rem;">Min <strong style="color:#F0F5F2;">€{inv['min']}</strong></span>
        </div>
    </div>
    """

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.2rem 0 0.5rem;">
        <div style="font-family:'DM Serif Display',serif;font-size:2.2rem;color:#2ECC71;letter-spacing:-0.02em;line-height:1;">Simplí</div>
        <div style="color:#8A9B90;font-size:0.78rem;margin-top:0.3rem;letter-spacing:0.06em;">Investing, Made Simple.</div>
        <div style="margin-top:0.8rem;display:inline-block;background:rgba(245,200,66,0.12);border:1px solid rgba(245,200,66,0.35);border-radius:20px;padding:3px 12px;">
            <span style="color:#F5C842;font-size:0.72rem;font-weight:700;letter-spacing:0.06em;">✦ No Ads. Ever.</span>
        </div>
    </div>
    <hr style="border-color:rgba(46,204,113,0.12);margin:1rem 0;">
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📋  The Menu", "🎯  Recommender", "📖  Walkthrough", "📊  Dashboard", "⚖️  Compare"],
        label_visibility="collapsed",
    )
    page = page.split("  ")[1]

    st.markdown("""
    <hr style="border-color:rgba(46,204,113,0.12);margin:1.5rem 0 1rem;">
    <div style="text-align:center;">
        <div style="color:#8A9B90;font-size:0.7rem;letter-spacing:0.04em;">🇮🇪 Built for Irish Investors</div>
        <div style="color:#8A9B90;font-size:0.68rem;margin-top:0.3rem;">Revenue-compliant tax rates</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 – THE MENU
# ══════════════════════════════════════════════════════════════════════════════
if page == "The Menu":
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <h1 style="font-family:'DM Serif Display',serif;font-size:2.6rem;color:#F0F5F2;margin:0;line-height:1.1;">
            The Investment Menu
        </h1>
        <p style="color:#8A9B90;font-size:1rem;margin-top:0.5rem;">
            13 categories. Every after-tax return. Zero jargon. Click any category to see a step-by-step guide.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filter bar
    col_f1, col_f2, col_f3 = st.columns([1, 1, 2])
    with col_f1:
        risk_filter = st.selectbox("Risk Level", ["All", "1 – Very Low", "2 – Low", "3 – Medium", "4 – High", "5 – Very High"])
    with col_f2:
        tax_filter = st.selectbox("Tax Type", ["All", "Tax-Free", "CGT 33%", "Exit Tax 41%", "DIRT 33%", "Income Tax"])
    with col_f3:
        sort_by = st.selectbox("Sort by", ["After-Tax Return ↓", "Gross Return ↓", "Risk ↑", "Min Investment ↑"])

    filtered = INVESTMENTS.copy()
    if risk_filter != "All":
        r = int(risk_filter[0])
        filtered = [i for i in filtered if i["risk"] == r]
    if tax_filter != "All":
        t = tax_filter.lower()
        filtered = [i for i in filtered if t in i["tax"].lower()]
    if sort_by == "After-Tax Return ↓":
        filtered.sort(key=lambda x: x["net"], reverse=True)
    elif sort_by == "Gross Return ↓":
        filtered.sort(key=lambda x: x["gross"], reverse=True)
    elif sort_by == "Risk ↑":
        filtered.sort(key=lambda x: x["risk"])
    elif sort_by == "Min Investment ↑":
        filtered.sort(key=lambda x: x["min"])

    st.markdown(f"<p style='color:#8A9B90;font-size:0.82rem;margin:0.5rem 0 1rem;'>{len(filtered)} of 13 categories shown</p>", unsafe_allow_html=True)

    cols = st.columns(3)
    for idx, inv in enumerate(filtered):
        with cols[idx % 3]:
            st.markdown(card(inv), unsafe_allow_html=True)
            if st.button(f"View Guide →", key=f"menu_btn_{inv['name']}"):
                st.session_state["walkthrough_inv"] = inv["name"]
                st.session_state["_nav"] = "Walkthrough"
                st.rerun()

    # Summary stats bar
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;margin-bottom:0.5rem;">
        <span style="color:#8A9B90;font-size:0.8rem;letter-spacing:0.06em;text-transform:uppercase;">Simplí Insight</span>
    </div>
    """, unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Best After-Tax Return", "10.1%", "Crypto (CGT 33%)")
    with m2:
        st.metric("Best Tax-Free Return", "3.0%", "An Post State Savings")
    with m3:
        st.metric("Lowest Risk Option", "Bank Deposits", "Risk 1/5")
    with m4:
        st.metric("Avg Tax Drag", "2.8%", "Gross minus Net")

# Handle nav redirect from button
if "_nav" in st.session_state:
    nav_target = st.session_state.pop("_nav")
    if nav_target == "Walkthrough":
        page = "Walkthrough"

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – THE RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Recommender":
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <h1 style="font-family:'DM Serif Display',serif;font-size:2.6rem;color:#F0F5F2;margin:0;line-height:1.1;">
            Find Your Perfect Investment
        </h1>
        <p style="color:#8A9B90;font-size:1rem;margin-top:0.5rem;">
            5 questions. 60 seconds. A personalised ranking of all 13 options.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "rec_step" not in st.session_state:
        st.session_state.rec_step = 0
    if "rec_answers" not in st.session_state:
        st.session_state.rec_answers = {}

    step = st.session_state.rec_step

    # Progress bar
    progress = step / 5
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <div style="display:flex;justify-content:space-between;margin-bottom:0.4rem;">
            <span style="color:#8A9B90;font-size:0.8rem;">Question {min(step+1,5)} of 5</span>
            <span style="color:#2ECC71;font-size:0.8rem;font-weight:600;">{int(progress*100)}% complete</span>
        </div>
        <div style="background:rgba(20,30,25,0.8);border-radius:20px;height:6px;">
            <div style="background:linear-gradient(90deg,#2ECC71,#27ae60);width:{int(progress*100)}%;height:6px;border-radius:20px;transition:width 0.4s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if step == 0:
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.6rem;color:#F0F5F2;margin-bottom:1rem;">How much are you looking to invest?</div>', unsafe_allow_html=True)
        amount = st.slider("", 500, 100000, 5000, step=500, format="€%d")
        st.markdown(f'<div style="color:#2ECC71;font-size:1.4rem;font-weight:700;text-align:center;margin:0.5rem 0;">€{amount:,}</div>', unsafe_allow_html=True)
        if st.button("Continue →"):
            st.session_state.rec_answers["amount"] = amount
            st.session_state.rec_step = 1
            st.rerun()

    elif step == 1:
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.6rem;color:#F0F5F2;margin-bottom:1.2rem;">How long can you leave it?</div>', unsafe_allow_html=True)
        horizon_opts = ["1–2 years", "3–5 years", "5–10 years", "10+ years"]
        sel = None
        cols = st.columns(2)
        for i, opt in enumerate(horizon_opts):
            with cols[i % 2]:
                chosen = st.session_state.rec_answers.get("horizon") == opt
                border = "rgba(46,204,113,0.7)" if chosen else "rgba(46,204,113,0.18)"
                bg = "rgba(46,204,113,0.1)" if chosen else "rgba(20,30,25,0.7)"
                st.markdown(f"""
                <div style="background:{bg};border:1px solid {border};border-radius:12px;padding:1rem;margin-bottom:0.5rem;text-align:center;">
                    <span style="font-size:0.95rem;color:#F0F5F2;font-weight:500;">{opt}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button(opt, key=f"h_{opt}", use_container_width=True):
                    st.session_state.rec_answers["horizon"] = opt
                    st.session_state.rec_step = 2
                    st.rerun()

    elif step == 2:
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.6rem;color:#F0F5F2;margin-bottom:0.5rem;">How would you feel if your investment dropped 20% in a year?</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#8A9B90;font-size:0.85rem;margin-bottom:1.2rem;">Be honest — it determines your risk profile.</div>', unsafe_allow_html=True)
        risk_opts = [
            ("😰", "I'd panic and sell", "risk_averse"),
            ("😬", "I'd be uncomfortable but hold", "conservative"),
            ("😐", "I wouldn't worry", "moderate"),
            ("😎", "I'd buy more", "aggressive"),
        ]
        for emoji, label, key in risk_opts:
            col_a, col_b = st.columns([1, 10])
            with col_a:
                st.markdown(f'<div style="font-size:1.8rem;text-align:center;padding-top:0.3rem;">{emoji}</div>', unsafe_allow_html=True)
            with col_b:
                if st.button(label, key=f"r_{key}", use_container_width=True):
                    st.session_state.rec_answers["risk_tolerance"] = key
                    st.session_state.rec_step = 3
                    st.rerun()

    elif step == 3:
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.6rem;color:#F0F5F2;margin-bottom:1.2rem;">What\'s the money for?</div>', unsafe_allow_html=True)
        goal_opts = [
            ("🛟", "Emergency fund"),
            ("🏠", "House deposit"),
            ("🏖️", "Retirement"),
            ("📈", "General growth"),
            ("🤔", "Just curious"),
        ]
        cols2 = st.columns(2)
        for i, (emoji, label) in enumerate(goal_opts):
            with cols2[i % 2]:
                if st.button(f"{emoji} {label}", key=f"g_{label}", use_container_width=True):
                    st.session_state.rec_answers["goal"] = label
                    st.session_state.rec_step = 4
                    st.rerun()

    elif step == 4:
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.6rem;color:#F0F5F2;margin-bottom:1.2rem;">How hands-on do you want to be?</div>', unsafe_allow_html=True)
        style_opts = [
            ("🤖", "Set it and forget it", "passive"),
            ("📆", "Check monthly", "semi_active"),
            ("🎯", "Actively manage", "active"),
        ]
        for emoji, label, key in style_opts:
            if st.button(f"{emoji}  {label}", key=f"s_{key}", use_container_width=True):
                st.session_state.rec_answers["style"] = key
                st.session_state.rec_step = 5
                st.rerun()

    elif step == 5:
        ans = st.session_state.rec_answers
        amount = ans.get("amount", 5000)
        horizon_str = ans.get("horizon", "5–10 years")
        risk_tol = ans.get("risk_tolerance", "moderate")
        goal = ans.get("goal", "General growth")
        style = ans.get("style", "passive")

        horizon_yrs = {"1–2 years": 1.5, "3–5 years": 4, "5–10 years": 7, "10+ years": 15}.get(horizon_str, 7)

        # Scoring algorithm
        risk_max = {"risk_averse": 1, "conservative": 2, "moderate": 3, "aggressive": 5}.get(risk_tol, 3)
        liquidity_pref = 3 if horizon_yrs <= 2 else 1

        scores = []
        for inv in INVESTMENTS:
            score = 0
            # Net return (most important)
            score += inv["net"] * 10
            # Risk match
            risk_diff = abs(inv["risk"] - risk_max)
            score -= risk_diff * 8
            # Liquidity match for short horizons
            liq_map = {"Very High": 5, "High": 4, "Medium": 3, "Low": 2, "Very Low": 1}
            if horizon_yrs <= 2 and liq_map.get(inv["liquidity"], 3) < 3:
                score -= 15
            # Goal-specific boosts
            if goal == "Retirement" and inv["name"] == "Pension / AVCs":
                score += 25
            if goal == "House deposit" and inv["risk"] <= 2:
                score += 10
            if goal == "Emergency fund" and inv["liquidity"] in ["Very High", "High"]:
                score += 8
            # Style match
            if style == "passive" and inv["name"] in ["ETFs", "Index Funds", "Pension / AVCs", "An Post State Savings"]:
                score += 8
            if style == "active" and inv["name"] in ["Individual Stocks", "Cryptocurrency"]:
                score += 8
            # Tax-free bonus for all
            if "Tax-Free" in inv["tax"]:
                score += 5
            scores.append((score, inv))

        scores.sort(reverse=True, key=lambda x: x[0])

        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(46,204,113,0.08),rgba(20,30,25,0.5));border:1px solid rgba(46,204,113,0.3);border-radius:16px;padding:1.5rem;margin-bottom:1.5rem;">
            <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;color:#F0F5F2;">Your Personalised Rankings</div>
            <div style="color:#8A9B90;font-size:0.85rem;margin-top:0.3rem;">Based on your profile • After Irish tax • Ranked best to worst</div>
        </div>
        """, unsafe_allow_html=True)

        # Top 3 highlighted
        for rank, (score, inv) in enumerate(scores[:3]):
            medals = ["🥇", "🥈", "🥉"]
            rec_reasons = {
                "ETFs": "Low-cost, diversified, and perfect for long-term passive investors.",
                "Index Funds": "Great for regular contributions with broad market exposure.",
                "Individual Stocks": "Best gross returns if you're comfortable with research and risk.",
                "Gold & Silver": "Solid inflation hedge that diversifies your portfolio.",
                "Bank Deposits": "Zero risk, zero hassle — perfect for short-term parking.",
                "Credit Union Savings": "Slightly better than banks with community ownership.",
                "Government Bonds": "Predictable, low-risk income with state backing.",
                "An Post State Savings": "Ireland's best risk-free return — completely tax-free.",
                "Prize Bonds": "State-backed capital with tax-free prize potential.",
                "REITs": "Property exposure without the landlord headaches.",
                "Peer-to-Peer Lending": "Higher yields for investors comfortable with credit risk.",
                "Pension / AVCs": "Unbeatable for retirement — tax relief makes it a no-brainer.",
                "Cryptocurrency": "Highest upside for aggressive investors with long time horizons.",
            }
            st.markdown(f"""
            <div style="background:rgba(46,204,113,0.06);border:1px solid rgba(46,204,113,0.35);border-radius:16px;padding:1.2rem 1.4rem;margin-bottom:0.8rem;">
                <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;">
                    <span style="font-size:1.5rem;">{medals[rank]}</span>
                    <span style="font-size:1.3rem;">{inv['icon']}</span>
                    <span style="font-family:'DM Serif Display',serif;font-size:1.2rem;color:#F0F5F2;">{inv['name']}</span>
                    <span style="margin-left:auto;color:#2ECC71;font-size:1.1rem;font-weight:700;">{inv['net']}% after tax</span>
                </div>
                <p style="color:#8A9B90;font-size:0.83rem;margin:0;">{rec_reasons.get(inv['name'], inv['desc'])}</p>
            </div>
            """, unsafe_allow_html=True)

        # Remaining ranked
        st.markdown("<details><summary style='color:#8A9B90;cursor:pointer;font-size:0.9rem;'>Show full ranking (all 13)</summary>", unsafe_allow_html=True)
        for rank, (score, inv) in enumerate(scores[3:], start=4):
            st.markdown(f"""
            <div style="display:flex;align-items:center;padding:0.6rem 1rem;border-bottom:1px solid rgba(46,204,113,0.08);">
                <span style="color:#8A9B90;width:2rem;font-size:0.85rem;">#{rank}</span>
                <span style="margin-right:0.5rem;">{inv['icon']}</span>
                <span style="color:#F0F5F2;flex:1;font-size:0.9rem;">{inv['name']}</span>
                <span style="color:#2ECC71;font-weight:600;font-size:0.9rem;">{inv['net']}%</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</details>", unsafe_allow_html=True)

        # Projected chart for top pick
        top_inv = scores[0][1]
        st.markdown(f"""
        <div style="margin:1.5rem 0 0.8rem;">
            <span style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:#F0F5F2;">Projected Value: {top_inv['icon']} {top_inv['name']}</span>
        </div>
        """, unsafe_allow_html=True)

        years = np.arange(0, int(horizon_yrs) + 1)
        values = [amount * (1 + top_inv["net"] / 100) ** y for y in years]
        inflation_values = [amount * (1 + 0.025) ** y for y in years]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=values,
            name=f"{top_inv['name']} ({top_inv['net']}% net)",
            line=dict(color="#2ECC71", width=3),
            fill="tozeroy", fillcolor="rgba(46,204,113,0.08)",
            hovertemplate="Year %{x}: €%{y:,.0f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=years, y=inflation_values,
            name="Inflation (2.5%)",
            line=dict(color="#8A9B90", width=1.5, dash="dot"),
            hovertemplate="Year %{x}: €%{y:,.0f}<extra></extra>",
        ))
        fig.add_annotation(
            x=years[-1], y=values[-1],
            text=f"€{values[-1]:,.0f}",
            showarrow=True, arrowhead=2, arrowcolor="#2ECC71",
            font=dict(color="#2ECC71", size=13, family="Sora"),
            bgcolor="rgba(20,30,25,0.8)", bordercolor="#2ECC71", borderwidth=1,
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(20,30,25,0.0)",
            plot_bgcolor="rgba(0,0,0,0.0)",
            font=dict(family="Sora", color="#8A9B90"),
            xaxis=dict(title="Years", gridcolor="rgba(46,204,113,0.08)", zeroline=False),
            yaxis=dict(title="Portfolio Value (€)", gridcolor="rgba(46,204,113,0.08)", zeroline=False, tickprefix="€", tickformat=",.0f"),
            legend=dict(x=0.02, y=0.98, bgcolor="rgba(0,0,0,0)"),
            height=350, margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        final = values[-1]
        gain = final - amount
        st.markdown(f"""
        <div style="display:flex;gap:1rem;margin-top:0.5rem;">
            <div style="flex:1;background:rgba(20,30,25,0.7);border:1px solid rgba(46,204,113,0.2);border-radius:12px;padding:0.9rem;text-align:center;">
                <div style="color:#8A9B90;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;">Starting amount</div>
                <div style="color:#F0F5F2;font-size:1.2rem;font-weight:700;">€{amount:,}</div>
            </div>
            <div style="flex:1;background:rgba(46,204,113,0.08);border:1px solid rgba(46,204,113,0.3);border-radius:12px;padding:0.9rem;text-align:center;">
                <div style="color:#8A9B90;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;">After {horizon_str}</div>
                <div style="color:#2ECC71;font-size:1.2rem;font-weight:700;">€{final:,.0f}</div>
            </div>
            <div style="flex:1;background:rgba(20,30,25,0.7);border:1px solid rgba(46,204,113,0.2);border-radius:12px;padding:0.9rem;text-align:center;">
                <div style="color:#8A9B90;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.06em;">After-tax gain</div>
                <div style="color:#2ECC71;font-size:1.2rem;font-weight:700;">+€{gain:,.0f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↩  Start Over"):
            st.session_state.rec_step = 0
            st.session_state.rec_answers = {}
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – THE WALKTHROUGH
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Walkthrough":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h1 style="font-family:'DM Serif Display',serif;font-size:2.6rem;color:#F0F5F2;margin:0;line-height:1.1;">
            Step-by-Step Guide
        </h1>
        <p style="color:#8A9B90;font-size:1rem;margin-top:0.5rem;">
            Select a category and follow the plain-language steps to get started today.
        </p>
    </div>
    """, unsafe_allow_html=True)

    default_inv = st.session_state.get("walkthrough_inv", "An Post State Savings")
    inv_names = [inv["name"] for inv in INVESTMENTS]
    default_idx = inv_names.index(default_inv) if default_inv in inv_names else 0

    selected_name = st.selectbox("Choose an investment category", inv_names, index=default_idx)
    inv = INV_MAP[selected_name]

    # Hero card
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(46,204,113,0.06),rgba(20,30,25,0.8));border:1px solid rgba(46,204,113,0.25);border-radius:20px;padding:1.8rem;margin:1rem 0 1.5rem;">
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;">
            <span style="font-size:2.5rem;">{inv['icon']}</span>
            <div>
                <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;color:#F0F5F2;">{inv['name']}</div>
                <div style="color:#8A9B90;font-size:0.9rem;">{inv['desc']}</div>
            </div>
        </div>
        <div style="display:flex;gap:1rem;flex-wrap:wrap;">
            <div style="background:rgba(46,204,113,0.1);border:1px solid rgba(46,204,113,0.25);border-radius:10px;padding:0.6rem 1.1rem;">
                <div style="color:#8A9B90;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;">After-Tax Return</div>
                <div style="color:#2ECC71;font-size:1.2rem;font-weight:700;">{inv['net']}% / yr</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:0.6rem 1.1rem;">
                <div style="color:#8A9B90;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;">Tax Treatment</div>
                <div style="color:#F5C842;font-size:0.9rem;font-weight:600;">{inv['tax']}</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:0.6rem 1.1rem;">
                <div style="color:#8A9B90;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;">Risk Level</div>
                <div style="color:#F0F5F2;font-size:0.95rem;font-weight:600;">{RISK_LABELS[inv['risk']]} ({inv['risk']}/5)</div>
            </div>
            <div style="background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:0.6rem 1.1rem;">
                <div style="color:#8A9B90;font-size:0.7rem;text-transform:uppercase;letter-spacing:0.06em;">Minimum</div>
                <div style="color:#F0F5F2;font-size:0.95rem;font-weight:600;">€{inv['min']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Pros & Cons
    col_p, col_c = st.columns(2)
    with col_p:
        pros_html = "".join([f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;"><span style="color:#2ECC71;font-size:0.9rem;">✓</span><span style="color:#F0F5F2;font-size:0.85rem;">{p}</span></div>' for p in inv["pros"]])
        st.markdown(f"""
        <div style="background:rgba(46,204,113,0.04);border:1px solid rgba(46,204,113,0.15);border-radius:12px;padding:1rem 1.2rem;">
            <div style="color:#2ECC71;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.6rem;font-weight:700;">Advantages</div>
            {pros_html}
        </div>
        """, unsafe_allow_html=True)
    with col_c:
        cons_html = "".join([f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem;"><span style="color:#e74c3c;font-size:0.9rem;">✗</span><span style="color:#F0F5F2;font-size:0.85rem;">{c}</span></div>' for c in inv["cons"]])
        st.markdown(f"""
        <div style="background:rgba(231,76,60,0.04);border:1px solid rgba(231,76,60,0.15);border-radius:12px;padding:1rem 1.2rem;">
            <div style="color:#e74c3c;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.6rem;font-weight:700;">Watch Out For</div>
            {cons_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'DM Serif Display',serif;font-size:1.4rem;color:#F0F5F2;margin-bottom:1rem;">
        How to Get Started
    </div>
    """, unsafe_allow_html=True)

    # Steps
    for i, (title, detail) in enumerate(inv["steps"]):
        num_colour = "#2ECC71" if i < len(inv["steps"]) - 1 else "#F5C842"
        connector = f'<div style="width:2px;height:20px;background:rgba(46,204,113,0.2);margin:0 auto 0 19px;"></div>' if i < len(inv["steps"]) - 1 else ""
        st.markdown(f"""
        <div style="display:flex;gap:1rem;align-items:flex-start;">
            <div style="flex-shrink:0;width:40px;height:40px;border-radius:50%;background:rgba(46,204,113,0.1);border:2px solid {num_colour};display:flex;align-items:center;justify-content:center;font-weight:700;color:{num_colour};font-size:0.9rem;">{i+1}</div>
            <div style="background:rgba(20,30,25,0.6);border:1px solid rgba(46,204,113,0.12);border-radius:12px;padding:0.9rem 1.1rem;flex:1;margin-bottom:0.3rem;">
                <div style="color:#F0F5F2;font-weight:600;font-size:0.95rem;margin-bottom:0.3rem;">{title}</div>
                <div style="color:#8A9B90;font-size:0.83rem;line-height:1.5;">{detail}</div>
            </div>
        </div>
        {connector}
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:1.5rem;background:rgba(245,200,66,0.06);border:1px solid rgba(245,200,66,0.2);border-radius:12px;padding:1rem 1.3rem;display:flex;align-items:center;gap:0.8rem;">
        <span style="font-size:1.3rem;">💡</span>
        <div style="color:#8A9B90;font-size:0.83rem;line-height:1.5;">
            <strong style="color:#F5C842;">Simplí Tip:</strong> With {inv['name']}, you keep <strong style="color:#2ECC71;">{inv['net']}%</strong> after Irish tax —
            versus {inv['gross']}% gross. That's the honest number. Most platforms only show you the gross.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 – DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Dashboard":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h1 style="font-family:'DM Serif Display',serif;font-size:2.6rem;color:#F0F5F2;margin:0;line-height:1.1;">
            My Portfolio
        </h1>
        <p style="color:#8A9B90;font-size:1rem;margin-top:0.5rem;">
            A clear view of your investments, tax events, and projected growth.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sample portfolio
    portfolio = [
        {"name": "An Post State Savings", "value": 5000, "net": 3.0, "icon": "🟢", "colour": "#2ECC71", "tax": "Tax-Free"},
        {"name": "ETFs", "value": 3000, "net": 4.7, "icon": "📊", "colour": "#3498db", "tax": "Exit Tax 41%"},
        {"name": "Government Bonds", "value": 2000, "net": 2.0, "icon": "📜", "colour": "#1abc9c", "tax": "CGT 33%"},
    ]
    total = sum(h["value"] for h in portfolio)

    # Top metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Portfolio Value", f"€{total:,}", "+€1,240 this year")
    with m2:
        blended_net = sum(h["value"] * h["net"] / total for h in portfolio)
        st.metric("Blended After-Tax Return", f"{blended_net:.1f}%", "Weighted average")
    with m3:
        val_5yr = sum(h["value"] * (1 + h["net"] / 100) ** 5 for h in portfolio)
        st.metric("Projected 5-Year Value", f"€{val_5yr:,.0f}", f"+€{val_5yr-total:,.0f}")
    with m4:
        st.metric("Holdings", "3", "Across 3 categories")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Growth line chart
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.2rem;color:#F0F5F2;margin-bottom:0.8rem;">Portfolio Growth Projection</div>', unsafe_allow_html=True)
        years = np.arange(0, 11)
        fig_growth = go.Figure()
        colours = ["#2ECC71", "#3498db", "#1abc9c"]
        port_total = np.zeros(len(years))
        for h, col_h in zip(portfolio, colours):
            vals = np.array([h["value"] * (1 + h["net"] / 100) ** y for y in years])
            port_total += vals
            fig_growth.add_trace(go.Scatter(
                x=years, y=vals, name=h["name"],
                line=dict(color=col_h, width=2),
                stackgroup="one",
                hovertemplate=f"{h['name']}<br>Year %{{x}}: €%{{y:,.0f}}<extra></extra>",
            ))
        fig_growth.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Sora", color="#8A9B90"),
            xaxis=dict(title="Years from now", gridcolor="rgba(46,204,113,0.06)", zeroline=False),
            yaxis=dict(title="Value (€)", gridcolor="rgba(46,204,113,0.06)", zeroline=False, tickprefix="€", tickformat=",.0f"),
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
            height=320, margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_growth, use_container_width=True)

    with col_right:
        # Donut chart
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.2rem;color:#F0F5F2;margin-bottom:0.8rem;">Allocation Breakdown</div>', unsafe_allow_html=True)
        fig_donut = go.Figure(data=[go.Pie(
            labels=[h["name"] for h in portfolio],
            values=[h["value"] for h in portfolio],
            hole=0.65,
            marker=dict(colors=["#2ECC71", "#3498db", "#1abc9c"], line=dict(color="#0B0F0E", width=3)),
            textinfo="percent",
            hovertemplate="%{label}<br>€%{value:,}<br>%{percent}<extra></extra>",
        )])
        fig_donut.add_annotation(
            text=f"€{total:,}", x=0.5, y=0.55, showarrow=False,
            font=dict(size=18, color="#F0F5F2", family="DM Serif Display"),
        )
        fig_donut.add_annotation(
            text="Total", x=0.5, y=0.42, showarrow=False,
            font=dict(size=12, color="#8A9B90", family="Sora"),
        )
        fig_donut.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(orientation="h", x=0, y=-0.1, font=dict(size=10), bgcolor="rgba(0,0,0,0)"),
            height=320, margin=dict(l=0, r=0, t=0, b=40),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # Holding cards
    st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.2rem;color:#F0F5F2;margin:1rem 0 0.8rem;">Holdings</div>', unsafe_allow_html=True)
    hold_cols = st.columns(3)
    for idx, h in enumerate(portfolio):
        val_5yr = h["value"] * (1 + h["net"] / 100) ** 5
        pct = h["value"] / total * 100
        with hold_cols[idx]:
            st.markdown(f"""
            <div style="background:rgba(20,30,25,0.7);border:1px solid rgba(46,204,113,0.18);border-radius:16px;padding:1.2rem;">
                <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.8rem;">
                    <span style="font-size:1.4rem;">{h['icon']}</span>
                    <span style="font-family:'DM Serif Display',serif;font-size:1rem;color:#F0F5F2;line-height:1.2;">{h['name']}</span>
                </div>
                <div style="font-size:1.6rem;font-weight:700;color:#2ECC71;margin-bottom:0.3rem;">€{h['value']:,}</div>
                <div style="color:#8A9B90;font-size:0.75rem;margin-bottom:0.8rem;">{pct:.0f}% of portfolio</div>
                <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:0.5rem 0.7rem;margin-bottom:0.6rem;">
                    <div style="color:#8A9B90;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.06em;">5-Year Projection</div>
                    <div style="color:#F0F5F2;font-weight:600;font-size:0.95rem;">€{val_5yr:,.0f}</div>
                </div>
                <div style="color:#F5C842;font-size:0.72rem;">{h['tax']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Tax Events
    st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.2rem;color:#F0F5F2;margin:1.5rem 0 0.8rem;">Upcoming Tax Events</div>', unsafe_allow_html=True)
    tax_events = [
        {"date": "31 Oct 2026", "type": "CGT Return", "desc": "Capital Gains Tax return due for 2025/2026 disposals", "holding": "Government Bonds", "urgency": "medium"},
        {"date": "01 Jun 2029", "type": "Deemed Disposal", "desc": "8-year deemed disposal on ETF holding — 41% Exit Tax applies to unrealised gains", "holding": "ETFs", "urgency": "high"},
        {"date": "31 Dec 2025", "type": "DIRT Summary", "desc": "Annual review of DIRT deducted at source — no action needed", "holding": "All", "urgency": "low"},
    ]
    urgency_colour = {"high": "#e74c3c", "medium": "#F5C842", "low": "#2ECC71"}
    for ev in tax_events:
        col_ev, col_detail = st.columns([1, 5])
        uc = urgency_colour[ev["urgency"]]
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:1rem;background:rgba(20,30,25,0.6);border:1px solid rgba(46,204,113,0.1);border-left:3px solid {uc};border-radius:10px;padding:0.8rem 1.1rem;margin-bottom:0.5rem;">
            <div style="min-width:100px;">
                <div style="color:{uc};font-size:0.75rem;font-weight:700;">{ev['date']}</div>
                <div style="color:#F0F5F2;font-size:0.82rem;font-weight:600;margin-top:2px;">{ev['type']}</div>
            </div>
            <div style="flex:1;">
                <div style="color:#8A9B90;font-size:0.8rem;">{ev['desc']}</div>
            </div>
            <div style="background:rgba(46,204,113,0.08);border-radius:6px;padding:3px 9px;font-size:0.72rem;color:#8A9B90;">{ev['holding']}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 – COMPARE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Compare":
    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <h1 style="font-family:'DM Serif Display',serif;font-size:2.6rem;color:#F0F5F2;margin:0;line-height:1.1;">
            Side-by-Side Comparison
        </h1>
        <p style="color:#8A9B90;font-size:1rem;margin-top:0.5rem;">
            The chart that changes minds. See how Irish tax affects your <em>real</em> returns over time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    inv_names = [inv["name"] for inv in INVESTMENTS]

    col_c1, col_c2, col_c3 = st.columns([3, 1.5, 1.5])
    with col_c1:
        selected = st.multiselect(
            "Select 2–4 investments to compare",
            inv_names,
            default=["ETFs", "An Post State Savings", "Cryptocurrency", "Bank Deposits"],
            max_selections=4,
        )
    with col_c2:
        cmp_amount = st.number_input("Investment amount (€)", min_value=100, max_value=500000, value=10000, step=500)
    with col_c3:
        cmp_years = st.slider("Time horizon (years)", 1, 30, 10)

    inflation_rate = 0.025

    if len(selected) < 2:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:#8A9B90;border:1px dashed rgba(46,204,113,0.2);border-radius:16px;margin-top:1rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📊</div>
            <div>Select at least 2 investments to compare</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        chart_colours = ["#2ECC71", "#3498db", "#F5C842", "#e74c3c", "#fd79a8", "#74b9ff"]
        years_arr = np.arange(0, cmp_years + 1)
        inflation_vals = [cmp_amount * (1 + inflation_rate) ** y for y in years_arr]

        fig_cmp = go.Figure()

        # Inflation baseline
        fig_cmp.add_trace(go.Scatter(
            x=years_arr, y=inflation_vals, name="Inflation (2.5%)",
            line=dict(color="rgba(138,155,144,0.5)", width=1.5, dash="dot"),
            hovertemplate="Inflation<br>Year %{x}: €%{y:,.0f}<extra></extra>",
        ))

        final_vals = []
        for i, name in enumerate(selected):
            inv = INV_MAP[name]
            net_r = inv["net"] / 100
            vals = [cmp_amount * (1 + net_r) ** y for y in years_arr]
            final_vals.append((name, vals[-1], inv["gross"], inv["net"], inv["tax_short"]))
            col_h = chart_colours[i % len(chart_colours)]
            fig_cmp.add_trace(go.Scatter(
                x=years_arr, y=vals,
                name=f"{inv['icon']} {name} ({inv['net']}% net)",
                line=dict(color=col_h, width=2.5),
                hovertemplate=f"{name}<br>Year %{{x}}: €%{{y:,.0f}}<extra></extra>",
            ))
            fig_cmp.add_annotation(
                x=cmp_years, y=vals[-1],
                text=f"€{vals[-1]:,.0f}",
                showarrow=False,
                xanchor="left", xshift=8,
                font=dict(color=col_h, size=11, family="Sora"),
            )

        fig_cmp.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Sora", color="#8A9B90"),
            xaxis=dict(title="Years", gridcolor="rgba(46,204,113,0.07)", zeroline=False),
            yaxis=dict(title="Portfolio Value (€)", gridcolor="rgba(46,204,113,0.07)", zeroline=False, tickprefix="€", tickformat=",.0f"),
            legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)"),
            height=480, margin=dict(l=10, r=100, t=20, b=10),
        )
        st.plotly_chart(fig_cmp, use_container_width=True)

        # Summary table
        st.markdown('<div style="font-family:\'DM Serif Display\',serif;font-size:1.2rem;color:#F0F5F2;margin:0.5rem 0 0.8rem;">Final Values After {} Years</div>'.format(cmp_years), unsafe_allow_html=True)
        final_vals.sort(key=lambda x: x[1], reverse=True)
        best_val = final_vals[0][1]
        for rank, (name, fval, gross, net, tax) in enumerate(final_vals):
            inv = INV_MAP[name]
            bar_pct = fval / best_val * 100
            col_bar = chart_colours[selected.index(name) % len(chart_colours)]
            diff_from_best = fval - best_val if rank == 0 else fval - best_val
            diff_label = f"+€{diff_from_best:,.0f}" if diff_from_best >= 0 else f"€{diff_from_best:,.0f}"
            diff_colour = "#2ECC71" if diff_from_best >= 0 else "#e74c3c"

            st.markdown(f"""
            <div style="background:rgba(20,30,25,0.7);border:1px solid rgba(46,204,113,0.12);border-radius:12px;padding:1rem 1.2rem;margin-bottom:0.5rem;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.6rem;">
                    <div style="display:flex;align-items:center;gap:0.6rem;">
                        <span style="font-size:1.2rem;">{inv['icon']}</span>
                        <span style="color:#F0F5F2;font-weight:600;">{name}</span>
                        <span style="background:rgba(245,200,66,0.1);border:1px solid rgba(245,200,66,0.2);border-radius:20px;padding:2px 8px;font-size:0.7rem;color:#F5C842;">{tax}</span>
                    </div>
                    <div style="text-align:right;">
                        <span style="color:#2ECC71;font-size:1.1rem;font-weight:700;">€{fval:,.0f}</span>
                        <span style="color:{diff_colour};font-size:0.8rem;margin-left:0.5rem;">{diff_label}</span>
                    </div>
                </div>
                <div style="background:rgba(0,0,0,0.3);border-radius:4px;height:5px;overflow:hidden;">
                    <div style="background:{col_bar};width:{bar_pct:.1f}%;height:5px;border-radius:4px;transition:width 0.5s ease;"></div>
                </div>
                <div style="display:flex;justify-content:space-between;margin-top:0.4rem;">
                    <span style="color:#8A9B90;font-size:0.72rem;">Gross: {gross}% → After tax: {net}%</span>
                    <span style="color:#8A9B90;font-size:0.72rem;">Tax drag: {gross-net:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # The key insight callout
        if len(final_vals) >= 2:
            top = final_vals[0]
            bottom = final_vals[-1]
            spread = top[1] - bottom[1]
            st.markdown(f"""
            <div style="margin-top:1rem;background:linear-gradient(135deg,rgba(46,204,113,0.06),rgba(20,30,25,0.6));border:1px solid rgba(46,204,113,0.3);border-radius:16px;padding:1.3rem 1.5rem;display:flex;align-items:flex-start;gap:1rem;">
                <span style="font-size:1.5rem;flex-shrink:0;">💡</span>
                <div>
                    <div style="color:#F0F5F2;font-weight:600;margin-bottom:0.3rem;">The Simplí Insight</div>
                    <div style="color:#8A9B90;font-size:0.85rem;line-height:1.6;">
                        After {cmp_years} years, <strong style="color:#2ECC71;">{top[0]}</strong> returns <strong style="color:#2ECC71;">€{top[1]:,.0f}</strong>
                        versus <strong style="color:#e74c3c;">€{bottom[1]:,.0f}</strong> from <strong style="color:#e74c3c;">{bottom[0]}</strong> —
                        a difference of <strong style="color:#F0F5F2;">€{spread:,.0f}</strong>.
                        This is what Irish tax really costs you. Most platforms hide this number. Simplí doesn't.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
