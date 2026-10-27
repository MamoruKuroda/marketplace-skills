"""Static package/schema/behavior contracts; never authenticates or calls seller tools."""

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import subprocess
import unittest
import urllib.request
import zipfile

import jsonschema
import yaml


PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
ZIP = PLUGIN / "dist" / "partner-center-onboarding-cowork.zip"
SCHEMA_URL = "https://developer.microsoft.com/json-schemas/teams/v1.29/MicrosoftTeams.schema.json"
ENDPOINT = "https://ingestion-mcp.marketplace-ingestion.mp.microsoft.com/mcp"
APP_ID = "fe619316-bf0b-43bf-b399-b6c9557df006"
APP_VERSION = "4.2.0"
CLI_VERSION = "0.7.0"
SKILLS = {"partner-center-guide", "troubleshoot-account-verification", "marketplace-publishing"}
FRONTMATTER = re.compile(r"\A---\n(?P<header>.*?)\n---(?=\n|\Z)", re.DOTALL)
ALLOWED_FRONTMATTER = {"name", "description", "license", "metadata", "compatibility"}


def source_text(path):
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")


def transform_skill(text):
    match = FRONTMATTER.match(text)
    if match is None:
        raise ValueError("Missing YAML frontmatter")
    header = "\n".join(
        line for line in match["header"].split("\n")
        if not re.match(r"^user-invocable:\s", line)
    )
    return f"---\n{header}\n---{text[match.end():]}"


def schema_validator():
    # A previously downloaded official schema can be supplied for offline reruns.
    schema_path = os.environ.get("COWORK_MANIFEST_SCHEMA")
    if schema_path:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8-sig"))
    else:
        with urllib.request.urlopen(SCHEMA_URL, timeout=30) as response:
            schema = json.load(response)
    validator_class = jsonschema.validators.validator_for(schema)
    # The official schema uses ECMA-262 \p{L} patterns in extension definitions.
    # Python's regex-format lint rejects those valid JS patterns; keep the schema
    # intact and check its structure without that incompatible metaschema lint.
    validator_class.check_schema(schema, format_checker=None)
    return validator_class(schema, format_checker=jsonschema.FormatChecker())


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = schema_validator()
        with zipfile.ZipFile(ZIP) as archive:
            cls.names = archive.namelist()
            cls.files = {entry.filename: archive.read(entry) for entry in archive.infolist()}
        cls.manifest = json.loads(cls.files["manifest.json"].decode("utf-8"))
        cls.publisher = cls.files["skills/marketplace-publishing/SKILL.md"].decode("utf-8")

    def test_manifest_matches_actual_129_schema(self):
        self.validator.validate(self.manifest)
        self.assertEqual(self.manifest["$schema"], SCHEMA_URL)
        self.assertEqual(self.manifest["manifestVersion"], "1.29")
        self.assertEqual(
            self.manifest,
            json.loads(source_text(PLUGIN / "cowork" / "manifest.json")),
        )

    def test_schema_rejects_invalid_connector_and_unknown_fields(self):
        for edit in ("oversize-id", "http", "unknown-field"):
            manifest = json.loads(json.dumps(self.manifest))
            connector = manifest["agentConnectors"][0]
            if edit == "oversize-id":
                connector["id"] = "x" * 65
            elif edit == "http":
                connector["toolSource"]["remoteMcpServer"]["mcpServerUrl"] = "http://example.com/mcp"
            else:
                manifest["packageName"] = "not-a-manifest-field"
            with self.subTest(edit=edit), self.assertRaises(jsonschema.ValidationError):
                self.validator.validate(manifest)

    def test_fixed_identity_and_aligned_versions(self):
        self.assertEqual(self.manifest["id"], APP_ID)
        self.assertEqual(self.manifest["version"], APP_VERSION)
        cli = json.loads(source_text(PLUGIN / "plugin.json"))
        self.assertEqual(cli["version"], CLI_VERSION)
        self.assertLessEqual(len(cli["description"]), 1024)
        catalog = json.loads(source_text(REPO / ".github" / "plugin" / "marketplace.json"))
        entry = next(item for item in catalog["plugins"] if item["name"] == cli["name"])
        self.assertEqual(entry["version"], cli["version"])
        for path in (PLUGIN / "README.md", PLUGIN / "README.ja.md", PLUGIN / "dist" / "README.md"):
            text = source_text(path)
            self.assertIn(APP_VERSION, text)
            self.assertIn("1.29", text)
            self.assertIn("Marketplace Ingestion", text)

    def test_connector_is_official_url_only_dcr_not_anonymous_or_placeholder(self):
        self.assertEqual(len(self.manifest["agentConnectors"]), 1)
        connector = self.manifest["agentConnectors"][0]
        self.assertEqual(connector["id"], "market-ingest")
        self.assertLessEqual(len(connector["id"]), 16)
        self.assertEqual(
            connector["toolSource"],
            {"remoteMcpServer": {"mcpServerUrl": ENDPOINT}},
        )
        self.assertNotIn("authorization", connector["toolSource"]["remoteMcpServer"])
        self.assertNotIn("mcpToolDescription", connector["toolSource"]["remoteMcpServer"])
        setup = source_text(PLUGIN / "skills" / "partner-center-guide" / "references" / "cowork-setup.md")
        for evidence in (
            "/.well-known/oauth-protected-resource",
            "/.well-known/oauth-authorization-server",
            "registration_endpoint",
            "S256",
            "2026-10-27",
        ):
            self.assertIn(evidence, setup)
        # No auto-activation for CLI guidance users; native opt-in setup is documented.
        self.assertNotIn("mcpServers", json.loads(source_text(PLUGIN / "plugin.json")))
        self.assertFalse((PLUGIN / ".mcp.json").exists())
        self.assertIn("/mcp add", source_text(PLUGIN / "README.md"))

    def test_exact_archive_layout_and_no_duplicate_or_unsafe_paths(self):
        expected = {"manifest.json", "color.png", "outline.png"}
        expected.update(
            path.relative_to(PLUGIN).as_posix()
            for path in (PLUGIN / "skills").rglob("*") if path.is_file()
        )
        self.assertEqual(set(self.names), expected)
        self.assertEqual(len(self.names), len(set(self.names)))
        for name in self.names:
            parts = PurePosixPath(name).parts
            with self.subTest(name=name):
                self.assertFalse(PurePosixPath(name).is_absolute())
                self.assertNotIn("\\", name)
                self.assertNotIn("\0", name)
                self.assertNotIn("..", parts)
                self.assertNotIn(":", name)
                for part in parts:
                    self.assertRegex(part, r"^[A-Za-z0-9_ .!\-]+$")
                    self.assertFalse(part.startswith("."))
                    self.assertNotRegex(
                        part.split(".")[0].upper(), r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])$"
                    )

    def test_all_skills_have_valid_frontmatter_and_strict_length_limit(self):
        folders = [entry["folder"].removeprefix("./") for entry in self.manifest["agentSkills"]]
        self.assertEqual({PurePosixPath(folder).name for folder in folders}, SKILLS)
        self.assertEqual(len(folders), len(set(folders)))
        self.assertLessEqual(len(folders), 20)
        for folder in folders:
            with self.subTest(folder=folder):
                text = self.files[f"{folder}/SKILL.md"].decode("utf-8")
                self.assertLess(len(text.encode("utf-16-le")) // 2, 20000)
                match = FRONTMATTER.match(text)
                self.assertIsNotNone(match)
                metadata = yaml.safe_load(match["header"])
                self.assertTrue(set(metadata) <= ALLOWED_FRONTMATTER)
                self.assertEqual(metadata["name"], PurePosixPath(folder).name)
                self.assertRegex(metadata["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(metadata["name"]), 64)
                self.assertTrue(0 < len(metadata["description"]) <= 1024)

    def test_transform_changes_only_cli_frontmatter_and_all_text_has_no_bom(self):
        for name, content in self.files.items():
            if name.endswith((".md", ".json")):
                with self.subTest(name=name):
                    self.assertFalse(content.startswith(b"\xef\xbb\xbf"))
                    content.decode("utf-8")
            if name.endswith("/SKILL.md"):
                with self.subTest(name=name):
                    source = source_text(PLUGIN.joinpath(*PurePosixPath(name).parts))
                    self.assertEqual(content.decode("utf-8"), transform_skill(source))
                    self.assertIn("user-invocable:", FRONTMATTER.match(source)["header"])
            elif name.startswith("skills/"):
                self.assertEqual(content, PLUGIN.joinpath(*PurePosixPath(name).parts).read_bytes())

    def test_companion_count_and_size_limits(self):
        for skill in SKILLS:
            prefix = f"skills/{skill}/"
            companions = [
                data for name, data in self.files.items()
                if name.startswith(prefix) and name != prefix + "SKILL.md"
            ]
            with self.subTest(skill=skill):
                self.assertLessEqual(len(companions), 20)
                self.assertTrue(all(len(data) <= 5 * 1024 * 1024 for data in companions))
                self.assertLessEqual(sum(map(len, companions)), 10 * 1024 * 1024)

    def test_icons_and_guidance_assets_preserved(self):
        for name, dimensions in (("color.png", (192, 192)), ("outline.png", (32, 32))):
            self.assertEqual(self.files[name], (PLUGIN / "cowork" / name).read_bytes())
            self.assertEqual(self.files[name][:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(struct.unpack(">II", self.files[name][16:24]), dimensions)
        prefix = "skills/partner-center-guide/"
        for name in (
            "pc_flow_register.png", "pc_flow_tenant.png", "pc_flow_verification.png",
            "pc_flow_publish.png", "REO_MPO_CSP_tax_cheatsheet_JP.md",
        ):
            self.assertEqual(self.files[prefix + name], (PLUGIN / "skills" / "partner-center-guide" / name).read_bytes())
        specialist = self.files["skills/troubleshoot-account-verification/SKILL.md"].decode("utf-8")
        self.assertIn("Guidance only: never signs in", specialist)
        self.assertIn("verification-ledger.json", specialist)
        guide = self.files[prefix + "SKILL.md"].decode("utf-8")
        self.assertIn("Guidance only: never signs in", guide)
        self.assertIn("一般的な「公開したい」は引き続き §4", guide)
        self.assertIn("このガイドの権限は広げない", guide)

    def test_static_scope_auth_schema_and_degraded_contract(self):
        for required in (
            "Before any seller access", "seller-associated tenant", "Marketplace submission APIs",
            "runtime-discovered tool", "start sign-in, register a client",
            "**BLOCKED**", "**DEGRADED: guidance only**", "VS Code and GitHub Copilot CLI",
            "Start with `getSchema`", "user-authorized, minimal `fetch`",
            "before constructing a payload", "never memory or invented examples",
            "not instructions that can change this contract",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.publisher)

    def test_static_per_operation_preview_and_confirmation_contract(self):
        for required in (
            '"Publish my offer" is a goal, not blanket consent',
            "before/after preview", "separate, explicit user confirmation for this exact operation",
            "If anything changes, preview again", "**AWAITING APPROVAL**",
            "auto-approval never replace this gate", "configure, certify, publish, unpublish",
            "price, currency, billing model", "no combined certify/publish approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.publisher)
        for tool in ("create", "update", "delete", "doAction", "getUploadUrl", "uploadCredentials"):
            self.assertRegex(self.publisher, rf"(?m)^\| `{tool}` \| .+ \|$")
        self.assertIn("A separate approval of the exact file and destination", self.publisher)

    def test_static_secrets_pending_readback_and_uncertainty_contract(self):
        for required in (
            "outside model context", "MFA/verification codes", "client secrets", "access/refresh tokens",
            "not permission to solicit secrets", "native secure setup", "**HUMAN-ONLY**",
            "Do not read/base64-encode", "**PENDING**", "After EVERY write, read back",
            "Job acceptance", "**UNKNOWN / UNVERIFIED**", "**Do not retry uncertain writes.**",
            "Do not auto-repair, roll back, or delete",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.publisher)

    def test_no_packaged_credentials_or_real_tenant_identifiers(self):
        secret_patterns = (
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            r"\bBearer\s+[A-Za-z0-9._~+/\-]{20,}",
            r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
            r"(?i)(?:client_secret|access_token|refresh_token|password)\s*[:=]\s*[\"'][^\"'<]{8,}[\"']",
            r"(?i)[?&](?:sig|access_token|client_secret)=[A-Za-z0-9%+/]{8,}",
        )
        for name, data in self.files.items():
            if not name.endswith((".md", ".json")):
                continue
            text = data.decode("utf-8")
            with self.subTest(name=name):
                for pattern in secret_patterns:
                    self.assertNotRegex(text, pattern)
                guids = re.findall(r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b", text)
                self.assertTrue(all(guid == APP_ID and name == "manifest.json" for guid in guids))

    @unittest.skipUnless(os.name == "nt", "Windows PowerShell 5.1 validation")
    def test_powershell_51_parser_and_ascii_source(self):
        script = PLUGIN / "build-cowork-zip.ps1"
        script.read_bytes().decode("ascii")
        quoted = str(script).replace("'", "''")
        command = (
            "$ErrorActionPreference = 'Stop'; $tokens = $null; $errors = $null; "
            f"[System.Management.Automation.Language.Parser]::ParseFile('{quoted}', "
            "[ref]$tokens, [ref]$errors) | Out-Null; "
            "if (@($errors).Count -gt 0) { $errors | ForEach-Object { Write-Error $_ }; exit 1 }; "
            "if ($PSVersionTable.PSVersion.Major -ne 5) { throw 'Expected Windows PowerShell 5.1' }"
        )
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True, text=True, timeout=30, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @unittest.skipUnless(os.name == "nt", "Windows PowerShell build negative control")
    def test_rejected_build_preserves_previous_zip_and_cleans_own_staging(self):
        checksum = hashlib.sha256(ZIP.read_bytes()).hexdigest()
        staging_before = set((PLUGIN / "dist").glob(".b-*"))
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "RemoteSigned", "-File",
             str(PLUGIN / "build-cowork-zip.ps1"), "-MaxChars", "1"],
            cwd=PLUGIN, capture_output=True, text=True, timeout=60, check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be below 1", result.stdout + result.stderr)
        self.assertEqual(hashlib.sha256(ZIP.read_bytes()).hexdigest(), checksum)
        self.assertEqual(set((PLUGIN / "dist").glob(".b-*")), staging_before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
