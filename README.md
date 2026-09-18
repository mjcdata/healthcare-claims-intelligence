![Healthcare Claims Intelligence](assets/README%20header.png)

## Overview

Healthcare Claims Intelligence is a healthcare analytics portfolio project focused on identifying claims cost drivers and opportunities to reduce allowed costs using synthetic healthcare claims data.

### Tableau Dashboard

**[View the Interactive Tableau Dashboard](https://public.tableau.com/shared/YT7JG4G57?:display_count=n&:origin=viz_share_link)**

The dashboard answers the primary business question:

**How can we reduce allowed cost?**

## Dataset

This project uses a synthetic healthcare claims dataset created specifically for the analysis. The data models healthcare claims activity across a five-year period and is structured around three primary datasets:

- **Claims:** Service-level healthcare claims including procedure, diagnosis, place of service, service category, and allowed amount.
- **Members:** Member demographic and enrollment information.
- **Providers:** Provider attributes including provider type, specialty, state, and network status.

Supporting procedure and diagnosis reference tables were also created to maintain realistic relationships between healthcare services, diagnoses, and procedures.

## Project Structure

### [Documentation](Documentation/)

Contains supporting project documentation:

- **[Data Model](Documentation/Data%20Model.md)** - Documents the analytical data model, dataset grain, keys, fields, and relationships
- **[Business Rules](Documentation/Business%20Rules.md)** - Documents the rules governing enrollment, provider compatibility, clinical relationships, geography, and data integrity
- **[Data Dictionary](Documentation/Data%20Dictionary.md)** - Documents dataset fields, definitions, and structure
- **[Synthetic Data Generation](Documentation/Synthetic%20Data%20Generation.md)** - Documents the methodology and rules used to generate the synthetic healthcare data
- **[Data Quality & Cleaning Log](Documentation/Data%20Quality%20%26%20Cleaning%20Log.md)** - Documents identified data quality issues, assessments, cleaning decisions, and validation results
- **[Insights & Recommendations](Documentation/Insights%20%26%20Recommendations.md)** - Documents the business findings, modeled cost reduction opportunity, recommendation, and measurement plan

### [Analysis](Analysis/)

Contains the project's profiling, cleaning, analysis, and supporting code:

- **[healthcare_profiling.ipynb](Analysis/healthcare_profiling.ipynb)** - Jupyter notebook containing data profiling and data quality assessment
- **[healthcare_cleaning.ipynb](Analysis/healthcare_cleaning.ipynb)** - Jupyter notebook containing documented data cleaning, correction, and validation
- **[healthcare_analysis.ipynb](Analysis/healthcare_analysis.ipynb)** - SQL and Python business analysis of healthcare claims costs, utilization, procedure concentration, provider characteristics, network status, geography, member patterns, and modeled cost reduction opportunities

#### [Analysis/Scripts](Analysis/Scripts/)

Contains supporting Python scripts used by the project:

- **[data_generation_mapping.py](Analysis/Scripts/data_generation_mapping.py)** - Defines mappings used to constrain synthetic claim generation to clinically and operationally plausible combinations

### [Data](Data/)

Contains the original synthetic healthcare claims datasets, supporting reference data, and cleaned analysis-ready datasets:

- **claims.csv** - Original synthetic healthcare claims dataset preserved unchanged
- **members.csv** - Original synthetic member demographic and enrollment dataset preserved unchanged
- **providers.csv** - Original synthetic provider dataset preserved unchanged
- **procedure_reference.csv** - Reference data containing procedure codes, descriptions, service categories, and baseline allowed amounts
- **diagnosis_reference.csv** - Reference data containing diagnosis codes, descriptions, and diagnosis groups

#### [Data/Cleaned](Data/Cleaned/)

Contains the cleaned and validated datasets produced from the documented profiling and cleaning process and used for downstream business analysis:

- **claims_clean.csv** - Cleaned and validated healthcare claims data used for cost and utilization analysis
- **members_clean.csv** - Cleaned and validated member data used for member-level analysis
- **providers_clean.csv** - Cleaned and validated provider data used for provider, network, and geographic analysis
- **healthcare_claims_tableau.csv** - Joined, analysis-ready dataset used as the primary Tableau dashboard data source

### [Assets](assets/)

Contains images used in the project README:

- **README header.png** - Project header image
- **Dashboard 1.png** - Tableau dashboard preview

## Dashboard

The Tableau dashboard translates the completed claims analysis into an interactive view focused on allowed cost trends, service category cost concentration, network-related cost differences, out-of-network excess cost, and modeled savings opportunities.

Key dashboard components include:

- Total Allowed Cost, Claim Lines, Unique Members, and Outpatient Procedure Cost KPIs
- Allowed cost trend over time
- Allowed cost by service category
- Average outpatient cost by network status
- Average cost by top outpatient procedure and network status
- Out-of-network excess cost by procedure
- Estimated savings under 25%, 50%, 75%, and 100% out-of-network shift scenarios

### Dashboard Preview

![Healthcare Claims Intelligence Tableau Dashboard](assets/Dashboard%201.png)

**[View the Interactive Tableau Dashboard](https://public.tableau.com/shared/YT7JG4G57?:display_count=n&:origin=viz_share_link)**

## Analysis & Key Findings

The analysis identified **Outpatient Procedure** as the largest allowed cost category, accounting for approximately **27% of total allowed cost**. The main driver was high cost per procedure rather than unusually high utilization.

Key findings:

- The four highest-cost outpatient procedures account for approximately **86% of outpatient allowed cost**
- Out-of-network services for these procedures cost approximately **20% more** than comparable in-network services
- Geographic cost variation is smaller, generally around **5% to 10%** after controlling for procedure and network status
- Individual provider comparisons are limited by sparse procedure volume
- Existing out-of-network utilization among the four highest-cost procedures represents approximately **$787K in modeled cost reduction opportunity**

### Recommendation

Reduce out-of-network utilization for the four highest-cost outpatient procedures by **25% next quarter** by steering appropriate services toward in-network providers. Based on observed cost differences, this represents approximately **$197K in modeled savings**.

## Tools & Technologies

- **Python** - Data generation, profiling, cleaning, validation, and analytical support
- **Pandas** - Data transformation, quality assessment, cleaning, and exploratory analysis
- **SQL / DuckDB** - Business analysis, aggregation, ranking, cost decomposition, and analytical queries
- **Jupyter Notebook / Google Colab** - Development environment for profiling, cleaning, and analysis workflows
- **Tableau** - Interactive dashboard development and data visualization
- **Google Drive** - Project organization, documentation, and file management