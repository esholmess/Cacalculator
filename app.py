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
        "Kırmızı Et": 27,
        "Tavuk": 6,
        "Balık":5,
        "Sebze":2,
        "Süt":1.5,
        "Peynir":10,
        "Ekmek/Unlu Mamülleri":1
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
    st.markdown("""
        <style>
        h3 {
            margin-bottom: -1rem;
            margin-top: 0.5rem
        }
        .stNumberInput {
            margin-top: -0.5rem;
        }
        </style>
        <h3>🌍 HARCAMA GİRİŞİ</h3>
        <p>Karbon ayakizi hesaplaması için aşağıdaki formda sizden istenen verileri giriniz. 🌱</p>
    """, unsafe_allow_html=True)

    with st.form("carbon_form"):

        with st.expander(" 🏢Şirket Bilgileri"):
            company_name = st.text_input("🏢 İşletme Adınızı Giriniz *", placeholder="Örn. Teknofest Suit Otel")
            date_input = st.text_input("Bulunduğunuz Ayı ve Yılı Girin", placeholder="Tarihi girin")
            customer_number = st.number_input("Verilerin ait olduğu tarihe ilişkin müşteri sayısını giriniz")
            
        with st.expander("🔌 Elektrik Tüketimi"):
                elektrik_total = 0
                user_inputs = {"Elektrik": {}}
                for item, factor in emission_factors["Elektrik"].items():
                    amount = st.number_input(f"{item} (kWh)", min_value=0.0, value=0.0, key="Elektrik_" + item)
                    footprint = amount * factor
                    user_inputs["Elektrik"][item] = footprint
                    elektrik_total += footprint

        with st.expander(" 🔥 Doğal Gaz Tüketimi"):
            gaz_total = 0
            user_inputs["Doğal Gaz"] = {}
            for item, factor in emission_factors["Doğal Gaz"].items():
                amount = st.number_input(f"{item} (m³)", min_value=0.0, value=0.0, key="Gaz_" + item)
                footprint = amount * factor
                user_inputs["Doğal Gaz"][item] = footprint
                gaz_total += footprint

        with st.expander("🚿 Su Kullanımı"):
            su_total = 0
            user_inputs["Su"] = {}
            for item, factor in emission_factors["Su"].items():
                amount = st.number_input(f"{item} (m³)", min_value=0.0, value=0.0, key="Su_" + item)
                footprint = amount * factor
                user_inputs["Su"][item] = footprint
                su_total += footprint

        with st.expander("🍽️ Gıda Tüketimi"):
            gida_total = 0
            user_inputs["Gıda Tüketimi"] = {}
            for item, factor in emission_factors["Gıda Tüketimi"].items():
                amount = st.number_input(f"{item} (kg)", min_value=0.0, value=0.0, key="Gida_" + item)
                footprint = amount * factor
                user_inputs["Gıda Tüketimi"][item] = footprint
                gida_total += footprint

        
        with st.expander("♻️ Atık Yönetimi"):
            atik_total = 0
            user_inputs["Atık Yönetimi"] = {}
            for item, factor in emission_factors["Atık Yönetimi"].items():
                amount = st.number_input(f"{item} (kg)", min_value=0.0, value=0.0, key="Atik_" + item)
                footprint = amount * factor
                user_inputs["Atık Yönetimi"][item] = footprint
                atik_total += footprint



        hesapla = st.form_submit_button("🌍 Karbon Ayak İzini Hesapla")

    if hesapla and company_name:
        total_footprint = elektrik_total + gaz_total + su_total + atik_total + gida_total
        footprint_kisibasi =  total_footprint / customer_number
        category_footprints = {
            "Elektrik": elektrik_total,
            "Doğal Gaz": gaz_total,
            "Su": su_total,
            "Atık Yönetimi": atik_total,
            "Gıda Tüketimi": gida_total
        }

        st.session_state.latest_result = {
            "Company": company_name,
            **category_footprints,
            "Toplam": total_footprint,
            "kisibasi" : footprint_kisibasi
        }
        st.session_state.latest_inputs = user_inputs
        st.session_state.latest_categories = category_footprints
        st.session_state.scoreboard.append(st.session_state.latest_result)
        st.success("✅ Karbon ayak izi başarıyla hesaplandı!")

    elif hesapla and not company_name:
        st.error("İşletme İsminizi Giriniz")


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
        st.metric("Kişi Başına Düşen Toplam Karbon Ayak İzi", f"{results['kisibasi']:.2f} kg CO2")

        # veri görselleştirme
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
