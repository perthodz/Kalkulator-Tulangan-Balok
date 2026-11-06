import streamlit as st
import math
import plotly.graph_objects as go

# Konfigurasi Halaman
st.set_page_config(page_title="Retro Beam Calc", page_icon="👾", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

    /* Terapkan font retro HANYA ke elemen teks spesifik agar tidak merusak ikon bawaan */
    html, body, p, label, div[data-testid="stMarkdownContainer"] {
        font-family: 'VT323', monospace !important;
        font-size: 1.3rem !important;
        color: #000000 !important;
    }

    h1, h2, h3 {
        font-family: 'Press Start 2P', cursive !important;
        text-transform: uppercase !important;
        color: #000000 !important;
        text-shadow: 2px 2px 0px #a3a3a3 !important;
    }

    .stApp {
        background-color: #d1d5db; 
        background-image: radial-gradient(#9ca3af 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* KUSTOMISASI EXPANDER & PERBAIKAN KONTRAS */
    div[data-testid="stExpander"] details {
        background-color: #ffffff !important;
        border: 4px solid #000000 !important;
        border-radius: 0px !important;
        box-shadow: 5px 5px 0px #000000 !important;
        margin-bottom: 10px;
    }
    
    /* Header Expander (Hitam Pekat) */
    div[data-testid="stExpander"] details summary {
        background-color: #111111 !important; 
        padding: 10px !important;
        border-bottom: 2px solid #000000 !important;
    }

    /* Teks Judul Expander (Putih Terang / Retro) */
    div[data-testid="stExpander"] details summary p, 
    div[data-testid="stExpander"] details summary span {
        color: #ffffff !important; 
        font-family: 'Press Start 2P', cursive !important;
        font-size: 12px !important;
    }

    /* Sembunyikan ikon teks 'arrow_right' bawaan yang bentrok */
    div[data-testid="stExpander"] details summary svg,
    div[data-testid="stExpander"] details summary [data-testid="stIconMaterial"] {
        display: none !important;
    }

    /* Isi dari expander (Background Putih) */
    div[data-testid="stExpanderDetails"] {
        padding: 15px !important;
        background-color: #ffffff !important;
    }

    /* TOMBOL ARCADE */
    .stButton>button {
        background-color: #ff003c !important;
        color: #ffffff !important;
        border: 4px solid #000000 !important;
        border-radius: 0px !important;
        box-shadow: 6px 6px 0px #000000 !important;
        height: 60px !important;
        font-family: 'Press Start 2P', cursive !important;
        font-size: 14px !important;
        text-transform: uppercase;
        transition: all 0.1s ease;
    }
    
    .stButton>button * {
        color: #ffffff !important;
    }
    
    .stButton>button:active {
        transform: translate(6px, 6px) !important;
        box-shadow: 0px 0px 0px #000000 !important;
    }

    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 4px solid #000000 !important;
        border-radius: 0px !important;
        box-shadow: 5px 5px 0px #000000 !important;
        padding: 10px;
    }

    input, .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-family: 'VT323', monospace !important;
        font-size: 1.2rem !important;
        background-color: #f3f4f6 !important;
        color: #000000 !important;
    }
    
    .stAlert {
        border: 3px solid #000000 !important;
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# Fungsi untuk membuat grafik interaktif Retro Bar Chart
def create_retro_chart(kapasitas, beban, judul):
    fig = go.Figure()
    
    # Bar Kapasitas (Biru Retro)
    fig.add_trace(go.Bar(
        x=['Kapasitas (Terpasang)'], y=[kapasitas],
        marker_color='#3b82f6',
        marker_line_color='black', marker_line_width=3,
        name='Kapasitas'
    ))
    
    # Bar Beban (Merah Retro)
    fig.add_trace(go.Bar(
        x=['Beban (Rencana)'], y=[beban],
        marker_color='#ef4444',
        marker_line_color='black', marker_line_width=3,
        name='Beban'
    ))
    
    # Styling batas aman
    fig.add_hline(y=beban, line_dash="dash", line_color="black", line_width=2, 
                  annotation_text="BATAS AMAN", annotation_position="top right")

    fig.update_layout(
        title={'text': judul, 'font': {'family': 'VT323', 'size': 24}},
        plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)',
        font={'family': 'VT323', 'size': 18, 'color': 'black'},
        margin=dict(l=20, r=20, t=50, b=20),
        height=300,
        showlegend=False,
        yaxis=dict(gridcolor='#e5e7eb', zerolinecolor='black', zerolinewidth=2),
        xaxis=dict(zerolinecolor='black', zerolinewidth=2)
    )
    return fig

st.title("👾 STRUKTUR BALOK CALC 8-BIT")
st.caption("TEKAN START UNTUK MENGECEK KEAMANAN STRUKTUR...")

# --- PANDUAN ---
# Menggunakan tanda [+] sebagai pengganti ikon panah agar terkesan jadul
with st.expander("[+] BUKU PETUNJUK TUTORIAL", expanded=False):
    st.markdown("""
    **LEVEL 1: PERSIAPAN DATA**
    * Masukkan mutu beton ($f_c'$), baja lentur ($f_y$), dan baja geser ($f_{ys}$).
    * Tentukan dimensi penampang ($b$ dan $h$).
    
    **LEVEL 2: AMBIL LOOT DARI ETABS/SAP2000**
    * Momen 3-3: Masukkan Momen Positif ($M_{u+}$) dan Negatif ($M_{u-}$).
    * Shear 2-2: Ambil gaya geser terbesar ($V_u$).
      
    **LEVEL 3: UJI TULANGAN**
    * Input jumlah dan diameter. Tekan **HITUNG**.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# --- INPUT DATA ---
with st.expander("[+] INVENTORY: BAHAN STRUKTUR", expanded=True):
    fc = st.number_input("Kuat tekan beton (fc') [MPa]", value=30.0, step=1.0)
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        fy = st.number_input("Baja lentur (fy) [MPa]", value=420.0, step=10.0)
    with col_b2:
        fys = st.number_input("Baja geser (fys) [MPa]", value=280.0, step=10.0)

with st.expander("[+] STATUS: DIMENSI BALOK", expanded=True):
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        b = st.number_input("Lebar (b) [mm]", value=400.0, step=10.0)
        D_lentur = st.number_input("Diameter lentur (D) [mm]", value=22.0, step=1.0)
    with col_d2:
        h = st.number_input("Tinggi (h) [mm]", value=600.0, step=10.0)
        D_geser = st.number_input("Diameter sengkang (Ø) [mm]", value=10.0, step=1.0, min_value=0.0)
    ts = st.number_input("Selimut beton (ts) [mm]", value=40.0, step=1.0)

with st.expander("[+] QUEST: GAYA RENCANA (ETABS)", expanded=True):
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        Mu_pos = st.number_input("Momen positif (Mu+) [kNm]", value=133.08)
    with col_m2:
        Mu_neg = st.number_input("Momen negatif (Mu-) [kNm]", value=251.96)
    Vu = st.number_input("Gaya geser (Vu) [kN]", value=212.94)

with st.expander("[+] EQUIPMENT: RENCANA TULANGAN", expanded=True):
    st.markdown("**-- TULANGAN TUMPUAN (Mu-) --**")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        n_tump = st.number_input("Jumlah (Tumpuan)", value=4, min_value=1)
    with col_t2:
        d_tump = st.number_input("Diameter (Tumpuan) [mm]", value=22, min_value=8)
        
    st.markdown("**-- TULANGAN LAPANGAN (Mu+) --**")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        n_lap = st.number_input("Jumlah (Lapangan)", value=4, min_value=1)
    with col_l2:
        d_lap = st.number_input("Diameter (Lapangan) [mm]", value=22, min_value=8)

    st.markdown("**-- TULANGAN GESER (Vu) --**")
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        d_seng = st.number_input("Diameter Geser [mm]", value=10, min_value=0)
    with col_g2:
        s_seng = st.number_input("Jarak Sengkang [mm]", value=150.0, min_value=0.0)
    with col_g3:
        kaki = st.selectbox("Jumlah Kaki", options=[0, 2, 3, 4, 6], index=1)

st.markdown("<br>", unsafe_allow_html=True)

# --- TOMBOL HITUNG ---
if st.button("🚀 HITUNG & CEK KEAMANAN", use_container_width=True):
    st.markdown("---")
    st.subheader("LAPORAN HASIL (STAGE CLEAR)")
    
    phi_lentur = 0.80  
    phi_geser = 0.75   
    
    ds = ts + D_geser + (D_lentur / 2)
    d = h - ds
    
    tab1, tab2, tab3 = st.tabs(["[ TUMPUAN ]", "[ LAPANGAN ]", "[ GESER ]"])
    
    # --- TAB 1: TUMPUAN ---
    with tab1:
        As_tump = n_tump * (math.pi / 4) * (d_tump ** 2)
        a_tump = (As_tump * fy) / (0.85 * fc * b)
        Mn_tump = As_tump * fy * (d - (a_tump / 2)) * 1e-6
        phi_Mn_tump = phi_lentur * Mn_tump
        
        colA, colB = st.columns(2)
        colA.metric("Kapasitas (φMn)", f"{phi_Mn_tump:.2f} kNm")
        colB.metric("Beban (Mu-)", f"{Mu_neg:.2f} kNm")
        
        if phi_Mn_tump >= Mu_neg:
            st.success(f"✅ MISSION PASSED! (φMn ≥ Mu-)")
        else:
            st.error(f"❌ GAME OVER! Kapasitas kurang.")
            
        st.plotly_chart(create_retro_chart(phi_Mn_tump, Mu_neg, "GRAFIK MOMEN TUMPUAN"), use_container_width=True)

    # --- TAB 2: LAPANGAN ---
    with tab2:
        As_lap = n_lap * (math.pi / 4) * (d_lap ** 2)
        a_lap = (As_lap * fy) / (0.85 * fc * b)
        Mn_lap = As_lap * fy * (d - (a_lap / 2)) * 1e-6
        phi_Mn_lap = phi_lentur * Mn_lap
        
        colC, colD = st.columns(2)
        colC.metric("Kapasitas (φMn)", f"{phi_Mn_lap:.2f} kNm")
        colD.metric("Beban (Mu+)", f"{Mu_pos:.2f} kNm")
        
        if phi_Mn_lap >= Mu_pos:
            st.success(f"✅ MISSION PASSED! (φMn ≥ Mu+)")
        else:
            st.error(f"❌ GAME OVER! Kapasitas kurang.")
            
        st.plotly_chart(create_retro_chart(phi_Mn_lap, Mu_pos, "GRAFIK MOMEN LAPANGAN"), use_container_width=True)

    # --- TAB 3: GESER ---
    with tab3:
        Vc = (math.sqrt(fc) / 6) * b * d * 1e-3 
        phi_Vc = phi_geser * Vc
        
        if d_seng == 0 or s_seng == 0 or kaki == 0:
            Vs_pakai = 0.0
        else:
            Av = kaki * (math.pi / 4) * (d_seng ** 2)
            Vs_pakai = (Av * fys * d) / s_seng * 1e-3  
            
        phi_Vn = phi_geser * (Vc + Vs_pakai)
        
        colE, colF = st.columns(2)
        colE.metric("Kapasitas Total (φVn)", f"{phi_Vn:.2f} kN")
        colF.metric("Beban Geser (Vu)", f"{Vu:.2f} kN")
        
        if phi_Vn >= Vu:
            st.success(f"✅ MISSION PASSED! (φVn ≥ Vu)")
        else:
            st.error(f"❌ GAME OVER! Kapasitas kurang.")
            
        st.plotly_chart(create_retro_chart(phi_Vn, Vu, "GRAFIK KAPASITAS GESER"), use_container_width=True)