"""
AI-powered veterinary analysis components for future veterinary technology
These components use pattern recognition and data analysis to provide insights
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import re


class VeterinaryAIAssistant:
    """
    AI-powered veterinary assistant with multiple analysis capabilities.
    This is designed to showcase future veterinary technology concepts.
    """

    def __init__(self):
        # Species-specific normal ranges
        self.vital_ranges = {
            "dog": {
                "heart_rate": (60, 140),
                "respiratory_rate": (10, 30),
                "temperature": (101.0, 102.5)
            },
            "cat": {
                "heart_rate": (140, 220),
                "respiratory_rate": (20, 30),
                "temperature": (100.5, 102.5)
            },
            "bird": {
                "heart_rate": (200, 400),
                "respiratory_rate": (15, 40),
                "temperature": (104.0, 108.0)
            },
            "rabbit": {
                "heart_rate": (180, 250),
                "respiratory_rate": (30, 60),
                "temperature": (101.0, 103.0)
            }
        }

        # Common conditions and their risk factors
        self.condition_risk_factors = {
            "hip_dysplasia": ["large_breed", "obesity", "rapid_growth"],
            "diabetes": ["obesity", "age_over_7", "breed_predisposition"],
            "kidney_disease": ["age_over_10", "breed_predisposition", "high_protein_diet"],
            "dental_disease": ["age_over_3", "no_dental_care", "small_breed"],
            "heart_disease": ["age_over_8", "breed_predisposition", "obesity"]
        }

    def analyze_symptoms(self, symptoms: List[str], species: str) -> Dict:
        """
        AI-powered symptom analysis using pattern recognition
        Returns potential diagnoses and urgency level
        """
        symptom_patterns = {
            "emergency": [
                "difficulty breathing", "seizure", "bleeding", "unconscious",
                "bloated abdomen", "unable to urinate", "severe pain"
            ],
            "urgent": [
                "vomiting", "diarrhea", "lethargy", "loss of appetite",
                "limping", "coughing", "excessive thirst"
            ],
            "routine": [
                "scratching", "dry skin", "mild odor", "slight weight change"
            ]
        }

        # Analyze urgency
        urgency = "routine"
        matching_patterns = []

        for level, pattern_list in symptom_patterns.items():
            for symptom in symptoms:
                symptom_lower = symptom.lower()
                for pattern in pattern_list:
                    if pattern in symptom_lower:
                        matching_patterns.append(pattern)
                        if level == "emergency":
                            urgency = "emergency"
                        elif level == "urgent" and urgency != "emergency":
                            urgency = "urgent"

        # Generate potential diagnoses based on symptom combinations
        potential_diagnoses = self._generate_diagnoses(symptoms, species)

        return {
            "urgency": urgency,
            "confidence": 0.75 if matching_patterns else 0.5,
            "matching_patterns": matching_patterns,
            "potential_diagnoses": potential_diagnoses,
            "recommended_tests": self._recommend_tests(symptoms, species),
            "analysis_timestamp": datetime.now().isoformat()
        }

    def _generate_diagnoses(self, symptoms: List[str], species: str) -> List[Dict]:
        """Generate potential diagnoses based on symptoms"""
        diagnoses = []
        symptoms_lower = [s.lower() for s in symptoms]

        # Respiratory conditions
        if any(s in " ".join(symptoms_lower) for s in ["cough", "breathing", "wheez"]):
            diagnoses.append({
                "condition": "Respiratory Infection",
                "probability": 0.65,
                "category": "Respiratory"
            })

        # Gastrointestinal conditions
        if any(s in " ".join(symptoms_lower) for s in ["vomit", "diarrhea", "appetite"]):
            diagnoses.append({
                "condition": "Gastrointestinal Upset",
                "probability": 0.70,
                "category": "Digestive"
            })

        # Skin conditions
        if any(s in " ".join(symptoms_lower) for s in ["scratch", "itch", "skin", "rash"]):
            diagnoses.append({
                "condition": "Dermatological Issue",
                "probability": 0.60,
                "category": "Skin"
            })

        # Musculoskeletal
        if any(s in " ".join(symptoms_lower) for s in ["limp", "pain", "stiff", "mobility"]):
            diagnoses.append({
                "condition": "Musculoskeletal Problem",
                "probability": 0.55,
                "category": "Orthopedic"
            })

        return diagnoses

    def _recommend_tests(self, symptoms: List[str], species: str) -> List[str]:
        """Recommend diagnostic tests based on symptoms"""
        tests = ["Complete Blood Count (CBC)", "Physical Examination"]
        symptoms_lower = [s.lower() for s in symptoms]

        if any(s in " ".join(symptoms_lower) for s in ["vomit", "diarrhea", "appetite"]):
            tests.extend(["Fecal Examination", "Blood Chemistry Panel"])

        if any(s in " ".join(symptoms_lower) for s in ["cough", "breathing"]):
            tests.extend(["Chest X-Ray", "Respiratory Panel"])

        if any(s in " ".join(symptoms_lower) for s in ["thirst", "urination"]):
            tests.extend(["Urinalysis", "Kidney Function Test"])

        return tests

    def assess_health_risks(self, patient_data: Dict) -> Dict:
        """
        AI-powered health risk assessment based on patient profile
        Analyzes breed, age, weight, and medical history
        """
        risks = []
        risk_score = 0.0

        # Age-based risks
        age_years = self._calculate_age(patient_data.get("date_of_birth", ""))
        if age_years > 10:
            risks.append({
                "risk": "Senior Health Issues",
                "severity": "medium",
                "probability": 0.70,
                "description": "Increased risk of age-related conditions"
            })
            risk_score += 0.3

        # Weight-based risks (simplified - would need breed standards in production)
        weight = patient_data.get("weight", 0)
        if weight > 50:  # Simplified check
            risks.append({
                "risk": "Obesity-related Complications",
                "severity": "medium",
                "probability": 0.60,
                "description": "Excess weight can lead to joint, heart, and metabolic issues"
            })
            risk_score += 0.25

        # Chronic conditions
        chronic_conditions = patient_data.get("chronic_conditions", [])
        for condition in chronic_conditions:
            risks.append({
                "risk": f"Complications from {condition}",
                "severity": "high",
                "probability": 0.50,
                "description": f"Ongoing management needed for {condition}"
            })
            risk_score += 0.20

        return {
            "overall_risk_score": min(risk_score, 1.0),
            "risk_level": self._categorize_risk(risk_score),
            "identified_risks": risks,
            "assessment_date": datetime.now().isoformat()
        }

    def _calculate_age(self, date_of_birth: str) -> float:
        """Calculate age in years from date of birth"""
        try:
            dob = datetime.fromisoformat(date_of_birth)
            age_days = (datetime.now() - dob).days
            return age_days / 365.25
        except:
            return 0

    def _categorize_risk(self, score: float) -> str:
        """Categorize risk score into levels"""
        if score < 0.3:
            return "low"
        elif score < 0.6:
            return "medium"
        else:
            return "high"

    def generate_preventive_care_plan(self, patient_data: Dict) -> List[Dict]:
        """
        Generate AI-powered preventive care recommendations
        Based on species, age, breed, and health history
        """
        recommendations = []
        species = patient_data.get("species", "").lower()
        age_years = self._calculate_age(patient_data.get("date_of_birth", ""))

        # Vaccination recommendations
        vaccinations = patient_data.get("vaccinations", [])
        if not vaccinations or self._needs_vaccination_update(vaccinations):
            recommendations.append({
                "category": "Vaccination",
                "recommendation": f"Annual {species} vaccination booster",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "reasoning": "Maintain immunity against common diseases"
            })

        # Dental care
        if age_years > 3:
            recommendations.append({
                "category": "Dental",
                "recommendation": "Professional dental cleaning",
                "priority": "medium",
                "due_date": (datetime.now() + timedelta(days=60)).isoformat(),
                "reasoning": "Prevent periodontal disease and maintain oral health"
            })

        # Wellness exams
        if age_years > 7:
            recommendations.append({
                "category": "Wellness",
                "recommendation": "Semi-annual senior wellness exam",
                "priority": "high",
                "due_date": (datetime.now() + timedelta(days=90)).isoformat(),
                "reasoning": "Early detection of age-related conditions"
            })
        else:
            recommendations.append({
                "category": "Wellness",
                "recommendation": "Annual wellness exam",
                "priority": "medium",
                "due_date": (datetime.now() + timedelta(days=180)).isoformat(),
                "reasoning": "Routine health monitoring"
            })

        # Parasite prevention
        recommendations.append({
            "category": "Parasite Prevention",
            "recommendation": f"Year-round heartworm and flea prevention for {species}",
            "priority": "high",
            "due_date": datetime.now().isoformat(),
            "reasoning": "Continuous protection against parasites"
        })

        return recommendations

    def _needs_vaccination_update(self, vaccinations: List[Dict]) -> bool:
        """Check if vaccinations need updating"""
        if not vaccinations:
            return True

        # Check most recent vaccination
        try:
            latest_vax = max(vaccinations, key=lambda x: x.get("date_administered", ""))
            vax_date = datetime.fromisoformat(latest_vax.get("date_administered", ""))
            days_since = (datetime.now() - vax_date).days
            return days_since > 365
        except:
            return True

    def predict_health_trends(self, patient_data: Dict) -> Dict:
        """
        AI-powered health trend prediction based on historical data
        Analyzes weight trends, medication patterns, and visit frequency
        """
        medical_history = patient_data.get("medical_history", [])

        trends = {
            "visit_frequency": self._analyze_visit_frequency(medical_history),
            "weight_trend": self._analyze_weight_trend(patient_data),
            "condition_progression": self._analyze_condition_progression(patient_data),
            "predicted_needs": [],
            "analysis_date": datetime.now().isoformat()
        }

        # Generate predictions based on trends
        if trends["visit_frequency"]["trend"] == "increasing":
            trends["predicted_needs"].append({
                "prediction": "May require increased monitoring",
                "confidence": 0.65,
                "timeframe": "next_3_months"
            })

        if trends["weight_trend"]["trend"] == "increasing":
            trends["predicted_needs"].append({
                "prediction": "Weight management program recommended",
                "confidence": 0.70,
                "timeframe": "immediate"
            })

        return trends

    def _analyze_visit_frequency(self, medical_history: List[Dict]) -> Dict:
        """Analyze visit frequency trends"""
        if len(medical_history) < 2:
            return {"trend": "insufficient_data", "visits_per_year": 0}

        recent_visits = len([v for v in medical_history
                           if self._is_recent(v.get("date", ""), 365)])

        return {
            "trend": "stable",
            "visits_per_year": recent_visits,
            "total_visits": len(medical_history)
        }

    def _analyze_weight_trend(self, patient_data: Dict) -> Dict:
        """Analyze weight trends (simplified - would use historical weights in production)"""
        current_weight = patient_data.get("weight", 0)

        return {
            "current_weight": current_weight,
            "trend": "stable",
            "recommendation": "Monitor weight regularly"
        }

    def _analyze_condition_progression(self, patient_data: Dict) -> Dict:
        """Analyze chronic condition progression"""
        chronic_conditions = patient_data.get("chronic_conditions", [])

        return {
            "active_conditions": len(chronic_conditions),
            "conditions": chronic_conditions,
            "status": "stable" if chronic_conditions else "healthy"
        }

    def _is_recent(self, date_str: str, days: int) -> bool:
        """Check if a date is within the last N days"""
        try:
            date = datetime.fromisoformat(date_str)
            return (datetime.now() - date).days <= days
        except:
            return False

    def smart_triage(self, symptoms: List[str], vitals: Dict, species: str) -> Dict:
        """
        AI-powered triage system for prioritizing appointments
        Combines symptom analysis with vital sign assessment
        """
        symptom_analysis = self.analyze_symptoms(symptoms, species)
        vital_assessment = self.assess_vitals(vitals, species)

        # Determine overall priority
        priority_score = 0
        if symptom_analysis["urgency"] == "emergency":
            priority_score = 10
        elif symptom_analysis["urgency"] == "urgent":
            priority_score = 7
        else:
            priority_score = 3

        if vital_assessment["status"] == "critical":
            priority_score = max(priority_score, 10)
        elif vital_assessment["status"] == "abnormal":
            priority_score = max(priority_score, 7)

        return {
            "triage_priority": self._priority_to_category(priority_score),
            "priority_score": priority_score,
            "recommended_action": self._get_triage_action(priority_score),
            "symptom_analysis": symptom_analysis,
            "vital_assessment": vital_assessment,
            "timestamp": datetime.now().isoformat()
        }

    def assess_vitals(self, vitals: Dict, species: str) -> Dict:
        """Assess vital signs against normal ranges"""
        species_lower = species.lower()
        normal_ranges = self.vital_ranges.get(species_lower, self.vital_ranges["dog"])

        assessments = {}
        abnormal_count = 0

        for vital, value in vitals.items():
            if vital in normal_ranges:
                min_val, max_val = normal_ranges[vital]
                if value < min_val:
                    assessments[vital] = {"status": "low", "value": value, "normal_range": normal_ranges[vital]}
                    abnormal_count += 1
                elif value > max_val:
                    assessments[vital] = {"status": "high", "value": value, "normal_range": normal_ranges[vital]}
                    abnormal_count += 1
                else:
                    assessments[vital] = {"status": "normal", "value": value, "normal_range": normal_ranges[vital]}

        overall_status = "normal"
        if abnormal_count >= 2:
            overall_status = "critical"
        elif abnormal_count == 1:
            overall_status = "abnormal"

        return {
            "status": overall_status,
            "assessments": assessments,
            "abnormal_count": abnormal_count
        }

    def _priority_to_category(self, score: int) -> str:
        """Convert priority score to category"""
        if score >= 9:
            return "emergency"
        elif score >= 6:
            return "urgent"
        elif score >= 4:
            return "soon"
        else:
            return "routine"

    def _get_triage_action(self, score: int) -> str:
        """Get recommended action based on triage score"""
        if score >= 9:
            return "Immediate emergency care required - seek veterinary attention now"
        elif score >= 6:
            return "Urgent care needed - schedule appointment within 24 hours"
        elif score >= 4:
            return "Schedule appointment within 3-5 days"
        else:
            return "Routine care - schedule at next convenient time"
