
# AWS IAM & S3 Least-Privilege Security Lab

## Executive Summary

An architecture-level security assessment of excessive Amazon S3 permissions assigned to a fictional research application's AWS IAM role.

The project demonstrates how an overprivileged IAM identity policy increases potential data exposure and destructive-operation risks, and how a least-privilege replacement narrows the permitted action and resource scope.

**Validation:** 5/5 synthetic authorization tests passed using a custom offline Python policy evaluator.

**Environment:** Local, offline, synthetic AWS resources. No AWS account, infrastructure deployment, or production data was used.

## Security Finding

**Finding:** Excessive S3 permissions granted to an application workload identity.

**Insecure configuration:**
- Action: `s3:*`
- Resource: `*`

**Least-privilege replacement:**
- Action: `s3:GetObject`
- Resource: `arn:aws:s3:::example-research-data/*`

The replacement preserves the application's required object-read permission while removing unnecessary S3 actions and access to unrelated resources within the tested policy model.

## Architecture and Threat Model

- [Architecture and trust boundaries](evidence/documentation/architecture.md)
- [STRIDE threat model and attack paths](evidence/documentation/threat-model.md)
- [Security controls and validation](evidence/documentation/security-controls.md)

The assessment considers unauthorized object reads, modification, deletion, bucket enumeration, credential misuse, and auditability.

## Policy Artifacts

- [Insecure IAM policy](policies/insecure-s3-policy.json)
- [Least-privilege IAM policy](policies/least-privilege-s3-policy.json)

Both policies use fictional resources and are provided for analysis and offline testing.

## Authorization Testing

The project includes five synthetic authorization test cases.

| Test | Scenario | Insecure | Least Privilege |
|---|---|---|---|
| TC-01 | Required object read | Allow | Allow |
| TC-02 | Object deletion | Allow | ImplicitDeny |
| TC-03 | Cross-bucket object read | Allow | ImplicitDeny |
| TC-04 | Object upload | Allow | ImplicitDeny |
| TC-05 | Bucket listing | Allow | ImplicitDeny |

**Result: 5/5 tests passed in the custom offline evaluator.**

### Evaluator Unit Test

TC-06 independently verifies that an explicit `Deny` statement overrides a matching `Allow` statement in the local Python evaluator.

Run the unit test:

```bash
python3 -B tests/test_explicit_deny.py
```

**Observed result:** 1/1 evaluator unit test passed.

This test validates the evaluator's explicit-deny precedence logic. It does not compare the two project policies or establish effective permissions in AWS.

[Evaluator unit test source](tests/test_explicit_deny.py)


### Reproduce the tests

From the repository root:

```bash
python3 tests/evaluate_policies.py
```

- [Test cases](tests/authorization-test-cases.json)
- [Python evaluator](tests/evaluate_policies.py)
- [Recorded test results](evidence/authorization-test-results.txt)

## Implementation Status

**Implemented and tested locally:**
- Action-level least-privilege policy definition
- Resource-level least-privilege policy definition
- Synthetic authorization test cases
- Limited offline policy evaluation

**Proposed, not implemented or tested:**
- Workload credential and role-assumption protections
- AWS audit logging and monitoring
- S3 recovery and data-protection controls
- AWS-native authorization validation

## Limitations and Residual Risk

The custom evaluator does not implement the complete AWS IAM authorization model. Its results must not be interpreted as effective permissions in an AWS account.

AWS resource policies, service control policies, permission boundaries, session policies, conditions, and operational security controls require separate evaluation.

A compromised workload identity could still read objects within its authorized scope.

## Project Outcome

This project demonstrates an architecture-focused workflow: identify excessive permissions, model security threats, design a least-privilege control, validate expected decisions in a defined offline model, and document residual risks.

The resulting artifacts provide a reproducible security assessment without relying on real credentials, production infrastructure, or confidential data.