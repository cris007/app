import streamlit as st
import yfinance as yf
import feedparser
import pandas as pd

# 1. Page Configuration for optimal mobile responsive viewing
st.set_page_config(
    page_title="Gold Core-Lock Cockpit",
    page_icon="🔱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Institutional CSS Injector for Dark Mode Accent Styles
st.markdown("""
    <style>
    .metric-card {
        background-color: #0E1612;
        border: 1px solid #1E3A24;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 15px;
    }
    .gauge-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .gauge-bg {
        width: 100%;
        max-width: 400px;
        background: #121A16;
        border-radius: 20px;
        border: 1px solid #233D2A;
        padding: 20px;
        text-align: center;
    }
    .status-text {
        font-size: 24px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚜️ Gold Alpha Intelligence Cockpit")
st.markdown("##### Institutional Macroeconomic Alignment & Sentiment Consensus Matrix")

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
if st.button("RUN DEEP SECTOR LIQUIDITY AND METRIC SCAN", type="primary", use_container_width=True):
    
    with st.spinner("Compiling cross-asset consensus framework database..."):
        
        error_logs = []
        news_log_entries = []
        table_rows = [] 
        
        dxy_score = 0.0
        tlt_score = 0.0   
        miner_points = 0.0
        secondary_points = 0.0
        news_points = 0.0
        
        core_direction = 0 
        headline_counter = 0

        # --- TRACK TIER-1 PRIORITY ANCHOR: DXY INDEX ---
        try:
            dxy_data = yf.Ticker("DX-Y.NYB").history(period="7d")
            if len(dxy_data) >= 2:
                dxy_val = dxy_data['Close'].iloc[-1]
                dxy_pct = ((dxy_val - dxy_data['Close'].iloc[-2]) / dxy_data['Close'].iloc[-2]) * 100
                dxy_score = 2.0 if dxy_pct <= 0 else -2.0
                status_dxy = "🟢 Falling (Bullish)" if dxy_pct <= 0 else "🔴 Rising (Bearish)"
                table_rows.append({"Type": "Primary Core", "Asset": "DXY (US Dollar Index)", "Value": f"{dxy_val:.2f}", "Change %": f"{dxy_pct:+.2f}%", "Points": f"{dxy_score:+.1f}"})
            else: 
                error_logs.append("❌ DXY Index: Empty array returned from database server.")
        except Exception as e: 
            error_logs.append(f"⚠️ DXY Index Data Link Error: {str(e)}")

        # --- TRACK TIER-1 PRIORITY ANCHOR: BOND YIELDS PROXY ---
        try:
            tlt_data = yf.Ticker("TLT").history(period="7d")
            if len(tlt_data) >= 2:
                tlt_val = tlt_data['Close'].iloc[-1]
                tlt_pct = ((tlt_val - tlt_data['Close'].iloc[-2]) / tlt_data['Close'].iloc[-2]) * 100
                tlt_score = 2.0 if tlt_pct > 0 else -2.0
                status_tlt = "🟢 Yields Dropping (Bullish)" if tlt_pct > 0 else "🔴 Yields Rising (Bearish)"
                table_rows.append({"Type": "Primary Core", "Asset": "US10Y Yield Proxy (TLT)", "Value": f"${tlt_val:.2f}", "Change %": f"{tlt_pct:+.2f}%", "Points": f"{tlt_score:+.1f}"})
            else: 
                error_logs.append("❌ Bond Yields: Empty array returned from database server.")
        except Exception as e: 
            error_logs.append(f"⚠️ Bond Yields Data Link Error: {str(e)}")

        # --- TRACK TIER-1 PRIORITY ANCHOR: MINERS BASKET CONSENSUS ---
        miner_basket = {"Barrick Gold": "GOLD", "Newmont Corp": "NEM", "Gold Fields": "GFI", "Agnico Eagle": "AEM", "Junior Miners ETF": "GDXJ"}
        miner_directions = []
        miner_errors = 0
        miner_val_sum = 0.0
        miner_pct_sum = 0.0
        
        for m_name, m_symbol in miner_basket.items():
            try:
                m_data = yf.Ticker(m_symbol).history(period="7d")
                if len(m_data) >= 2:
                    m_val = m_data['Close'].iloc[-1]
                    m_change = ((m_val - m_data['Close'].iloc[-2]) / m_data['Close'].iloc[-2]) * 100
                    miner_val_sum += m_val
                    miner_pct_sum += m_change
                    miner_directions.append(1 if m_change > 0 else -1)
                else: miner_errors += 1
            except: miner_errors += 1
                
        miner_status_display = "⚪ MIXED MARKET CHOP (Miners out of sync)"
        
        if miner_errors == 0 and len(miner_directions) == 5:
            avg_m_val = miner_val_sum / 5
            avg_m_pct = miner_pct_sum / 5
            if all(d == 1 for d in miner_directions):
                miner_points = 2.5
                miner_status_display = "🟢 UNANIMOUS BULLISH ACCUMULATION"
            elif all(d == -1 for d in miner_directions):
                miner_points = -2.5
                miner_status_display = "🔴 UNANIMOUS BEARISH DISTRIBUTION"
            table_rows.append({"Type": "Primary Core", "Asset": "Miners Basket (5 Giants)", "Value": f"Avg: ${avg_m_val:.2f}", "Change %": f"{avg_m_pct:+.2f}%", "Points": f"{miner_points:+.1f}"})
        else:
            error_logs.append("⚠️ Gold Miners Basket Data Feed Latency Timeout.")

        # --- VERIFY CRITICAL CORE-LOCK GATE ---
        if dxy_score == 2.0 and tlt_score == 2.0 and miner_points == 2.5:
            core_direction = 1  # Bullish Lock Passed
        elif dxy_score == -2.0 and tlt_score == -2.0 and miner_points == -2.5:
            core_direction = -1 # Bearish Lock Passed
        # --- TRACK TIER-2 SECONDARY MACRO ANCHORS ---
        secondary_tickers = {"VIX (CBOE Fear Index)": "^VIX", "SPY (S&P 500 Benchmark)": "SPY", "TIP (Real Yields Tracker)": "TIP", "FXE (Euro Safe Haven Flux)": "FXE"}
        
        for name, symbol in secondary_tickers.items():
            try:
                data = yf.Ticker(symbol).history(period="7d")
                if len(data) >= 2:
                    val = data['Close'].iloc[-1]
                    pct = ((val - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
                    
                    if symbol == "^VIX": w = 1.5 if val > 20 else -0.5
                    elif symbol == "SPY": w = -1.0 if pct > 0 else 1.0
                    elif symbol == "TIP": w = 1.5 if pct > 0 else -1.5
                    elif symbol == "FXE": w = -1.0 if pct > 0 else 1.5
                    
                    if core_direction != 0:
                        secondary_points += w
                        table_rows.append({"Type": "Secondary Vector", "Asset": name, "Value": f"{val:.2f}" if symbol == "^VIX" else f"${val:.2f}", "Change %": f"{pct:+.2f}%", "Points": f"{w:+.1f}"})
                    else:
                        table_rows.append({"Type": "Secondary Vector", "Asset": name, "Value": f"{val:.2f}" if symbol == "^VIX" else f"${val:.2f}", "Change %": f"{pct:+.2f}%", "Points": "LOCKED"})
            except:
                error_logs.append(f"⚠️ {name} Connection Latency Timeout.")

        # --- PARSE LIVE RSS NEWS DATA STREAMS ---
        if core_direction != 0:
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
                        tag = "🟢 Bull" if comp_score > 0 else "🔴 Bear" if comp_score < 0 else "⚪ Neut"
                        news_log_entries.append(f"*{tag}* -> {text_headline}")
                except: pass
            news_points = max(-1.5, min(1.5, news_score_total))
            table_rows.append({"Type": "Secondary Vector", "Asset": f"News Sentiment ({headline_counter} items)", "Value": "NLP Text", "Change %": "N/A", "Points": f"{news_points:+.1f}"})
        else:
            table_rows.append({"Type": "Secondary Vector", "Asset": "News Sentiment Scorer", "Value": "LOCKED", "Change %": "LOCKED", "Points": "LOCKED"})

        # Master Net Score Calculation Formula
        master_final_score = dxy_score + tlt_score + miner_points + secondary_points + news_points
        if core_direction == 0: master_final_score = 0.0

        # --- PHASE 3: RENDER THE SPEEDOMETER METER HUD ---
        if core_direction == 0:
            label_text, panel_color, text_color = "CHOP WAIT / FLAT", "#FF9900", "#FFFFFF"
        elif master_final_score >= 5.5:
            label_text, panel_color, text_color = "STRONG BUY", "#00FF66", "#000000"
        elif master_final_score >= 1.0:
            label_text, panel_color, text_color = "BUY", "#88FF88", "#000000"
        elif master_final_score <= -5.5:
            label_text, panel_color, text_color = "STRONG SELL", "#FF0033", "#FFFFFF"
        else:
            label_text, panel_color, text_color = "SELL", "#FF8888", "#000000"

        st.markdown(f"""
            <div class="gauge-container">
                <div class="gauge-bg">
                    <div style="font-size: 14px; text-transform: uppercase; color: #889988; letter-spacing: 1px;">Market Directive Meter</div>
                    <div class="status-text" style="color: {panel_color}; text-shadow: 0 0 10px {panel_color}44;">{label_text}</div>
                    <div style="font-size: 28px; font-weight: bold; margin-top: 5px; color: #FFFFFF;">{master_final_score:+.2f} <span style="font-size:14px; color:#888;">PTS</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # --- PHASE 4: RENDER THE PROFESSIONAL SCORECARD PERFORMANCE TABLE ---
        st.subheader("📋 Macro Portfolio Scorecard Matrix")
        df_scorecard = pd.DataFrame(table_rows)
        st.dataframe(df_scorecard, use_container_width=True, hide_index=True)

        # Dropdown Logs Tracing Sections
        if core_direction != 0 and headline_counter > 0:
            with st.expander("📰 Trace Scraped Headline Intelligence Streams", expanded=False):
                for entry in news_log_entries: st.write(entry)
                
        if len(error_logs) > 0:
            with st.expander("⚠️ Review Active Connectivity Diagnostic Audits", expanded=True):
                for log in error_logs: st.error(log)
