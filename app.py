import streamlit as st
import math

# Konfigurasi Halaman Website
st.set_page_config(page_title="Kalkulator Analisis Balok", page_icon="🏗️", layout="wide")

# Custom CSS untuk mempercantik Metric (Kotak Hasil) dan Tombol
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: rgba(128, 128, 128, 0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 15px;
        border-radius: 10px;
    }
    .stButton>button {
        border-radius: 8px;
        height: 55px;
        font-size: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏗️ Kalkulator Analisis Balok")
st.caption("Aplikasi interaktif untuk mengecek keamanan desain tulangan lentur dan geser pada penampang balok beton bertulang berdasarkan Standar Nasional Indonesia (SNI).")
st.divider()

# --- BAGIAN INPUT DATA ---
st.header("📝 Data Perencanaan")

with st.container():
    col_in1, col_in2, col_in3 = st.columns(3)

    with col_in1:
        st.subheader("🧱 Bahan Struktur")
        fc = st.number_input("Kuat tekan beton (fc') [MPa]", value=30.0, step=1.0)
        fy = st.number_input("Teg. leleh baja lentur (fy) [MPa]", value=420.0, step=10.0)
        fys = st.number_input("Teg. leleh baja geser (fys) [MPa]", value=280.0, step=10.0)

    with col_in2:
        st.subheader("📏 Dimensi Balok")
        b = st.number_input("Lebar balok (b) [mm]", value=400.0, step=10.0)
        h = st.number_input("Tinggi balok (h) [mm]", value=600.0, step=10.0)
        D_lentur = st.number_input("Diameter tul. deform (D) [mm]", value=22.0, step=1.0)
        D_geser = st.number_input("Diameter sengkang polos (Ø) [mm]", value=10.0, step=1.0, min_value=0.0)
        ts = st.number_input("Tebal selimut beton (ts) [mm]", value=40.0, step=1.0)

    with col_in3:
        st.subheader("⚖️ Gaya Rencana (Output Etabs/SAP)")
        Mu_pos = st.number_input("Momen positif (Mu+) [kNm]", value=133.08)
        Mu_neg = st.number_input("Momen negatif (Mu-) [kNm]", value=251.96)
        Vu = st.number_input("Gaya geser (Vu) [kN]", value=212.94)

st.divider()

# --- AREA RENCANA TULANGAN ---
st.header("🛠️ Rencana Tulangan Terpasang")
with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔴 Tumpuan (Mu-)")
        n_tump = st.number_input("Jumlah tulangan (n tumpuan)", value=4, min_value=1)
        d_tump = st.number_input("Diameter (D tumpuan) [mm]", value=22, min_value=8)

    with col2:
        st.markdown("### 🔵 Lapangan (Mu+)")
        n_lap = st.number_input("Jumlah tulangan (n lapangan)", value=4, min_value=1)
        d_lap = st.number_input("Diameter (D lapangan) [mm]", value=22, min_value=8)

    with col3:
        st.markdown("### 🟢 Geser (Vu)")
        d_seng = st.number_input("Diameter sengkang (Ø geser) [mm]", value=10, min_value=0)
        s_seng = st.number_input("Jarak sengkang (s) [mm]", value=150.0, min_value=0.0)
        kaki = st.selectbox("Jumlah kaki sengkang", options=[0, 2, 3, 4, 6], index=1)

st.markdown("<br>", unsafe_allow_html=True)

# --- TOMBOL HITUNG LINTAS KOLOM ---
if st.button("🚀 HITUNG & CEK KEAMANAN STRUKTUR", type="primary", use_container_width=True):
    st.markdown("---")
    st.header("📊 Laporan Hasil Pengecekan")
    
    # Parameter Penampang Ekivalen
    phi_lentur = 0.80  
    phi_geser = 0.75   
    
    # Tinggi efektif d
    ds = ts + D_geser + (D_lentur / 2)
    d = h - ds
    
    # --- MENGGUNAKAN TABS UNTUK HASIL ---
    tab1, tab2, tab3 = st.tabs(["🔴 Analisis Tumpuan", "🔵 Analisis Lapangan", "🟢 Analisis Geser"])
    
    # --- TAB 1: TUMPUAN ---
    with tab1:
        As_tump = n_tump * (math.pi / 4) * (d_tump ** 2)
        a_tump = (As_tump * fy) / (0.85 * fc * b)
        Mn_tump = As_tump * fy * (d - (a_tump / 2)) * 1e-6
        phi_Mn_tump = phi_lentur * Mn_tump
        
        colA, colB = st.columns(2)
        colA.metric(label="Kapasitas Momen (φMn)", value=f"{phi_Mn_tump:.2f} kNm", delta="Kapasitas Tersedia", delta_color="normal")
        colB.metric(label="Momen Rencana (Mu-)", value=f"{Mu_neg:.2f} kNm", delta="Beban Terfaktor", delta_color="inverse")
        
        # Visualisasi Progress Bar
        ratio_tump = min(Mu_neg / phi_Mn_tump, 1.0) if phi_Mn_tump > 0 else 1.0
        st.caption(f"**Rasio Penggunaan Kapasitas:** {ratio_tump*100:.1f}%")
        st.progress(ratio_tump)
        
        if phi_Mn_tump >= Mu_neg:
            st.success(f"✅ **STATUS AMAN!** Kapasitas penampang (φMn = {phi_Mn_tump:.2f} kNm) lebih besar dari beban tumpuan (Mu- = {Mu_neg:.2f} kNm).")
        else:
            st.error(f"❌ **TIDAK AMAN!** Kapasitas penampang kurang. Tambah jumlah atau diameter tulangan tumpuan.")

    # --- TAB 2: LAPANGAN ---
    with tab2:
        As_lap = n_lap * (math.pi / 4) * (d_lap ** 2)
        a_lap = (As_lap * fy) / (0.85 * fc * b)
        Mn_lap = As_lap * fy * (d - (a_lap / 2)) * 1e-6
        phi_Mn_lap = phi_lentur * Mn_lap
        
        colC, colD = st.columns(2)
        colC.metric(label="Kapasitas Momen (φMn)", value=f"{phi_Mn_lap:.2f} kNm", delta="Kapasitas Tersedia", delta_color="normal")
        colD.metric(label="Momen Rencana (Mu+)", value=f"{Mu_pos:.2f} kNm", delta="Beban Terfaktor", delta_color="inverse")
        
        ratio_lap = min(Mu_pos / phi_Mn_lap, 1.0) if phi_Mn_lap > 0 else 1.0
        st.caption(f"**Rasio Penggunaan Kapasitas:** {ratio_lap*100:.1f}%")
        st.progress(ratio_lap)
        
        if phi_Mn_lap >= Mu_pos:
            st.success(f"✅ **STATUS AMAN!** Kapasitas penampang (φMn = {phi_Mn_lap:.2f} kNm) lebih besar dari beban lapangan (Mu+ = {Mu_pos:.2f} kNm).")
        else:
            st.error(f"❌ **TIDAK AMAN!** Kapasitas penampang kurang. Tambah jumlah atau diameter tulangan lapangan.")

    # --- TAB 3: GESER ---
    with tab3:
        Vc = (math.sqrt(fc) / 6) * b * d * 1e-3 
        phi_Vc = phi_geser * Vc
        
        st.write("##### Evaluasi Kebutuhan Sengkang Berdasarkan Kuat Beton (φVc)")
        if Vu <= 0.5 * phi_Vc:
            st.info(f"💡 **Status Teoritis:** Vu ({Vu:.2f} kN) ≤ 0.5 φVc ({0.5 * phi_Vc:.2f} kN). **Tidak perlu sengkang penahan beban**, cukup gunakan sengkang minimum/praktis.")
        elif Vu <= phi_Vc:
            st.warning(f"⚠️ **Status Teoritis:** Vu ({Vu:.2f} kN) > 0.5 φVc ({0.5 * phi_Vc:.2f} kN). **Perlu tulangan sengkang minimum**.")
        else:
            st.error(f"🚨 **Status Teoritis:** Vu ({Vu:.2f} kN) > φVc ({phi_Vc:.2f} kN). **Mutlak perlu tulangan sengkang penahan beban**.")
            
        st.divider()
        st.write("##### Analisis Kapasitas Terpasang (Sumbangan Beton + Sengkang)")
        
        if d_seng == 0 or s_seng == 0 or kaki == 0:
            Vs_pakai = 0.0
        else:
            Av = kaki * (math.pi / 4) * (d_seng ** 2)
            Vs_pakai = (Av * fys * d) / s_seng * 1e-3  
            
        phi_Vn = phi_geser * (Vc + Vs_pakai)
        
        colE, colF = st.columns(2)
        colE.metric(label="Total Kapasitas Geser (φVn)", value=f"{phi_Vn:.2f} kN", delta="Kapasitas Tersedia", delta_color="normal")
        colF.metric(label="Gaya Geser Rencana (Vu)", value=f"{Vu:.2f} kN", delta="Beban Terfaktor", delta_color="inverse")
        
        ratio_geser = min(Vu / phi_Vn, 1.0) if phi_Vn > 0 else 1.0
        st.caption(f"**Rasio Penggunaan Kapasitas:** {ratio_geser*100:.1f}%")
        st.progress(ratio_geser)

        if phi_Vn >= Vu:
            st.success(f"✅ **STATUS AMAN!** Kapasitas geser total (φVn = {phi_Vn:.2f} kN) sanggup menahan beban rencana (Vu = {Vu:.2f} kN).")
        else:
            st.error(f"❌ **TIDAK AMAN!** Kapasitas geser kurang. Rapatkan jarak sengkang (s) atau perbesar diameternya (Ø).")