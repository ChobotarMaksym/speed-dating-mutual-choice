# Methodology & Data Dictionary

This document explains the feature pruning (reducing the raw dataset from 195 to 53 core columns), provides a data dictionary,
and describes the statistical methods: Gini coefficient with a null model, logistic regression, a binomial GLM check, and the out-of-sample ranking evaluation.

---

## 1. Feature Pruning: Excluded Variables & Rationale

The original speed dating dataset contains 195 features collected across multiple experimental touchpoints (pre-event surveys, in-event scorecards, follow-ups on day 2, and follow-ups 3–4 weeks later). Over **140 features were deliberately excluded** from the core analysis to maintain analytical integrity:

1. **Preventing Data Leakage & Survivor Bias:**
   - **Excluded:** All variables with suffixes `_2` (day-after survey) and `_3` (3–4 weeks post-event), such as `attr7_2`, `date_3`, `numdat_3`, `you_call`, and `them_cal`.
   - **Rationale:** The objective is to model the decision at the moment of the date ($T=0$). Post-event feedback is an outcome of a match rather than a predictor. Both follow-up surveys are also sparse (for example `num_in_3` 92% missing, `sinc7_2` 77%), and the respondents are likely a self-selected subset of participants.
2. **Stated vs. Revealed Preferences:**
   - **Excluded:** Theoretical preference blocks `attr1_1`–`shar1_1` (self-reported trait importance), `attr2_1` (perceived opposite-sex preferences), and `attr3_1` (self-perception).
   - **Rationale:** In product analytics, stated intentions frequently diverge from revealed behavior. To evaluate real matching dynamics, we focus strictly on actual evaluations assigned to partners during the live interaction rather than abstract self-assessments.
3. **Socioeconomic Noise & High Missingness:**
   - **Excluded:** `income`, `zipcode`, `tuition`, `mn_sat`, and `undergra`.
   - **Rationale:** Participants did not have access to verified income data or standardized test scores during brief 4-minute interactions. These fields introduce extraneous variance, noise, and substantial missing values.

---

## 2. Data Dictionary

The cleaned analytical dataset retains 53 core columns. The analysis adds derived fields: the partner profile join (`goal_o`, `<interest>_o`), `goal_match`, `interest_cos`, `age_diff_signed`, and candidate statistics `pop_j`, `sel_j`.

*Data grain: each date appears in two rows (`iid`→`pid` and `pid`→`iid`). Date-level analyses use the `gender == 1` rows (male viewer, female candidate).*

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
| `goal` | `float` | Primary participation goal (1 = Seemed like a fun night out, 2 = To meet new people, 3 = To get a date, 4 = Looking for a serious relationship, 5 = To say I did it, 6 = Other). |
| `date`, `go_out` | `float` | General frequency of dating and of going out (1 = several times a week ... 7 = almost never). |
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
* **Definition:** A dispersion metric from 0 (perfect equality) to 1 (perfect inequality).
* **Product context:** In two-sided platforms, if incoming attention is concentrated in a small share of profiles, the rest of the user base may face match starvation while top profiles may be overwhelmed. This dataset cannot measure ghosting or churn; the metric is used only as a measure of concentration.
* **Formula (sample Gini):**
  $$G = \frac{\sum_{i=1}^{n} (2i - n - 1) x_{(i)}}{n \sum_{i=1}^{n} x_{(i)}}$$
  where $x_{(i)}$ is the ascending-sorted popularity of participants (received yes-rate), computed separately by gender.
* **Null model:** with a finite number of dates, sampling noise alone gives Gini > 0. The observed value is compared with a wave-aware null: for each participant, received yes ~ Binomial($n_{dates}$, $p_{wave}$), where $p_{wave}$ is the mean popularity in the participant's wave and gender (1,000 simulations, 95th percentile).
* **Uncertainty:** 95% CI by bootstrap, resampling participants (1,000 iterations). The top-20% share is reported alongside Gini as a more direct measure of concentration.

### 3.2. Logistic Regression & Odds Ratios (Decision Drivers)
* **Model:** $$\ln\left(\frac{P(Y=1)}{1 - P(Y=1)}\right) = \beta_0 + \sum_{k=1}^{m} \beta_k X_k$$
  with $Y$ = the viewer's decision (`dec`) and $X$ = the six post-date trait ratings.
* **Use:** interpretation of associations. Ratings are standardized within gender, so a coefficient is the change in log-odds per 1 SD; $\text{OR}_k = e^{\beta_k}$. Standard errors are clustered by participant (`iid`), since each participant appears in many dates.
* **Caveats:** the coefficients are associations, not causal effects. The ratings are recorded together with the decision (halo effect), are collinear (`attr`, `fun`, `shar`), and each coefficient is conditional on the other ratings.

### 3.3. Match Conversion (H2)
* **Pooled conversion:** $\sum \text{matches} / \sum \text{yes decisions sent}$ per selectivity quintile, with quintiles built within gender and ties broken randomly.
* **Confounding check:** binomial GLM with outcome (matches, yes − matches) and predictors selectivity and popularity, with robust (HC1) standard errors. A match requires the partner's "yes", so conversion is closely tied to the sender's popularity.

### 3.4. Out-of-Sample Ranking Evaluation (H3)
* **Unit:** one row per date (male viewer, female candidate).
* **Candidate statistics:** `pop_j` is the share of training viewers who said yes to candidate j; `sel_j` is j's own yes-rate toward training viewers. For training rows they are computed out-of-fold (inner grouped 5-fold), so a row's label never enters its own features. Leave-one-out encodings were rejected because they leak the label.
* **Pair features:** `int_corr`, signed age gap, `samerace`, `goal_match`, `interest_cos`.
* **Models:** gradient boosting (`HistGradientBoostingClassifier`, `max_depth=3`). Model A predicts the viewer's own "yes"; model B predicts a mutual match. Ablations: B without pair features, and B without `sel_j`.
* **Evaluation:** 5-fold grouped CV by viewer; each viewer's dates are ranked by model score. Metrics are per-user AUC (users with both outcomes) and the top-3 match rate. Model comparisons use paired per-viewer differences with 95% CI = mean ± 1.96 SEM across viewers.
* **Decision threshold:** +0.02 per-user AUC for pair-level features. Other comparisons are exploratory.
