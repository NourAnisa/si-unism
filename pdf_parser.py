import pdfplumber
import re

def parse_skkm_pdf(file_path: str):
    activities = []
    
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            
            # Contoh parsing sederhana (sesuaikan dengan format PDF Anda)
            matches = re.finditer(
                r"(?P<date>\d{2}/\d{2}/\d{4})\s+(?P<activity>.+?)\s+(?P<level>.+?)\s+(?P<achievement>.+?)\s*$",
                text,
                re.MULTILINE
            )
            
            for match in matches:
                activities.append({
                    'date': match.group('date'),
                    'activity': match.group('activity'),
                    'level': match.group('level'),
                    'achievement': match.group('achievement')
                })
    
    return activities
