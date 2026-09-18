# Healthcare Claims Intelligence

## Business Rules

### Purpose

This document defines the rules that records in the synthetic Healthcare Claims Intelligence dataset must satisfy. Distribution targets and generation methods are documented separately in Synthetic Data Generation.

## Member Business Rules

### Enrollment

- Enrollment activity covers January 1, 2021 through December 31, 2025.
- Active members must have a null `termination_date`.
- Terminated members must have a populated `termination_date`.
- `termination_date` must occur after `enrollment_date`.
- Terminated members must have at least 30 days between enrollment and termination.

### Plan Type

- Valid plan types are Commercial PPO, Commercial HMO, Medicare Advantage PPO, and Medicare Advantage HMO.
- Medicare Advantage membership is primarily associated with members age 65 or older, while a small under-65 population is permitted.

### Member Identification

- `member_id` must be unique and non-null.
- `member_id` follows the `MBR######` format.

## Provider Business Rules

### Provider Type and Specialty

- Valid provider types are Physician, Clinic, Hospital, Urgent Care, Ambulatory Surgical Center, Laboratory, and Imaging Center.
- Physician specialties: Primary Care, Cardiology, Orthopedics, Dermatology, OB/GYN, Pediatrics, Gastroenterology, Neurology, Pulmonology, and Endocrinology.
- Clinic specialties: Primary Care, Multi-Specialty, Women's Health, and Pediatrics.
- Hospital specialty: General Acute Care.
- Urgent Care specialty: Urgent Care.
- Ambulatory Surgical Center specialty: Ambulatory Surgery.
- Laboratory specialty: Clinical Laboratory.
- Imaging Center specialty: Diagnostic Imaging.
- `specialty` must be logically appropriate for `provider_type`.

### Provider Identification

- `provider_id` must be unique and non-null.
- `provider_id` follows the `PRV######` format.
- Provider names are fictional and appropriate for provider type.
- Provider names are not required to be unique.

### Network

- Valid network statuses are In-Network and Out-of-Network.

## Claims Business Rules

### Observation Period and Service Dates

- Claims cover January 1, 2021 through December 31, 2025.
- `service_date` must fall within the observation period.
- `service_date` must occur on or after the member's `enrollment_date`.
- For terminated members, `service_date` must occur on or before `termination_date`.

### Claim Identification

- `claim_id` follows the `CLM########` format.
- A `claim_id` may repeat across multiple service lines.
- `service_line_number` begins at 1 and increments sequentially within each claim.
- `claim_id + service_line_number` must be unique.

### Referential Integrity

- Every Claims `member_id` must exist in Members.
- Every Claims `provider_id` must exist in Providers.
- Orphan claim records are not valid in the clean synthetic dataset.

### Procedures and Diagnoses

- Each `procedure_code` must map to a fixed `procedure_description` and `service_category`.
- Valid service categories are Primary Care, Specialist Visit, Preventive Care, Emergency, Urgent Care, Laboratory, Imaging, Outpatient Procedure, Inpatient, and Therapy.
- Each `diagnosis_code` must map to a fixed `diagnosis_description`.
- Diagnoses and procedures must be assigned using logical relationships rather than independently.

### Place of Service and Provider Compatibility

- Valid `place_of_service` values are Office, Inpatient Hospital, Outpatient Hospital, Emergency Department, Urgent Care, Ambulatory Surgical Center, Laboratory, and Imaging Center.
- Primary Care is compatible with Physicians and Clinics, primarily in Office settings.
- Specialist Visit is compatible with Physicians and Clinics in Office or Outpatient Hospital settings.
- Emergency is compatible with Hospitals in Emergency Department settings.
- Urgent Care is compatible with Urgent Care providers in Urgent Care settings.
- Inpatient is compatible with Hospitals in Inpatient Hospital settings.
- Outpatient Procedure is compatible with Hospitals, Ambulatory Surgical Centers, and Physicians in Outpatient Hospital, Ambulatory Surgical Center, or Office settings.
- Imaging is compatible with Imaging Centers and Hospitals in Imaging Center or Outpatient Hospital settings.
- Laboratory services are compatible with Laboratories and Hospitals in Laboratory or Outpatient Hospital settings.
- Therapy is compatible with Clinics in Office or Outpatient Hospital settings.
- Preventive Care is compatible with Physicians and Clinics, primarily in Office settings.

### Allowed Amount

- `allowed_amount` must be greater than zero.
- Expected allowed cost depends primarily on the procedure.
- Out-of-network services may have higher allowed amounts than comparable in-network services, but overlap is permitted.

## Validation Principle

- Structural and integrity rules require zero tolerance for invalid records.
- Approximate population and distribution targets are evaluated using reasonable tolerance rather than exact equality.