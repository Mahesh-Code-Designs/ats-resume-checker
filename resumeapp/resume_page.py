import PyPDF2
import csv
import re



class Resumepage:

    def __init__ (self,pdf_path):
        self.pdf_path = pdf_path
        self.text = self.extract_text()
    
    def extract_text(self):
        text = ""
        with open (self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        return text.lower()
    
    def get_email(self):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'
        match = re.findall( email_pattern , self.text)
        
        if match:
            return match[0] 
        else:
            return "Not Found"
    
    def get_name(self):
        lines = self.text.split('\n')
        return lines[0].strip() if lines else "Unknown"
    
    def load_keywords(self):
        with open('keywords.csv', 'r') as file:
            reader =csv.reader(file)
            return [row[0].lower() for row in reader]
    
    def calculate_score(self):
        keywords = self.load_keywords()
        matched = 0

        for keyword in keywords:
            if keyword in self.text:
                matched += 1

        total = len(keywords)
        score = int((matched/total) *100) if total > 0 else 0

        return score     


            


