
from evaluate_policies import evaluate


def test_explicit_deny_precedence():
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*",
            },
            {
                "Effect": "Deny",
                "Action": "s3:DeleteObject",
                "Resource": "*",
            },
        ],
    }

    resource = "arn:aws:s3:::example-research-data/test.txt"

    result = evaluate(policy, "s3:DeleteObject", resource)

    assert result == "ExplicitDeny", (
        f"Expected ExplicitDeny, received {result}"
    )

    print("TC-06: PASS | Explicit Deny overrides Allow")


if __name__ == "__main__":
    test_explicit_deny_precedence()
