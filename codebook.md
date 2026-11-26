# Codebook

## Groups and families
| `group` | `family` | Meaning |
|---|---|---|
| built-in | `concept` | concept bottleneck and self-explaining models (CBM, CEM, PCBM, LF-CBM, SENN) |
| built-in | `prototype` | prototype networks (ProtoPNet, ProtoTree, PIP-Net) |
| built-in | `additive` | GAMs and neural additive models |
| built-in | `xbm` | explanation bottlenecks that predict from generated text or language-model concepts |
| boundary | `posthoc` | attacks on post-hoc explanations whose transfer to built-in explanations is open |
| boundary | `privacy` | privacy and extraction attacks through explanations or prediction APIs |
| secondary | `secondary` | surveys and SoKs used for seeding and comparison |

## Evidence type
- **direct security**: an explicit adversary, attack success measure, or defense on a built-in explanation.
- **direct reliability**: a failure mode (misalignment, instability, noisy concepts, non-identifiability, leakage, human non-use) that can undermine an audit without an attacker.
- **certified defense / verification**: a proof of a property of a model or explanation.
- **mitigation**: a design change that reduces a failure mode, without an adversarial evaluation.
- **robustness to noise**: statistical robustness, explicitly not adversarial.
- **architecture**: a family-defining paper that fixes the intended meaning of the explanation.
- **boundary**: post-hoc or privacy work showing a mechanism that may transfer.
- **secondary**: survey or SoK.

## Stage
`input`, `training`, `model` (provider-side selection or manipulation), `edit` (intervention interface), `API` (read path), `human loop`; `-` if not applicable. Multiple stages are separated by `;`.

## Properties
P1 prediction integrity, P2 explanation integrity, P3 semantic alignment, P4 intervention safety, P5 audit reliability, P6 confidentiality (definitions in Sec. IV of the paper).

- `properties_direct`: the work evaluates the property explicitly.
- `properties_adjacent`: a result informs the property without testing it under the paper's definitions.

When a paper shows a prediction-preserving attack, P1 is coded as preserved and P2 as broken, so that a model is not called robust merely because its label did not change.

## Family-level map (`family_map.csv`)
A qualitative synthesis over the works of each family and threat category:
`full` = studied directly, `partial` = adjacent or partial evidence, `none` = no evidence found in the map. Cells are coded `partial` rather than `none` when in doubt. "Direct" means the topic is studied, not necessarily under an adaptive attacker.

## Final update
`added_in_update = 1` marks the five works added in the final update of the map (Sec. V-H of the paper).
