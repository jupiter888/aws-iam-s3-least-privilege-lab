import json
from fnmatch import fnmatchcase
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def evaluate(policy, action, resource):
    statements = policy["Statement"]
    if isinstance(statements, dict):
        statements = [statements]

    allowed = False

    for statement in statements:
        actions = statement.get("Action", [])
        resources = statement.get("Resource", [])

        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]

        action_matches = any(
            fnmatchcase(action.lower(), pattern.lower())
            for pattern in actions
        )
        resource_matches = any(
            fnmatchcase(resource, pattern)
            for pattern in resources
        )

        if action_matches and resource_matches:
            if statement["Effect"] == "Deny":
                return "ExplicitDeny"
            if statement["Effect"] == "Allow":
                allowed = True

    return "Allow" if allowed else "ImplicitDeny"


def main():
    insecure = load_json(ROOT / "policies/insecure-s3-policy.json")
    restricted = load_json(
        ROOT / "policies/least-privilege-s3-policy.json"
    )
    cases = load_json(ROOT / "tests/authorization-test-cases.json")

    failures = 0

    for case in cases:
        actual_insecure = evaluate(
            insecure, case["action"], case["resource"]
        )
        actual_restricted = evaluate(
            restricted, case["action"], case["resource"]
        )

        passed = (
            actual_insecure == case["insecure_expected"]
            and actual_restricted == case["least_privilege_expected"]
        )

        status = "PASS" if passed else "FAIL"

        print(
            f'{case["id"]}: {status} | '
            f'Insecure={actual_insecure} | '
            f'LeastPrivilege={actual_restricted}'
        )

        if not passed:
            failures += 1

    print(f"\nResults: {len(cases) - failures}/{len(cases)} passed")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
