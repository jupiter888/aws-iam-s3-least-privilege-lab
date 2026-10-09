
# AWS IAM & S3 Least-Privilege Security Lab

## Security Controls and Validation

### 1. Purpose

This document defines security controls for a fictional research application using an AWS IAM role to access Amazon S3.

The assessment compares an overprivileged identity policy with a least-privilege replacement.

Only local policy definitions and a limited offline authorization evaluator were implemented. No AWS resources or production security controls were deployed.

### 2. Security Control Register

| ID | Control | Objective | Status |
|---|---|---|---|
| SC-01 | Action-level least privilege | Restrict the role to required S3 actions | Defined and tested offline |
| SC-02 | Resource-level least privilege | Restrict access to designated research objects | Defined and tested offline |
| SC-03 | Workload identity protection | Reduce credential theft and misuse risk | Proposed; not implemented |
| SC-04 | Audit logging and monitoring | Support detection and investigation | Proposed; not implemented |
| SC-05 | Data protection and recovery | Reduce impact of modification or deletion | Proposed; not implemented |
| SC-06 | AWS-native authorization validation | Verify effective permissions in AWS | Proposed; not implemented |

### 3. Control Specifications

#### SC-01 — Action-Level Least Privilege

**Requirement:** The research application must only have the S3 actions necessary for its business function.

**Implementation:** The local least-privilege policy defines `s3:GetObject` rather than `s3:*`.

**Acceptance criteria:**
- Authorized object reads are permitted.
- Object deletion is not permitted by this identity policy.
- Object uploads are not permitted by this identity policy.
- Bucket listing is not permitted by this identity policy.

**Validation:** TC-01, TC-02, TC-04, TC-05.

**Observed status:** Passed in the custom offline evaluator. Not deployed or validated in AWS.

#### SC-02 — Resource-Level Least Privilege

**Requirement:** The workload identity must be restricted to the designated research-data objects.

**Implementation:** The local least-privilege policy specifies `arn:aws:s3:::example-research-data/*`.

**Acceptance criteria:**
- Reads of objects within the designated bucket are permitted.
- Reads of objects outside the designated bucket are not permitted by this identity policy.

**Validation:** TC-01 and TC-03.

**Observed status:** Passed in the custom offline evaluator. Not deployed or validated in AWS.

#### SC-03 — Workload Identity Protection

**Requirement:** Protect workload credentials and limit unauthorized role assumption.

**Proposed controls:** Use appropriately scoped IAM role trust policies, temporary credentials, and workload-specific identity configuration.

**Acceptance criteria:** Only authorized workloads can assume the role; credentials are not embedded in source code or configuration artifacts.

**Status:** Proposed; not implemented or tested.

#### SC-04 — Audit Logging and Monitoring

**Requirement:** Record security-relevant IAM and S3 activity to support detection and investigation.

**Proposed controls:** Configure appropriate AWS CloudTrail logging, including relevant S3 data events, and alerts for suspicious access or policy changes.

**Acceptance criteria:** Relevant events are captured, retained, and available for investigation; alerting is validated.

**Status:** Proposed; not implemented or tested.

#### SC-05 — Data Protection and Recovery

**Requirement:** Reduce the impact of accidental or malicious modification and deletion.

**Proposed controls:** Evaluate S3 Versioning, backup or replication requirements, and recovery procedures based on data criticality.

**Acceptance criteria:** Recovery objectives are defined and restoration procedures are tested.

**Status:** Proposed; not implemented or tested.

#### SC-06 — AWS-Native Authorization Validation

**Requirement:** Validate effective permissions before deploying the policy to production.

**Proposed controls:** Use AWS IAM policy validation and simulation where applicable, review interacting policies, and conduct authorized integration testing.

**Acceptance criteria:** Required actions succeed and prohibited actions fail in the intended AWS environment, accounting for relevant identity, resource, organization, and session controls.

**Status:** Proposed; not implemented or tested.

### 4. Offline Validation Matrix

| Test | Control | Insecure Policy | Least-Privilege Policy | Result |
|---|---|---|---|---|
| TC-01 | SC-01, SC-02 | Allow | Allow | PASS |
| TC-02 | SC-01 | Allow | ImplicitDeny | PASS |
| TC-03 | SC-02 | Allow | ImplicitDeny | PASS |
| TC-04 | SC-01 | Allow | ImplicitDeny | PASS |
| TC-05 | SC-01 | Allow | ImplicitDeny | PASS |

**Observed result:** 5/5 test cases passed in the custom offline evaluator.

[Authorization test evidence](../authorization-test-results.txt)


#### Additional Evaluator Unit Test — TC-06

**Purpose:** Verify that an explicit `Deny` statement overrides a matching `Allow` statement in the local evaluator.

**Test:** [Explicit Deny precedence unit test](../../tests/test_explicit_deny.py)

**Execution command:**

```bash
python3 -B tests/test_explicit_deny.py
```

**Observed result:** 1/1 evaluator unit test passed.

TC-06 validates evaluator behavior independently of the five policy-comparison tests. It does not establish effective AWS permissions.

**Combined local validation:** 5/5 policy-comparison tests and 1/1 evaluator unit test passed.

### 5. Residual Risks

Even with the least-privilege policy, the following risks remain:

- Credential compromise could expose authorized research objects.
- Other AWS policies and authorization mechanisms could affect effective access.
- The offline evaluator does not implement the complete AWS IAM authorization model.
- Audit logging, monitoring, recovery, and AWS-native policy validation have not been performed.

### 6. Implementation Summary

**Implemented and tested locally:** SC-01 and SC-02, within the limited offline evaluation model.

**Proposed but not implemented:** SC-03, SC-04, SC-05, and SC-06.

No production controls were deployed, and no AWS authorization behavior was directly tested.
