# Healthcare Claims Intelligence

## Data Model

### Overview

The Healthcare Claims Intelligence project uses a three table analytical model designed to support healthcare cost and utilization analysis. The model consists of Claims, Members, and Providers. Claims serves as the fact table, while Members and Providers serve as dimension tables.

The MVP focuses on finalized healthcare claims and does not model claim adjudication. Allowed amount is used as the primary measure of healthcare cost.

## Claims

### Purpose

The Claims table represents healthcare services utilized by members and delivered by providers.

### Grain

One row represents one service line within a healthcare claim. A claim can contain multiple service lines.

### Key

The combination of `claim_id` and `service_line_number` uniquely identifies a service line.

### Fields

- `claim_id`: Identifies the overall healthcare claim.
- `service_line_number`: Identifies the individual service line within a claim.
- `member_id`: Links the service line to the member who received care.
- `provider_id`: Links the service line to the provider associated with the service.
- `service_date`: Date the healthcare service occurred.
- `procedure_code`: Standardized code identifying the healthcare service performed.
- `procedure_description`: Readable description of the procedure code.
- `diagnosis_code`: Standardized code identifying the diagnosis associated with the service.
- `diagnosis_description`: Readable description of the diagnosis code.
- `place_of_service`: Identifies where the healthcare service was delivered.
- `service_category`: Groups procedures into broader categories for cost and utilization analysis.
- `allowed_amount`: Finalized cost measure associated with the service line.

## Members

### Purpose

The Members table contains attributes used to describe and analyze the health plan's member population.

### Grain

One row represents one member.

### Key

`member_id` uniquely identifies a member.

### Fields

- `member_id`: Unique identifier for the member.
- `date_of_birth`: Member's date of birth. Age can be derived when needed for analysis.
- `gender`: Member gender.
- `state`: Member's state, supporting geographic analysis and state-level mapping.
- `plan_type`: Identifies the member's health plan type.
- `enrollment_date`: Date the member enrolled in the health plan.
- `enrollment_status`: Indicates the member's enrollment status.
- `termination_date`: Date the member's health plan coverage ended. This field is null for active members and populated for terminated members.

## Providers

### Purpose

The Providers table contains attributes describing healthcare providers associated with claim service lines.

### Grain

One row represents one provider.

### Key

`provider_id` uniquely identifies a provider.

### Fields

- `provider_id`: Unique identifier for the provider.
- `provider_name`: Readable provider name.
- `provider_type`: Identifies the type of provider, such as physician, hospital, or clinic.
- `specialty`: Identifies the provider's healthcare specialty.
- `state`: Provider's state.
- `network_status`: Identifies the provider's network status.

## Data Types

### Claims

- `claim_id`: VARCHAR
- `service_line_number`: INTEGER
- `member_id`: VARCHAR
- `provider_id`: VARCHAR
- `service_date`: DATE
- `procedure_code`: VARCHAR
- `procedure_description`: VARCHAR
- `diagnosis_code`: VARCHAR
- `diagnosis_description`: VARCHAR
- `place_of_service`: VARCHAR
- `service_category`: VARCHAR
- `allowed_amount`: DECIMAL(10,2)

### Members

- `member_id`: VARCHAR
- `date_of_birth`: DATE
- `gender`: VARCHAR
- `state`: VARCHAR
- `plan_type`: VARCHAR
- `enrollment_date`: DATE
- `enrollment_status`: VARCHAR
- `termination_date`: DATE, nullable

### Providers

- `provider_id`: VARCHAR
- `provider_name`: VARCHAR
- `provider_type`: VARCHAR
- `specialty`: VARCHAR
- `state`: VARCHAR
- `network_status`: VARCHAR

## Relationships

### Members to Claims

`Members.member_id` has a one-to-many relationship with `Claims.member_id`. One member can be associated with many claim service lines.

### Providers to Claims

`Providers.provider_id` has a one-to-many relationship with `Claims.provider_id`. One provider can be associated with many claim service lines.

## Analytical Structure

Claims functions as the fact table because it records healthcare service events and contains the measurable cost field, `allowed_amount`. Members and Providers function as dimension tables because they provide descriptive context used to analyze those healthcare services.

## Business Rules

The Data Model retains only the core rules required to define valid table relationships and records. Detailed business rules are maintained in the separate Business Rules document.

- `Claims.member_id` must reference an existing `Members.member_id`.
- `Claims.provider_id` must reference an existing `Providers.provider_id`.
- `claim_id + service_line_number` must uniquely identify each claim service line.
- `service_line_number` begins at 1 and increments sequentially within each claim.
- Claim service dates must fall within the member's applicable enrollment period.
- Active members have a null `termination_date`. Terminated members have a populated `termination_date` after `enrollment_date`.
- `provider_type` and `specialty` must form a valid combination.
- `service_category`, `provider_type`, and `place_of_service` must form a valid combination.
- `procedure_code` must map to its defined `procedure_description` and `service_category`.
- `diagnosis_code` must map to its defined `diagnosis_description`.
- `allowed_amount` must be greater than zero.