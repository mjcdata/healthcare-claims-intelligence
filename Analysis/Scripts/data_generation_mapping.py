"""Generation mappings for the Healthcare Claims Intelligence project.

These mappings constrain synthetic claim generation to clinically and
operationally plausible combinations. They are generation logic, not fields
added to the analytical tables.
"""

DIAGNOSIS_TO_SERVICE = {
    "Hypertension / Cardiovascular": {
        "Primary Care": 0.30, "Specialist Visit": 0.25, "Laboratory": 0.20,
        "Imaging": 0.10, "Emergency": 0.05, "Inpatient": 0.05,
        "Preventive Care": 0.05,
    },
    "Diabetes / Endocrine": {
        "Primary Care": 0.35, "Specialist Visit": 0.20, "Laboratory": 0.30,
        "Preventive Care": 0.10, "Emergency": 0.03, "Inpatient": 0.02,
    },
    "Respiratory": {
        "Primary Care": 0.35, "Urgent Care": 0.20, "Laboratory": 0.10,
        "Imaging": 0.10, "Specialist Visit": 0.10, "Emergency": 0.10,
        "Inpatient": 0.05,
    },
    "Musculoskeletal": {
        "Primary Care": 0.15, "Specialist Visit": 0.20, "Imaging": 0.20,
        "Outpatient Procedure": 0.15, "Therapy": 0.25, "Urgent Care": 0.05,
    },
    "Gastrointestinal": {
        "Primary Care": 0.25, "Specialist Visit": 0.20,
        "Outpatient Procedure": 0.20, "Laboratory": 0.10, "Imaging": 0.10,
        "Urgent Care": 0.05, "Emergency": 0.07, "Inpatient": 0.03,
    },
    "Mental / Behavioral Health": {
        "Primary Care": 0.45, "Specialist Visit": 0.45,
        "Laboratory": 0.05, "Emergency": 0.05,
    },
    "Infectious Disease": {
        "Primary Care": 0.35, "Urgent Care": 0.25, "Laboratory": 0.20,
        "Emergency": 0.10, "Imaging": 0.05, "Inpatient": 0.05,
    },
    "Injury": {
        "Urgent Care": 0.30, "Emergency": 0.25, "Imaging": 0.20,
        "Primary Care": 0.10, "Outpatient Procedure": 0.05,
        "Specialist Visit": 0.05, "Therapy": 0.05,
    },
    "Neurological": {
        "Primary Care": 0.20, "Specialist Visit": 0.30, "Imaging": 0.20,
        "Laboratory": 0.05, "Emergency": 0.10,
        "Outpatient Procedure": 0.05, "Therapy": 0.10,
    },
    "General / Symptoms": {
        "Primary Care": 0.40, "Preventive Care": 0.15, "Laboratory": 0.15,
        "Urgent Care": 0.10, "Imaging": 0.05, "Specialist Visit": 0.05,
        "Emergency": 0.05, "Therapy": 0.05,
    },
}

SERVICE_TO_PROVIDER_SPECIALTY = {
    "Primary Care": ["Primary Care", "Family Medicine", "Internal Medicine"],
    "Specialist Visit": ["Cardiology", "Endocrinology", "Pulmonology",
                         "Orthopedics", "Gastroenterology", "Neurology",
                         "Ophthalmology", "Behavioral Health"],
    "Preventive Care": ["Primary Care", "Family Medicine", "Internal Medicine"],
    "Emergency": ["Emergency Medicine"],
    "Urgent Care": ["Urgent Care", "Family Medicine"],
    "Laboratory": ["Laboratory"],
    "Imaging": ["Radiology"],
    "Outpatient Procedure": ["Gastroenterology", "Orthopedics", "Ophthalmology",
                             "General Surgery", "Dermatology"],
    "Inpatient": ["Hospitalist", "Internal Medicine"],
    "Therapy": ["Physical Therapy"],
}

SERVICE_TO_PROVIDER_TYPE = {
    "Primary Care": ["Physician", "Clinic"],
    "Specialist Visit": ["Physician", "Clinic"],
    "Preventive Care": ["Physician", "Clinic"],
    "Emergency": ["Hospital"],
    "Urgent Care": ["Urgent Care"],
    "Laboratory": ["Laboratory"],
    "Imaging": ["Imaging Center", "Hospital"],
    "Outpatient Procedure": ["Ambulatory Surgical Center", "Hospital", "Physician"],
    "Inpatient": ["Hospital"],
    "Therapy": ["Clinic"],
}

SERVICE_TO_POS = {
    "Primary Care": ["Office"],
    "Specialist Visit": ["Office"],
    "Preventive Care": ["Office"],
    "Emergency": ["Emergency Room - Hospital"],
    "Urgent Care": ["Urgent Care Facility"],
    "Laboratory": ["Independent Laboratory", "Office"],
    "Imaging": ["Independent Clinic", "Outpatient Hospital"],
    "Outpatient Procedure": ["Ambulatory Surgical Center", "Outpatient Hospital", "Office"],
    "Inpatient": ["Inpatient Hospital"],
    "Therapy": ["Office", "Outpatient Hospital"],
}


def build_service_to_procedures(procedure_reference):
    """Derive service-to-procedure choices from procedure_reference.csv."""
    return (
        procedure_reference.groupby("service_category")["procedure_code"]
        .apply(list)
        .to_dict()
    )


def validate_mappings(diagnosis_reference, procedure_reference):
    """Validate mapping coverage and probability totals before generation."""
    diagnosis_groups = set(diagnosis_reference["diagnosis_group"].unique())
    procedure_categories = set(procedure_reference["service_category"].unique())

    assert diagnosis_groups == set(DIAGNOSIS_TO_SERVICE), (
        "Diagnosis mapping groups do not match diagnosis_reference.csv"
    )
    assert procedure_categories == set(SERVICE_TO_PROVIDER_SPECIALTY), (
        "Provider-specialty mapping does not cover all procedure service categories"
    )
    assert procedure_categories == set(SERVICE_TO_PROVIDER_TYPE), (
        "Provider-type mapping does not cover all procedure service categories"
    )
    assert procedure_categories == set(SERVICE_TO_POS), (
        "POS mapping does not cover all procedure service categories"
    )

    for group, weights in DIAGNOSIS_TO_SERVICE.items():
        assert set(weights).issubset(procedure_categories), (
            f"{group} contains an unknown service category"
        )
        assert abs(sum(weights.values()) - 1.0) < 1e-9, (
            f"{group} service weights must sum to 1.0"
        )

    return True
