"""
Database models for Veterinary PIMS (Practice Information Management System)
"""
from datetime import datetime
from typing import Optional, List, Dict
import json


class Patient:
    """Veterinary patient model with comprehensive medical data"""

    def __init__(self, patient_id: str, name: str, species: str, breed: str,
                 owner_name: str, owner_contact: str, date_of_birth: str,
                 gender: str, weight: float, microchip_id: Optional[str] = None):
        self.patient_id = patient_id
        self.name = name
        self.species = species
        self.breed = breed
        self.owner_name = owner_name
        self.owner_contact = owner_contact
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.weight = weight
        self.microchip_id = microchip_id
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

        # Medical records
        self.medical_history: List[Dict] = []
        self.vaccinations: List[Dict] = []
        self.medications: List[Dict] = []
        self.allergies: List[str] = []
        self.chronic_conditions: List[str] = []

        # AI-enhanced features
        self.ai_risk_assessment: Optional[Dict] = None
        self.ai_preventive_care_recommendations: List[Dict] = []
        self.predicted_health_trends: Optional[Dict] = None

    def add_medical_record(self, date: str, diagnosis: str, treatment: str,
                          veterinarian: str, notes: str = ""):
        """Add a medical record entry"""
        record = {
            "date": date,
            "diagnosis": diagnosis,
            "treatment": treatment,
            "veterinarian": veterinarian,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }
        self.medical_history.append(record)
        self.updated_at = datetime.now().isoformat()

    def add_vaccination(self, vaccine_name: str, date_administered: str,
                       due_date: str, veterinarian: str, batch_number: str = ""):
        """Add vaccination record"""
        vaccination = {
            "vaccine_name": vaccine_name,
            "date_administered": date_administered,
            "due_date": due_date,
            "veterinarian": veterinarian,
            "batch_number": batch_number,
            "timestamp": datetime.now().isoformat()
        }
        self.vaccinations.append(vaccination)
        self.updated_at = datetime.now().isoformat()

    def add_medication(self, medication_name: str, dosage: str, frequency: str,
                      start_date: str, end_date: Optional[str], prescribing_vet: str):
        """Add medication record"""
        medication = {
            "medication_name": medication_name,
            "dosage": dosage,
            "frequency": frequency,
            "start_date": start_date,
            "end_date": end_date,
            "prescribing_vet": prescribing_vet,
            "active": end_date is None or end_date > datetime.now().isoformat(),
            "timestamp": datetime.now().isoformat()
        }
        self.medications.append(medication)
        self.updated_at = datetime.now().isoformat()

    def add_allergy(self, allergy: str):
        """Add allergy to patient record"""
        if allergy not in self.allergies:
            self.allergies.append(allergy)
            self.updated_at = datetime.now().isoformat()

    def add_chronic_condition(self, condition: str):
        """Add chronic condition to patient record"""
        if condition not in self.chronic_conditions:
            self.chronic_conditions.append(condition)
            self.updated_at = datetime.now().isoformat()

    def update_weight(self, new_weight: float):
        """Update patient weight"""
        self.weight = new_weight
        self.updated_at = datetime.now().isoformat()

    def set_ai_risk_assessment(self, risk_data: Dict):
        """Set AI-generated risk assessment"""
        self.ai_risk_assessment = risk_data
        self.updated_at = datetime.now().isoformat()

    def add_ai_recommendation(self, recommendation: Dict):
        """Add AI-generated preventive care recommendation"""
        self.ai_preventive_care_recommendations.append(recommendation)
        self.updated_at = datetime.now().isoformat()

    def set_health_trends(self, trends: Dict):
        """Set AI-predicted health trends"""
        self.predicted_health_trends = trends
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert patient object to dictionary"""
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "owner_name": self.owner_name,
            "owner_contact": self.owner_contact,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "weight": self.weight,
            "microchip_id": self.microchip_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "medical_history": self.medical_history,
            "vaccinations": self.vaccinations,
            "medications": self.medications,
            "allergies": self.allergies,
            "chronic_conditions": self.chronic_conditions,
            "ai_risk_assessment": self.ai_risk_assessment,
            "ai_preventive_care_recommendations": self.ai_preventive_care_recommendations,
            "predicted_health_trends": self.predicted_health_trends
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Patient':
        """Create patient object from dictionary"""
        patient = cls(
            patient_id=data["patient_id"],
            name=data["name"],
            species=data["species"],
            breed=data["breed"],
            owner_name=data["owner_name"],
            owner_contact=data["owner_contact"],
            date_of_birth=data["date_of_birth"],
            gender=data["gender"],
            weight=data["weight"],
            microchip_id=data.get("microchip_id")
        )
        patient.created_at = data.get("created_at", patient.created_at)
        patient.updated_at = data.get("updated_at", patient.updated_at)
        patient.medical_history = data.get("medical_history", [])
        patient.vaccinations = data.get("vaccinations", [])
        patient.medications = data.get("medications", [])
        patient.allergies = data.get("allergies", [])
        patient.chronic_conditions = data.get("chronic_conditions", [])
        patient.ai_risk_assessment = data.get("ai_risk_assessment")
        patient.ai_preventive_care_recommendations = data.get("ai_preventive_care_recommendations", [])
        patient.predicted_health_trends = data.get("predicted_health_trends")
        return patient


class PatientDatabase:
    """Simple in-memory patient database (can be replaced with SQLAlchemy/PostgreSQL)"""

    def __init__(self):
        self.patients: Dict[str, Patient] = {}

    def add_patient(self, patient: Patient) -> bool:
        """Add a patient to the database"""
        if patient.patient_id in self.patients:
            return False
        self.patients[patient.patient_id] = patient
        return True

    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """Retrieve a patient by ID"""
        return self.patients.get(patient_id)

    def update_patient(self, patient: Patient) -> bool:
        """Update a patient record"""
        if patient.patient_id not in self.patients:
            return False
        self.patients[patient.patient_id] = patient
        return True

    def delete_patient(self, patient_id: str) -> bool:
        """Delete a patient from the database"""
        if patient_id in self.patients:
            del self.patients[patient_id]
            return True
        return False

    def search_patients(self, query: str) -> List[Patient]:
        """Search patients by name, owner name, or patient ID"""
        query_lower = query.lower()
        results = []
        for patient in self.patients.values():
            if (query_lower in patient.name.lower() or
                query_lower in patient.owner_name.lower() or
                query_lower in patient.patient_id.lower()):
                results.append(patient)
        return results

    def get_all_patients(self) -> List[Patient]:
        """Get all patients"""
        return list(self.patients.values())

    def get_patients_by_species(self, species: str) -> List[Patient]:
        """Get all patients of a specific species"""
        return [p for p in self.patients.values() if p.species.lower() == species.lower()]
