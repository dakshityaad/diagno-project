import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document

class CoordinatorAgent:
    def __init__(self, agents: list, upload_folder="uploads"):
        """
        agents: list of agent objects in this order:
        [symptom_agent, report_agent, knowledge_agent]
        """
        self.symptom_agent = agents[0]
        self.report_agent = agents[1]
        self.knowledge_agent = agents[2]

        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

    def save_file(self, file):
        """Save uploaded file securely"""
        filepath = os.path.join(
            self.upload_folder,
            secure_filename(file.filename)
        )
        file.save(filepath)
        return filepath

    def extract_text(self, filepath):
        """Extract text from PDF, DOCX, or TXT"""
        if filepath.endswith(".pdf"):
            reader = PdfReader(filepath)
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        elif filepath.endswith(".docx"):
            doc = Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = "Unsupported file format."
        return text

    def handle_report(self, file):
        """Main logic: save → extract → send to ReportAgent"""
        filepath = self.save_file(file)
        text = self.extract_text(filepath)
        reply = self.report_agent.respond(text)
        return reply

    def handle_message(self, message: str) -> str:
        """Route the user message to the right agent based on keywords."""
        if not message or not message.strip():
            return "⚠️ Please enter a valid message."

        msg = message.lower()

        symptom_keywords = ["symptom", "fever", "cold", "cough", "pain", "headache",
                            "nausea", "vomiting", "diarrhea", "fatigue", "dizziness", "chills", "sore throat","fungal", "inflammation", "ulcer", "swelling", "bruising", 
                            "numbness", "tingling", "burning sensation", "seizure", "confusion", "memory loss", 
                            "difficulty speaking", "blurred speech", "balance issues", "tremor", "chest pain", "high blood pressure",
                            "low blood pressure", "irregular heartbeat", "palpitations", "menstrual cramps", 
                            "back pain", "neck pain", "shoulder pain", "hip pain", "knee pain", "ankle pain", 
                            "foot pain", "joint swelling", "stiff joints", "hair loss", "dry skin", "skin discoloration", 
                            "skin peeling", "acne", "eczema", "psoriasis", "allergic reaction", "food intolerance", "dehydration", 
                            "electrolyte imbalance", "eye strain", "hearing loss", "ear infection", "toothache", "gum swelling",
                            "bad breath", "weight gain", "obesity", "high cholesterol", "diabetes", "thyroid disorder",
                            "autoimmune disease", "arthritis", "asthma", "cancer", "stroke", "heart attack",
                            "respiratory distress", "pneumonia", "tuberculosis", "liver disease", "kidney stones", 
                            "urinary tract infection", "bladder pain", "constipation", "irritable bowel syndrome", "Crohn's disease",
                            "ulcerative colitis", "anemia", "blood disorder", "hemophilia", "menopause", "pregnancy", "lactation",
                            "hormonal imbalance", "fertility issues", "sexual dysfunction", "STD", "HIV", "AIDS", 
                            "hepatitis", "malaria", "dengue", "chikungunya", "typhoid", "sleep apnea", "restless legs", 
                            "migraine", "cluster headache", "tension headache", "brain tumor", "multiple sclerosis", 
                            "Parkinson's", "Alzheimer's", "epilepsy", "psychiatric disorder", "bipolar disorder", "schizophrenia",
                            "OCD", "PTSD", "addiction", "substance abuse", "withdrawal symptoms", "burnout", "fatigue syndrome", 
                            "viral load", "antibody", "immunization", "vaccine", "allergic rhinitis", "eczema flare-up", 
                            "hormonal therapy", "blood sugar", "insulin resistance", "thyroid hormone", "glucose levels", 
                            "iron deficiency", "vitamin deficiency", "calcium imbalance", "magnesium deficiency", "painkiller", 
                            "antibiotic", "antiviral", "antifungal", "anti-inflammatory", "steroid", "chemotherapy", "radiation", 
                            "surgery", "therapy", "counseling", "rehabilitation", "physical therapy", "occupational therapy", 
                            "speech therapy", "diet plan", "nutrition", "hydration", "rest", "exercise", "yoga", "meditation", 
                            "breathing exercises", "stress management", "mental health", "wellness", "preventive care", 
                            "early detection", "screening", "checkup", "lab test", "blood test", "urine test", "MRI", "CT scan",
                            "X-ray", "ultrasound", "ECG", "EEG", "biopsy", "pathology", "genetics", "mutation", "family history", 
                            "risk factors", "chronic condition", "acute illness", "self-care", "over-the-counter", "prescription", 
                            "dose", "side effect", "reaction", "recovery", "relapse", "complication", "prognosis", "infection control",
                            "hygiene", "sanitation", "isolation", "quarantine", "immune system", "white blood cells",
                            "red blood cells", "platelets", "clotting", "blood pressure", "cholesterol level", "lipid profile",
                            "bone density", "fracture", "osteoporosis", "joint replacement", "vascular disease", "artery", 
                            "vein", "circulation", "oxygenation", "respiration", "lung function", "heart rate", "pulse",
                            "body temperature", "metabolism", "hormone therapy", "psychiatric medication", "pain management", 
                            "allopathy", "ayurveda", "homeopathy", "naturopathy", "acupuncture", "chiropractic", "holistic care",
                            "alternative medicine", "herbal remedy", "aromatherapy", "detoxification", "supplement", 
                            "probiotic", "antioxidant", "enzyme", "pharmacy", "drug interaction", "prescription pad",
                            "generic medicine", "overdose", "pain relief", "anti-allergy", "immunotherapy", "blood transfusion",
                            "dialysis", "organ transplant", "stem cell therapy", "genetic testing", "biomedical research",
                            "clinical trial", "medical ethics", "informed consent", "palliative care", "hospice", 
                            "end-of-life care", "terminal illness", "life support", "ventilator", "defibrillator", 
                            "syringe", "intravenous", "catheter", "prosthetics", "orthotics", "wheelchair", "walker", 
                            "crutches", "bandage", "splint", "cast", "stitches", "wound care", "infection prevention", 
                            "sterilization", "disinfection", "hand sanitizer", "gloves", "face mask", 
                            "personal protective equipment", "surgical mask", "N95 mask", "health insurance", 
                            "co-pay", "deductible", "medical bill", "billing code", "healthcare provider", "primary care", 
                            "specialist", "nutritionist", "dietitian", "phlebotomist", "radiologist", "anesthesiologist", 
                            "dermatologist", "neurologist", "cardiologist", "oncologist", "endocrinologist", "psychiatrist",
                            "urologist", "gastroenterologist", "rheumatologist", "immunologist", "audiologist", 
                            "speech pathologist", "occupational health", "clinical psychologist", "health assessment",
                            "medical history", "symptom checker", "triage", "emergency care", 
                            "first aid", "CPR", "resuscitation", "ambulance", "emergency room", 
                            "intensive care", "blood pressure monitor", "glucometer", "pulse oximeter", 
                            "thermometer", "stethoscope", "ECG machine", "MRI scanner", "ultrasound device",
                            "X-ray plate", "defibrillation pads", "heart monitor", "nebulizer", "oxygen cylinder", 
                            "oxygen concentrator", "inhaler", "peak flow meter", "hearing aid", "vision test", "eye drop",
                            "contact lens", "spectacles", "dental floss", "mouthwash", "braces", "cavity", "gingivitis",
                            "periodontitis", "oral cancer", "TMJ disorder", "snoring", "sleep disorder", "jet lag", 
                            "circadian rhythm", "melatonin", "serotonin", "dopamine", "neurotransmitter", "brain chemistry",
                            "nerve damage", "neuropathy", "Parkinsonism", "Alzheimer's disease", "dementia", "cognitive decline",
                            "learning disability", "developmental disorder", "ADHD", "autism spectrum", "behavior therapy", 
                            "family counseling", "support group", "mental resilience", "self-esteem", "anger management",
                            "grief counseling", "postpartum care", "breastfeeding", "infant care", "child health", 
                            "immunization schedule", "growth chart", "development milestones", "school health",
                            "adolescent health", "menstrual hygiene", "PCOS", "endometriosis", "fertility treatment", 
                            "contraception", "sexual health", "STD prevention", "HIV testing", "viral hepatitis",
                            "tuberculosis screening", "malaria prevention", "vector control", "sanitation campaign", 
                            "public health", "epidemic", "pandemic", "outbreak control", "disease surveillance", 
                            "quarantine protocol", "contact tracing", "health education", "awareness program", 
                            "community health worker", "telemedicine", "e-health", "mobile clinic", "health app", 
                            "wearable device", "fitness tracker", "sleep tracker", "calorie counter", "step counter",
                            "meditation app", "mental wellness platform", "stress relief techniques", "work-life balance",
                            "ergonomics", "posture correction", "eye protection", "sun exposure", "UV index", "skin cancer",
                            "sunscreen", "moisturizer", "hydration therapy", "electrolyte replacement", "protein supplement", 
                            "nutritional deficiency", "micronutrients", "macronutrients", "dietary fiber", "plant-based diet", 
                            "keto diet", "intermittent fasting", "gluten intolerance", "lactose intolerance", "celiac disease",
                            "food allergy", "meal planning", "portion control", "calorie deficit", "weight management", 
                            "body mass index", "fitness regimen", "strength training", "cardio exercise", "flexibility training", 
                            "balance training", "recovery workout", "rehydration", "muscle recovery", "joint lubrication", 
                            "sports injury", "sprain", "strain", "fracture management", "rehab program"]

        if any(word in msg for word in symptom_keywords):
            return self.symptom_agent.respond(message)

       
        report_keywords = ["report", "test", "scan", "result", "blood", "x-ray", "mri", "upload","file", "document", "pdf"]
        if any(word in msg for word in report_keywords):
            return self.report_agent.respond(message)

        
        knowledge_keywords = ["how","why","you","i","know","what","how","explain", "what is", "knowledge", "info", "information", "tell", "meaning of"]
        if any(word in msg for word in knowledge_keywords):
            return self.knowledge_agent.respond(message)

        
        return self.knowledge_agent.respond(message)
