# Speed Dating: popularity, selectivity or compatibility?

> Product analytics case: how much of a match comes from popularity, selectivity or compatibility?
> Speed dating data, Python/pandas, bootstrap, Gini.

**Status:** in progress (data audit stage)

## Business question

**Decision:** should a recommender system rank profiles by the predicted probability of a
*mutual* match, instead of optimizing only for the viewer's own interest?

**Question:** how concentrated is attention ("yes" decisions) across participants, and how much
of a match is explained by popularity, selectivity or pair-level compatibility?

## Hypotheses

- **H1 (inequality):** "yes" decisions received are concentrated among a small share of
  participants (Gini clearly above 0).
- **H2 (selectivity):** the share of "yes" answers that turn into a match declines as a
  participant's own yes-rate grows.
- **H3 (compatibility):** the observed match rate is higher than expected if the two decisions
  were independent, $\overline{p_i\,p_j}$, and pair-level features (age gap, shared-interest
  rating) add predictive power beyond popularity and selectivity.

**What would change my mind:** if pair-level features give no improvement over the
popularity + selectivity baseline (the improvement threshold will be fixed *before* modelling),
the recommendation is not to switch the ranking objective on this evidence.

## Data

Speed dating experiment (Fisman & Iyengar, Columbia Business School, 2002-2004).
Download instructions: see [`data/README.md`](data/README.md). Raw data is not stored in this repo.

## Approach

- [ ] Data audit: unit of analysis (each date appears in two rows), missing values, consistency of `match`, `dec`, `dec_o`
- [ ] Independence benchmark: observed match rate vs $\overline{p_i\,p_j}$
- [ ] Popularity and selectivity per participant, Lorenz curve and Gini with bootstrap CI (resampling participants)
- [ ] Match precision vs yes-rate (H2)
- [ ] Pair-level model with leave-one-out popularity/selectivity (to avoid leakage), grouped cross-validation by participant
- [ ] Recommendation and limitations

## Limitations (draft)

Heterosexual pairs only, students of Columbia graduate programs, in-person 4-minute dates
(not swipes), 2002-2004. Findings describe mutual-choice mechanics, not any specific app's users.

## Repo structure

```
data/         how to get the data
notebooks/    analysis, numbered
src/          helper functions
reports/figures/
```
