"""The shared preset never turns on automerge.

Every repo that extends `local>dvystrcil/renovate-config` inherits what
default.json sets, on its next Renovate run. An automerge rule here would
merge PRs, unreviewed, in every one of them, including repos where a merge
is a deployment. A repo that wants automerge sets it in its own
renovate.json, where its own checks can see it.

Fails on `automerge: true` anywhere in default.json or renovate.json (top
level, a manager block, a packageRule), and on any automerge preset in an
`extends` (`:automergeMinor`, `:automergeAll`, ...).

    python3 -m unittest discover -s tests -v
"""
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = ("default.json", "renovate.json")


def violations(config, path) -> list[str]:
    found = []
    if isinstance(config, dict):
        if config.get("automerge") is True:
            found.append(f"{path}: automerge: true")
        for preset in config.get("extends") or []:
            if "automerge" in str(preset).lower():
                found.append(f"{path}.extends: {preset}")
        for k, v in config.items():
            found += violations(v, f"{path}.{k}")
    elif isinstance(config, list):
        for i, v in enumerate(config):
            found += violations(v, f"{path}[{i}]")
    return found


class Detector(unittest.TestCase):
    def test_clean(self):
        self.assertEqual(violations({"packageRules": [
            {"matchPackageNames": ["x"], "automerge": False}]}, "f"), [])

    def test_automerge_anywhere_is_flagged(self):
        for cfg in ({"automerge": True},
                    {"github-actions": {"automerge": True}},
                    {"packageRules": [{"matchUpdateTypes": ["patch"],
                                       "automerge": True}]}):
            self.assertEqual(len(violations(cfg, "f")), 1, cfg)

    def test_automerge_presets_are_flagged(self):
        self.assertEqual(len(violations({"extends": [":automergeMinor"]}, "f")), 1)
        self.assertEqual(len(violations(
            {"packageRules": [{"extends": [":automergePatch"]}]}, "f")), 1)


class Preset(unittest.TestCase):
    def test_no_automerge_in_the_preset(self):
        for name in FILES:
            with self.subTest(file=name):
                config = json.loads((ROOT / name).read_text())
                self.assertIn("extends", config, f"{name}: read the wrong file?")
                self.assertEqual(violations(config, name), [])


if __name__ == "__main__":
    unittest.main()
