import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from cleaner import clean_data
from analyzer import analyze_data
from health import RuleBasedHealthStrategy, HealthContext
from prediction import predict_failures
from recommendation import generate_recommendations
from report_factory import ReportFactory
from database import init_db, save_results, load_results
from config import Config

# Veritabanını başlat
init_db()

st.set_page_config(page_title="Vehicle Predictive Maintenance", layout="wide")

# Config nesnesini (Singleton) al
config = Config()

# Başlık
st.title("Connected Vehicle Predictive Maintenance System")
st.markdown("Araç sensör verilerini analiz ederek kestirimci bakım önerileri sunan yapay zeka destekli sistem.")

# Ana sayfada kısa analiz akışı bilgisini göster
st.info("🔄 **Analysis Flow:** Data Entry → Data Cleaning → Health Score → Failure Prediction → Maintenance Recommendation → Report → Database")

# Beklenen kolonlar
expected_cols = ["vehicle_id", "speed", "engine_temp", "fuel_consumption", "mileage", "battery_voltage", "brake_wear", "vibration", "oil_quality", "tire_pressure"]

# --- ORTAK ANALİZ FONKSİYONU ---
def run_analysis(df_raw, r_type):
    with st.spinner("Analiz yapılıyor..."):
        # Mevcut modülleri kullanarak akışı çalıştır
        df = clean_data(df_raw)
        analysis_summary = analyze_data(df)
        
        # Strategy Pattern ile Health Score Hesaplama
        strategy = RuleBasedHealthStrategy()
        health_context = HealthContext(strategy)
        df = health_context.calculate_health_score(df)
        
        # Tahmin ve Öneriler
        df = predict_failures(df)
        df = generate_recommendations(df)

        # health_score'a göre risk_level kolonu ekle
        def calculate_risk_level(score):
            if score >= 80:
                return "Low Risk"
            elif score >= 50:
                return "Medium Risk"
            else:
                return "High Risk"
                
        df['risk_level'] = df['health_score'].apply(calculate_risk_level)

        # Analiz Sonucu SQLite veritabanına kaydedilsin.
        save_results(df)
        
        # Raporlama Mantığı
        report_key = "llm" if r_type == "LLM Report" else "basic"
        generator = ReportFactory.create_report_generator(report_key)
        
        report_text = generator.generate(analysis_summary, df)
        
        if report_key == "llm" and ("failed" in report_text.lower() or "error" in report_text.lower()):
            st.session_state['report_warning'] = "LLM raporu oluşturulamadı veya Ollama çalışmıyor. Temel (Basic) rapora dönülüyor..."
            fallback_generator = ReportFactory.create_report_generator("basic")
            report_text = fallback_generator.generate(analysis_summary, df)
        else:
            st.session_state['report_warning'] = ""

        # Verileri etkileşimli ekranlar için Session State'e kaydet
        st.session_state['df'] = df
        st.session_state['analysis_summary'] = analysis_summary
        st.session_state['report_text'] = report_text
        st.session_state['analysis_done'] = True


# --- SIDEBAR ---
st.sidebar.header("Ayarlar")

# Kullanıcı Basic Report veya LLM Report seçebilsin
report_type = st.sidebar.selectbox(
    "Rapor Türü Seçiniz",
    ("Basic Report", "LLM Report")
)

# Sidebar'da Config sınıfından alınan eşik değerleri göster
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Sensör Uyarı Limitleri")
st.sidebar.markdown(f"""
- **Speed:** > {config.speed_threshold}
- **Engine Temp:** > {config.engine_temp_threshold}
- **Fuel:** > {config.fuel_threshold}
- **Mileage:** > {config.mileage_threshold}
- **Battery Volts:** < {config.battery_voltage_threshold}
- **Brake Wear:** > {config.brake_wear_threshold}
- **Vibration:** > {config.vibration_threshold}
- **Oil Quality:** < {config.oil_quality_threshold}
- **Tire Pressure:** < {config.tire_pressure_threshold}
""")


# --- VERİ GİRİŞ SEÇENEKLERİ ---
input_mode = st.radio("Veri Giriş Yöntemi", ["Toplu Analiz (CSV Yükle)", "Manuel Araç Girişi"], horizontal=True)

uploaded_file = None

if input_mode == "Toplu Analiz (CSV Yükle)":
    uploaded_file = st.file_uploader("Araç Verisi (CSV)", type="csv")
    
    if st.button("Analizi Başlat (CSV)"):
        # Dosya yüklenmezse varsayılan olarak data.csv kullanılsın.
        if uploaded_file is not None:
            try:
                df_raw = pd.read_csv(uploaded_file)
                missing_cols = [col for col in expected_cols if col not in df_raw.columns]
                if missing_cols:
                    st.session_state['warning_msg'] = f"⚠️ Yüklenen dosyada bazı kolonlar eksik: {', '.join(missing_cols)}. Bu durum analizi etkileyebilir."
                else:
                    st.session_state['warning_msg'] = "Yüklenen dosya kullanılıyor."
            except Exception as e:
                st.error(f"Dosya okuma hatası: {e}")
                df_raw = pd.read_csv("data.csv")
                st.session_state['warning_msg'] = "Dosya okunamadı, varsayılan data.csv kullanılıyor."
        else:
            df_raw = pd.read_csv("data.csv")
            st.session_state['warning_msg'] = "Varsayılan data.csv kullanılıyor."
            
        run_analysis(df_raw, report_type)

elif input_mode == "Manuel Araç Girişi":
    st.subheader("Manuel Araç Girişi")
    st.write("Tek bir aracın sensör verilerini girerek anlık analiz yapabilirsiniz.")
    
    with st.form("manual_entry_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            m_id = st.text_input("Vehicle ID", value="11")
            m_speed = st.number_input("Speed", value=95.0)
            m_fuel = st.number_input("Fuel Consumption", value=7.8)
            m_temp = st.number_input("Engine Temp", value=96.0)
        with col2:
            m_mileage = st.number_input("Mileage", value=28000.0)
            m_battery = st.number_input("Battery Voltage", value=12.2)
            m_brake = st.number_input("Brake Wear", value=50.0)
        with col3:
            m_vib = st.number_input("Vibration", value=3.4)
            m_oil = st.number_input("Oil Quality", value=70.0)
            m_tire = st.number_input("Tire Pressure", value=31.0)
            
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_single_btn = st.form_submit_button("Sadece Bu Aracı Analiz Et")
        with col_btn2:
            submit_append_btn = st.form_submit_button("Listeye Ekle ve Toplu Analiz Et")
        
        if submit_single_btn or submit_append_btn:
            try:
                df_manual = pd.DataFrame([{
                    "vehicle_id": str(m_id),
                    "speed": float(m_speed),
                    "fuel_consumption": float(m_fuel),
                    "engine_temp": float(m_temp),
                    "mileage": float(m_mileage),
                    "battery_voltage": float(m_battery),
                    "brake_wear": float(m_brake),
                    "vibration": float(m_vib),
                    "oil_quality": float(m_oil),
                    "tire_pressure": float(m_tire)
                }])
                
                if submit_single_btn:
                    st.session_state['warning_msg'] = "Sadece manuel girilen araç analiz edildi."
                    run_analysis(df_manual, report_type)
                    
                elif submit_append_btn:
                    # Mevcut veriyi al (yüklü dosya varsa o, yoksa varsayılan)
                    if uploaded_file is not None:
                        try:
                            df_base = pd.read_csv(uploaded_file)
                        except:
                            df_base = pd.read_csv("data.csv")
                    else:
                        df_base = pd.read_csv("data.csv")
                        
                    # Yeni aracı listeye ekle
                    df_combined = pd.concat([df_base, df_manual], ignore_index=True)
                    st.session_state['warning_msg'] = "Manuel araç mevcut verisetine eklendi ve tüm liste analiz edildi."
                    run_analysis(df_combined, report_type)
                    
            except Exception as e:
                st.error(f"Giriş hatası: Lütfen değerlerin doğruluğunu kontrol ediniz. ({e})")


# --- SONUÇLARI GÖSTER (Session State üzerinden) ---
if st.session_state.get('analysis_done', False):
    df = st.session_state['df']
    
    # Varsa uyarıları göster
    if st.session_state.get('warning_msg'):
        if "eksik" in st.session_state['warning_msg'] or "varsayılan" in st.session_state['warning_msg'].lower():
            st.warning(st.session_state['warning_msg'])
        else:
            st.success(st.session_state['warning_msg'])
            
    st.success("Analiz tamamlandı ve sonuçlar veritabanına kaydedildi.")

    # Analiz tamamlandıktan sonra üst kısımda 4 metric kart göster
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    total_vehicles = len(df)
    normal_vehicles = len(df[df['risk_level'] == 'Low Risk'])
    high_risk_vehicles = len(df[df['risk_level'] == 'High Risk'])
    avg_health = df['health_score'].mean()
    
    col1.metric("Toplam Araç Sayısı", total_vehicles)
    col2.metric("Normal Araç Sayısı", normal_vehicles)
    col3.metric("High Risk Araç Sayısı", high_risk_vehicles)
    col4.metric("Ortalama Health Score", f"{avg_health:.1f}")
    st.markdown("---")

    # Analiz sonuçlarını CSV olarak indirme butonu
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Tüm Sonuçları İndir (CSV)",
        data=csv_data,
        file_name='vehicle_analysis_results.csv',
        mime='text/csv',
    )

    rename_map = {
        "vehicle_id": "Araç ID",
        "health_score": "Sağlık Skoru",
        "status": "Durum",
        "failure_risk_score": "Arıza Risk Skoru",
        "risk_level": "Risk Seviyesi",
        "predicted_fault": "Tahmin Edilen Arıza",
        "maintenance_recommendation": "Bakım Önerisi"
    }
    display_cols = ["vehicle_id", "health_score", "status", "risk_level", "predicted_fault", "maintenance_recommendation"]

    # Ekran Düzeni ve Sekmeler
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Sonuç Tablosu", 
        "Health Score Grafiği", 
        "Risk Dağılımı Grafiği",
        "En Kritik 5 Araç",
        "Araç Detay & Bildirimler",
        "Rapor", 
        "Geçmiş Kayıtlar"
    ])

    # Sonuç Tablosu ve Filtreleme
    with tab1:
        st.subheader("Tüm Araç Analiz Sonuçları")
        
        # Sonuç tablosu için risk_level filtresi ekle
        risk_filter = st.selectbox("Risk Seviyesine Göre Filtrele:", ["All", "Low Risk", "Medium Risk", "High Risk"])
        
        filtered_df = df.copy()
        if risk_filter != "All":
            filtered_df = filtered_df[filtered_df['risk_level'] == risk_filter]
            
        filtered_df = filtered_df[[c for c in display_cols if c in filtered_df.columns]].rename(columns=rename_map)
        
        # Sonuç tablosunda risk_level değerine göre satırları renklendir
        def highlight_risk(row):
            risk_val = row.get('Risk Seviyesi', '')
            if risk_val == 'High Risk':
                return ['background-color: rgba(255, 99, 71, 0.3)'] * len(row)  # Hafif kırmızı
            elif risk_val == 'Medium Risk':
                return ['background-color: rgba(255, 215, 0, 0.3)'] * len(row) # Hafif sarı
            elif risk_val == 'Low Risk':
                return ['background-color: rgba(144, 238, 144, 0.3)'] * len(row) # Hafif yeşil
            else:
                return [''] * len(row)
        
        st.dataframe(filtered_df.style.apply(highlight_risk, axis=1), use_container_width=True)

    # Health Score Grafiği
    with tab2:
        st.subheader("Araç Sağlık Skorları (Health Scores)")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(df['vehicle_id'].astype(str), df['health_score'], color='skyblue')
        ax.set_ylabel('Health Score')
        ax.set_xlabel('Vehicle ID')
        ax.set_title('Vehicle Health Scores')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Ayrı bir tab olarak Risk Dağılımı grafiği ekle
    with tab3:
        st.subheader("Risk Dağılımı")
        risk_counts = df['risk_level'].value_counts()
        
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        colors = {'Low Risk': '#90ee90', 'Medium Risk': '#ffd700', 'High Risk': '#ff6347'}
        bar_colors = [colors.get(x, 'blue') for x in risk_counts.index]
        
        bars = ax2.bar(risk_counts.index, risk_counts.values, color=bar_colors)
        ax2.set_ylabel('Araç Sayısı')
        ax2.set_title('Risk Seviyesi Dağılımı')
        
        # Barların üstüne değerleri yazdır
        for bar in bars:
            yval = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')
            
        st.pyplot(fig2)

    # “En Kritik 5 Araç” bölümü ekle
    with tab4:
        st.subheader("🚨 En Kritik 5 Araç")
        # health_score değerine göre küçükten büyüğe sırala ve ilk 5 aracı göster
        top_5_critical = df.sort_values(by='health_score', ascending=True).head(5)
        top_5_display = top_5_critical[[c for c in display_cols if c in top_5_critical.columns]].rename(columns=rename_map)
        st.dataframe(top_5_display, use_container_width=True)

    # Yeni Araç Detay ve Bildirimler Sekmesi
    with tab5:
        st.subheader("Araç Detay Analizi ve Bildirimler (Observer Pattern)")
        
        # Üst Kısım: Seçili Araç Detayları
        col_select, col_info = st.columns([1, 2])
        
        with col_select:
            st.markdown("##### Detay Görmek İçin Araç Seçin")
            selected_vid = st.selectbox("Vehicle ID:", df['vehicle_id'].unique())
            
        with col_info:
            if selected_vid is not None:
                vehicle_data = df[df['vehicle_id'] == selected_vid].iloc[0]
                
                st.markdown(f"#### Araç {selected_vid} Özeti")
                st.write(f"**Sağlık Skoru:** {vehicle_data.get('health_score', 'N/A')}")
                st.write(f"**Risk Seviyesi:** {vehicle_data.get('risk_level', 'N/A')}")
                st.write(f"**Tahmin Edilen Arıza:** {vehicle_data.get('predicted_fault', 'N/A')}")
                st.write(f"**Bakım Önerisi:** {vehicle_data.get('maintenance_recommendation', 'N/A')}")
                
                # Sensör analizi ve risk nedeni tahmini
                reasons = []
                if vehicle_data.get('engine_temp', 0) > config.engine_temp_threshold:
                    reasons.append("motor sıcaklığı yüksek")
                if vehicle_data.get('fuel_consumption', 0) > config.fuel_threshold:
                    reasons.append("yakıt tüketimi yüksek")
                if vehicle_data.get('brake_wear', 0) > config.brake_wear_threshold:
                    reasons.append("fren aşınması yüksek")
                if vehicle_data.get('tire_pressure', 100) < config.tire_pressure_threshold:
                    reasons.append("lastik basıncı düşük")
                if vehicle_data.get('battery_voltage', 100) < config.battery_voltage_threshold:
                    reasons.append("akü voltajı düşük")
                if vehicle_data.get('vibration', 0) > config.vibration_threshold:
                    reasons.append("titreşim yüksek")
                if vehicle_data.get('speed', 0) > config.speed_threshold:
                    reasons.append("hız limiti aşımı")
                if vehicle_data.get('mileage', 0) > config.mileage_threshold:
                    reasons.append("kilometre yüksek")
                if vehicle_data.get('oil_quality', 100) < config.oil_quality_threshold:
                    reasons.append("yağ kalitesi düşük")
                    
                if reasons:
                    st.warning("⚠️ **Riskin Kaynaklanabileceği Sensörler:**\n" + "\n".join([f"- {r.capitalize()}" for r in reasons]))
                else:
                    st.success("✅ Sensör değerleri normal sınırlarda.")

        st.markdown("---")
        
        # Alt Kısım: Observer Pattern Çıktıları (Sadece High Risk)
        st.subheader("🔔 Bakım Bildirimleri (High Risk)")
        high_risk_list = df[df['risk_level'] == 'High Risk']['vehicle_id'].tolist()
        
        if high_risk_list:
            for vid in high_risk_list:
                st.error(
                    f"🚨 **Araç {vid} yüksek riskli.**\n"
                    f"- `MaintenanceNotifier` bakım ekibine bildirim gönderdi.\n"
                    f"- `DashboardNotifier` araç ekranı için uyarı oluşturdu."
                )
        else:
            st.info("Şu an yüksek riskli araç bulunmamaktadır. Herhangi bir bildirim tetiklenmedi.")

    # Raporlama
    with tab6:
        st.subheader("Analiz Raporu")
        st.info("ℹ️ Bu rapor Factory Method Pattern kullanılarak oluşturulmuştur.")
        
        if st.session_state.get('report_warning'):
            st.warning(st.session_state['report_warning'])
            
        st.text_area("Rapor Çıktısı", value=st.session_state['report_text'], height=300)
        
        st.download_button(
            label="📝 Raporu İndir (.txt)",
            data=st.session_state['report_text'],
            file_name='vehicle_analysis_report.txt',
            mime='text/plain',
        )

    # Geçmiş Kayıtlar
    with tab7:
        st.subheader("Geçmiş Analiz Kayıtları (Veritabanından)")
        st.info("ℹ️ Bu kayıtlar SQLite veritabanından okunmaktadır.")
        past_results_df = load_results()
        if not past_results_df.empty:
            st.dataframe(past_results_df.rename(columns=rename_map), use_container_width=True)
        else:
            st.info("Henüz geçmiş kayıt bulunmamaktadır.")
