# AWS GovCloud CMMC Level 2 — LZA configuration starter

Prepared 2026-11-09. This is a new, reviewable baseline, not a patch against a supplied deployment. No AWS resources have been deployed. Customer IDs, emails, network allocations, identity assignments, operational integrations, and contractual decisions remain to be completed.

## Start here

1. Read `docs/IMPLEMENTATION-STEPS.md` and `docs/CHANGE-MATRIX.md`.
2. Confirm the installed LZA version and current resource ownership. This package targets **LZA v1.17.0**, source commit `6f3c35300f7dd487f61ee0f4c9c3170e4e1f9a16`. It is not a claim that this is the customer's installed version or the newest release.
3. Replace every `REPLACE-*` value and all eight repeated-digit account IDs. Use real **GovCloud** IDs and account emails. The `${ACCOUNT_ID}` token in endpoint policy JSON is an intentional native LZA replacement and must remain.
4. Merge each desired change into the customer's version-controlled configuration. Do not replace an existing landing zone's configuration wholesale. Preserve account/resource names, Control Tower settings, execution-role names, logging ownership, and existing customizations.
5. Validate offline, then run the customer's matching LZA validator and pipeline synth/diff in staging. Close every item in `customer-decisions.yaml` with actual evidence.

```bash
python -m pip install -r requirements.txt
python tools/validate.py
python tools/validate.py --ready
```

The first command checks structure with bundled upstream schemas and basic references. The `--ready` mode intentionally fails on the delivered package because placeholders and prerequisite decisions are open. Neither mode certifies compliance or replaces official LZA validation, AWS deployment, IAM analysis, or effectiveness testing.

Only the contents of `config/` belong in the LZA configuration source. `customer-decisions.yaml`, `docs/`, `schemas/`, and `tools/` are project support files and are not LZA configuration inputs. Depending on the installation, use the configuration repository or the configured S3 configuration ZIP workflow; retain its existing layout.

## Included settings

| Area | Proposed configuration |
| --- | --- |
| Deployment model | Customer-owned GovCloud organization; already provisioned accounts; no Control Tower in this example |
| Regions | `us-gov-west-1` only; multi-Region CloudTrail; second Region requires coordinated changes |
| Accounts | Management, LogArchive, Audit, Network, SharedServices, CUIProd, CUIDev, Sandbox |
| OUs | Security, Infrastructure, CUI-Production, CUI-Development, Sandbox, Quarantine |
| Governance | Approved-Region SCP and telemetry-protection SCP; quarantine automation deliberately disabled |
| Networks | Three separate /16 private VPCs, two AZs each, no internet gateway/NAT/TGW/hybrid route |
| Endpoints | Per-VPC S3 gateway plus SSM, SSM Messages, EC2 Messages, Logs, Monitoring, KMS, Secrets Manager, STS and EC2 interfaces |
| Sessions | Identity Center permission sets: 60 minutes; SSM idle: 15 minutes; SSM maximum: 60 minutes |
| Security | Config recorder/rules, GuardDuty with S3 protection/export, Security Hub FSBP, Access Analyzer, S3 account public access blocking, default EBS encryption |
| Logging | Organization CloudTrail with S3 data events, CloudWatch centralization, SSM session logging, VPC flow logs and DNS query logs |
| Retention proposal | CloudWatch: 365 days; S3 log lifecycle expiration: 2,555 days; archive transition at 365 days |
| Evidence | Separate retained KMS-encrypted bucket with 2,555-day default COMPLIANCE Object Lock, deployed through LZA customizations |
| Backups | Workload backup vaults only; plans, selections, vault protection, copies, and restore tests remain |

These numeric settings are proposed organizational policy values, not universal CMMC requirements. Identity Center's sign-in session, AWS role credentials, SSM sessions, WorkSpaces/OS lock, and application sessions are separate controls.

## Material implementation boundaries

- **No identity access is granted:** permission sets are defined, assignments are empty, and the IdP/MFA configuration is external.
- **No inspected egress or hybrid network exists:** isolated VPCs are a starting point. Package/EDR update paths and directory connectivity must be designed and tested.
- **FIPS is not configured end to end:** standard service endpoints appear in this baseline. Select and verify each required FIPS endpoint/client path before processing CUI.
- **The LZA central log bucket is not Object Locked by these files.** The custom evidence bucket is separate. Implement central log immutability under the proper resource owner and verify existing-object handling.
- **No log-failure alarms, SIEM connector, patch schedule, hardening association, EDR agent, workload backup plan, or Bedrock application is deployed.** Their completion steps and tests are explicit in the guide.
- **SCP protection is partial:** SCPs do not constrain the organization management account or service-linked roles. The telemetry policy does not protect every log object, KMS key, or IAM role. Protect those through appropriate resource/key/IAM policies and monitoring.
- **Object Lock COMPLIANCE retention on an object version cannot be shortened before expiry.** Approve retention before uploading objects. Retained KMS keys must remain enabled and recoverable; retaining a key resource alone does not prevent its later administrative deletion.
- **Costs need review:** three VPCs × nine interface endpoint services × two AZs = 54 endpoint ENIs, plus logging/data events, security services, storage, and processing. Remove unnecessary endpoints only after dependency analysis.

## Package layout

| Path | Purpose |
| --- | --- |
| `config/*-config.yaml` | Seven LZA configuration inputs |
| `config/service-control-policies/` | Region and telemetry SCP documents |
| `config/endpoint-policies/` | Account-scoped interface policy and S3 bootstrap policy |
| `config/iam-policies/` | Restricted operational read-only policy |
| `config/cloudformation/evidence-store.yaml` | Separate evidence-store custom stack |
| `customer-decisions.yaml` | Sixteen pending customer implementation/validation decisions |
| `docs/IMPLEMENTATION-STEPS.md` | Ordered actions, ownership and acceptance criteria |
| `docs/CHANGE-MATRIX.md` | File-level settings, rationale and remaining work |
| `docs/VALIDATION.md` | Actual checks performed and their limitations |
| `docs/SOURCES.md` | AWS/DoD source links and schema provenance |
| `schemas/` | Pinned upstream schema copies with AWS license/notice |
| `tools/validate.py` | Offline structural and readiness checker |

LZA supports infrastructure that helps meet technical requirements. CMMC assessment also depends on the scoped system, personnel, procedures, organizational responsibilities, and effective operation of the controls.
