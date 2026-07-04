import streamlit as st
import yfinance as yf
import feedparser

# 1. Page Configuration for optimal mobile scannability
st.set_page_config(
    page_title="Gold Core-Lock Matrix",
    page_icon="🔱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.title("🦅 Gold Core-Lock Alpha Matrix")
st.markdown("##### Priority Intermarket Alignment & Consensus Filter Engine")

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
if st.button("EXECUTE CORE-LOCK CONSENSUS SCAN", type="primary", use_container_width=True):
    
    with st.spinner("Evaluating Tier-1 Priority Anchors (DXY, Yields, Miners)..."):
        
        error_logs = []
        ticker_details = []
        
        # --- TRACK TIER-1 CORE MACRO ANCHORS ---
        core_direction = 0 #  0 = Conflict, 1 = Perfect Bullish Core, -1 = Perfect Bearish Core
        dxy_score = 0.0
        tlt_score = 0.0   # (TLT rising means yields are dropping)
        
        try:
            dxy_data = yf.Ticker("DX-Y.NYB").history(period="7d")
            tlt_data = yf.Ticker("TLT").history(period="7d")
            
            if len(dxy_data) >= 2 and len(tlt_data) >= 2:
                dxy_pct = ((dxy_data['Close'].iloc[-1] - dxy_data['Close'].iloc[-2]) / dxy_data['Close'].iloc[-2]) * 100
                tlt_pct = ((tlt_data['Close'].iloc[-1] - tlt_data['Close'].iloc[-2]) / tlt_data['Close'].iloc[-2]) * 100
                
                dxy_score = 2.0 if dxy_pct <= 0 else -2.0
                tlt_score = 2.0 if tlt_pct > 0 else -2.0
                
                dxy_status = "🟢 DXY Falling (Bullish)" if dxy_pct <= 0 else "🔴 DXY Rising (Bearish)"
                tlt_status = "🟢 Yields Dropping (Bullish)" if tlt_pct > 0 else "🔴 Yields Rising (Bearish)"
                
                ticker_details.append(f"**DXY Index**: {dxy_status} | *Weight: {dxy_score:+.1f} pts*")
                ticker_details.append(f"**US10Y Bond Proxy (TLT)**: {tlt_status} | *Weight: {tlt_score:+.1f} pts*")
            else:
                error_logs.append("❌ Core Tickers: Broken data frame structure array from server.")
        except Exception as e:
            error_logs.append(f"⚠️ Core Tickers Connection Error: {str(e)}")

        # --- TRACK TIER-1 MINERS basket CONSENSUS ---
        miner_basket = {"Barrick Gold": "GOLD", "Newmont Corp": "NEM", "Gold Fields": "GFI", "Agnico Eagle": "AEM", "Junior Miners ETF": "GDXJ"}
        miner_directions = []
        miner_errors = 0
        
        for m_name, m_symbol in miner_basket.items():
            try:
                m_data = yf.Ticker(m_symbol).history(period="7d")
                if len(m_data) >= 2:
                    m_change = m_data['Close'].iloc[-1] - m_data['Close'].iloc[-2]
                    miner_directions.append(1 if m_change > 0 else -1)
                else: miner_errors += 1
            except: miner_errors += 1
                
        miner_points = 0.0
        miner_status_display = "⚪ MIXED CHOP MARKET ACTION (Miners are fighting each other)"
        
        if miner_errors == 0 and len(miner_directions) == 5:
            if all(d == 1 for d in miner_directions):
                miner_points = 2.5
                miner_status_display = "🟢 UNANIMOUS BULLISH ACCUMULATION (All 5 Giants are rising)"
            elif all(d == -1 for d in miner_directions):
                miner_points = -2.5
                miner_status_display = "🔴 UNANIMOUS BEARISH DISTRIBUTION (All 5 Giants are falling)"
        else:
            error_logs.append("⚠️ Miners Basket: Isolated due to background server latency pings.")

        # --- EVALUATE STRICTOR TIER-1 CORE-LOCK ALIGNMENT GATE ---
        if dxy_score == 2.0 and tlt_score == 2.0 and miner_points == 2.5:
            core_direction = 1 # Perfect Bullish Core Lock Unlocked
        elif dxy_score == -2.0 and tlt_score == -2.0 and miner_points == -2.5:
            core_direction = -1 # Perfect Bearish Core Lock Unlocked
        else:
            core_direction = 0 # CORE DIRECTIVES CONFLICTING -> Force Immediate Safe Wait Halt
        master_score = dxy_score + tlt_score + miner_points
        headline_counter = 0
        news_points = 0.0
        news_log_entries = []

        # Process secondary multipliers ONLY if the strict core priority anchors match direction perfectly
        if core_direction != 0:
            secondary_tickers = {"VIX (CBOE Fear Index)": "^VIX", "SPY (S&P 500 Stock Benchmark)": "SPY", "TIP (Real Yields Tracker)": "TIP", "FXE (Euro Safe Haven Flux)": "FXE"}
            for name, symbol in secondary_tickers.items():
                try:
                    data = yf.Ticker(symbol).history(period="7d")
                    if len(data) >= 2:
                        prev_close = data['Close'].iloc[-2]
                        curr_close = data['Close'].iloc[-1]
                        pct_change = ((curr_close - prev_close) / prev_close) * 100
                        
                        if symbol == "^VIX":
                            w = 1.5 if curr_close > 20 else -0.5
                            status = f"📊 Volatility Level: {curr_close:.2f}"
                        elif symbol == "SPY":
                            w = -1.0 if pct_change > 0 else 1.0
                            status = "🔴 Rallying (Risk-On)" if pct_change > 0 else "🟢 Correcting (Risk-Off)"
                        elif symbol == "TIP":
                            w = 1.5 if pct_change > 0 else -1.5
                            status = "🟢 Bonds Inflow (Bullish)" if pct_change > 0 else "🔴 Bonds Outflow (Bearish)"
                        elif symbol == "FXE":
                            w = -1.0 if pct_change > 0 else 1.5
                            status = "🔴 Euro Strong" if pct_change > 0 else "🟢 Inflows Active"
                            
                        master_score += w
                        ticker_details.append(f"**{name}**: {status} | *Weight: {w:+.1f} pts*")
                except: pass

            # --- LIVE NEWS SENTIMENT INTEGRATION MODULE ---
            rss_urls = ["https://google.com", "https://google.com"]
            news_score_total = 0.0
            for url in rss_urls:
                try:
                    feed = feedparser.parse(url)
                    for entry in feed.entries[:4]:
                        text_headline = entry.title
                        comp_score = calculate_headline_sentiment(text_headline)
                        news_score_total += comp_score
                        headline_counter += 1
                        tag = "🟢 Bullish" if comp_score > 0 else "🔴 Bearish" if comp_score < 0 else "⚪ Neutral"
                        news_log_entries.append(f"*{tag}* -> {text_headline}")
                except: pass
            news_points = max(-1.5, min(1.5, news_score_total))
            master_score += news_points

        # --- PHASE 4: RENDER RESPONSIVE MOBILE DASHBOARD INTERFACE CANVAS ---
        st.markdown("---")
        st.subheader("📊 Definitive Priority Directive")
        
        if core_direction == 0:
            st.warning("### ⏳ DIRECTION: CORE MATRIX CONFLICT / CHOP WAIT\n"
                       "**Reason**: Your core priority pillars (DXY, Yields, and Miners) are out of alignment. "
                       "The fundamental engine has blocked all further scans to save your trading capital from sideways range traps.")
        elif core_direction == 1:
            if master_score >= 6.0:
                st.success("### 🔥 DIRECTION: STRONG BULLISH BUY\nCore pillars are locked long, and secondary multipliers confirm heavy macro tailwinds.")
            else:
                st.success("### 📈 DIRECTION: STANDARD BULLISH BUY\nCore anchors confirm buy alignment, but secondary market vectors sit flat.")
        elif core_direction == -1:
            if master_score <= -6.0:
                st.error("### 📉 DIRECTION: STRONG BEARISH SELL\nCore pillars are locked short, and institutions are heavily distributing safe-haven liquidity.")
            else:
                st.error("### 📉 DIRECTION: STANDARD BEARISH SELL\nCore anchors confirm short alignment, but secondary market sentiment sits flat.")

        st.metric(label="Consensus Score Summary", value=f"{master_score:+.2f} Points" if core_direction != 0 else "0.00 LOCKED", delta="Priority lock requires un-conflicting Tier-1 alignment")
        
        with st.expander("🔎 View Macro Assets Priority Matrix Breakdown", expanded=True):
            for detail in ticker_details: st.write(detail)
            st.write(f"**Gold Miners Basket Consensus**: {miner_status_display} | *Weight: {miner_points:+.1f} pts*")
                
        if core_direction != 0 and headline_counter > 0:
            with st.expander(f"📰 View Scraped Headline Database Logs ({headline_counter} items)", expanded=False):
                st.write(f"**Headline Structural Impact Score**: `{news_points:+.2f} pts`")
                for log in news_log_entries: st.write(log)
                
        if len(error_logs) > 0:
            with st.expander("⚠️ View Real-Time Server Error Audits", expanded=False):
                for err in error_logs: st.write(err)
