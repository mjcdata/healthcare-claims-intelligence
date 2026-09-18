# Healthcare Claims Intelligence

## Data Dictionary

## Members

| Field | Data Type | Description | Key / Relationship | Nullable |
|---|---|---|---|---|
| `member_id` | VARCHAR | Unique identifier for a member. | Primary Key | No |
| `date_of_birth` | DATE | Member date of birth. | | No |
| `gender` | VARCHAR | Member gender. | | No |
| `state` | VARCHAR | Two-character state associated with the member. | | No |
| `plan_type` | VARCHAR | Member health plan type. | | No |
| `enrollment_date` | DATE | Date the member's enrollment period begins. | | No |
| `enrollment_status` | VARCHAR | Current enrollment status: Active or Terminated. | | No |
| `termination_date` | DATE | Date coverage terminated. Null for active members. | | Yes |

## Providers

| Field | Data Type | Description | Key / Relationship | Nullable |
|---|---|---|---|---|
| `provider_id` | VARCHAR | Unique identifier for a provider. | Primary Key | No |
| `provider_name` | VARCHAR | Synthetic provider or organization name. | | No |
| `provider_type` | VARCHAR | Provider organizational or practitioner type. | | No |
| `specialty` | VARCHAR | Provider specialty associated with the provider type. | | No |
| `state` | VARCHAR | Two-character state where the provider is located. | | No |
| `network_status` | VARCHAR | Indicates whether the provider is In-Network or Out-of-Network. | | No |

## Claims

| Field | Data Type | Description | Key / Relationship | Nullable |
|---|---|---|---|---|
| `claim_id` | VARCHAR | Identifier for the claim. A claim can contain multiple service lines. | Composite Key with `service_line_number` | No |
| `service_line_number` | INTEGER | Sequential service-line number within a claim. | Composite Key with `claim_id` | No |
| `member_id` | VARCHAR | Member associated with the claim service line. | Foreign Key → `Members.member_id` | No |
| `provider_id` | VARCHAR | Provider associated with the claim service line. | Foreign Key → `Providers.provider_id` | No |
| `service_date` | DATE | Date the healthcare service was provided. | | No |
| `procedure_code` | VARCHAR | Procedure or service code associated with the service line. | Foreign Key → `Procedure Reference.procedure_code` | No |
| `procedure_description` | VARCHAR | Description of the procedure or service. | | No |
| `diagnosis_code` | VARCHAR | Diagnosis code associated with the service line. | Foreign Key → `Diagnosis Reference.diagnosis_code` | No |
| `diagnosis_description` | VARCHAR | Description of the diagnosis. | | No |
| `place_of_service` | VARCHAR | Setting where the healthcare service occurred. | | No |
| `service_category` | VARCHAR | High-level category of healthcare service. | | No |
| `allowed_amount` | DECIMAL | Synthetic finalized allowed amount for the service line. | | No |

## Procedure Reference

| Field | Data Type | Description | Key / Relationship | Nullable |
|---|---|---|---|---|
| `procedure_code` | VARCHAR | Synthetic CPT/HCPCS-style procedure or service code. | Primary Key | No |
| `procedure_description` | VARCHAR | Description of the procedure or service. | | No |
| `service_category` | VARCHAR | High-level service category used in claims generation. | | No |
| `baseline_allowed_amount` | DECIMAL | Synthetic baseline allowed amount used to generate claim-level allowed amounts. | | No |

## Diagnosis Reference

| Field | Data Type | Description | Key / Relationship | Nullable |
|---|---|---|---|---|
| `diagnosis_code` | VARCHAR | ICD-10-CM diagnosis code used in synthetic claims generation. | Primary Key | No |
| `diagnosis_description` | VARCHAR | Description of the diagnosis. | | No |
| `diagnosis_group` | VARCHAR | Higher-level diagnosis grouping used in claims generation. | | No |