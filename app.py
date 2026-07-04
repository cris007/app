import streamlit as st
import yfinance as yf
import feedparser

# 1. Page Configuration for mobile screen responsive viewing
st.set_page_config(
    page_title="Gold Intel Matrix",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# App Header Interface
st.title("🔱 Gold Fundamental Intel")
st.markdown("##### Real-Time Intermarket Macroeconomic Matrix Dashboard")

# Robust local lexicon scoring dictionary logic (Bypasses NLTK completely)
def calculate_headline_sentiment(headline_text):
    text_lower = headline_text.lower()
    
    # Custom high-impact economic dictionary weights to guide the score engine on Gold macro
    bullish_keywords = {
        'rate cut': 1.5, 'inflation spike': 1.5, 'recession': 2.0, 'escalation': 1.5,
        'safe haven': 2.0, 'banking crisis': 2.5, 'fed dovish': 1.5, 'gold rally': 1.5,
        'crisis': 1.0, 'panic': 1.0, 'war': 2.0, 'geopolitical': 1.5, 'uncertainty': 1.0
    }
    bearish_keywords = {
        'rate hike': -1.5, 'strong jobs': -1.5, 'fed hawkish': -1.5, 'gdp growth': -1.0,
        'economic boom': -2.0, 'dollar surge': -2.0, 'inflation falls': -1.0,
        'rate increases': -1.5, 'hawkish fed': -1.5, 'strong economy': -1.5
    }
    
    headline_score = 0.0
    # Scan text strings for market catalysts
    for word, weight in bullish_keywords.items():
        if word in text_lower: headline_score += weight
    for word, weight in bearish_keywords.items():
        if word in text_lower: headline_score += weight
        
    return headline_score

# Massive Processing Action Button
if st.button("RUN CORE SENTIMENT SCAN", type="primary", use_container_width=True):
    
    with st.spinner("Fetching global ticker streams and parsing financial news feeds..."):
        
        # --- PHASE 1: SCAN TICKER VALUES MATRIX ---
        tickers = {
            "DXY (US Dollar Index)": "DX-Y.NYB",
            "US10Y (10-Yr Treasury Bond Yield)": "^TNX",
            "VIX (CBOE Fear Gauge Index)": "^VIX",
            "SPY (S&P 500 Market Tracker)": "SPY",
            "GDX (Gold Miners Equities)": "GDX"
        }
        
        master_score = 0.0
        ticker_details = []
        
        for name, symbol in tickers.items():
            try:
                ticker_obj = yf.Ticker(symbol)
                # Fetch 2 days of history to compare today's closing difference
                data = ticker_obj.history(period="2d")
                if len(data) >= 2:
                    prev_close = data['Close'].iloc[0]
                    curr_close = data['Close'].iloc[1]
                    pct_change = ((curr_close - prev_close) / prev_close) * 100
                    
                    # Point system mapping logic rules
                    if symbol == "DX-Y.NYB":
                        w = -2.0 if pct_change > 0 else 2.0
                        status = "🟢 Falling (Bullish)" if pct_change <= 0 else "🔴 Rising (Bearish)"
                    elif symbol == "^TNX":
                        w = -2.0 if pct_change > 0 else 2.0
                        status = "🟢 Falling (Bullish)" if pct_change <= 0 else "🔴 Rising (Bearish)"
                    elif symbol == "^VIX":
                        w = 1.5 if curr_close > 20 else -0.5
                        status = f"📊 Index Level: {curr_close:.2f}"
                    elif symbol == "SPY":
                        w = -1.0 if pct_change > 0 else 1.0
                        status = "🔴 Rallying (Risk-On)" if pct_change > 0 else "🟢 Correcting (Risk-Off)"
                    elif symbol == "GDX":
                        w = 2.0 if pct_change > 0 else -2.0
                        status = "🟢 Accumulating (Inflow)" if pct_change > 0 else "🔴 Distributing (Outflow)"
                        
                    master_score += w
                    ticker_details.append(f"**{name}**: {status} | *Weight: {w:+.1f} pts*")
            except Exception as e:
                ticker_details.append(f"⚠️ **{name}**: Data link timeout connection error. Details: {str(e)}")

        # --- PHASE 2: PARSE LIVE HEADLINE TEXT STREAMS ---
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
                for entry in feed.entries[:4]: # Grab the top 4 headlines from each feed path
                    text_headline = entry.title
                    comp_score = calculate_headline_sentiment(text_headline)
                    
                    news_score_total += comp_score
                    headline_counter += 1
                    
                    tag = "🟢 Bullish" if comp_score > 0 else "🔴 Bearish" if comp_score < 0 else "⚪ Neutral"
                    news_log_entries.append(f"*{tag}* -> {text_headline}")
            except Exception as e:
                news_log_entries.append(f"⚠️ Error parsing RSS stream: {str(e)}")
                
        # Keep boundaries balanced between -1.5 and +1.5 maximum points
        news_points = max(-1.5, min(1.5, news_score_total))
        master_score += news_points
        
        # --- PHASE 3: RENDER THE MOBILE OUTPUT BLOCKS ---
        st.markdown("---")
        st.subheader("📊 Ultimate Fundamental Directive")
        
        # Dynamic Color Indicator Panel Logic
        if master_score >= 4.0:
            st.success("### 🔥 DIRECTION: STRONG BULLISH BUY\nFundamentals align perfectly. Clear macro tailwinds are pushing capital into Gold.")
        elif master_score <= -4.0:
            st.error("### 📉 DIRECTION: STRONG BEARISH SELL\nSurging yields or a safe dollar environment are breaking Gold's support anchors.")
        else:
            st.warning("### ⏳ DIRECTION: MARKET CONFLICT / CHOP WAIT\nThe macro indicators are fighting each other. **Do not place trades right now.**")
            
        # Display Unified Score Metric
        st.metric(label="Total Combined Score", value=f"{master_score:+.2f} Points", delta="Target threshold requirement is +/- 4.0")
        
        # Expanded breakdown drawers for scannability
        with st.expander("🔎 View Intermarket Assets Matrix Breakdown", expanded=True):
            for detail in ticker_details:
                st.write(detail)
                
        with st.expander(f"📰 View Scraped Headlines Log ({headline_counter} parsed items)", expanded=False):
            st.write(f"**Processed Headlines Net Impact Score**: `{news_points:+.2f} pts`")
            for log in news_log_entries:
                st.write(log)
