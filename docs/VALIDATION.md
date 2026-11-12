# Validation record

Checked 2026-11-09 against bundled LZA v1.17.0 schemas.

| Check | Observed result |
| --- | --- |
| Seven LZA YAML files against upstream Draft-07 JSON schemas | PASS |
| YAML/JSON parsing, referenced local assets | PASS |
| Account/OU target names, VPC CIDR/subnet overlap, local route-table references and endpoint policy references | PASS |
| Evidence-store CloudFormation template with cfn-lint | PASS, no diagnostics |
| Readiness gate on supplied starter | Expected FAIL: placeholders and all 16 customer prerequisites remain open |
| AWS LZA official semantic validator, synthesis and deployment | NOT RUN |
| Live GovCloud service/endpoint availability and IAM policy effectiveness | NOT TESTED |
| Log delivery, patching, FIPS, restore and CMMC control tests | NOT TESTED |

The schemas do not validate every LZA cross-file/business rule. Policy JSON syntax checking is not IAM Access Analyzer validation. The readiness checklist is a project gate based on declared completion, not independent evidence verification or certification. No AWS credentials were used and no AWS resources were changed.
