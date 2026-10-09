
# AWS IAM & S3 Least-Privilege Security Lab

## Threat Model

### 1. Scope and Objectives

This assessment evaluates excessive Amazon S3 permissions assigned to a fictional research application's IAM role.

The application requires read-only access to objects within the `example-research-data` bucket.

The insecure baseline permits `s3:*` on `*`. The least-privilege replacement permits only `s3:GetObject` on `arn:aws:s3:::example-research-data/*`.

No AWS infrastructure was deployed. Authorization testing used synthetic requests and a limited offline Python evaluator.

### 2. Assets and Security Objectives

| Asset | Security Objective |
|---|---|
| Research data | Preserve confidentiality and integrity |
| S3 objects | Prevent unauthorized reads, writes, and deletion |
| Workload IAM role | Minimize permissions and credential exposure |
| Other S3 resources | Prevent unintended cross-resource access |
| IAM policy definitions | Maintain controlled, reviewable authorization |

### 3. Trust Boundaries

**TB-01 — Workload identity:** The fictional research application uses an IAM role to authorize AWS requests. Credential issuance and role assumption were not simulated.

**TB-02 — AWS authorization:** AWS evaluates applicable authorization controls before permitting S3 operations. Our offline evaluator models only a subset of identity-based policy decisions.

**TB-03 — Resource scope:** The intended permission boundary limits object reads to the designated research-data bucket.

**TB-04 — Offline assessment:** Synthetic requests and local IAM policy JSON files are processed by the Python evaluator. No communication with AWS occurs.

### 4. STRIDE Threat Assessment

| ID | STRIDE Category | Threat | Potential Impact |
|---|---|---|---|
| T-01 | Spoofing | Stolen workload credentials allow an attacker to impersonate the application | Unauthorized actions using the workload identity |
| T-02 | Tampering | Excessive S3 permissions permit unauthorized object modification | Loss of data integrity |
| T-03 | Repudiation | Insufficient audit logging prevents reliable attribution of S3 operations | Reduced incident investigation capability |
| T-04 | Information Disclosure | Wildcard resource permissions permit unintended object reads | Exposure of unrelated research or business data |
| T-05 | Denial of Service | Excessive permissions permit destructive S3 operations | Data loss or service disruption |
| T-06 | Elevation of Privilege | A compromised workload identity possesses capabilities beyond its business requirements | Increased attacker capability and impact |

These threats are hypothetical. No attacks against AWS infrastructure were performed.

### 5. Attack Paths

#### AP-01 — Cross-Bucket Data Exposure

1. An attacker compromises the research application's workload identity.
2. The attacker requests an object from an unrelated S3 bucket.
3. The insecure identity policy allows `s3:GetObject` on the requested object.
4. Access may succeed unless another applicable AWS authorization control prevents it.

**Related threat:** T-04 — Information Disclosure.

**Validation:** TC-03 demonstrated that the insecure policy allowed the synthetic cross-bucket read, while the least-privilege policy returned `ImplicitDeny`.

**Mitigation:** Restrict the identity policy's resource ARN to objects within the designated research-data bucket.

#### AP-02 — Unauthorized Object Deletion

1. An attacker compromises or misuses the workload identity.
2. The attacker requests deletion of an S3 object.
3. The insecure identity policy permits `s3:DeleteObject`.
4. Data loss or service disruption may occur if other controls do not prevent the operation.

**Related threats:** T-02 — Tampering; T-05 — Denial of Service.

**Validation:** TC-02 demonstrated that the insecure policy allowed the synthetic deletion request, while the least-privilege policy returned `ImplicitDeny`.

**Mitigation:** Remove unnecessary delete permissions. Consider S3 Versioning, recovery protections, and appropriate monitoring.

#### AP-03 — Unauthorized Object Modification

1. An attacker compromises or misuses the workload identity.
2. The attacker submits an S3 object write request.
3. The insecure identity policy permits `s3:PutObject`.
4. Research data may be modified or replaced.

**Related threat:** T-02 — Tampering.

**Validation:** TC-04 demonstrated that the insecure policy allowed the synthetic write request, while the least-privilege policy returned `ImplicitDeny`.

**Mitigation:** Restrict the role to required read operations.

#### AP-04 — Excessive Bucket Enumeration

1. An attacker gains the ability to use the workload identity.
2. The attacker requests a listing of objects within an S3 bucket.
3. The insecure identity policy permits `s3:ListBucket`.
4. Object names and associated listing metadata may become visible.

**Related threat:** T-04 — Information Disclosure.

**Validation:** TC-05 demonstrated that the insecure policy allowed the synthetic bucket-listing request, while the least-privilege policy returned `ImplicitDeny`.

**Mitigation:** Omit `s3:ListBucket` when the application does not require bucket listing.

### 6. Security Controls and Threat Traceability

| Control | Description | Related Threats | Implementation Status |
|---|---|---|---|
| SC-01 | Restrict S3 actions to `s3:GetObject` | T-02, T-05, T-06 | Defined and tested offline |
| SC-02 | Restrict resource ARNs to designated research-data objects | T-04, T-06 | Defined and tested offline |
| SC-03 | Protect workload credentials and role assumption | T-01 | Proposed; not implemented |
| SC-04 | Enable appropriate S3 and IAM audit logging | T-03 | Proposed; not implemented |
| SC-05 | Apply versioning, recovery, and data protection controls | T-02, T-05 | Proposed; not implemented |
| SC-06 | Validate effective permissions using AWS-native tools | T-01 through T-06 | Proposed; not implemented |

SC-01 and SC-02 were evaluated only in the custom offline Python evaluator. No AWS infrastructure or production security controls were deployed.

### 7. Validation Evidence

Five synthetic authorization tests were executed against both policy definitions.

| Test | Scenario | Insecure Policy | Least-Privilege Policy |
|---|---|---|---|
| TC-01 | Authorized object read | Allow | Allow |
| TC-02 | Object deletion | Allow | ImplicitDeny |
| TC-03 | Cross-bucket object read | Allow | ImplicitDeny |
| TC-04 | Object upload | Allow | ImplicitDeny |
| TC-05 | Bucket listing | Allow | ImplicitDeny |

**Observed result:** 5/5 tests passed in the custom offline Python evaluator.

[Authorization test evidence](../authorization-test-results.txt)

These results do not establish effective permissions in AWS. The evaluator supports only a limited subset of IAM identity-policy semantics.

#### Additional Evaluator Validation — TC-06

A separate unit test verifies explicit `Deny` precedence over a matching `Allow` statement in the custom offline evaluator.

**Test:** [Explicit Deny precedence unit test](../../tests/test_explicit_deny.py)

**Observed result:** TC-06 passed (1/1).

This unit test validates evaluator behavior, not the effectiveness of either project policy in AWS.

**Combined validation:** 5/5 policy-comparison tests and 1/1 evaluator unit test passed.

### 8. Residual Risks and Limitations

**RR-01 — Credential compromise:** Least privilege reduces potential impact but does not prevent workload credential theft or misuse.

**RR-02 — Authorized data exposure:** A compromised workload identity could still read objects within its permitted resource scope.

**RR-03 — Other AWS policies:** Resource policies, service control policies, permission boundaries, and session policies were not evaluated.

**RR-04 — IAM conditions:** The custom evaluator does not implement condition evaluation.

**RR-05 — Operational controls:** Logging, alerting, versioning, backup, and recovery mechanisms were not deployed or tested.

**RR-06 — Simulation fidelity:** The local evaluator does not reproduce the complete AWS authorization decision process.

### 9. Assessment Conclusion

The insecure baseline grants substantially more S3 permissions than the fictional research application requires.

The least-privilege replacement preserves the required object-read capability while removing unnecessary actions and resource scope within the limited offline evaluation model.

The five executed tests support this conclusion within the model's defined scope.

Production adoption would require AWS-native authorization validation, review of interacting policies, and operational security controls.
