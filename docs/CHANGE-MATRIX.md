# Proposed changes and remaining actions

Current deployed values are unknown because no customer configuration was supplied. Each row is a proposed baseline, not an observed current-to-new diff. The Dxx references link to detailed steps in `IMPLEMENTATION-STEPS.md`.

| File / setting | Proposed value or behavior | Additional steps / evidence |
| --- | --- | --- |
| `accounts-config.yaml` | Eight logical accounts with dedicated Audit/LogArchive | D01–D03: real GovCloud accounts, emails/IDs, enrollment, execution roles, ownership |
| `organization-config.yaml` | Security, Infrastructure, CUI production/development, Sandbox and Quarantine OUs | D01/D02: approve boundaries; OU structure alone does not enforce isolation |
| Region SCP | Deny non-exempt API operations outside us-gov-west-1 | D04/D07: global-service exceptions, recovery Region, staging and pipeline tests |
| Telemetry SCP | Deny selected logging/security management operations except sample deployment roles | D07: narrow/protect exceptions, cover omitted bucket/key/IAM threats, test administration paths |
| Quarantine | New-account quarantine disabled; OU present | D07: add actual SCP and recovery/release workflow if required |
| `global-config.yaml` | Non-Control-Tower organization example; management access role OrganizationAccountAccessRole | D03: preserve actual installation ownership/settings; resolve existing Config/trail resources |
| CloudTrail | Organization/multi-Region trail, management and S3 data events, CloudWatch delivery | D11: verify delivery/validation, selectors and cost; Lambda data events currently disabled |
| Central log and CloudTrail S3 lifecycle | 365-day Glacier transition, 2,555-day expiration | D08: customer approval, retrieval needs, Object Lock design and existing-version retention |
| CloudWatch logs | Centralization and CMK encryption; 365-day retention | D11: collector configuration, IAM/KMS delivery, subscription coexistence, failure metrics |
| SSM sessions | S3 + CloudWatch logging, 15-minute idle, 60-minute maximum, streaming | D06/D10: node profile and agents, client/session restrictions, session tests |
| SNS Security topics | Operations mailbox placeholder | D11: real address, confirmed subscriptions, routing/on-call, test ticket |
| SSM inventory | Enabled for Infrastructure and CUI OUs | D10: node registration, supported platforms, inventory health |
| Backup vaults | Vault per CUI account | D12: plans, selections, schedules, IAM, protection, copies, restores |
| `network-config.yaml` default VPC | Delete default VPCs in managed scope | D05: dependency inventory and migration before enabling deletion on an existing system |
| Private VPCs | CUIProd 10.40/16; CUIDev 10.41/16; SharedServices 10.42/16; two /24 subnets each | D05/D13: approve IPAM/AZs; supply explicit workload SG rules and approved connectivity |
| Transit Gateway | CMMC-TGW in Network account (ASN 64512), shared to CUI/Infrastructure OUs; single shared route table with explicit association/propagation; TGW flow logs to S3 | D05/D13: approve inter-VPC flows, segmentation/inspection needs, TGW route-table isolation and RAM share scope |
| VPC routing | S3 gateway endpoints plus TGW routes to all peer VPC CIDRs; no IGW/NAT/default internet route or hybrid path | D13: inspected egress, directory/hybrid routes and isolation tests if required |
| Gateway/interface endpoints | S3 and nine interface services per VPC | D05/D09: availability, endpoint policies, FIPS selection, DNS and connection tests |
| Endpoint policies | Own-account principal restriction; selected AWS S3 bootstrap reads | D05: exact AWS-owned buckets, signed/unsigned requests, instance IAM, resource scoping and cross-account use |
| VPC flow and DNS query logs | S3 destinations, all traffic, 60-second flow aggregation | D05/D11: delivered records, source inventory, access/retention; DNS filtering is separate |
| `security-config.yaml` | Audit delegation, Config recorder/rules, GuardDuty/export, Security Hub FSBP + NIST 800-53 Rev 5 + CIS v3.0.0, region aggregation, CloudWatch finding logging, Access Analyzer | D03/D11: supported services/rules in Region, existing-service ownership, complete account coverage and findings routing |
| S3 public access block / EBS encryption | Enabled | D12: inspect existing resources; default encryption does not retrofit all data or select the custom CUI key |
| CUIDataKey | Rotating retained key in CUI OUs | D12: service/application selection, key policies, grants and recovery; rotation alone is not a complete encryption control |
| IAM password policy | 14 chars, complexity, 24 remembered, 90-day age | D06: approve policy for remaining IAM users; federation password/MFA is controlled at the IdP |
| Config evaluations | Encryption, S3 access/TLS, CloudTrail, root MFA/keys, EC2 public IP/IMDSv2, key rotation, SSM management | D10/D15: rules detect only; resolve findings and map evidence to the actual assessment objectives |
| SSM automation documents | Empty | D10: deploy controlled documents, execution roles, approvals, associations/triggers if needed |
| CloudWatch metric/alarm sets | Empty | D11: implement delivery-failure checks, independent canaries, thresholds and response routing |
| `iam-config.yaml` node role | SSM/CloudWatch Agent managed policies and instance profile, all accounts | D10: attach only to approved nodes, install/configure agents, review managed-policy breadth and add required artifact permissions |
| Identity Center permission sets | SecurityAudit, PlatformAdmin and operational metadata reader; 60 minutes | D06: enable Identity Center, configure IdP/MFA, verified group assignments, access reviews and emergency access |
| Identity Center assignments | Empty | D06: nobody is granted access by these files until approved assignments are added |
| `customizations-config.yaml` | Evidence-store custom stack in LogArchive; Security Hub findings/alerts/insights stack in Audit | D08/D11/D15: approve compliance retention, define evidence exports and scoped key/bucket access; confirm SNS subscription, finding delivery and insight queries |
| `cloudformation/evidence-store.yaml` | Versioned SSE-KMS bucket, public access blocked, TLS-only, default 2,555-day COMPLIANCE retention | D08: irreversible object retention decision; central log bucket remains separately managed; protect KMS availability |
| `cloudformation/security-hub.yaml` | KMS-encrypted S3 finding-export bucket with COMPLIANCE Object Lock, Firehose delivery, EventBridge rules for all and high/critical findings, SNS alerts, CloudWatch Logs, four CMMC-relevant Security Hub insights | D08/D11: confirm finding delivery to S3/CloudWatch, SNS subscription/alerting, insight query results; does not create Hub or Standard resources (LZA-managed) |
| Bedrock/containers | Not deployed in foundation package | D14: add required supported services, endpoints, policies, logs and application resources when in scope |
| WorkSpaces/OS/EDR | Not deployed/configured | D06/D10: OS lock/session policy, patching, malware protection and operating evidence |
| Multi-Region DR | Not deployed | D04/D12: approved recovery Region, SCP alignment, backup replication, workload recovery and test |
