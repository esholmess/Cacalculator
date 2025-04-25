import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import json
from downloadpdf import save_as_pdf
import datetime
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


st.set_page_config(page_title="KARBON-AT", page_icon="🌍", layout="wide") #sayfa ayarı
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
        background:linear-gradient(to top, #006d57, #255F38); 
        color: #015551
        }


    </style>
    <h2 style="margin-bottom: -40px">🌿KARBON<span style="color:yellow">AT</span></h2>
    
""", unsafe_allow_html = True
)



with st.sidebar: #sidebar ayarları
    st.header("HAKKINDA")
    st.write("""
        KarbonAT size daha sürdürülebilir bir işletme olma konusunda yol gösterir!
    """)
    st.markdown("""
        <style>
                #sidebarh3{
                margin-top: -5px;
                }
                #sidebarul{
                margin-right:25px;
                text-align:justify
                }
                </style>
        <h3 id="sidebarh3">KarbonAT'ı kullanmaya başla:</h3><p>
        <ul id="sidebarul">
        <li> Sizden istenen verileri aylık harcama raporlarınıza dayanarak giriniz. (Örn: Su faturası)</li>
        <li> Ardından formun sonundaki butona tıklayınız</li>
        <li> Raporlar ve Öneriler sekmesinde hesaplanmış karbon ayakizinizi ve önerilerinizi bulacaksınız :)</li>
        <li> Scoreboardda ise yerinizi alabilirsiniz</li>
        </ul>
        </p>
        </div>
        </div>

    """,unsafe_allow_html=True)

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



tab1, tab2, tab3, tab4 = st.tabs(["🏠", "Hesap Makinesi", "Rapor & Öneriler", "🏆"]) #sekmeler

with tab1: #ana sayfa
   

    st.markdown("""
    <style>
       
        .stMarkdown div {
            border-radius: 5px;
            margin-bottom: 1rem;
            transition: transform 0.2s ease-in-out;
            color: white;  
            margin-top: 0.7rem;
            
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
            background: linear-gradient(45deg, #28a7462b, #11a0753d);  
            border: 1px solid #28a745;
            color: white;
            border-radius: 10px;
            display:flex;
            flex-direction: column;
            align-items:center;
            justify-content:center;
            font-size:10px;
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
                margin-bottom: -30px
                }

        .banner h3 {
                margin-bottom: -10px;
                margin-top: -10px;}

    </style>
    <div class="banner-container">
    <div class="banner">
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



with tab2: #hesap makinesi sekmesi
    st.markdown("""
        <style>
        h3 {
            margin-bottom: -1rem;
            margin-top: 0.5rem
        }
        .stNumberInput {
            margin-top: -0.5rem;
 
        }
        .stForm {
            background-color: rgba(0, 174, 128, 0.1);  
            margin: 0.4rem 1rem;             
        }
        .form_title {
                margin: 0rem 1rem
        }
        #formp {
                margin-top: -0.7rem
                }

         
        }
        #form {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;}

        </style>
        <div id= "form">
        <h3 class = "form_title">🌍 HARCAMA GİRİŞİ</h3>
        <p class="form_title" id="formp">Karbon ayakizi hesaplaması için aşağıdaki formda sizden istenen verileri giriniz. 🌱</p>
        </div>
                
                """, unsafe_allow_html=True)


    with st.form("carbon_form"): # şirket verisi ve hesaplama için harcama verileri girişleri

  
        with st.expander("🏢 İŞLETME BİLGİLERİ *"):
                company_name = st.text_input("İşletme Adı", placeholder="Örn. Teknofest Suit Otel")
                col1, col2 = st.columns(2)
                with col1:
                    date_input = st.date_input("Bulunduğunuz Ayı ve Yılı Girin", datetime.date.today())
                with col2:
                    customer_number = st.number_input("Verilerin ait olduğu tarihe ilişkin müşteri sayısını giriniz", min_value=1, step=1)

                col3, col4 = st.columns(2)
                with col3:
                    metrekare_number = st.number_input("İşletmenizin toplam metrekare sayısını giriniz", min_value=1, step=1)
                with col4:
                    room_number =  st.number_input("İşletmenizin toplam oda sayısını giriniz", min_value=1, step=1)
        
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



        hesapla = st.form_submit_button("🌍 Karbon Ayak İzini Hesapla") # verileri gönderme (submitleme) butonu

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
            "Kisi Basi" : footprint_kisibasi,
            "Tarih": date_input
        }
        st.session_state.latest_inputs = user_inputs
        st.session_state.latest_categories = category_footprints
        st.session_state.scoreboard.append(st.session_state.latest_result)
        st.success("✅ Karbon ayak izi başarıyla hesaplandı!")

    elif hesapla and not company_name:
        st.error("İşletme İsminizi Giriniz")
    elif hesapla and not customer_number:
        st.error("Müşteri sayısını giriniz - Müşteri sayısı en az 1 olmalıdır.")
    


# Raporlar ve Öneriler Sekmesi

with tab3:
    st.subheader("📊 Raporlar ve Öneriler")

    if 'latest_result' in st.session_state:
        results = st.session_state.latest_result

        st.markdown(f"""
        <h2 style='text-align: center; color:#2ECC71'>{results["Company"]} 🚀</h2>
        <p style='text-align: center; font-size: 18px;'>📅 Tarihli Karbon Ayak İzi Raporu</p>
        """, unsafe_allow_html=True)

        # Emisyon detayları + grafik
        st.markdown("## 📊 Detaylı Emisyon Verileri (Alt Tür Bazlı)")
        for category, items in st.session_state.latest_inputs.items():
            with st.expander(f"📁 {category}", expanded=False):
                df = pd.DataFrame(list(items.items()), columns=["Alt Tür", "Emisyon (kg CO2)"])
                st.dataframe(df, use_container_width=True)

                # Grafik
                fig, ax = plt.subplots(figsize=(6, 3), facecolor='black')
                bars = ax.bar(df["Alt Tür"], df["Emisyon (kg CO2)"], color='#2ECC71')  # yeşil
                ax.set_facecolor('black')
                ax.set_ylabel("CO2 (kg)", color='white')
                ax.set_title(f"{category} - Alt Tür Emisyonları", color='white')
                ax.tick_params(axis='x', rotation=45, labelcolor='white')
                ax.tick_params(axis='y', labelcolor='white')
                ax.spines[:].set_color('white')
                st.pyplot(fig)

        # Kategori özeti
        df_summary = pd.DataFrame({
            "Kategori": list(st.session_state.latest_categories.keys()),
            "Toplam Emisyon (kg CO2)": list(st.session_state.latest_categories.values())
        })

        st.markdown("## 🔎 Kategori Bazlı Toplam Emisyon")

        st.dataframe(df_summary, use_container_width=True)
    
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='black')
        ax.barh(df_summary["Kategori"], df_summary["Toplam Emisyon (kg CO2)"], color='#27AE60')  # koyu yeşil
        ax.set_xlabel("CO2 (kg)", color='white')
        ax.set_title("Kategoriye Göre Karbon Ayak İzi", color='white')
        ax.tick_params(axis='x', labelcolor='white')
        ax.tick_params(axis='y', labelcolor='white')
        ax.set_facecolor('black')
        ax.spines[:].set_color('white')
        st.pyplot(fig)

        # Özet metrikler
        st.markdown("## 📌 Emisyon Özeti")
        col3, col4 = st.columns(2)
        col3.metric("Toplam Karbon Ayak İzi", f"{results['Toplam']:.2f} kg CO2")
        col4.metric("Kişi Başına Düşen", f"{results['Kisi Basi']:.2f} kg CO2")

        # Genel öneriler
        st.markdown("## 💡 Genel Öneriler")
        for rec in get_general_recommendations(results["Toplam"]):
            st.markdown(f"- {rec}")

        # Yapay zeka önerileri
        st.markdown("## 🤖 AI Tabanlı Öneriler")
        ai_button = st.button("AI ile Öneri Üret 🧠")
        ai_rec = [
            "🌱 Karbon dengeleme (offset) projelerine yatırım yapın.",
            "🚲 Personel için bisiklet paylaşım sistemleri kurun.",
            "🏭 Enerji tüketiminizi düzenli olarak izleyin ve raporlayın."
        ]
        if ai_button:
            with st.spinner("Yapay zeka öneriler üretiyor..."):
                time.sleep(2)
                st.success("İlave öneriler üretildi:")
                for i in ai_rec:
                    st.markdown(f"- {i}")

        # PDF çıktısı
        st.markdown("## 📝 Raporu PDF Olarak İndir")
        pdf_data = save_as_pdf(
            results=st.session_state.latest_result,
            category_footprints=st.session_state.latest_categories,
            recommendations=ai_rec,
            logo_path="logo.png"
        )

        st.download_button(
            label="📄 PDF İndir",
            data=pdf_data,
            file_name=f"{results['Company'].replace(' ', '_')}_karbon_raporu.pdf",
            mime="application/pdf"
        )
    else:
        st.info("📌 Lütfen önce hesaplama yapın.")
    


# Scoreboard Sekmesi

with tab4:
    st.subheader("🏆 Scoreboard")
    if st.session_state.scoreboard:
        df_scoreboard = pd.DataFrame(st.session_state.scoreboard)
        df_sorted = df_scoreboard.sort_values("Toplam").reset_index(drop=True)
        df_sorted.index += 1
        st.dataframe(df_sorted.rename_axis('Sıra'), use_container_width=True)
    else:
        st.info("Henüz hiçbir veri girilmedi.")
