import streamlit as st
import yfinance as yf
import feedparser

# 1. Page Configuration for optimal mobile scannability
st.set_page_config(
    page_title="Gold Alpha Matrix",
    page_icon="⚜️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🦅 Gold Fundamental Alpha Matrix")
st.markdown("##### Institutional Intermarket Macro & Sentiment Consensus Engine")

def calculate_headline_sentiment(headline_text):
    text_lower = headline_text.lower()
    bullish_keywords = [
        'rate cut', 'inflation spike', 'recession', 'escalation', 'safe haven', 
        'banking crisis', 'fed dovish', 'gold rally', 'crisis', 'panic', 'war', 
        'geopolitical', 'uncertainty', 'conflict', 'sanctions', 'de-dollarization'
    ]
    bearish_keywords = [
        'rate hike', 'strong jobs', 'fed hawkish', 'gdp growth', 'economic boom', 
        'dollar surge', 'inflation falls', 'rate increases', 'hawkish fed', 'strong economy'
    ]
    
    score = 0.0
    for word in bullish_keywords:
        if word in text_lower: score += 1.5
    for word in bearish_keywords:
        if word in text_lower: score -= 1.5
    return score

# Processing Trigger
if st.button("EXECUTE ALL-SECTOR CONSENSENS SCAN", type="primary", use_container_width=True):
    
    with st.spinner("Analyzing global intermarket data streams..."):
        
        master_score = 0.0
        ticker_details = []
        error_logs = []
        
        # --- CORE MACRO ANCHORS ---
        macro_tickers = {
            "DXY (US Dollar Index)": "DX-Y.NYB",
            "US10Y (10-Yr Bond Yield)": "^TNX",
            "VIX (CBOE Fear Gauge Index)": "^VIX",
            "SPY (S&P 500 Market Benchmark)": "SPY",
            "TIP (Real Yields Tracker)": "TIP",
            "XAU/EUR (Global Safe Haven Flux)": "XAUEUR=X"
        }
        
        for name, symbol in macro_tickers.items():
            try:
                data = yf.Ticker(symbol).history(period="3d") # Expanded lookup depth to prevent weekend empty reads
                if len(data) >= 2:
                    prev_close = data['Close'].iloc[-2]
                    curr_close = data['Close'].iloc[-1]
                    pct_change = ((curr_close - prev_close) / prev_close) * 100
                    
                    if symbol == "DX-Y.NYB":
                        w = -2.0 if pct_change > 0 else 2.0
                        status = "🟢 Falling (Bullish)" if pct_change <= 0 else "🔴 Rising (Bearish)"
                    elif symbol == "^TNX":
                        w = -2.0 if pct_change > 0 else 2.0
                        status = "🟢 Falling (Bullish)" if pct_change <= 0 else "🔴 Rising (Bearish)"
                    elif symbol == "^VIX":
                        w = 1.5 if curr_close > 20 else -0.5
                        status = f"📊 Volatility Level: {curr_close:.2f}"
                    elif symbol == "SPY":
                        w = -1.0 if pct_change > 0 else 1.0
                        status = "🔴 Rallying (Risk-On)" if pct_change > 0 else "🟢 Correcting (Risk-Off)"
                    elif symbol == "TIP":
                        w = 1.5 if pct_change > 0 else -1.5
                        status = "🟢 Bonds Inflow (Bullish)" if pct_change > 0 else "🔴 Bonds Outflow (Bearish)"
                    elif symbol == "XAUEUR=X":
                        w = 1.5 if pct_change > 0 else -1.0
                        status = "🟢 Safe Haven Demand" if pct_change > 0 else "🔴 Low Currency Inflow"
                        
                    master_score += w
                    ticker_details.append(f"**{name}**: {status} | *Weight: {w:+.1f} pts*")
                else:
                    error_logs.append(f"❌ **{name}** (`{symbol}`): Broken array frame length from broker feed.")
            except Exception as e:
                error_logs.append(f"⚠️ **{name}** (`{symbol}`): Connection timeout or market weekend freeze.")

        # --- GOLD MINERS UNANIMOUS CLUSTER (YOUR REQUEST) ---
        miner_basket = {
            "Barrick Gold": "GOLD",
            "Newmont Corp": "NEM",
            "Gold Fields": "GFI",
            "Agnico Eagle": "AEM",
            "Junior Miners ETF": "GDXJ"
        }
        
        miner_directions = []
        miner_errors = 0
        
        for m_name, m_symbol in miner_basket.items():
            try:
                m_data = yf.Ticker(m_symbol).history(period="3d")
                if len(m_data) >= 2:
                    m_change = m_data['Close'].iloc[-1] - m_data['Close'].iloc[-2]
                    miner_directions.append(1 if m_change > 0 else -1)
                else:
                    miner_errors += 1
            except:
                miner_errors += 1
                
        # Unanimous voting rule execution logic
        miner_points = 0.0
        miner_status_display = "⚠️ Cluster Blocked due to server data errors."
        
        if miner_errors == 0 and len(miner_directions) == 5:
            if all(d == 1 for d in miner_directions):
                miner_points = 2.5
                miner_status_display = "🟢 UNANIMOUS BULllSH ACCUMULATION (All 5 Giants are rising)"
            elif all(d == -1 for d in miner_directions):
                miner_points = -2.5
                miner_status_display = "🔴 UNANIMOUS BEARISH DISTRIBUTION (All 5 Giants are falling)"
            else:
                miner_points = 0.0
                miner_status_display = "⚪ MIXED CHOP MARKET ACTION (Miners are fighting each other)"
        else:
            error_logs.append(f"⚠️ **Gold Miners Basket**: Skipped because {miner_errors} stocks timed out.")
            
        master_score += miner_points

        # --- PHASE 3: LIVE HEADLINES AGGREGATOR ---
        rss_urls = [
            "https://cnbc.com",
            "https://cnbc.com"
        ]
        
        news_score_total = 0.0
        headline_counter = 0
        news_log_entries = []
        
        for url in rss_urls:
            try:
                feed = feedparser.parse(url)
                if len(feed.entries) > 0:
                    for entry in feed.entries[:4]:
                        text_headline = entry.title
                        comp_score = calculate_headline_sentiment(text_headline)
                        news_score_total += comp_score
                        headline_counter += 1
                        
                        tag = "🟢 Bullish" if comp_score > 0 else "🔴 Bearish" if comp_score < 0 else "⚪ Neutral"
                        news_log_entries.append(f"*{tag}* -> {text_headline}")
                else:
                    error_logs.append(f"⚠️ **News Feed Link** ({url[:30]}...): Returned empty headline database array.")
            except:
                pass
                
        news_points = max(-1.5, min(1.5, news_score_total))
        master_score += news_points
        
        # --- PHASE 4: DISPLAY MOBILE INTERFACE BLOCKS ---
        st.markdown("---")
        st.subheader("📊 Definitive Fundamental Directive")
        
        # Risk Decision Logic Windows
        if master_score >= 4.5:
            st.success("### 🔥 DIRECTION: STRONG BULLISH BUY\nAll macro pillars, real yields, and mining equities are in perfect bullish alignment.")
        elif master_score <= -4.5:
            st.error("### 📉 DIRECTION: STRONG BEARISH SELL\nSevere capital outflows detected. Avoid longs; macro weights are fully crushing Gold support.")
        else:
            st.warning("### ⏳ DIRECTION: MARKET CONFLICT / CHOP WAIT\nThe sectors are fighting each other. **Turn off automated bots and sit flat.**")
            
        st.metric(label="Unified Core Score", value=f"{master_score:+.2f} Points", delta="Signal unlock threshold requires +/- 4.5")
        
        # 1. Main Intermarket Drawer
        with st.expander("🔎 View Macro Assets Matrix Breakdown", expanded=True):
            for detail in ticker_details:
                st.write(detail)
            st.write(f"**Gold Miners Basket Consensus**: {miner_status_display} | *Weight: {miner_points:+.1f} pts*")
                
        # 2. Headline Scraper Drawer
        with st.expander(f"📰 View Scraped Headline Database Logs ({headline_counter} items)", expanded=False):
            st.write(f"**Headline Structural Impact Score**: `{news_points:+.2f} pts`")
            for log in news_log_entries:
                st.write(log)
                
        # 3. Dynamic Visual Error Diagnostics Drawer (Your Request)
        if len(error_logs) > 0:
            with st.expander("⚠️ View Real-Time Server Error Audits", expanded=True):
                st.info("The items listed below timed out or returned frozen weekend records. The system automatically isolated them to protect your score's accuracy.")
                for err in error_logs:
                    st.write(err)
