import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import json

# -------------------------
# Emisyon Faktörleri (kg CO2) - Referans Tablosu Verileri
# -------------------------
emission_factors = {
    "Elektrik": {
        "Rüzgar Enerjisi": 0.233,
        "Fosil Yakıt (TR ORT)": 0.478,
        "Güneş Enerjisi": 0.012,
        "Hidro Elektrik": 0.048
    },
    "Doğal Gaz": {
        "Doğal Gaz": 2.02,
        "LNG": 2.75,
        "Biyogaz": 0.5,
        "Propan": 2.98
    },
    "Su": {
        "Su Kullanımı": 0.422,
        "Deniz suyu arıtma": 1.5,
        "Atık su arıtma": 0.8
    },
    "Atık Yönetimi": {
        "Organik Atık": 0.5,
        "Plastik Atık": 3.5,
        "Cam": 0.33,
        "Kağıt": 0.2,
        "Metal": 2.0
    },
    "Gıda Tüketimi": {
        "Et ve Et Ürünleri": 27.0,
        "Süt Ürünleri": 13.0,
        "Sebze ve Meyve": 2.0,
        "Tahıl ve Baklagil": 1.4
    }
}

# -------------------------
# Sayfa Ayarı
# -------------------------
st.set_page_config(page_title="KARBON-AT", page_icon="🌍", layout="wide")
# Sayfa Stilleri
st.markdown(
    """
    <style>
        .main{
        background: linear-gradient(to bottom, black, #18230F);
        
        }
        p, h1, h2, h3, h4, h5, h6, ul {
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        [data-testid="stSidebar"]{
        background:linear-gradient(to top, #1F7D53, #255F38);
        color: #015551
        }
        [data-testid="stTabs"]{
        }

    </style>
    <h3 style="margin-bottom: -40px">KARBON-AT 🦊</h3>
""", unsafe_allow_html = True
)


# -------------------------
# Sidebar
# -------------------------
with st.sidebar:
    st.header("Hakkında")
    st.write("""
        KarbonAT size daha sürdürülebilir bir işletme olma konusunda yol gösterir!:
        - Karbon Ayakizinizi hesaplayın
        - Öneriler Alın
        - Sıralamanızı öğrenin
    """)

if 'scoreboard' not in st.session_state:
    st.session_state.scoreboard = []

# -------------------------
# Geri Bildirim Fonksiyonları
# -------------------------
def get_general_recommendations(total):
    recommendations = []
    if total < 4000:
        recommendations.extend([
            "🌞 Güneş enerjisine geçmeyi değerlendirin.",
            "💻 Video konferans sistemlerini daha sık kullanın.",
            "♻️ Mevcut tasarruf ve geri dönüşüm uygulamalarınızı sürdürün."
        ])
    elif 4000 < total < 10000:
        recommendations.extend([
            "💡 LED aydınlatma sistemleri kullanın.",
            "🚛 Tedarik zincirinizde yerel üreticilere öncelik verin.",
            "🥗 Gıda israfını azaltacak planlamalar yapın."
        ])
    else:
        recommendations.extend([
            "🌱 Karbon dengeleme (offset) projelerine yatırım yapın.",
            "🚲 Personel için bisiklet paylaşım sistemleri kurun.",
            "🏭 Enerji tüketiminizi düzenli olarak izleyin ve raporlayın."
        ])
    return recommendations



# -------------------------
# Sekmeler
# -------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🏠", "Hesap Makinesi", "Rapor & Öneriler", "🏆"])

# -------------------------
# ANASAYFA
# -------------------------
with tab1:
    st.markdown("""
    <style>
       
        .stMarkdown div {
            border-radius: 10px;
            margin-bottom: 1rem;
            transition: transform 0.2s ease-in-out;
            color: white;

            

        }
        .stMarkdown div:hover {
            transform: translateY(-1px);
        }
        .banner-container{
            display:flex;
            flex-direction: column;
            justify-content:center;
            align-items:center;}
        .banner {
            text-align: justify;
            padding: 2rem;
            background: linear-gradient(45deg, #28a74683, #11a0758f);
            color: white;
            border-radius: 10px;
            display:flex;
            flex-direction: column;
            align-items:center;
            justify-content:center;
            font-size:15px;
            width:70vw;
            
            
        }
        .banner p {
                max-width: 700px}

        .stButton button {
            background: linear-gradient(45deg, #28a745, #20c997);
            color: white;
            border: none;
            padding: 0.5rem 2rem;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        #guide{
                text-align: left;
                align-items: center;
                justify-content:center;
                display:flex;
                flex-direction: column;
                gap:-5px;
                
            }


        #guide h3{
                margin-bottom: -30px}

    </style>
    <div class="banner-container">
    <div class="banner">
        <h1>🌍</h1>
        <h3> KARBONUNU HESAPLA GELECEĞİNİ PLANLA</h3>
        <p>KarbonAt; otellerin enerji, su, gıda ve doğalgaz gibi alanlardaki karbon emisyonlarını hesaplayarak ve yönetmelerine yardımcı olarak sürdürülebilirlik hareketine katkı sağlar.</p>
    </div>
    <div class="banner" id="guide">
                <h3>KarbonAT'ı kullanmaya başla:</h3><p>
                <ul>
                <p>- Sizden istenen verileri aylık harcama raporlarınıza dayanarak giriniz. (Örn: Su faturası)</p>
                <p>- Ardından formun sonundaki butona tıklayınız</p>
                <p>- Raporlar ve Öneriler sekmesinde hesaplanmış karbon ayakizinizi ve önerilerinizi bulacaksınız :)</p>
                <p>- Scoreboardda ise yerinizi alabilirsiniz</p>
                </ul>
                </p>
                </div>
                </div>
    """, unsafe_allow_html=True)


# -------------------------
# Hesaplama Sekmesi
# -------------------------
with tab2:
    company_name = st.text_input("İşletme Adınızı Giriniz *", placeholder = " İşletme adınızı girin. Örn. 'Teknofest Suit Otel'")
    st.header("Harcama Miktarlarınızı Girin")

    user_inputs = {}
    total_footprint = 0
    category_footprints = {}

    # Elektrik
    st.subheader("Elektrik")
    elektrik_total = 0
    user_inputs["Elektrik"] = {}
    for item, factor in emission_factors["Elektrik"].items():
        amount = st.number_input(f"{item} tüketimi", min_value=0.0, value=0.0, key="Elektrik_"+item)
        footprint = amount * factor
        user_inputs["Elektrik"][item] = footprint
        elektrik_total += footprint
    category_footprints["Elektrik"] = elektrik_total
    total_footprint += elektrik_total

    # Doğal Gaz
    st.subheader("Doğal Gaz")
    gaz_total = 0
    user_inputs["Doğal Gaz"] = {}
    for item, factor in emission_factors["Doğal Gaz"].items():
        amount = st.number_input(f"{item} tüketimi", min_value=0.0, value=0.0, key="Gaz_"+item)
        footprint = amount * factor
        user_inputs["Doğal Gaz"][item] = footprint
        gaz_total += footprint
    category_footprints["Doğal Gaz"] = gaz_total
    total_footprint += gaz_total

    # Su
    st.subheader("Su")
    su_total = 0
    user_inputs["Su"] = {}
    for item, factor in emission_factors["Su"].items():
        amount = st.number_input(f"{item} tüketimi", min_value=0.0, value=0.0, key="Su_"+item)
        footprint = amount * factor
        user_inputs["Su"][item] = footprint
        su_total += footprint
    category_footprints["Su"] = su_total
    total_footprint += su_total

    # Atık Yönetimi
    st.subheader("Atık Yönetimi")
    atik_total = 0
    user_inputs["Atık Yönetimi"] = {}
    for item, factor in emission_factors["Atık Yönetimi"].items():
        amount = st.number_input(f"{item} miktarı", min_value=0.0, value=0.0, key="Atik_"+item)
        footprint = amount * factor
        user_inputs["Atık Yönetimi"][item] = footprint
        atik_total += footprint
    category_footprints["Atık Yönetimi"] = atik_total
    total_footprint += atik_total

    # Gıda Tüketimi
    st.subheader("Gıda Tüketimi")
    gida_total = 0
    user_inputs["Gıda Tüketimi"] = {}
    for item, factor in emission_factors["Gıda Tüketimi"].items():
        amount = st.number_input(f"{item} tüketimi", min_value=0.0, value=0.0, key="Gida_"+item)
        footprint = amount * factor
        user_inputs["Gıda Tüketimi"][item] = footprint
        gida_total += footprint
    category_footprints["Gıda Tüketimi"] = gida_total
    total_footprint += gida_total

    if st.button("Karbon Ayak İzini Hesapla") and company_name:
        st.session_state.latest_result = {
            "Company": company_name,
            **category_footprints,
            "Toplam": total_footprint
        }
        st.session_state.latest_inputs = user_inputs
        st.session_state.latest_categories = category_footprints
        st.session_state.scoreboard.append(st.session_state.latest_result)
        st.success("Karbon ayak izi hesaplandı!")


# Raporlar ve Öneriler Sekmesi

with tab3:
    if 'latest_result' in st.session_state:
        results = st.session_state.latest_result
        st.header(results["Company"] + " 🚀")
        st.subheader("Karbon Ayak İzi Raporu")

        for category, items in st.session_state.latest_inputs.items():
            st.markdown(f"### {category}")
            df = pd.DataFrame(list(items.items()), columns=["Alt Tür", "Emisyon (kg CO2)"])
            st.dataframe(df, use_container_width=True)

        df_summary = pd.DataFrame({
            "Kategori": list(st.session_state.latest_categories.keys()),
            "Toplam Emisyon (kg CO2)": list(st.session_state.latest_categories.values())
        })
        st.markdown("### Kategori Bazlı Toplam Emisyon")
        st.dataframe(df_summary, use_container_width=True)

        st.metric("Toplam Karbon Ayak İzi", f"{results['Toplam']:.2f} kg CO2")

        fig, ax = plt.subplots()
        ax.bar(df_summary["Kategori"], df_summary["Toplam Emisyon (kg CO2)"])
        ax.set_ylabel("CO2 (kg)")
        ax.set_title("Kategoriye Göre Karbon Ayak İzi")
        st.pyplot(fig)

        st.subheader("💡 Öneriler")
        for rec in get_general_recommendations(results["Toplam"]):
            st.markdown(f"- {rec}")
        st.write("İlerleyen süreçte aktif:")
        ai_button = st.button("Öneri Üret AI ile 🧠")
        #ai button function
        ai_rec =[
                "🌱 Karbon dengeleme (offset) projelerine yatırım yapın.",
                "🚲 Personel için bisiklet paylaşım sistemleri kurun.",
                "🏭 Enerji tüketiminizi düzenli olarak izleyin ve raporlayın."
        ]
        if ai_button :
            with st.spinner("Yapay zeka öneriler üretiyor..."):
                time.sleep(2)
                st.success("İlave öneriler: ")
                for i in ai_rec:
                    st.markdown(f"-{i}")
        ##
        st.subheader("📝 Raporu İndir")
        df_report = pd.DataFrame([results])
        csv = df_report.to_csv(index=False).encode('utf-8')
        st.download_button("Raporu CSV Olarak İndir", data=csv, file_name="karbon_raporu.csv", mime="text/csv")
    else:
        st.info("Önce hesaplama yapın.")


# Scoreboard Sekmesi

with tab4:
    st.header("🏆 Scoreboard")
    if st.session_state.scoreboard:
        df_scoreboard = pd.DataFrame(st.session_state.scoreboard)
        df_sorted = df_scoreboard.sort_values("Toplam").reset_index(drop=True)
        df_sorted.index += 1
        st.dataframe(df_sorted.rename_axis('Sıra'), use_container_width=True)
    else:
        st.info("Henüz hiçbir veri girilmedi.")
