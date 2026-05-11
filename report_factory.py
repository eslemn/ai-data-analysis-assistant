from llm_report import LLMReportGenerator

class BasicReportGenerator:  #basit manuesl rapor üreten sınıf
    def generate(self, summary, df):
        report_lines = [
            "=========================================",
            "         TEMEL ARAÇ ANALİZ RAPORU        ",
            "=========================================\n",
            f"Toplam Araç Sayısı    : {len(df)}",
            f"Ortalama Sağlık Skoru : {df['health_score'].mean():.2f}",
            f"Kritik Araç Sayısı    : {(df['status'] == 'Critical').sum()}",
            f"Yüksek Riskli Araç    : {(df['risk_level'] == 'High Risk').sum() if 'risk_level' in df.columns else 'N/A'}\n",
            "--- Sensör İstatistikleri (Ortalama / Min / Maks) ---"
        ]
        
        for col in summary.columns:
            if col in ['vehicle_id']: continue
            
            mean_val = summary.loc['mean', col]
            min_val = summary.loc['min', col]
            max_val = summary.loc['max', col]
            
            report_lines.append(f"• {col.upper()}: Ort={mean_val:.1f} | Min={min_val:.1f} | Maks={max_val:.1f}")

        report_lines.append("\n=========================================")
        
        return "\n".join(report_lines)

class ReportFactory:   #doğru nesneyi üretmekten sorumlu sınıf
    @staticmethod      #neden statik çünkü nesne oluşturmadan çağırıyoruz
    def create_report_generator(report_type):
        if report_type == "basic":
            return BasicReportGenerator()
        elif report_type == "llm":
            return LLMReportGenerator()
        else:
            raise ValueError(f"Unknown report type: {report_type}")        
        

        #factory pattern nesne oluşturma işlemini merkezi bir yapıya alarak sistemin bağımlılığını azaltır ve yeni rapor türleri eklemeyi kolaylaştırır.
        #  Yeni bir rapor türü eklemek için sadece yeni bir sınıf oluşturup factory methodunu güncellemek yeterlidir.