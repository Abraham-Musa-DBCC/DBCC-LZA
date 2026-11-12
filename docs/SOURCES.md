# Source references and provenance

Reviewed 2026-11-09. AWS/DoD guidance supports the architecture; numeric timeout/retention settings in this package are proposed customer policy, not quoted CMMC mandates.

- [AWS LZA v1.17.0 source](https://github.com/awslabs/landing-zone-accelerator-on-aws/tree/v1.17.0), commit `6f3c35300f7dd487f61ee0f4c9c3170e4e1f9a16`.
- Bundled JSON schemas copied from `source/packages/@aws-accelerator/config/lib/schemas/` at that commit. AWS Apache 2.0 license and notice are included under `schemas/`.
- [LZA configuration files](https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/using-configuration-files.html).
- [LZA configuration best practices](https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/configuration-file-best-practices.html).
- [GovCloud deployment options](https://docs.aws.amazon.com/solutions/latest/landing-zone-accelerator-on-aws/deployment-options-for-aws-govcloud-us-workloads.html).
- [GovCloud LZA sample design](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.17.0/sample-configurations/govcloud-us/).
- [LZA centralized logging](https://awslabs.github.io/landing-zone-accelerator-on-aws/v1.17.0/user-guide/logging/).
- [GovCloud VPC endpoint availability](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/using-govcloud-vpc-endpoints.html).
- [GovCloud service endpoints](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/using-govcloud-endpoints.html).
- [AWS FIPS endpoints and validation guidance](https://aws.amazon.com/compliance/fips/).
- [Systems Manager VPC endpoint prerequisites](https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-create-vpc.html).
- [SSM Agent technical details and AWS-managed S3 dependencies](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-technical-details.html).
- [Patch operation S3 bucket reference](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-operations-s3-buckets.html). Verify GovCloud-specific bucket names from the supported service documentation/account testing rather than assuming standard-partition names.
- [Amazon S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html).
- [Amazon Bedrock GovCloud differences](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-bedrock.html).
- [Bedrock invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html).
- [AWS CMMC shared responsibility considerations](https://docs.aws.amazon.com/prescriptive-guidance/latest/cmmc-level-2-compliance-on-aws/aws-cloud-considerations.html).
- [DoD CMMC resources and assessment guides](https://dodcio.defense.gov/CMMC/Resources-Documentation/).

Release-specific source checks also confirmed that Identity Center permission-set `sessionDuration` is converted from minutes and IAM role `maxSessionDuration` is interpreted as seconds. Endpoint policy files use LZA's policy replacement machinery, including `${ACCOUNT_ID}`. Do not replace CloudFormation pseudo-parameters in the custom template.
