# Healthcare Claims Intelligence

## Data Quality & Cleaning Log

| Issue ID | Dataset | Field(s) | Data Quality Dimension | Records Affected | Percent Affected | Status |
|---|---|---|---|---:|---:|---|
| DQ-001 | Members | `enrollment_status`, `termination_date` | Completeness / Conditional requirement | 44,980 | 89.96% | Validated - No Issue |
| DQ-002 | Members | `date_of_birth`, `enrollment_date` | Validity / Business rule | 881 | 1.76% | Resolved |
| DQ-003 | Members | `member_id` | Uniqueness / Completeness | 0 | 0.00% | Validated - No Issue |
| DQ-004 | Providers | `provider_id`; all provider fields | Uniqueness / Completeness | 0 | 0.00% | Validated - No Issue |
| DQ-005 | Providers | `provider_type`, `specialty` | Validity / Business rule | 0 | 0.00% | Validated - No Issue |
| DQ-006 | Claims | `claim_id`, `service_line_number` | Uniqueness / Completeness | 0 | 0.00% | Validated - No Issue |
| DQ-007 | Claims | All 12 claims fields | Completeness | 0 | 0.00% | Validated - No Issue |
| DQ-008 | Claims | `member_id`, `provider_id` | Referential integrity | 0 | 0.00% | Validated - No Issue |
| DQ-009 | Claims | `service_date` | Validity / Date format | 0 | 0.00% | Validated - No Issue |
| DQ-010 | Claims | `service_date`, `enrollment_date`, `termination_date` | Validity / Business rule | 165,200 | 33.04% | Resolved |
| DQ-011 | Claims | `member_id`, `provider_id`, `state` | Validity / Business rule | 476,718 | 95.34% | Resolved |
| DQ-012 | Claims | `allowed_amount`, `provider_id`, `network_status`, `procedure_code` | Validity / Business Rule | 499,996 | 100.00% | Resolved |
| DQ-013 | Claims | `service_date`, `member_id` | Validity / Temporal Pattern | Trend-level finding | N/A | Resolved |
| DQ-014 | Claims | `provider_id`, `service_category`, `place_of_service` | Validity / Business Rule Conformance | 31,686 | 9.52% | Resolved |

## Detailed Findings

### DQ-001: Member Termination Date Completeness

**Dataset:** Members  
**Fields:** `enrollment_status`, `termination_date`  
**Dimension:** Completeness / Conditional requirement  
**Status:** Validated - No Issue

**Profiling Finding**

`termination_date` is null for all 44,980 Active members and populated for all 5,020 Terminated members. The missing values are expected based on enrollment status.

**Business / Analytical Impact**

No data quality issue identified. The null pattern is consistent with the apparent enrollment-status rule.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during member completeness and distribution profiling.

---

### DQ-002: Enrollment Before Date of Birth

**Dataset:** Members  
**Fields:** `date_of_birth`, `enrollment_date`  
**Dimension:** Validity / Business rule  
**Records Affected:** 881 (1.76%)  
**Status:** Resolved

**Profiling Finding**

881 member records have an `enrollment_date` earlier than `date_of_birth`. Initial sample review did not reveal an obvious pattern.

**Business / Analytical Impact**

Invalid enrollment chronology could affect eligibility, age-at-enrollment, and claims eligibility analysis.

**Cleaning Decision**

Set `enrollment_date` equal to `date_of_birth` when `enrollment_date` precedes `date_of_birth`.

**Cleaning Action**

Updated the 881 affected member records by setting `enrollment_date` equal to `date_of_birth`, then revalidated member enrollment chronology and downstream claim eligibility.

**Result / Notes**

All 881 invalid enrollment dates were corrected. Final validation found 0 members enrolled before date of birth. Raw source data remained unchanged.

---

### DQ-003: Member ID Integrity

**Dataset:** Members  
**Field:** `member_id`  
**Dimension:** Uniqueness / Completeness  
**Status:** Validated - No Issue

**Profiling Finding**

50,000 rows contain 50,000 unique member IDs with 0 missing and 0 duplicate IDs. Intended grain of one row per member is confirmed.

**Business / Analytical Impact**

No data quality issue identified. Member primary key integrity is intact.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during member structure profiling.

---

### DQ-004: Provider ID and Field Completeness

**Dataset:** Providers  
**Fields:** `provider_id`; all provider fields  
**Dimension:** Uniqueness / Completeness  
**Status:** Validated - No Issue

**Profiling Finding**

2,500 rows contain 2,500 unique provider IDs with 0 missing and 0 duplicate IDs. No provider fields contain missing values.

**Business / Analytical Impact**

No data quality issue identified. Provider grain and required-field completeness are intact.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during provider profiling.

---

### DQ-005: Provider Type and Specialty Compatibility

**Dataset:** Providers  
**Fields:** `provider_type`, `specialty`  
**Dimension:** Validity / Business rule  
**Status:** Validated - No Issue

**Profiling Finding**

Observed provider type and specialty combinations are internally sensible. No obvious compatibility violations were identified.

**Business / Analytical Impact**

No data quality issue identified for provider type and specialty compatibility.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during provider profiling.

---

### DQ-006: Claims Composite Key Integrity

**Dataset:** Claims  
**Fields:** `claim_id`, `service_line_number`  
**Dimension:** Uniqueness / Completeness  
**Status:** Validated - No Issue

**Profiling Finding**

499,996 service lines contain 0 missing claim IDs, 0 missing service line numbers, and 0 duplicate `claim_id + service_line_number` combinations. Intended service-line grain is confirmed.

**Business / Analytical Impact**

No data quality issue identified. Claims composite key integrity is intact.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during claims profiling.

---

### DQ-007: Claims Completeness

**Dataset:** Claims  
**Fields:** All 12 claims fields  
**Dimension:** Completeness  
**Status:** Validated - No Issue

**Profiling Finding**

No missing values were identified across any of the 12 claims fields.

**Business / Analytical Impact**

No data quality issue identified for claims completeness.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during claims profiling.

---

### DQ-008: Claims Referential Integrity

**Dataset:** Claims  
**Fields:** `member_id`, `provider_id`  
**Dimension:** Referential integrity  
**Status:** Validated - No Issue

**Profiling Finding**

All claim member IDs exist in Members and all claim provider IDs exist in Providers. No orphaned foreign keys were identified.

**Business / Analytical Impact**

No data quality issue identified. Claims relationships to Members and Providers are intact.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during claims profiling.

---

### DQ-009: Service Date Validity

**Dataset:** Claims  
**Field:** `service_date`  
**Dimension:** Validity / Date format  
**Status:** Validated - No Issue

**Profiling Finding**

All service dates are parseable. Observed range is 2021-01-05 through 2025-12-31, with 0 invalid or unparseable values.

**Business / Analytical Impact**

No technical date-format issue identified. Logical enrollment-period validity is tracked separately.

**Cleaning Decision**

No cleaning required.

**Result / Notes**

Confirmed during claims profiling.

---

### DQ-010: Claims Outside Enrollment Periods

**Dataset:** Claims  
**Fields:** `service_date`, `enrollment_date`, `termination_date`  
**Dimension:** Validity / Business rule  
**Records Affected:** 165,200 (33.04%)  
**Status:** Resolved

**Profiling Finding**

165,200 of 499,996 claim service lines fall outside the member enrollment period: 141,273 occur before enrollment and 23,927 occur after termination. Sample review shows violations beyond simple boundary-date differences.

**Business / Analytical Impact**

Claims outside enrollment periods could materially distort utilization, allowed-cost, eligibility, member, and trend analyses.

**Cleaning Decision**

After correcting invalid member enrollment dates, revalidate enrollment eligibility and exclude remaining claim lines outside the valid enrollment period from the cleaned analytical dataset.

**Cleaning Action**

Revalidated claim eligibility after DQ-002 and excluded 167,256 claim service lines that remained outside valid member enrollment periods. Service dates were not shifted.

**Result / Notes**

332,740 claim lines were retained. Final validation found 0 claims before enrollment and 0 claims after termination. Raw source data remained unchanged.

---

### DQ-011: Member and Provider Geography

**Dataset:** Claims  
**Fields:** `member_id`, `provider_id`, `state`  
**Dimension:** Validity / Business rule  
**Records Affected:** 476,718 (95.34%)  
**Status:** Resolved

**Profiling Finding**

476,718 of 499,996 claim service lines connect members and providers in different states. Only 23,278 claim lines (4.66%) are same-state, which conflicts with the documented geography generation target of approximately 90% same-state service.

**Business / Analytical Impact**

The geographic mismatch could materially distort state-level utilization, provider access, network, and allowed-cost analyses.

**Cleaning Decision**

Use controlled provider reassignment to restore the intended approximately 90% same-state service distribution while retaining realistic cross-state care.

**Cleaning Action**

Reassigned selected cross-state claims to compatible same-state providers while preserving network status where possible. Provider compatibility was subsequently corrected under DQ-014 and geography was revalidated.

**Result / Notes**

Final geography was 93.25% same-state and 6.75% cross-state across 332,740 retained claim lines, with 0 provider compatibility violations after DQ-014.

---

### DQ-012: Network Cost Adjustment

**Dataset:** Claims  
**Fields:** `allowed_amount`, `provider_id`, `network_status`, `procedure_code`  
**Dimension:** Validity / Business Rule  
**Records Affected:** 499,996 (100.00%)  
**Status:** Resolved

**Profiling Finding**

Allowed amounts do not demonstrate the expected network-status adjustment. After normalizing allowed amount to the procedure baseline, In-Network and Out-of-Network claim lines have essentially identical average ratios (1.034999 vs. 1.034916).

**Business / Analytical Impact**

Network cost comparisons may be misleading because the expected network-status effect is not reflected in allowed amounts.

**Cleaning Decision**

Recalculate affected allowed amounts using the documented cost-generation rules after provider and geography corrections are complete.

**Cleaning Action**

Recalculated allowed amounts using the procedure-specific baseline, natural cost variation of approximately ±20%, and an approximately 20% upward adjustment for out-of-network services using the final provider assignment.

**Result / Notes**

Final validation found 0 missing or nonpositive allowed amounts. Average normalized allowed amount was 1.00 for in-network claims and 1.20 for out-of-network claims, restoring the documented 20.00% average network cost effect. No geography cost adjustment was applied because none is specified in the documented generation rule.

---

### DQ-013: Artificial Temporal Utilization Growth

**Dataset:** Claims  
**Fields:** `service_date`, `member_id`  
**Dimension:** Validity / Temporal Pattern  
**Status:** Resolved

**Profiling Finding**

Claim utilization intensity increases substantially over calendar time beyond enrollment growth. Claim lines per claiming member rise from 3.02 in 2021 to 7.51 in 2025, while monthly claim lines per 1,000 enrolled members rise from 101 in January 2021 to 1,176 in December 2025. No documented generation rule specifies intentional year-over-year utilization growth.

**Business / Analytical Impact**

Can materially distort utilization and total-cost trend analysis by creating artificial growth over time that is not explained solely by enrollment growth.

**Cleaning Decision**

Correct the temporal distribution of claim activity while preserving realistic utilization variation and existing clinical and cost composition.

**Cleaning Action**

Redistributed whole claims across valid member enrollment periods using monthly member enrollment exposure as the utilization basis. Preserved claim-level service-date consistency, clinical and cost composition, and controlled month-to-month variation.

**Result / Notes**

All 332,740 service lines and 207,653 claims were retained. Monthly utilization ranged from 257.93 to 303.55 claim lines per 1,000 enrolled members, averaging 280.34. Final validation found 0 claims outside enrollment periods and removed the artificial sustained year-over-year utilization growth.

---

### DQ-014: Provider Compatibility

**Dataset:** Claims  
**Fields:** `provider_id`, `service_category`, `place_of_service`  
**Dimension:** Validity / Business Rule Conformance  
**Records Affected:** 31,686 (9.52%)  
**Status:** Resolved

**Profiling Finding**

During DQ-011 validation, 31,686 claim lines were identified with provider types incompatible with the documented service category and place-of-service rules.

**Business / Analytical Impact**

Invalid provider assignments could distort provider utilization, service-category analysis, geographic analysis, and downstream cost analysis.

**Cleaning Decision**

Reassign incompatible claims to compatible providers, prioritizing same-state and same-network providers where available, with compatible same-network providers used as a fallback.

**Cleaning Action**

Reassigned all 31,686 affected claim lines using documented service category, place-of-service, and provider-type compatibility rules. Network status was preserved.

**Result / Notes**

0 provider compatibility violations remained after cleaning. Of the affected records, 21,274 were reassigned to compatible same-state providers and 10,412 required compatible cross-state fallback providers. Final overall geography was 93.25% same-state and 6.75% cross-state. All 332,740 claim lines were retained.