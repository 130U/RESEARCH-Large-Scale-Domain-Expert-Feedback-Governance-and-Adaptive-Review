# Where this work sits

One pool of expert hours has to measure a batch and repair it. Each half of that sentence has a literature. Survey
sampling and prediction-powered inference cover the measurement; repeated labeling and learning to defer cover the
repair. Every one of them stops at one of the two jobs. This page records what each line establishes, where it
stops, and what the article adds. The complete list of 154 sources is in the [bibliography](bibliography.md).

## The short version

| Line of work | What it establishes | Where it stops | What the article adds |
| --- | --- | --- | --- |
| Survey sampling: Neyman, Horvitz-Thompson, Cochran, Isaki-Fuller, Chen-Lumley | Purposive selection cannot measure; unbiased estimation under unequal probabilities; the square-root optimum | One survey, one use of the sample; cost by stratum at most | A cost for every item, and a second use of the same audit: repair |
| Prediction-powered and active inference: PPI, PPI++, Active Statistical Inference, cost-optimal evaluation | Valid inference from a few labels and many predictions; labels chosen by model uncertainty | Labels of equal price, or two rater types at one price each; nothing is repaired | The budget identity $`\kappa`$, the quarter-variance law, and the joint rule |
| Label-efficient model evaluation: Active Risk Estimation, Active Testing | Selection bias in evaluation and its importance-weighted correction | The target is a model's risk, not a batch's defect rate | The same correction as a production measurement with operating standards |
| Repeated labeling and learning to defer: Sheng et al., Karger et al., Okati et al., DeCCaF | Which items deserve another human pass, under cost and capacity | Batch quality is outside the objective | One program in which the audit's repair enters its own price |
| Reviewer reliability: Dawid-Skene and successors | Latent-truth models of annotator error | No sampling design, no budget | The price of an auditor's error in audit hours (D14) |
| Audit practice: GAO Financial Audit Manual, risk-limiting audits | Risky items examined in full, a random sample projected; validity whatever the error rates | No allocation inside the random stream, no shared budget | The allocation inside the projectable stream |

## Timing

The formulation dates from late 2023. Prediction-Powered Inference (January 2023) and design-based supervised
learning (June 2023) precede it, and PPI++ appeared that November. Active Statistical Inference (2024), stratified
PPI (2024), DeCCaF (2024), cost-optimal active evaluation (2025) and robust sampling (2025) appeared while the
program was running. The later papers reach the square-root form for labels of equal cost; none of them prices
repair.

## Key sources

### Sampling design

<a id="neyman1934"></a>
**Neyman (1934), "On the Two Different Aspects of the Representative Method."** [doi](https://doi.org/10.2307/2342192)
Optimal stratified allocation is proportional to stratum size times within-stratum standard deviation, and a sample
matched purposively on some characters fails on the others. This is the equal-cost ancestor of the audit rule and
the original argument against reading a risk-targeted queue as a measurement. Cost enters only with Cochran's
optimum allocation, and then by stratum.

<a id="nedyalkova2008"></a>
**Nedyalkova and Tillé (2008), "Optimal Sampling and Estimation Strategies under the Linear Model."** [doi](https://doi.org/10.1093/biomet/asn027)
Under a linear model the efficiency bound is reached by inclusion probabilities proportional to the error standard
deviation with the Horvitz-Thompson estimator; the best purely model-based strategy takes the largest units
purposively and gives up design validity. The paper confirms the square-root rule for model-assisted estimation and
names, in survey terms, the choice Section 1 makes for a review queue.

<a id="chenlumley2020"></a>
**Chen and Lumley (2020), "Optimal Multiwave Sampling for Regression Modeling in Two-Phase Designs."** [doi](https://doi.org/10.1002/sim.8760)
The optimal two-phase design for a design-based estimator is Neyman allocation on influence functions, approximated
wave by wave with priors from earlier waves. For a batch mean the influence function is the residual, so the audit
rule is this construction with a cost for every item, and a weekly program is the multiwave design. The paper has
no audit costs and one use for each sampled unit.

<a id="gao2018"></a>
**U.S. Government Accountability Office (2018), Financial Audit Manual, Volume 1.** [pdf](https://www.gao.gov/assets/gao-18-601g.pdf)
The auditor examines large and unusual items in full, samples the remainder, projects only the sample and documents
which selection is which. Audit practice already separates escalation from the random stream. It does not allocate
within the projectable stream or set the two against one budget.

<a id="stark2023"></a>
**Stark (2023), "ALPHA: Audit that Learns from Previously Hand-Audited Ballots."** [doi](https://doi.org/10.1214/22-AOAS1646)
Risk-limiting audits compare a machine record with random hand readings and remain valid whatever the machine's
error rates. This is the mature public precedent for combining predictions with a random audit under design-based
validity. An election audit tests one decision; a data program needs a rate, with its interval, every week.

### Predictions plus a few labels

<a id="angelopoulos2023ppi"></a>
**Angelopoulos, Bates, Fannjiang, Jordan and Zrnic (2023), "Prediction-Powered Inference."** [doi](https://doi.org/10.1126/science.adi6000)
Valid inference from a small labeled set and a large set of predictions, with no assumption on the model. For a
mean the estimator is the difference estimator of survey sampling, as the authors note. Labels are drawn uniformly,
so the queue bias of Section 1 cannot be written in this framework: there is no targeting to be biased by.

<a id="angelopoulos2023ppipp"></a>
**Angelopoulos, Duchi and Zrnic (2023), "PPI++: Efficient Prediction-Powered Inference."** [arXiv](https://arxiv.org/abs/2311.01453)
A tuning weight on the predictions interpolates between classical inference and PPI and is asymptotically never
worse than the classical estimator. Labels remain uniform. My estimator puts the full weight on the predictions;
under a Bernoulli design with known probabilities a weight per stratum, fitted on an earlier batch, keeps the
estimate unbiased, and the design notes use it for a stratum whose predictions are poor.

<a id="egami2023"></a>
**Egami, Hinck, Stewart and Wei (2023), "Using Imperfect Surrogates for Downstream Inference."** [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2023/hash/d862f7f5445255090de13b825b880d59-Abstract.html)
The validity of LLM-assisted estimates comes from a known probability of gold labeling, which may be non-uniform.
The paper leaves the choice of that probability open. Section 3 answers it for a batch mean.

<a id="zrnic2024"></a>
**Zrnic and Candès (2024), "Active Statistical Inference."** [PMLR](https://proceedings.mlr.press/v235/zrnic24a.html)
Labeling probability proportional to the square root of the conditional squared error, mixed with the uniform
design. The same square-root form, reached for labels of equal price. It carries no cost per item, no finite-batch
variance and no repair.

<a id="fisch2024"></a>
**Fisch et al. (2024), "Stratified Prediction-Powered Inference for Effective Hybrid Evaluation of Language Models."** [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c9fcd02e6445c7dfbad6986abee53d0d-Abstract.html)
A tuning weight and a Neyman-type allocation of human ratings per stratum, which helps when the automatic rater's
quality differs across strata. The allocation is in counts of ratings. Expert audits differ in price by a factor of
three across strata, and my rule allocates hours.

<a id="angelopoulos2025"></a>
**Angelopoulos, Eisenstein, Berant, Agarwal and Fisch (2025), "Cost-Optimal Active AI Model Evaluation."** [arXiv](https://arxiv.org/abs/2506.07949)
Cost-optimal policies for a weak and a strong rater, with a square-root rule and a threshold above which an item
goes straight to the strong rater. This is the closest work on cost. Its prices are one per rater type for all
items, and the labels repair nothing. In the joint rule the threshold $`r_i \ge \lambda c_i`$ comes from the
audit's repair value, which is the quantity this paper has no place for.

<a id="li2025"></a>
**Li, Zrnic and Candès (2025), "Robust Sampling for Active Statistical Inference."** [arXiv](https://arxiv.org/abs/2511.08991)
A budget-preserving path from the active design to the uniform one, with the mixing weight chosen by variance
minimization and an asymptotic guarantee against both endpoints. The bound of D10 is the complementary statement:
a finite-batch ceiling at a fixed weight that holds for any residual estimates.

<a id="dorner2025"></a>
**Dorner, Nastl and Hardt (2025), "Limits to Scalable Evaluation at the Frontier: LLM as Judge Won't Beat Twice the Data."** [arXiv](https://arxiv.org/abs/2410.13341)
Under uniform sampling a judge no better than the model it scores can at most double the effective sample. The
result bounds what the prediction term can save. The gains of Sections 3 and 4 come from where audits are sent, a
source of efficiency the bound does not cover.

### Evaluating a model with few labels

<a id="sawade2010"></a>
**Sawade, Landwehr, Bickel and Scheffer (2010), "Active Risk Estimation."** [ICML](https://mlanthology.org/icml/2010/sawade2010icml-active)
The variance-minimizing sampling distribution for importance-weighted risk estimation has a square-root form.
The target is a model's risk and every label costs the same.

<a id="kossen2021"></a>
**Kossen, Farquhar, Gal and Rainforth (2021), "Active Testing: Sample-Efficient Model Evaluation."** [arXiv](https://arxiv.org/abs/2103.05331)
Actively chosen test points bias a risk estimate, and importance weighting removes the bias. This is the premise of
Section 1 for model evaluation. It is not applied to the defect rate of a data batch, and it has no repair side.

<a id="kossen2022"></a>
**Kossen, Farquhar, Gal and Rainforth (2022), "Active Surrogate Estimators."** [NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2022/hash/9b9cfd5428153ccfbd4ba34b7e007305-Abstract-Conference.html)
Surrogate-model estimates of test risk use labels more efficiently than importance-weighted ones and are biased to
the extent the surrogate is wrong. I take the other side of that trade deliberately: a number that governs
contributors and rubrics has to be unbiased before it is efficient.

<a id="hesterberg1995"></a>
**Hesterberg (1995), "Weighted Average Importance Sampling and Defensive Mixture Distributions."** [doi](https://doi.org/10.1080/00401706.1995.10484303)
Mixing an importance-sampling density with the nominal one bounds every weight and with it the variance. D10 is
this bound written for a Bernoulli audit design at a fixed budget.

### Repair under cost and capacity

<a id="sheng2008"></a>
**Sheng, Provost and Ipeirotis (2008), "Get Another Label?"** [doi](https://doi.org/10.1145/1401890.1401965)
Repeated labeling improves data quality with diminishing returns, and relabeling the uncertain items beats
relabeling in rotation. This is tiered review as repair. It is silent on what the relabeled sample says about the
batch.

<a id="karger2014"></a>
**Karger, Oh and Shah (2014), "Budget-Optimal Task Allocation for Reliable Crowdsourcing Systems."** [doi](https://doi.org/10.1287/opre.2013.1235)
For anonymous crowds a non-adaptive assignment is order-optimal, and adaptive routing pays only when workers have
persistent identities. A standing workforce of specialists with reliability records is that case, which is why
adaptive review is worth designing here.

<a id="okati2021"></a>
**Okati, De and Gomez-Rodriguez (2021), "Differentiable Learning Under Triage."** [NeurIPS](https://proceedings.nips.cc/paper_files/paper/2021/file/4c4c937b67cc8d785cea1e42ccea185c-Paper.pdf)
Under a budget on the share of cases sent to humans, the optimal policy is a threshold on model loss minus human
loss. D11 is the same structure in review form, with removable loss as the key.

<a id="alves2024"></a>
**Alves et al. (2024), "Cost-Sensitive Learning to Defer to Multiple Experts with Workload Constraints."** [arXiv](https://arxiv.org/abs/2403.06906)
An expert-correctness model with constrained assignment under per-expert capacity. The authors send random
instances to experts so that experts can be evaluated fairly, which is the measurement problem seen from the repair
side. It stays outside their objective.

<a id="dawid1979"></a>
**Dawid and Skene (1979), "Maximum Likelihood Estimation of Observer Error-Rates Using the EM Algorithm."** [doi](https://doi.org/10.2307/2346806)
Each observer has a confusion matrix against an unobserved truth, estimated jointly with it. The model has no
sampling design and no budget. I use its two-parameter form, sensitivity and specificity, to price an auditor's
error in audit hours.

### Practice in post-training data

<a id="lightman2023"></a>
**Lightman et al. (2023), "Let's Verify Step by Step."** [arXiv](https://arxiv.org/abs/2305.20050)
The authors chose convincing wrong-answer solutions for labeling, which made process labels far more
data-efficient, and noted that the choice biased the data set toward wrong answers. Both values of a review appear
in one frontier-lab data operation. The bias is stated and left uncorrected.

<a id="stiennon2020"></a>
**Stiennon et al. (2020), "Learning to Summarize from Human Feedback."** [arXiv](https://arxiv.org/abs/2009.01325)
Labeler quality is controlled with calibration items and agreement thresholds, and agreement varies strongly with
the difficulty of the comparison. Calibration streams are standard practice; a sampling design for them is not, and
the dependence on difficulty is the task-mix effect of Section 1.

<a id="zhang2024"></a>
**Zhang et al. (2024), "Diverging Preferences: When do Annotators Disagree and do Models Know?"** [arXiv](https://arxiv.org/abs/2410.14632)
A large share of disagreement on preference pairs comes from style and underspecification, not error. The paper
fixes the scope of a defect rate: it is defined for tasks with acceptance criteria, which is how the program
specified its tasks.

<a id="brown2008"></a>
**Brown (2008), "In-Season Prediction of Batting Averages."** [arXiv](https://arxiv.org/abs/0803.3697)
Shrinking binomial rates by sample size beats the raw rate, and the method fails when sample size is correlated
with ability. Tiered review creates exactly that correlation. Section 7 removes it with the random audit stream,
whose selection does not depend on the contributor's record.

<a id="livingston2014"></a>
**Livingston (2014), Equating Test Scores (Without IRT).** [pdf](https://www.ets.org/Media/Research/pdf/LIVINGSTON2ed.pdf)
For judgment-scored tasks, scoring standards drift, and rescoring a sample of earlier responses links the scales.
The dual-version anchors of Section 2 are this rescoring design, and the same anchor set detects drift between
rubric changes.
