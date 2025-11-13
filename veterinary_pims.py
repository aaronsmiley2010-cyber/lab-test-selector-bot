"""
Veterinary PIMS (Practice Information Management System) Routes
Combines traditional interface with AI-powered features
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import uuid

from models import Patient, PatientDatabase
from ai_veterinary import VeterinaryAIAssistant

# Create Blueprint for PIMS routes
pims_bp = Blueprint('pims', __name__, url_prefix='/pims')

# Initialize database and AI assistant
patient_db = PatientDatabase()
ai_assistant = VeterinaryAIAssistant()


# ==================== Traditional PIMS Routes ====================

@pims_bp.route('/')
def index():
    """Main PIMS dashboard"""
    patients = patient_db.get_all_patients()
    return render_template('pims/dashboard.html', patients=patients)


@pims_bp.route('/patient/new', methods=['GET', 'POST'])
def new_patient():
    """Create new patient profile"""
    if request.method == 'POST':
        # Generate unique patient ID
        patient_id = f"P{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"

        # Create patient object
        patient = Patient(
            patient_id=patient_id,
            name=request.form.get('name'),
            species=request.form.get('species'),
            breed=request.form.get('breed'),
            owner_name=request.form.get('owner_name'),
            owner_contact=request.form.get('owner_contact'),
            date_of_birth=request.form.get('date_of_birth'),
            gender=request.form.get('gender'),
            weight=float(request.form.get('weight', 0)),
            microchip_id=request.form.get('microchip_id')
        )

        # Add allergies if provided
        allergies = request.form.get('allergies', '').split(',')
        for allergy in allergies:
            if allergy.strip():
                patient.add_allergy(allergy.strip())

        # Add to database
        patient_db.add_patient(patient)

        # Run initial AI assessment
        ai_assessment = ai_assistant.assess_health_risks(patient.to_dict())
        patient.set_ai_risk_assessment(ai_assessment)

        # Generate preventive care plan
        preventive_care = ai_assistant.generate_preventive_care_plan(patient.to_dict())
        for recommendation in preventive_care:
            patient.add_ai_recommendation(recommendation)

        patient_db.update_patient(patient)

        return redirect(url_for('pims.view_patient', patient_id=patient_id))

    return render_template('pims/new_patient.html')


@pims_bp.route('/patient/<patient_id>')
def view_patient(patient_id):
    """View patient profile with traditional and AI data"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return "Patient not found", 404

    return render_template('pims/patient_profile.html', patient=patient)


@pims_bp.route('/patient/<patient_id>/edit', methods=['GET', 'POST'])
def edit_patient(patient_id):
    """Edit patient information"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return "Patient not found", 404

    if request.method == 'POST':
        # Update basic information
        patient.name = request.form.get('name', patient.name)
        patient.breed = request.form.get('breed', patient.breed)
        patient.owner_name = request.form.get('owner_name', patient.owner_name)
        patient.owner_contact = request.form.get('owner_contact', patient.owner_contact)
        patient.weight = float(request.form.get('weight', patient.weight))
        patient.microchip_id = request.form.get('microchip_id', patient.microchip_id)

        patient_db.update_patient(patient)
        return redirect(url_for('pims.view_patient', patient_id=patient_id))

    return render_template('pims/edit_patient.html', patient=patient)


@pims_bp.route('/patient/<patient_id>/medical-record', methods=['POST'])
def add_medical_record(patient_id):
    """Add medical record to patient"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    patient.add_medical_record(
        date=request.form.get('date', datetime.now().strftime('%Y-%m-%d')),
        diagnosis=request.form.get('diagnosis'),
        treatment=request.form.get('treatment'),
        veterinarian=request.form.get('veterinarian'),
        notes=request.form.get('notes', '')
    )

    patient_db.update_patient(patient)
    return redirect(url_for('pims.view_patient', patient_id=patient_id))


@pims_bp.route('/patient/<patient_id>/vaccination', methods=['POST'])
def add_vaccination(patient_id):
    """Add vaccination record"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    patient.add_vaccination(
        vaccine_name=request.form.get('vaccine_name'),
        date_administered=request.form.get('date_administered'),
        due_date=request.form.get('due_date'),
        veterinarian=request.form.get('veterinarian'),
        batch_number=request.form.get('batch_number', '')
    )

    patient_db.update_patient(patient)
    return redirect(url_for('pims.view_patient', patient_id=patient_id))


@pims_bp.route('/patient/<patient_id>/medication', methods=['POST'])
def add_medication(patient_id):
    """Add medication to patient"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    patient.add_medication(
        medication_name=request.form.get('medication_name'),
        dosage=request.form.get('dosage'),
        frequency=request.form.get('frequency'),
        start_date=request.form.get('start_date'),
        end_date=request.form.get('end_date') or None,
        prescribing_vet=request.form.get('prescribing_vet')
    )

    patient_db.update_patient(patient)
    return redirect(url_for('pims.view_patient', patient_id=patient_id))


@pims_bp.route('/search')
def search_patients():
    """Search for patients"""
    query = request.args.get('q', '')
    if query:
        results = patient_db.search_patients(query)
    else:
        results = patient_db.get_all_patients()

    return render_template('pims/search_results.html', patients=results, query=query)


# ==================== AI-Powered Routes ====================

@pims_bp.route('/ai/symptom-analyzer')
def symptom_analyzer():
    """AI symptom analyzer interface"""
    return render_template('pims/ai_symptom_analyzer.html')


@pims_bp.route('/ai/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    """Analyze symptoms using AI"""
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    species = data.get('species', 'dog')

    analysis = ai_assistant.analyze_symptoms(symptoms, species)
    return jsonify(analysis)


@pims_bp.route('/patient/<patient_id>/ai/risk-assessment', methods=['POST'])
def get_risk_assessment(patient_id):
    """Get AI risk assessment for patient"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    risk_assessment = ai_assistant.assess_health_risks(patient.to_dict())
    patient.set_ai_risk_assessment(risk_assessment)
    patient_db.update_patient(patient)

    return jsonify(risk_assessment)


@pims_bp.route('/patient/<patient_id>/ai/preventive-care', methods=['POST'])
def generate_preventive_care(patient_id):
    """Generate AI preventive care recommendations"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    recommendations = ai_assistant.generate_preventive_care_plan(patient.to_dict())

    # Store recommendations
    patient.ai_preventive_care_recommendations = recommendations
    patient_db.update_patient(patient)

    return jsonify(recommendations)


@pims_bp.route('/patient/<patient_id>/ai/health-trends', methods=['POST'])
def predict_health_trends(patient_id):
    """Predict health trends using AI"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    trends = ai_assistant.predict_health_trends(patient.to_dict())
    patient.set_health_trends(trends)
    patient_db.update_patient(patient)

    return jsonify(trends)


@pims_bp.route('/ai/triage', methods=['POST'])
def smart_triage():
    """AI-powered triage system"""
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    vitals = data.get('vitals', {})
    species = data.get('species', 'dog')

    triage_result = ai_assistant.smart_triage(symptoms, vitals, species)
    return jsonify(triage_result)


# ==================== API Routes (for external integrations) ====================

@pims_bp.route('/api/patients', methods=['GET'])
def api_get_patients():
    """API: Get all patients"""
    patients = patient_db.get_all_patients()
    return jsonify([p.to_dict() for p in patients])


@pims_bp.route('/api/patient/<patient_id>', methods=['GET'])
def api_get_patient(patient_id):
    """API: Get specific patient"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    return jsonify(patient.to_dict())


@pims_bp.route('/api/patient', methods=['POST'])
def api_create_patient():
    """API: Create new patient"""
    data = request.get_json()

    patient_id = f"P{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"

    patient = Patient(
        patient_id=patient_id,
        name=data.get('name'),
        species=data.get('species'),
        breed=data.get('breed'),
        owner_name=data.get('owner_name'),
        owner_contact=data.get('owner_contact'),
        date_of_birth=data.get('date_of_birth'),
        gender=data.get('gender'),
        weight=float(data.get('weight', 0)),
        microchip_id=data.get('microchip_id')
    )

    patient_db.add_patient(patient)

    return jsonify(patient.to_dict()), 201


@pims_bp.route('/api/patient/<patient_id>', methods=['PUT'])
def api_update_patient(patient_id):
    """API: Update patient"""
    patient = patient_db.get_patient(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    data = request.get_json()

    # Update fields
    for field in ['name', 'breed', 'owner_name', 'owner_contact', 'weight', 'microchip_id']:
        if field in data:
            setattr(patient, field, data[field])

    patient_db.update_patient(patient)

    return jsonify(patient.to_dict())


@pims_bp.route('/api/patient/<patient_id>', methods=['DELETE'])
def api_delete_patient(patient_id):
    """API: Delete patient"""
    if patient_db.delete_patient(patient_id):
        return jsonify({"message": "Patient deleted successfully"})
    return jsonify({"error": "Patient not found"}), 404


# ==================== Statistics and Reports ====================

@pims_bp.route('/reports/dashboard')
def reports_dashboard():
    """Analytics dashboard"""
    patients = patient_db.get_all_patients()

    # Calculate statistics
    total_patients = len(patients)
    species_breakdown = {}
    high_risk_patients = 0

    for patient in patients:
        # Species count
        species = patient.species
        species_breakdown[species] = species_breakdown.get(species, 0) + 1

        # High risk count
        if patient.ai_risk_assessment:
            risk_level = patient.ai_risk_assessment.get('risk_level', 'low')
            if risk_level == 'high':
                high_risk_patients += 1

    stats = {
        'total_patients': total_patients,
        'species_breakdown': species_breakdown,
        'high_risk_patients': high_risk_patients
    }

    return render_template('pims/reports_dashboard.html', stats=stats, patients=patients)
