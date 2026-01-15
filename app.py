import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import base64
import os

# ==========================================
# 0. Page Config
# ==========================================
st.set_page_config(
    page_title="2026米兰冬奥会 Dashboard",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 1. CSS & Assets (The Visual Magic)
# ==========================================

# Helper to encode images for CSS usage
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# Try to load local assets if they exist
snowflake_img = get_base64_of_bin_file("assets/snowflake_nav.png")
if snowflake_img:
    snowflake_css_url = f"data:image/png;base64,{snowflake_img}"
else:
    # Use a large SVG data URI for reliability
    snowflake_svg = '''
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 2V22M2 12H22M4.92893 4.92893L19.0711 19.0711M19.0711 4.92893L4.92893 19.0711" stroke="rgba(255,255,255,0.1)" stroke-width="2" stroke-linecap="round"/>
    <path d="M12 2L10 5H14L12 2ZM12 22L10 19H14L12 22Z" fill="rgba(255,255,255,0.1)"/>
    </svg>
    '''
    snowflake_css_url = "https://img.icons8.com/ios/100/ffffff/snowflake.png" 

# Milan 2026 Theme (Sunset/Purple) - FIXED DEFAULT
bg_gradient = "linear-gradient(135deg, #1a2980 0%, #26d0ce 30%, #764ba2 100%)" # Deep Blue to Ice to Purple

# CSS Injection
st.markdown(f"""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700;900&family=Lato:wght@300;400;700&family=Playfair+Display:ital,wght@1,700&display=swap');

    /* -------------------------------------------------------------------------
       1. BACKGROUND & THEME
    ------------------------------------------------------------------------- */
    .stApp {{
        background: {bg_gradient};
        background-size: 200% 200%;
        animation: gradientBG 15s ease infinite;
        background-attachment: fixed;
    }}
    
    @keyframes gradientBG {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    /* -------------------------------------------------------------------------
       TYPOGRAPHY
    ------------------------------------------------------------------------- */
    /* Global Text */
    html, body, [class*="css"] {{
        font-family: 'Lato', sans-serif;
        color: #E0F7FA;
    }}

    /* Headings */
    h1 {{
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 900 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 3rem !important;
        background: linear-gradient(120deg, #fff, #87CEFA, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }}

    h2 {{
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 700 !important;
        font-size: 2.2rem !important;
        color: #FFFFFF !important;
        letter-spacing: 1px;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
        border-bottom: 2px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
        display: inline-block;
    }}

    h3 {{
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.6rem !important;
        color: #FFFFFF !important; /* Reverted to White */
    }}
    
    h4 {{
        font-family: 'Montserrat', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1.3rem !important;
        color: #FFD700 !important; /* Gold */
    }}

    /* Body Text & Paragraphs */
    p, div, li {{
        font-family: 'Lato', sans-serif;
        font-size: 1.1rem;
        line-height: 1.6;
        font-weight: 300;
        color: #E0F7FA;
    }}

    /* Highlighted Numbers/Stats */
    .stat-number {{
        font-family: 'Montserrat', sans-serif;
        font-weight: 800;
        font-size: 2.5rem;
        color: #FFD700;
    }}

    /* Quotes */
    blockquote {{
        font-family: 'Playfair Display', serif;
        font-size: 1.3rem !important;
        font-style: italic;
        color: #B0C4DE;
        border-left: 4px solid #87CEFA;
        padding-left: 20px;
        margin: 20px 0;
    }}

    /* Streamlit specific overrides */
    div[data-testid="stMarkdownContainer"] p {{
        font-size: 1.1rem;
    }}

    /* -------------------------------------------------------------------------
       2. UI COMPONENTS (Frosted Glass)
    ------------------------------------------------------------------------- */
    .frosted-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    
    .frosted-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 40px rgba(118, 75, 162, 0.3); /* Purple Glow */
        border-color: rgba(255, 215, 0, 0.4); /* Gold Border Hint */
    }}

    /* -------------------------------------------------------------------------
       3. CUSTOM YEAR SELECTOR STYLING
    ------------------------------------------------------------------------- */
    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] div[role="radiogroup"] {{
        flex-direction: column;
        background: rgba(0,0,0,0.2);
        border-radius: 15px;
        padding: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        z-index: 2;
        position: relative;
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background: transparent;
        margin-bottom: 5px;
        transition: all 0.3s;
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {{
        background: rgba(255,255,255,0.1);
        border-radius: 5px;
        padding-left: 10px;
    }}

    /* -------------------------------------------------------------------------
       4. ANIMATIONS & DECORATION
    ------------------------------------------------------------------------- */
    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    .astrolabe-bg {{
        position: fixed;
        top: 100px;
        left: -100px;
        width: 500px;
        height: 500px;
        background-image: url("https://img.icons8.com/ios/500/ffffff/snowflake.png");
        background-size: contain;
        background-repeat: no-repeat;
        opacity: 0.05;
        animation: rotate 120s linear infinite;
        pointer-events: none;
        z-index: 0;
    }}

    /* Snowflakes CSS Implementation */
    .snowflake {{
        color: #fff;
        font-size: 1em;
        font-family: Arial, sans-serif;
        text-shadow: 0 0 5px #000;
        position: fixed;
        top: -10%;
        z-index: 9999;
        user-select: none;
        cursor: default;
        animation-name: snowflakes-fall, snowflakes-shake;
        animation-duration: 10s, 3s;
        animation-timing-function: linear, ease-in-out;
        animation-iteration-count: infinite, infinite;
        animation-play-state: running, running;
        opacity: 0.3;
    }}
    @keyframes snowflakes-fall {{
        0% {{ top: -10%; }}
        100% {{ top: 100%; }}
    }}
    @keyframes snowflakes-shake {{
        0%, 100% {{ transform: translateX(0); }}
        50% {{ transform: translateX(80px); }}
    }}
    .snowflake:nth-of-type(0) {{ left: 1%; animation-delay: 0s, 0s; }}
    .snowflake:nth-of-type(1) {{ left: 10%; animation-delay: 1s, 1s; }}
    .snowflake:nth-of-type(2) {{ left: 20%; animation-delay: 6s, .5s; }}
    .snowflake:nth-of-type(3) {{ left: 30%; animation-delay: 4s, 2s; }}
    .snowflake:nth-of-type(4) {{ left: 40%; animation-delay: 2s, 2s; }}
    .snowflake:nth-of-type(5) {{ left: 50%; animation-delay: 8s, 3s; }}
    .snowflake:nth-of-type(6) {{ left: 60%; animation-delay: 6s, 2s; }}
    .snowflake:nth-of-type(7) {{ left: 70%; animation-delay: 2.5s, 1s; }}
    .snowflake:nth-of-type(8) {{ left: 80%; animation-delay: 1s, 0s; }}
    .snowflake:nth-of-type(9) {{ left: 90%; animation-delay: 3s, 1.5s; }}
    .snowflake:nth-of-type(10) {{ left: 25%; animation-delay: 2s, 0s; }}
    .snowflake:nth-of-type(11) {{ left: 65%; animation-delay: 4s, 2.5s; }}
</style>
""", unsafe_allow_html=True)

# Add Snowflakes
st.markdown("""
<div class="snowflake">❅</div><div class="snowflake">❆</div><div class="snowflake">❅</div>
<div class="snowflake">❆</div><div class="snowflake">❅</div><div class="snowflake">❆</div>
<div class="snowflake">❅</div><div class="snowflake">❆</div><div class="snowflake">❅</div>
<div class="snowflake">❆</div><div class="snowflake">❅</div><div class="snowflake">❆</div>
<div class="astrolabe-bg"></div>
""", unsafe_allow_html=True)

# ==========================================
# 2. Data Logic
# ==========================================
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        
        # Basic Cleaning
        # 1. Clean Discipline names
        if 'discipline' in df.columns:
            df['discipline_clean'] = df['discipline'].apply(lambda x: x.split('(')[0].strip() if isinstance(x, str) else x)
        
        # 2. Map NOC to Country Names (Simplified)
        noc_map = {
            'USA': 'United States', 'CHN': 'China', 'NOR': 'Norway', 'GER': 'Germany', 
            'AUT': 'Austria', 'CAN': 'Canada', 'ITA': 'Italy', 'FRA': 'France',
            'SWE': 'Sweden', 'SUI': 'Switzerland', 'NED': 'Netherlands', 'RUS': 'Russia',
            'FIN': 'Finland', 'JPN': 'Japan', 'KOR': 'South Korea'
        }
        df['Country'] = df['noc'].map(noc_map).fillna(df['noc'])
        
        # 3. Score for sorting (Gold=3, Silver=2, Bronze=1)
        medal_score = {'Gold': 3, 'Silver': 2, 'Bronze': 1}
        df['score'] = df['medal'].map(medal_score).fillna(0)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data("data.csv")

if df.empty:
    st.stop()

# ==========================================
# 3. Sidebar / Layout
# ==========================================

col_left, col_center, col_right = st.columns([1, 3, 1.2])

# --- LEFT: SNOWFLAKE ASTROLABE (Navigation) ---
with col_left:
    # Removed broken HTML wrappers that caused empty boxes
    st.markdown("### ❄️ 年份")
    
    # Get available years and sort descending
    years = sorted(df['year'].unique(), reverse=True)
    
    selected_year = st.radio(
        "Select Year",
        years,
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 国家筛选")
    
    # Top countries for the filter
    top_countries = df['Country'].value_counts().head(10).index.tolist()
    selected_country = st.selectbox("Select Nation", ["All"] + top_countries)

# --- DATA FILTERING ---
filtered_df = df[df['year'] == selected_year]
if selected_country != "All":
    filtered_df = filtered_df[filtered_df['Country'] == selected_country]

# --- CENTER: TREEMAP (The Ice Block) ---
with col_center:
    st.markdown(f'<h2 style="text-align: center; text-shadow: 0 0 10px #764ba2;">Winter Olympics {selected_year} Medal Distribution</h2>', unsafe_allow_html=True)
    
    # TREEMAP LOGIC
    # We use the raw data to allow drilling down: Discipline -> Country -> Medal -> Event -> Athlete
    
    # Prepare data for Treemap
    treemap_df = filtered_df.copy()
    # Rename 'as' column to 'Athlete' if it exists, for better labeling
    if 'as' in treemap_df.columns:
        treemap_df = treemap_df.rename(columns={'as': 'Athlete'})
    else:
        treemap_df['Athlete'] = 'Unknown'
        
    # Fill NaNs for display
    treemap_df['event'] = treemap_df['event'].fillna('Unknown Event')
    treemap_df['Athlete'] = treemap_df['Athlete'].fillna('Unknown Athlete')
    
    # We want to color by score (Gold=3, Silver=2, Bronze=1)
    # This naturally makes Gold blocks "warmer/brighter"
    
    if selected_country == "All":
        path_list = [px.Constant("All Events"), 'discipline_clean', 'Country', 'medal', 'event', 'Athlete']
    else:
        # If a country is selected, the Country level is redundant. Show Discipline directly.
        path_list = [px.Constant(selected_country), 'discipline_clean', 'medal', 'event', 'Athlete']

    fig_tree = px.treemap(
        treemap_df,
        path=path_list,
        color='score', 
        color_continuous_scale=[
            [0.0, 'rgba(173, 216, 230, 0.5)'], # Light Blue (Ice/Bronze-ish low)
            [0.5, 'rgba(255, 255, 255, 0.8)'], # White (Silver-ish mid)
            [1.0, '#FFD700']  # Gold (High)
        ],
        hover_data=['event', 'Athlete', 'medal'],
        maxdepth=3 # Initially show up to Country/Medal level to avoid clutter
    )
    
    fig_tree.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, l=0, r=0, b=0),
        font=dict(color='white', family="Helvetica Neue"),
        hoverlabel=dict(
            bgcolor="rgba(11, 16, 38, 0.9)",
            font_size=14,
            font_family="Helvetica Neue"
        ),
        coloraxis_showscale=False # Hide the color bar for cleaner look
    )
    
    # Add borders
    fig_tree.update_traces(
        marker=dict(
            line=dict(width=1.5, color='rgba(255,255,255,0.7)'),
            pad=dict(t=2, l=2, r=2, b=2)
        ),
        tiling=dict(packing='squarify'),
        textinfo="label+value"
    )

    st.plotly_chart(fig_tree, use_container_width=True)
    
    # --- BOTTOM: TREND LINE (The Ski Track) ---
    st.markdown("### 表现趋势")
    
    # Logic for "All": Show the trend of the TOP NATION of the CURRENTLY SELECTED YEAR
    # Logic for Specific Country: Show that country's trend
    
    if selected_country == "All":
        # Find top nation of selected year
        if not filtered_df.empty:
            top_nation_year = filtered_df.groupby('Country')['score'].sum().idxmax()
            trend_nation = top_nation_year
            title_suffix = f"Top Nation of {selected_year}: {trend_nation}"
        else:
            trend_nation = None # Fallback
            title_suffix = "No Data"
    else:
        trend_nation = selected_country
        title_suffix = trend_nation
        
    if trend_nation:
        # Get historical data for this nation
        trend_data = df[df['Country'] == trend_nation].groupby('year')['score'].sum().reset_index().sort_values('year')
        
        fig_line = px.line(trend_data, x='year', y='score', markers=True)
        
        # Make it look like a ski track (Smooth Spline, Glow)
        fig_line.update_traces(
            line_shape='spline', 
            line_color='#00d2ff', 
            line_width=4,
            marker=dict(size=10, color='white', line=dict(width=2, color='#00d2ff'))
        )
        
        # Remove grid, add "Glow" shadow via drop-shadow filter (in CSS usually, but here we simulate with layout)
        fig_line.update_layout(
            title=dict(text=f"Medal Score History ({title_suffix})", font=dict(color='white')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.02)',
            font=dict(color='white'),
            xaxis=dict(
                showgrid=False, 
                gridcolor='rgba(255,255,255,0.05)',
                zeroline=False,
                showline=False
            ),
            yaxis=dict(
                showgrid=False, 
                gridcolor='rgba(255,255,255,0.05)',
                zeroline=False,
                showline=False
            ),
            margin=dict(t=40, l=10, r=10, b=10),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Add descriptive text below Trend Line
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 15px; margin-top: 10px; border-left: 4px solid #FFD700;">
            <h4 style="color: #FFD700; margin: 0 0 10px 0;">百年冰雪：从“北欧后花园”到全球竞技场</h4>
            <p style="color: #ddd; font-size: 0.9em; margin-bottom: 8px;">
                <b>传统强国的底色与波幅 (1920-1960年代)</b><br>
                以 <b>挪威、德国、美国、奥地利</b> 为代表的传统劲旅，凭借地理优势和深厚的冰雪文化，垄断了奖牌榜的大半。
            </p>
            <p style="color: #ddd; font-size: 0.9em; margin-bottom: 8px;">
                <b>全球化浪潮 (1990年代至今)</b><br>
                世界冰雪版图经历了一次大洗牌，职业化与商业化将竞技水平推向了新高。
            </p>
             <p style="color: #ddd; font-size: 0.9em; margin-bottom: 0;">
                <b>东亚力量的崛起</b><br>
                近二十年 <b>中、日、韩</b> 等东亚国家的强势崛起，打破了“冰雪运动不出欧洲/北美”的旧格局。
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("No data available for trend analysis.")

# --- RIGHT: INFO & PORTAL ---
with col_right:
    # 1. Top Performing Nations
    st.markdown("### 表现前五位")
    
    medal_counts = filtered_df.groupby('Country')['score'].sum().sort_values(ascending=False).head(5)
    
    fig_bar = px.bar(
        x=medal_counts.values,
        y=medal_counts.index,
        orientation='h',
        text=medal_counts.values
    )
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=0, l=0, r=50, b=0), # Increased right margin for labels
        xaxis=dict(visible=False),
        yaxis=dict(autorange="reversed"),
        height=200,
        barcornerradius=5
    )
    fig_bar.update_traces(
        marker_color='rgba(255, 215, 0, 0.8)', # Soft Gold
        textposition='outside',
        cliponaxis=False, # Allow text to extend beyond axis
        marker_line_width=0
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    # 2. Milan 2026 Portal (Visual Only)
    st.markdown(f"""
    <div class="frosted-card floating-element" style="
        border: 2px solid rgba(163, 108, 253, 0.6); 
        background: linear-gradient(135deg, rgba(163, 108, 253, 0.2) 0%, rgba(0, 210, 255, 0.2) 100%);
        text-align: center;
    ">
        <h2 style="margin-top:0; color: #fff; text-shadow: 0 0 10px #a36cfd;">米兰 2026</h2>
        <p style="font-size: 1.1em; opacity: 0.9;">下一篇章</p>
        <p style="font-size: 0.8em; opacity: 0.7;">February 6 - 22, 2026</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 3. Facts / Carousel
    if not filtered_df.empty:
        st.markdown("#### 你知道吗？")
        try:
            fact = filtered_df.sample(1).iloc[0]
            st.info(f"In {selected_year}, {fact['as']} from {fact['Country']} took home {fact['medal']} in {fact['discipline_clean']}!")
        except:
            st.write("没有更多数据了！")

# --- SECTION: PROJECT EVOLUTION (Tree Chart) ---
st.markdown("---")
col_evo_text, col_evo_chart = st.columns([1.2, 2])

with col_evo_text:
    # Use flexbox to center content vertically and provide better spacing
    st.markdown("""
<div style="height: 800px; display: flex; flex-direction: column; justify-content: center; padding: 20px; color: #eee;">
<h3 style="color: #fff; border-bottom: 2px solid #fff; padding-bottom: 10px; line-height: 1.4; margin-bottom: 30px;">
项目变迁：<br>从“生存技能”到“感官极限”
</h3>
<div style="margin-bottom: 40px;">
<h4 style="color: #fff; margin-bottom: 10px; font-size: 1.2rem;">📈 项目的扩张</h4>
<p style="font-size: 1rem; color: #fff;">
越野滑雪、花样滑冰等 9 个传统大项，发展到如今 109 个小项。混合接力、大跳台 (Big Air) 是近二十年的新宠。
</p>
</div>
<div style="margin-bottom: 40px;">
<h4 style="color: #fff; margin-bottom: 10px; font-size: 1.2rem;">✨ 新增与取消</h4>
<p style="font-size: 1rem; color: #fff;">
“军事巡逻”的隐退，拥抱了 <b style="color: #fff;">单板滑雪 (Snowboarding)</b> 和 <b style="color: #fff;">自由式滑雪 (Freestyle Skiing)</b> 等极具观赏性、吸引年轻一代的极限运动。
</p>
</div>
<div>
<h4 style="color: #fff; margin-bottom: 10px; font-size: 1.2rem;">⚖️ 性别的平衡</h4>
<p style="font-size: 1rem; color: #fff;">
女子单人雪车、混合团体接力等新增项目，正不断填补性别奖牌分布的空白。米兰冬奥会女性运动员占比达 47%，创冬奥会历史新高。
</p>
</div>
</div>
""", unsafe_allow_html=True)

with col_evo_chart:
    st.subheader(f"📊 冬奥项目百年变迁 (Olympic Program History)")
    
    # Data Prep for ECharts Tree
    # We want to show: Root -> Discipline -> Events
    # For each event, we show when it started and ended.
    
    if 'event' in df.columns and 'discipline_clean' in df.columns:
        # 1. Aggregate Event History
        # Group by Discipline, Event -> Get Min Year, Max Year
        event_history = df.groupby(['discipline_clean', 'event'])['year'].agg(['min', 'max']).reset_index()
        
        # Structure for ECharts Tree
        # {
        #   name: "Winter Games",
        #   children: [
        #       {
        #           name: "Skiing",
        #           children: [
        #               { name: "Alpine Skiing (1936-Present)", value: "1936-2026" }
        #           ]
        #       }
        #   ]
        # }
        
        tree_data = {"name": "❄️ Winter Olympics", "children": []}
        
        # Get all disciplines
        disciplines = sorted(event_history['discipline_clean'].unique())
        
        for disc in disciplines:
            disc_node = {"name": disc, "children": []}
            
            # Get events for this discipline
            disc_events = event_history[event_history['discipline_clean'] == disc]
            
            for _, row in disc_events.iterrows():
                evt_name = row['event']
                start_year = row['min']
                end_year = row['max']
                latest_year = max(years) # Assuming 'years' list exists and is sorted desc
                
                # Determine status
                is_active = (end_year == latest_year)
                
                # Format label
                if is_active:
                    time_str = f"{start_year} - Present"
                    # Highlight New Events (e.g. started in last 2 cycles)
                    if start_year >= latest_year - 4: 
                        label = f"✨ {evt_name}"
                        item_style = {"color": "#00FF7F"} # New Green
                    else:
                        label = evt_name
                        item_style = {"color": "#87CEFA"} # Active Blue
                else:
                    time_str = f"{start_year} - {end_year}"
                    label = f"❌ {evt_name}"
                    item_style = {"color": "#FF6347"} # Discontinued Red
                
                # Add node
                # We add time_str to name or tooltip? 
                # Tree chart shows 'name'.
                disc_node["children"].append({
                    "name": label,
                    "value": time_str, # Tooltip value
                    "itemStyle": item_style,
                    "label": {"color": "#fff" if is_active else "#aaa"}
                })
                
            tree_data["children"].append(disc_node)

        # ECharts Options
        option = {
            "tooltip": {
                "trigger": "item",
                "triggerOn": "mousemove",
                "formatter": "{b}: {c}"
            },
            "series": [
                {
                    "type": "tree",
                    "data": [tree_data],
                    "top": "5%",
                    "left": "15%",
                    "bottom": "5%",
                    "right": "20%",
                    "symbolSize": 7,
                    "label": {
                        "position": "left",
                        "verticalAlign": "middle",
                        "align": "right",
                        "fontSize": 14,
                        "color": "#fff"
                    },
                    "leaves": {
                        "label": {
                            "position": "right",
                            "verticalAlign": "middle",
                            "align": "left"
                        }
                    },
                    "emphasis": {
                        "focus": "descendant"
                    },
                    "expandAndCollapse": True,
                    "animationDuration": 550,
                    "animationDurationUpdate": 750,
                    "initialTreeDepth": 1, # Only show Discipline level initially
                    "lineStyle": {
                        "color": "rgba(255,255,255,0.5)",
                        "curveness": 0.5
                    }
                }
            ]
        }
        
        # Render
        try:
            from streamlit_echarts import st_echarts
            st_echarts(options=option, height="800px")
        except ImportError:
            st.error("Please install streamlit-echarts to view this chart.")

    else:
        st.warning("Data missing necessary columns for Project Evolution.")

# --- SECTION: CHINA TEAM MILAN 2026 PREDICTION ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
<div style="font-family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif; font-weight: 800; font-size: 2.4em; color: #fff; letter-spacing: 2px; margin-bottom: 10px;">
2026 米兰冬奥 · 中国队前瞻
</div>
<p style="color: #cfd8dc; font-size: 1.05em; font-family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif;">点击下方圆环，查看重点项目与核心选手预测</p>
</div>
""", unsafe_allow_html=True)

# 1. Load Data for China Prediction from CSV
try:
    china_df = pd.read_csv('china_data.csv')
    china_df = china_df.fillna("")
except Exception as e:
    st.error(f"Error loading china_data.csv: {e}")
    china_df = pd.DataFrame()

if not china_df.empty:
    # --- DATA PROCESSING FOR HIERARCHY ---
    # 1. Group by Sport to get total medals for the parent node
    sport_group = china_df.groupby(['sport', 'icon'])['medals'].sum().reset_index()
    sport_group['label'] = sport_group['sport']
    sport_group['id'] = sport_group['sport'] + " " + sport_group['icon']
    sport_group['parent'] = "" # Root nodes
    
    # 2. Create Athlete nodes (Children)
    china_df['parent'] = china_df['sport'] + " " + china_df['icon']
    china_df['label'] = china_df['athlete']
    china_df['id'] = china_df['parent'] + " - " + china_df['athlete'] # Unique ID
    
    # 3. Combine for Sunburst
    # Sunburst needs: id, label, parent, value
    # Parent nodes (Sports)
    df_parents = sport_group[['id', 'label', 'parent', 'medals', 'sport', 'icon']].copy()
    df_parents['athlete'] = ""
    df_parents['desc'] = ""
    df_parents['img'] = ""
    
    # Child nodes (Athletes)
    df_children = china_df[['id', 'label', 'parent', 'medals', 'sport', 'icon', 'athlete', 'desc', 'img']].copy()
    
    # Combine
    sunburst_df = pd.concat([df_parents, df_children], axis=0)

    unique_sports = sunburst_df['sport'].dropna().unique().tolist()
    base_colors = [
        "#FFB3B3",
        "#FFD6A5",
        "#FFF59D",
        "#C8E6C9",
        "#BBDEFB",
        "#D1C4E9",
        "#F8BBD0",
        "#B2EBF2",
    ]
    sport_color_map = {sport: base_colors[i % len(base_colors)] for i, sport in enumerate(unique_sports)}

    # Layout: Left (Chart) - Right (Card)
    c_col1, c_col2 = st.columns([1.5, 1])

    with c_col1:
        # Sunburst Chart with Hierarchy: Sport -> Athlete
        # "3D Layered" effect simulated with colors and borders
        fig_sun = px.sunburst(
            sunburst_df,
            ids='id',
            names='label',
            parents='parent',
            values='medals',
            color='sport',
            color_discrete_map=sport_color_map,
            hover_data=['sport', 'medals']
        )
        
        fig_sun.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=10, l=10, r=10, b=10), # Compact
            font=dict(color='#263238', family="Microsoft YaHei, Noto Sans SC, PingFang SC, sans-serif", size=13),
            uniformtext=dict(minsize=10, mode="hide"),
        )
        
        fig_sun.update_traces(
            textinfo="label+value",
            insidetextorientation='radial',
            marker=dict(
                line=dict(color='rgba(255,255,255,0.85)', width=2), # Strong borders for "Ice Block" look
            ),
            textfont=dict(
                family="Microsoft YaHei, Noto Sans SC, PingFang SC, sans-serif",
                size=12,
                color="#263238",
            ),
            leaf=dict(opacity=0.95)
        )
        
        # Enable click selection
        selection = st.plotly_chart(fig_sun, use_container_width=True, on_select="rerun", selection_mode="points")
        
        # Add descriptive text below Sunburst Chart (Left Column)
        st.markdown("""
        <div style="background: rgba(0, 0, 0, 0.2); border-radius: 10px; padding: 15px; margin-top: 10px; border-left: 4px solid #FF4500;">
            <p style="color: #ddd; font-size: 0.9em; margin-bottom: 8px;">
                预计将有来自全球约 2900 名运动员参赛，在 8 个大项、16 个分项中展开角逐，最终将产生 116 枚金牌。
            </p>
            <p style="color: #ddd; font-size: 0.9em; margin-bottom: 0;">
                中国代表团将参与 <b>自由式滑雪、单板滑雪、短道速滑、速度滑冰、钢架雪车</b> 等项目，将在传统项目短道速滑、速度滑冰、自由式滑雪等项目上冲击奖牌甚至金牌。
                <br><br>
                <span style="color: #FFD700; font-weight: bold;">预测本届冬奥会中国代表团将取得 6 金 5 银 7 铜的战绩，将有望创造境外参赛最佳战绩！</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # --- DETERMINE SELECTED CONTENT ---
    selected_athletes = []
    selected_sport_name = "自由式滑雪" # Default
    selected_sport_icon = "⛷️"
    selected_total_medals = 0

    # Default view (first sport)
    if not china_df.empty:
        default_sport = china_df.iloc[0]['sport']
        selected_athletes = china_df[china_df['sport'] == default_sport].to_dict('records')
        selected_sport_name = default_sport
        selected_sport_icon = china_df.iloc[0]['icon']
        selected_total_medals = sum(a['medals'] for a in selected_athletes)

    # Handle Selection
    if selection:
        try:
            points = []
            if hasattr(selection, "selection") and selection.selection:
                points = selection.selection.points or []
            elif isinstance(selection, dict):
                if "selection" in selection and isinstance(selection["selection"], dict):
                    points = selection["selection"].get("points", []) or []
                elif "points" in selection:
                    points = selection.get("points", []) or []
            if points:
                point = points[0]
                clicked_label = point.get("label") or point.get("id") or ""
                if clicked_label:
                    sport_match = china_df[china_df['sport'] == clicked_label]
                    if sport_match.empty:
                        sport_match = china_df[china_df['sport'].apply(lambda x: x in clicked_label)]
                    if not sport_match.empty:
                        selected_sport_name = sport_match.iloc[0]['sport']
                        selected_sport_icon = sport_match.iloc[0]['icon']
                        selected_athletes = china_df[china_df['sport'] == selected_sport_name].to_dict('records')
                        selected_total_medals = sum(a['medals'] for a in selected_athletes)
                    else:
                        athlete_match = china_df[china_df['athlete'] == clicked_label]
                        if not athlete_match.empty:
                            selected_athletes = athlete_match.to_dict('records')
                            selected_sport_name = selected_athletes[0]['sport']
                            selected_sport_icon = selected_athletes[0]['icon']
                            selected_total_medals = selected_athletes[0]['medals']
        except Exception:
            pass

    with c_col2:
        # --- RENDER CARD (Fixing HTML Indentation Bug) ---
        # We build the HTML string carefully to avoid indentation issues in st.markdown
        
        # Header
        st.markdown(f"""
<div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.3); padding: 25px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); color: white; margin-top: 20px; animation: fadeIn 0.5s ease-in; font-family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif;">
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 10px; margin-bottom: 15px;">
        <h2 style="margin:0; font-size: 1.8em; color: #FFD700;">{selected_sport_name}</h2>
        <span style="font-size: 1.2em; font-weight: bold; background: rgba(255,0,0,0.6); padding: 5px 10px; border-radius: 10px;">预测: {selected_total_medals} 枚</span>
    </div>
""", unsafe_allow_html=True)

        # List of Athletes
        for athlete in selected_athletes:
            # Prepare Image HTML (Local file support)
            img_src = ""
            if athlete.get('img'):
                img_path = athlete['img']
                if img_path.startswith("http"):
                    img_src = img_path
                else:
                    # Handle local file
                    try:
                        # Check if file exists relative to cwd
                        if os.path.exists(img_path):
                            with open(img_path, "rb") as f:
                                b64_data = base64.b64encode(f.read()).decode()
                                # Detect mime type roughly
                                mime = "image/jpeg"
                                if img_path.lower().endswith(".png"):
                                    mime = "image/png"
                                img_src = f"data:{mime};base64,{b64_data}"
                    except:
                        pass
            
            if img_src:
                img_content = f'<img src="{img_src}" style="width: 100%; height: 100%; object-fit: cover;">'
            else:
                img_content = '<div style="font-size: 14px; line-height: 80px; text-align: center; color: #555;">无头像</div>'

            # Athlete Item HTML (No indentation to prevent code block rendering)
            athlete_html = f"""
<div style="display: flex; align-items: center; margin-bottom: 15px; background: rgba(0,0,0,0.2); padding: 10px; border-radius: 15px;">
    <div style="width: 80px; height: 80px; min-width: 80px; border-radius: 50%; border: 2px solid #fff; overflow: hidden; background: #fff; margin-right: 15px;">
        {img_content}
    </div>
    <div>
        <h3 style="margin: 0 0 5px 0; color: #fff; font-size: 1.2em; font-family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif;">{athlete['athlete']}</h3>
        <p style="margin: 0; color: #ccc; font-size: 0.9em; line-height: 1.4; font-family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif;">{athlete['desc']}</p>
        <div style="margin-top: 5px; font-size: 0.8em; color: #FFD700; font-family: 'Microsoft YaHei', 'Noto Sans SC', 'PingFang SC', sans-serif;">个人预测: {athlete['medals']} 枚</div>
    </div>
</div>
"""
            st.markdown(athlete_html, unsafe_allow_html=True)

        # Footer
        st.markdown("</div>", unsafe_allow_html=True)

# --- CONCLUSION ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 40px 20px; color: #fff;">
<blockquote style="border-left: none; font-size: 1.3em; background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); color: #fff;">
&ldquo; 结语： 每一段折线的攀升，都记录了人类在极寒之境对极限的挑战。                  从最初少数国家的冰雪派对，到如今覆盖全球的奥林匹克盛事，
冬奥会的变迁不仅是竞技水平的提高，更是人类不断寻找自然与自身平衡点的过程。 &rdquo;
</blockquote>
</div>
""", unsafe_allow_html=True)

