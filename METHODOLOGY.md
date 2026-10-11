# Feature Selection & Methodology (Data Audit)

This document outlines the rationale behind feature pruning (reducing the raw dataset from 195 to 53 core features), provides a comprehensive data dictionary for the selected variables, and explains the statistical foundation of the analytical framework (Gini Coefficient and Logistic Regression).

---

## 1. Feature Pruning: Excluded Variables & Rationale

The original speed dating dataset contains 195 features collected across multiple experimental touchpoints (pre-event surveys, in-event scorecards, follow-ups on day 2, and follow-ups 3–4 weeks later). Over **140 features were deliberately excluded** from the core analysis to maintain analytical integrity:

1. **Preventing Data Leakage & Survivor Bias:**
   - **Excluded:** All variables with suffixes `_2` (day-after survey) and `_3` (3–4 weeks post-event), such as `attr7_2`, `date_3`, `numdat_3`, `you_call`, and `them_cal`.
   - **Rationale:** The objective is to identify the drivers of initial attraction (`dec` / swipe-equivalent) and mutual conversion (`match`) at the point of decision ($T=0$). Post-event feedback is an outcome of a match rather than a predictor. Furthermore, wave `_3` suffers from $>75\%$ missing values, introducing significant survivor bias (primarily completed by participants who successfully established post-event contact).
2. **Stated vs. Revealed Preferences:**
   - **Excluded:** Theoretical preference blocks `attr1_1`–`shar1_1` (self-reported trait importance), `attr2_1` (perceived opposite-sex preferences), and `attr3_1` (self-perception).
   - **Rationale:** In product analytics, stated intentions frequently diverge from revealed behavior. To evaluate real matching dynamics, we focus strictly on actual evaluations assigned to partners during the live interaction rather than abstract self-assessments.
3. **Socioeconomic Noise & High Missingness:**
   - **Excluded:** `income`, `zipcode`, `tuition`, `mn_sat`, and `undergra`.
   - **Rationale:** Participants did not have access to verified income data or standardized test scores during brief 4-minute interactions. These fields introduce extraneous variance, noise, and substantial missing values.

---

## 2. Data Dictionary

The cleaned analytical dataset retains 53 columns capturing the interaction core at the moment of decision.  
*Data Grain: One row represents a single speed date (an evaluation from participant `iid` to partner `pid`).*

### 2.1. Interaction & Target Variables
| Field | Type | Description |
| :--- | :--- | :--- |
| `wave` | `int` | Experimental event wave index (1–21). |
| `iid` | `int` | Unique participant identifier (evaluator). |
| `pid` | `int` | Unique partner identifier (target of evaluation). |
| `gender` | `int` | Evaluator gender (0 = Female, 1 = Male). |
| `round` | `int` | Total number of dates scheduled for the participant during the event. |
| `order` | `int` | Sequence order of the specific date during the evening. |
| `dec` | `int` | **Target 1:** Decision by participant `iid` (1 = Yes, 0 = No). Swipe-right equivalent. |
| `dec_o` | `int` | **Target 2:** Decision by partner `pid` regarding `iid` (1 = Yes, 0 = No). |
| `match` | `int` | **Target 3:** Mutual match indicator ($dec = 1 \land dec\_o = 1$). |

### 2.2. Participant & Partner Demographics
| Field | Type | Description |
| :--- | :--- | :--- |
| `age`, `age_o` | `float` | Age of evaluator and partner, respectively. |
| `race`, `race_o` | `float` | Categorical race (1 = Black, 2 = Caucasian, 3 = Latino, 4 = Asian, 6 = Other). |
| `samerace` | `int` | Binary racial concordance flag (1 = Same race, 0 = Different). |
| `imprace`, `imprelig`| `float` | Participant self-rated importance of shared racial/religious background (1–10 scale). |
| `goal` | `float` | Primary participation goal (1 = Seemed like a fun night out ... 6 = Looking for a serious relationship). |
| `date`, `go_out` | `float` | General baseline frequency of dating and social outings. |
| `int_corr` | `float` | Pearson correlation coefficient between the interest profiles of `iid` and `pid`. |

### 2.3. Perceived Trait Ratings (Post-Date Evaluation)
Scored on a scale from 1 to 10 immediately following the 4-minute interaction. Suffix `_o` denotes ratings *received* from the partner.
| Field | Description |
| :--- | :--- |
| `attr`, `attr_o` | Physical Attractiveness. |
| `sinc`, `sinc_o` | Sincerity. |
| `intel`, `intel_o` | Intelligence. |
| `fun`, `fun_o` | Fun / Charisma. |
| `amb`, `amb_o` | Ambition. |
| `shar`, `shar_o` | Perceived Shared Interests. |
| `like`, `like_o` | Overall liking score. |
| `prob`, `prob_o` | Perceived subjective probability of mutual interest. |

### 2.4. Interest Vectors (Hobby Portfolio)
Continuous ratings (`float`, 1–10) capturing individual leisure activities:  
`sports`, `tvsports`, `exercise`, `dining`, `museums`, `art`, `hiking`, `gaming`, `clubbing`, `reading`, `tv`, `theater`, `movies`, `concerts`, `music`, `shopping`, `yoga`.

---

## 3. Mathematical Foundations & Product Metrics

### 3.1. Gini Coefficient (Quantifying Attention Inequality)
* **Definition:** A statistical dispersion metric representing the inequality of a distribution. Ranging from 0 (perfect equality) to 1 (perfect inequality), it is commonly applied in econometrics to study income distribution.
* **Product Analytics Context:** Two-sided matching platforms suffer heavily from liquidity imbalances. If incoming attention is monopolized by a minor fraction of profiles, the platform faces supply-demand friction: the top percentile becomes overwhelmed (leading to high ghosting rates), while the remaining user base experiences severe match starvation and subsequent churn.
* **Mathematical Formulation (Sample Gini):**
  $$G = \frac{\sum_{i=1}^{n} (2i - n - 1) x_{(i)}}{n \sum_{i=1}^{n} x_{(i)}}$$
  where $x_{(i)}$ represents the ordered vector of positive decisions received by individual participants ($x_{(1)} \le x_{(2)} \le \dots \le x_{(n)}$).

### 3.2. Logistic Regression & Odds Ratios (Isolating Decision Drivers)
* **Definition:** A generalized linear model for binary classification modeling the probability of an outcome $P(Y=1)$ via the logit link function:
  $$\ln\left(\frac{P(Y=1)}{1 - P(Y=1)}\right) = \beta_0 + \sum_{k=1}^{m} \beta_k X_k$$
* **Why Logistic Regression Over Black-Box Machine Learning (XGBoost / Random Forest):**
  In product and recommendation strategy, pure predictive performance (`AUC-ROC`) is secondary to **causal interpretability and parameter isolation**. 
  
  By taking the natural exponential of the regression coefficients:
  $$\text{Odds Ratio (OR)}_k = e^{\beta_k}$$
  we isolate the marginal impact of a specific feature while holding all other evaluated dimensions constant. This directly answers key product design questions, such as: *"What is the exact percentage change in the odds of a positive swipe for a 1-point increase in physical attractiveness versus a 1-point increase in perceived intelligence or shared interests?"*
