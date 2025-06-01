# Diabetes Risk Analysis by Age Group and BMI

This project investigates the relationship between Body Mass Index (BMI) and the likelihood of developing type 2 diabetes across different age groups using a logistic regression model.

## Dataset

- Source: [Dryad Public Dataset](https://doi.org/10.5061/dryad.ft8750v)
- Population: 211,833 Chinese adults (> 20 years old) from health screening programs
- Key Features: `Age`, `BMI`, `Diabetes`, and more
- Target variable: `Diabetes` (0 = No, 1 = Yes)

##  Objective

To assess how BMI affects diabetes risk in different age groups (20–30, 30–40, 40–50, ..., 70+), and to determine whether the association is stronger in younger adults, as suggested in prior research.

##  Methodology

- BMI and diabetes status were analyzed using:
  - Logistic Regression (using `statsmodels`)
  - Age groups were segmented and modeled separately
- Visualization tools used:
  - Boxplots, Violin plots
  - Normality and distribution checks

## Key Results

| Age Group | BMI Coefficient | p-value | Effect Summary |
|-----------|------------------|---------|----------------|
| 20–30     | 0.0169           | 0.865   | Not significant |
| 30–40     | 0.1467           | 0.000   | Highly significant |
| 40–50     | 0.1761           | 0.000   | Stronger effect |
| 60–70     | 0.0665           | 0.009   | Significant but weaker |
| 70+       | 0.0975           | 0.010   | Mild effect |

## Key Findings

While the original study suggested that BMI has a stronger impact on diabetes risk in younger adults, our analysis shows that:

- The **association between BMI and diabetes was statistically significant** in most age groups.
- However, **the effect was not strongest in the youngest group (20–30)**. In fact, this group showed **no significant association** (p = 0.865).
- The **strongest associations** were observed in middle-aged adults (30–60).

## Conclusion

The relationship between BMI and diabetes is statistically significant in middle-aged and older adults. Contrary to the original study's findings, **our analysis did not find a stronger effect in younger adults** (age 20–30), likely due to the small number of diabetes cases in that group.

This highlights the importance of **re-analyzing public datasets** independently to validate published findings.

##  Tech Stack

- Python
- Pandas, Matplotlib, Seaborn
- Statsmodels
- Jupyter Notebook
