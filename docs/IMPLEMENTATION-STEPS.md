# Implementation and additional completion steps

Status for this delivery: configuration prepared; offline validation performed; no AWS deployment or customer control testing. All D01–D16 items are pending. Complete the actual work before marking an item complete. Use `customer-decisions.yaml` to record evidence locations.

## Phase 1 — Boundary and deployment prerequisites

### D01 — System boundary and ownership — Customer security owner

1. Document CUI intake, storage, processing, transmission, administrative paths, endpoints and external service providers.
2. Identify CUI assets, security protection assets, and approved connections. Development accounts handling CUI remain in the assessed scope. Security logs can contain sensitive data and need scope and protection decisions.
3. Approve account/OU responsibilities and a data-flow diagram. Keep customer boundaries separate unless an approved shared-service design explicitly addresses isolation and responsibility.

Acceptance: signed boundary diagram, asset inventory, external dependencies, and responsibility matrix tied to the SSP.

### D02 — Accounts, enrollment, and execution role — Cloud platform owner

1. Provision or enroll GovCloud accounts using the organization's approved commercial/GovCloud account-vending approach. These files cover the GovCloud-side baseline only; they do not provision linked commercial accounts.
2. Replace placeholder account emails and IDs in `accounts-config.yaml`; verify each ID against the intended GovCloud account. Preserve mandatory LZA logical names Management, Audit and LogArchive.
3. Verify organization membership, OU placement, trusted access and required deployment roles in each account. Replace `OrganizationAccountAccessRole` with the actual existing management access role; do not rename existing roles blindly.
4. Confirm SNS operations mailbox ownership. Do not place CUI in account names, tags or emails.

Acceptance: account inventory verified with AWS Organizations and successful least-privilege deployment-role assumption.

### D03 — Release and current ownership — LZA maintainer

1. Obtain the current seven configuration files, custom assets, installed LZA version, installer parameters and configuration source.
2. Compare this v1.17.0 package to the deployed release's schemas. Backport supported changes or upgrade LZA using its documented procedure first.
3. The example uses `controlTower.enable: false`. If Control Tower exists, preserve its enabled configuration and determine which service owns organization trails, Config recorders, account enrollment and controls. Do not create competing owners for those resources.
4. Merge by logical resource name; review any rename/removal for replacement or deletion.

Acceptance: reviewed Git diff and resource-ownership table. No conflicting CloudTrail/Config/Identity Center ownership.

### D04 — Region policy and recovery — Architecture and security owners

1. Approve `us-gov-west-1` as the sole deployment Region, or choose an alternative.
2. If adding `us-gov-east-1`, update `enabledRegions`, the Region SCP, endpoint availability checks, regional templates, logging/key design and recovery runbook together. Merely enabling the Region does not create standby workloads.
3. Test the SCP's global-service exceptions and regional API behavior. Global exceptions are not an exfiltration boundary.

Acceptance: allowed-Region call succeeds; non-exempt denied-Region call fails; required global and deployment operations succeed.

## Phase 2 — Identity, network and cryptography

### D05 — CIDRs, AZs, DNS and endpoints — Network owner

1. Approve or replace `10.40.0.0/16`, `10.41.0.0/16`, and `10.42.0.0/16` against enterprise IPAM. Confirm account-specific AZ mappings and availability; replace AZ letters if necessary.
2. Inventory default VPC dependencies before leaving `defaultVpc.delete: true`. Remove/migrate dependencies first. Disable deletion during an existing-environment pilot if needed.
3. In the target GovCloud Region, run `aws ec2 describe-vpc-endpoint-services --region us-gov-west-1` and verify each requested service, supported AZs and `VpcEndpointPolicySupported` value. For a service without policy support, use `applyPolicy: false` only after documenting compensating SG/IAM/resource-policy controls.
4. Confirm private DNS resolution and TCP 443 from the intended node subnets to endpoint ENIs. Narrow `allowedCidrs` to approved subnets or use explicit endpoint SGs where required. Workload SGs still require explicit application rules.
5. Review `endpoint-policies/s3-bootstrap.json`: candidate AWS-owned bootstrap bucket names must match actual GovCloud dependencies. Add exact approved patch-manager/OS-repository buckets and instance-role permissions; endpoint permission alone does not authorize S3 access. The file is not a complete patching or cross-account data perimeter.
6. Test scoped AWS API calls, SSM registration, inventory, log upload, and DNS query delivery. Check that unsigned AWS-owned artifact downloads are handled intentionally.

Acceptance: successful private calls and denied unauthorized calls; no unexpected public fallback; DNS and flow-log samples from all three VPCs.

### D06 — Federation, MFA, sessions and emergency access — Identity owner

1. Enable the intended organization IAM Identity Center instance in the home Region before the IAM configuration is deployed. Connect the approved identity provider and provision the intended users/groups.
2. Enforce MFA, account lifecycle, access reviews and authentication policies at the actual identity source. An IAM user password policy does not configure the IdP.
3. Add `identityCenterAssignments` under `iam-config.yaml`, mapping verified group names and permission sets to explicitly approved account targets. Do not give routine administrators access to Management or LogArchive by default.
4. Limit PlatformAdmin membership; create a separate scoped deployment/operator role when needed. The Operator permission set is read-only metadata and cannot start SSM sessions or read CUI logs. Add scoped session permissions only after approving instance tags, session document ARNs, KMS permissions and termination rights.
5. Test 60-minute permission-set sessions independently of workforce sign-in duration. Configure workstation lock, WorkSpaces idle/disconnect, and application timeouts separately.
6. Establish monitored emergency credentials with protected recovery methods and a periodic recovery exercise. Restrict SSH and port-forwarding session documents if full shell session logging is required; these session types do not provide equivalent command-content logging.

Example assignment to merge after verifying the real group name:

```yaml
identityCenterAssignments:
  - name: CUIProdSecurityAudit
    permissionSetName: CMMC-SecurityAudit
    principals:
      - type: GROUP
        name: REPLACE-VERIFIED-SECURITY-GROUP
    deploymentTargets:
      accounts:
        - CUIProd
```

Acceptance: authorized/unauthorized login and role tests, MFA evidence, session-duration tests and monitored emergency access exercise.

### D07 — SCP exceptions and deployment safety — Security and LZA owners

1. Inspect actual LZA/CloudFormation execution principal ARNs. Replace the sample `AWSAccelerator-*` role-name exception with the narrowest tested deployment principals supported by the installation.
2. Prevent ordinary administrators from creating, changing or assuming exempt deployment roles or changing their trust/policies. Role-name exemptions are a bypass if those names are not protected.
3. Pilot in a staging OU. Test required LZA deployments, log subscriptions, operational log-group provisioning and emergency procedures before wider attachment. Add scoped workload log-retention automation exceptions if required.
4. Confirm protection of log objects, bucket policies, KMS keys, Config rules and IAM roles through separate controls; the provided SCP covers selected telemetry management APIs only.
5. The Quarantine OU has no quarantine SCP and new-account quarantine is disabled. If needed, create a restrictive policy, use tested onboarding exceptions, configure LZA `quarantineNewAccounts`, and test successful release and failed-pipeline recovery.

Acceptance: recorded policy tests, successful pipeline run, denied tampering by ordinary roles, and a documented rollback path. SCPs do not apply to the management account or service-linked roles.

### D09 — FIPS and CUI encryption paths — Security engineering owner

1. Inventory the CUI paths: application TLS, database connections, storage, administrative access, service APIs and hybrid VPN/Direct Connect paths.
2. Select service-specific AWS FIPS endpoints and validated cryptographic modules as required. Verify GovCloud interface-endpoint availability and private DNS behavior for the exact endpoint. Do not assume adding `-fips` to every service name is valid.
3. Configure SDK/CLI/client FIPS settings where supported, and verify traffic does not silently fall back. Verify application/OS libraries and certificates separately.
4. Verify transport encryption over the actual path; private networking and generic TLS alone are not evidence of FIPS validation.

Acceptance: service/endpoint/module inventory, client configuration, connection tests and retained evidence for the scoped paths. This baseline does not claim FIPS completion.

## Phase 3 — Logging, operations and recovery

### D08 — Retention and immutability — Records and security owners

1. Approve 365-day CloudWatch retention and 2,555-day S3 retention or replace them consistently. Check lifecycle transitions, retrieval timing, legal hold and cost. These values are proposed policy, not CMMC-prescribed periods.
2. Review `customizations-config.yaml` before deploying the evidence-store stack. Its evidence objects get COMPLIANCE retention and its bucket/key are retained on stack deletion/replacement. COMPLIANCE retention for existing object versions cannot be shortened by changing the template.
3. Implement immutability on the **actual LZA central log bucket** under its owning IaC, or use a supported pre-created/imported Object-Locked bucket with appropriate policies and key integration. Do not deploy a second stack that also owns the same bucket. The separate evidence store does not solve central log immutability.
4. Verify bucket versioning, default retention, existing-version retention/backfill, delivery-service permissions, replication behavior if used, and deletion-denial behavior. Review CloudTrail buckets separately from the central aggregation bucket.
5. Restrict key disable/deletion and bucket administration; separate evidence readers, writers and key administrators. Preserve KMS key availability throughout retention. The evidence key's account-IAM delegation is only a starting point.

Acceptance: actual-bucket Object Lock configuration, protected object-version sample, delivery test, key administration review and customer retention approval.

### D10 — Managed nodes, patching, hardening and malware protection — Endpoint owner

1. Attach the `CMMC-ManagedNodeRole` instance profile to approved EC2 instances or merge equivalent permissions into their existing workload role. Do not overwrite application role requirements.
2. Install/update SSM Agent and CloudWatch Agent; supply a scoped agent configuration for OS/security/application logs and required KMS/service permissions. No EC2 instances or agents are created by these files.
3. Define OS-specific patch baselines, approval delays, maintenance windows, target tags, reboot rules and exception handling. Permit approved patch repositories through private mirrors or controlled egress and add exact S3 bucket permissions.
4. Deploy approved hardening through images/State Manager/other tooling. Enforce IMDSv2 in launch templates; the supplied Config rule only detects violations.
5. Onboard approved malware/EDR tooling, configure scanning and updates, and route detections/agent health to the response team. GuardDuty does not replace endpoint malware protection. WorkSpaces requires its own endpoint/agent design and credentials.
6. Define a controlled runbook lifecycle with execution roles, approval gates, versioning and triggers. Native `centralSecurityServices.ssmAutomation.documentSets` can distribute supported runbook documents; more complex associations/triggers belong in separate custom templates. This starter defines no remediation runbooks.

Acceptance: managed-node inventory, patch scan/install reports, hardening evaluation, EDR health/detection test and SSM session log sample.

### D11 — Complete log coverage and failure alerting — Security operations owner

1. Build a source/account/Region/destination/owner/retention inventory. Confirm organization CloudTrail status and log validation, Config coverage, S3 data-event selectors, DNS/flow logs, SSM session records, application/OS/database/EDR logs and any Bedrock logs.
2. Review organization-wide S3 data-event volume/cost; use supported scoped selectors if required. Lambda data events are disabled in this proposal and must be enabled or separately scoped when relevant to the control design.
3. Confirm SNS email subscriptions and route alerts to an actively monitored queue. Email configuration is not evidence of operational response.
4. Add a scheduled read-only health checker for CloudTrail `GetTrailStatus` (including delivery errors and last-delivery timestamps), Config recorder/channel status and central-log freshness. Publish health metrics; alert on explicit failure and missing expected heartbeats.
5. Add appropriate pipeline metrics: CloudWatch subscription delivery errors/throttling, Firehose delivery success/freshness, EventBridge failed invocations and DLQs, and collector/agent heartbeat status. Thresholds and missing-data behavior must fit each source.
6. Generate scheduled identifiable canary events and verify them at the final destination. Alert on missing canaries using a separate monitoring path so a failed log path does not also silence its own failure alarm.
7. If Sentinel or another SIEM is used, deploy the actual connector and approved authentication/networking. Verify ingestion, schema parsing, duplicate handling, alerting and ticket routing. Review the receiving environment against the approved CUI/security-protection-data boundary.
8. Test controlled failures in staging and retain timestamps and alert/ticket records. The supplied security configuration has empty metric/alarm sets; no failure detector is deployed.

Acceptance: end-to-end trace per source; simulated pipeline failure produces a timely actionable ticket; documented on-call owner and log-review procedure.

### D12 — Workload keys and backup recovery — Workload and recovery owners

1. `CUIDataKey` is created only in the CUI accounts. Grant approved services/roles scoped access and select the key in workload storage/database definitions. The account default EBS encryption setting here is not bound to that custom key.
2. Review LZA-generated and workload key policies, eligible-key rotation, grants, log access and recovery. Rotation does not retroactively re-encrypt existing data.
3. The provided backup vaults are empty until backup plans, schedules, resource selections and IAM permissions are added. Configure these in supported LZA fields or custom stacks with a single resource owner.
4. Decide immutability/vault lock and cross-account/Region copies based on RPO/RTO. Pilot irreversible vault lock settings before production use.
5. Perform a restore to an isolated environment and validate data, application startup, key access and recovery time.

Acceptance: encryption/key-policy evidence, successful backups, isolated restore results, and measured recovery objectives.

### D13 — Egress, hybrid access and DNS policy — Network owner

1. Decide whether isolated operation is sufficient. These VPCs have local routes and private endpoints only; there is no TGW, VPN, Direct Connect, internet gateway or NAT.
2. For required connectivity, define TGW route-table separation and explicit allowed flows. Add centralized or distributed inspection, symmetric routing and allowed egress destinations using a reviewed topology.
3. Configure resolver inbound/outbound endpoints and forwarding rules for the actual directories/domains. Add DNS Firewall rules where required; query logging alone does not filter DNS.
4. Add application SG rules and verify east-west separation. Default VPC SG rules are removed, but explicit workload SGs still need to be created.
5. Test production/development isolation, hybrid DNS, inspection bypass prevention, permitted updates, and denied egress.

Acceptance: approved connectivity diagram, routes and firewall rule review, observed traffic-path tests, and denied-flow evidence. If a feature is out of scope, record the approved rationale.

### D14 — Bedrock and container extensions — AI/platform owners, if in scope

1. Confirm exact Bedrock models/features and endpoints available in the chosen GovCloud Region. Add only required runtime/control/agent endpoints and approved IAM actions to the intended VPC/account.
2. Define guardrails, evaluation, prompt-injection defenses, approved tools, data sources and human approval for changes to infrastructure. Deploy application resources through LZA customizations or a separately owned pipeline.
3. Configure Bedrock invocation logging explicitly. S3 invocation log destinations must be in the same account/Region; design any central replication/forwarding separately. Review prompt/response sensitivity and retention.
4. For containers, add ECR API/Docker and S3 access plus EKS/ECS endpoints/permissions actually required. Scope repository access and test private image pulls.
5. Do not route CUI to commercial-partition models as a fallback without a separately approved data-flow and compliance design.

Acceptance: private invocation/image-pull tests, model/feature availability record, IAM denial tests, approved data paths and sensitive-log access tests; or approved exclusion if unused.

## Phase 4 — Evidence and release

### D15 — Evidence and operating procedures — Customer compliance owner

1. Populate the separate evidence bucket using approved exports/jobs; create scoped writer/reader roles and encryption permissions. The template creates storage only.
2. Record actual configurations, policy documents, asset inventories, tests, tickets, approvals, log reviews and restore results. Protect evidence access and retention.
3. Map each relevant CMMC assessment objective to the implemented mechanism, responsible party and evidence. Use AWS Artifact customer responsibility/compliance materials for inherited portions; do not equate a Config/Security Hub score with full compliance.
4. Complete the SSP, access reviews, incident response, training, personnel/process requirements and recurring operational tasks.

Acceptance: traceable control/evidence matrix, current SSP, assigned owners and demonstrable operating procedures.

### D16 — Validate and deploy — LZA maintainer

1. Run `python tools/validate.py` after edits. Optionally install `cfn-lint` and lint `config/cloudformation/evidence-store.yaml`.
2. Use the exact installed LZA source/build environment and run its official configuration validator against the merged configuration. In a built matching source tree, the v1.17.0 script is `yarn validate-config /absolute/path/to/config`; supply the GovCloud partition/Region and credentials required by that environment. Example environment prefix: `PARTITION=aws-us-gov AWS_REGION=us-gov-west-1`. The official validator may require real account/organization access.
3. Run the existing pipeline validation/synthesis/review process; inspect the CDK/CloudFormation diff, especially replacements, SCP attachments, Config/CloudTrail ownership, bucket changes and IAM trust. Do not edit generated templates as the source of truth.
4. Deploy a staging/customer pilot, then run D04–D15 acceptance tests. Review endpoint/logging/security costs before broader rollout.
5. Promote the reviewed commit through the approved production pipeline. Preserve the prior configuration commit and rollback instructions. A Git rollback cannot undo compliance retention or automatically restore deleted/replaced resources.
6. Mark checklist entries complete only with actual acceptance evidence. Run `python tools/validate.py --ready` as a project gate. This gate reports declared completion, not an independent certification.

Acceptance: official validator output, reviewed synth/diff, deployment record, successful acceptance tests and approved production release.
