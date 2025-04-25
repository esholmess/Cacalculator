def get_general_recommendations(total):
    recommendations = []
    
    if total < 4000:
        
        recommendations.extend([
            "**Tebrikler!** Karbon ayak iziniz oldukça düşük.",
            "🌞 Güneş enerjisine geçmeyi değerlendirin.",
            "💻 Video konferans sistemlerini daha sık kullanın.",
            "♻️ Mevcut tasarruf ve geri dönüşüm uygulamalarınızı sürdürün."
        ])
    elif 4000 < total < 10000:
        
        recommendations.extend([
            "**İyi iş çıkardınız!** Ancak daha fazla tasarruf yapabileceğiniz alanlar var.",
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

