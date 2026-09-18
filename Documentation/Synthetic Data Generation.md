# Healthcare Claims Intelligence

## Synthetic Data Generation

### Purpose

This document describes how the clean synthetic Healthcare Claims Intelligence datasets will be manufactured from the approved data model and business rules. Generation logic is supporting methodology and does not add fields to the core analytical tables unless explicitly stated.

## Target Dataset Size

- Members: approximately 50,000 unique members.
- Providers: approximately 2,500 unique providers.
- Claims: approximately 500,000 service lines.
- Approximately 90% of members have at least one claim and approximately 10% have no claims.

## Observation Period

- Enrollment and claims activity cover January 1, 2021 through December 31, 2025.
- Member age is calculated using December 31, 2025 as the reference date.

## Member Generation

### Demographics

- Gender distribution target: approximately 51% Female and 49% Male.
- Age distribution targets: 0-17 15%, 18-34 18%, 35-49 20%, 50-64 22%, 65-79 20%, and 80+ 5%.
- `date_of_birth` is generated from the target age distribution.
- Members may reside in any of the 50 U.S. states.
- State distribution approximately follows U.S. population distribution.

### Plan Type

- Approximate distribution: Commercial PPO 40%, Commercial HMO 35%, Medicare Advantage PPO 15%, and Medicare Advantage HMO 10%.
- Approximately 95% of Medicare Advantage members are age 65 or older, with approximately 5% under age 65.

### Enrollment

- Approximately 90% of members are Active and 10% are Terminated.
- Enrollment dates are weighted somewhat toward more recent years while retaining meaningful long-tenured membership.

## Provider Generation

- Provider type distribution target: Physician 50%, Clinic 20%, Hospital 10%, Urgent Care 5%, Ambulatory Surgical Center 5%, Laboratory 5%, and Imaging Center 5%.
- Physician Primary Care is more common than the other physician specialties rather than specialties being equally weighted.
- Providers are distributed across all 50 states approximately in proportion to member geography.
- Network distribution target: approximately 85% In-Network and 15% Out-of-Network.
- Network status is generated independently of provider type.

## Reference Data

### Procedure Reference

- `procedure_reference.csv` contains `procedure_code`, `procedure_description`, `service_category`, and `baseline_allowed_amount`.
- Approximately 75 curated CPT/HCPCS-style procedure codes and descriptions are used.
- `baseline_allowed_amount` is generation metadata and is not a Claims field.
- Procedure counts by service category: Primary Care 8, Specialist Visit 8, Preventive Care 6, Emergency 6, Urgent Care 5, Laboratory 10, Imaging 8, Outpatient Procedure 10, Inpatient 6, and Therapy 8.
- Procedure utilization is not uniform. Routine services are generally more frequent than higher-intensity services.

### Diagnosis Reference

- `diagnosis_reference.csv` contains `diagnosis_code`, `diagnosis_description`, and `diagnosis_group`.
- Approximately 50 curated ICD-10-CM diagnosis codes and descriptions are used.
- `diagnosis_group` is generation metadata and is not a Claims field.
- Diagnosis counts by group: Hypertension / Cardiovascular 5, Diabetes / Endocrine 5, Respiratory 5, Musculoskeletal 5, Gastrointestinal 5, Mental / Behavioral Health 5, Infectious Disease 5, Injury 5, Neurological 5, and General / Symptoms 5.

## Diagnosis-to-Service Generation Logic

- Hypertension / Cardiovascular primarily influences Primary Care, Specialist Visit, Laboratory, Imaging, and Inpatient services.
- Diabetes / Endocrine primarily influences Primary Care, Specialist Visit, Laboratory, and Preventive Care.
- Respiratory primarily influences Primary Care, Urgent Care, Emergency, Laboratory, and Imaging.
- Musculoskeletal primarily influences Primary Care, Specialist Visit, Imaging, Outpatient Procedure, and Therapy.
- Gastrointestinal primarily influences Primary Care, Specialist Visit, Laboratory, Imaging, Outpatient Procedure, and Emergency services.
- Mental / Behavioral Health primarily influences Primary Care and Specialist Visit services.
- Infectious Disease primarily influences Primary Care, Urgent Care, Emergency, and Laboratory services.
- Injury primarily influences Urgent Care, Emergency, Imaging, Outpatient Procedure, and Therapy.
- Neurological primarily influences Primary Care, Specialist Visit, Imaging, and Emergency services.
- General / Symptoms primarily influences Primary Care, Preventive Care, Urgent Care, Laboratory, and Imaging.
- Diagnosis-to-service mappings define valid service categories available to the generator. Weighted probabilities are used within valid choices so common combinations occur more frequently without allowing incompatible combinations.

## Utilization and Claim Volume

- Member utilization is intentionally right-skewed.
- Generation-only utilization tendencies are approximately: No Utilization 10%, Low 50%, Moderate 30%, High 8%, and Very High 2%.
- Utilization tendency is not stored as a field in Members or Claims.
- Member age influences the probability of utilization level and service mix without acting as a hard rule.
- Approximate service-line distribution per claim: 1 line 60%, 2 lines 25%, 3 lines 10%, and 4+ lines 5%.
- The generation process is calibrated to land near 500,000 service lines rather than forcing an exact row count.

## Service and Provider Generation

- Generation follows the sequence: member characteristics, diagnosis group, weighted valid service category, procedure from that service category, compatible provider specialty/type, and compatible place of service.
- Service category mappings are implemented as weighted lookup structures. Procedure selection is restricted to the selected service category. Provider specialty/type and place of service are then restricted to compatible choices for that service.
- Approximately 90% of services occur with a provider in the member's state and approximately 10% occur out of state.

## Allowed Amount Generation

- Each procedure has a baseline allowed amount in `procedure_reference.csv`.
- Allowed amounts normally vary approximately ±20% around the procedure-specific baseline, with most values remaining relatively close to baseline.
- Out-of-network services receive an upward cost tendency of approximately 20% on average.
- Variation is retained so in-network and out-of-network allowed amounts can overlap.
- Generation sequence: procedure baseline, natural cost variation, network adjustment, final `allowed_amount`.
- Final `allowed_amount` must remain greater than zero.

## Generation Validation

- Approximate distribution targets are checked using reasonable tolerance rather than exact equality.
- Structural and integrity rules are validated separately and require zero invalid records in the clean synthetic datasets.

## Generation Mappings

The following mappings constrain synthetic claim generation to clinically and operationally plausible combinations. They are generation logic, not fields added to the analytical tables.

```python
DIAGNOSIS_TO_SERVICE = {
    "Hypertension / Cardiovascular": {
        "Primary Care": 0.30,
        "Specialist Visit": 0.25,
        "Laboratory": 0.20,
        "Imaging": 0.10,
        "Emergency": 0.05,
        "Inpatient": 0.05,
        "Preventive Care": 0.05,
    },
    "Diabetes / Endocrine": {
        "Primary Care": 0.35,
        "Specialist Visit": 0.20,
        "Laboratory": 0.30,
        "Preventive Care": 0.10,
        "Emergency": 0.03,
        "Inpatient": 0.02,
    },
    "Respiratory": {
        "Primary Care": 0.35,
        "Urgent Care": 0.20,
        "Laboratory": 0.10,
        "Imaging": 0.10,
        "Specialist Visit": 0.10,
        "Emergency": 0.10,
        "Inpatient": 0.05,
    },
    "Musculoskeletal": {
        "Primary Care": 0.15,
        "Specialist Visit": 0.20,
        "Imaging": 0.20,
        "Outpatient Procedure": 0.15,
        "Therapy": 0.25,
        "Urgent Care": 0.05,
    },
    "Gastrointestinal": {
        "Primary Care": 0.25,
        "Specialist Visit": 0.20,
        "Outpatient Procedure": 0.20,
        "Laboratory": 0.10,
        "Imaging": 0.10,
        "Urgent Care": 0.05,
        "Emergency": 0.07,
        "Inpatient": 0.03,
    },
    "Mental / Behavioral Health": {
        "Primary Care": 0.45,
        "Specialist Visit": 0.45,
        "Laboratory": 0.05,
        "Emergency": 0.05,
    },
    "Infectious Disease": {
        "Primary Care": 0.35,
        "Urgent Care": 0.25,
        "Laboratory": 0.20,
        "Emergency": 0.10,
        "Imaging": 0.05,
        "Inpatient": 0.05,
    },
    "Injury": {
        "Urgent Care": 0.30,
        "Emergency": 0.25,
        "Imaging": 0.20,
        "Primary Care": 0.10,
        "Outpatient Procedure": 0.05,
        "Specialist Visit": 0.05,
        "Therapy": 0.05,
    },
    "Neurological": {
        "Primary Care": 0.20,
        "Specialist Visit": 0.30,
        "Imaging": 0.20,
        "Laboratory": 0.05,
        "Emergency": 0.10,
        "Outpatient Procedure": 0.05,
        "Therapy": 0.10,
    },
    "General / Symptoms": {
        "Primary Care": 0.40,
        "Preventive Care": 0.15,
        "Laboratory": 0.15,
        "Urgent Care": 0.10,
        "Imaging": 0.05,
        "Specialist Visit": 0.05,
        "Emergency": 0.05,
        "Therapy": 0.05,
    },
}

SERVICE_TO_PROVIDER_SPECIALTY = {
    "Primary Care": ["Primary Care", "Family Medicine", "Internal Medicine"],
    "Specialist Visit": [
        "Cardiology",
        "Endocrinology",
        "Pulmonology",
        "Orthopedics",
        "Gastroenterology",
        "Neurology",
        "Ophthalmology",
        "Behavioral Health",
    ],
    "Preventive Care": ["Primary Care", "Family Medicine", "Internal Medicine"],
    "Emergency": ["Emergency Medicine"],
    "Urgent Care": ["Urgent Care", "Family Medicine"],
    "Laboratory": ["Laboratory"],
    "Imaging": ["Radiology"],
    "Outpatient Procedure": [
        "Gastroenterology",
        "Orthopedics",
        "Ophthalmology",
        "General Surgery",
        "Dermatology",
    ],
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
    "Outpatient Procedure": [
        "Ambulatory Surgical Center",
        "Hospital",
        "Physician",
    ],
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
    "Outpatient Procedure": [
        "Ambulatory Surgical Center",
        "Outpatient Hospital",
        "Office",
    ],
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

    diagnosis_groups = set(
        diagnosis_reference["diagnosis_group"].unique()
    )

    procedure_categories = set(
        procedure_reference["service_category"].unique()
    )

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