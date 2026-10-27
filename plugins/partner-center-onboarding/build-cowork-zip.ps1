<#
Builds dist/partner-center-onboarding-cowork.zip from the repo skills plus the
Teams manifest and icons, applying the Cowork frontmatter allowlist transform.

Why a transform: GitHub Copilot CLI skills use a `user-invocable` frontmatter
field (e.g. troubleshoot-account-verification is `user-invocable: false` so it is
reached only by delegation). Microsoft 365 Copilot Cowork rejects any frontmatter
key outside name / description / license / metadata / compatibility, and caps each
SKILL.md at 20000 characters. This script strips the `user-invocable` line for the
packaged copies only; the repo copies keep it for the CLI install path.

Manifest + icons are loose files under `cowork/` (manifest.json, color.png,
outline.png) so packaging metadata such as the version bump is reviewable in a git
diff. Run from anywhere; paths are resolved relative to this script.
#>
[CmdletBinding()]
param(
  [ValidateRange(1, 20000)]
  [int]$MaxChars = 20000
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression

$plugin = $PSScriptRoot
$pkgsrc = Join-Path $plugin 'cowork'
$dist   = Join-Path $plugin 'dist'
$zip    = Join-Path $dist 'partner-center-onboarding-cowork.zip'
$build  = Join-Path $dist ('.b-' + [guid]::NewGuid().ToString('N'))
$zipStage = $build + '.zip'
$utf8   = New-Object System.Text.UTF8Encoding($false)   # no BOM

try {
  New-Item -ItemType Directory -Path $build | Out-Null

  # 1) manifest.json + icons: loose files under cowork/ (source of truth for packaging metadata)
  foreach ($f in @('manifest.json','color.png','outline.png')) {
    $srcFile = Join-Path $pkgsrc $f
    if (-not (Test-Path $srcFile)) { throw "Packaging source file not found: $srcFile" }
    Copy-Item $srcFile (Join-Path $build $f) -Force
  }

  # 2) skills: copy from repo, then strip disallowed frontmatter for Cowork
  Copy-Item (Join-Path $plugin 'skills') $build -Recurse -Force
  $skillFiles = @(Get-ChildItem $build -Recurse -Filter SKILL.md -File)
  foreach ($skillFile in $skillFiles) {
    $txt = [System.IO.File]::ReadAllText($skillFile.FullName).Replace("`r`n", "`n")
    $frontmatter = [regex]::Match($txt, '\A---\n(?<header>[\s\S]*?)\n---(?=\n|\z)')
    if (-not $frontmatter.Success) { throw "Missing YAML frontmatter: $($skillFile.FullName)" }
    $headerLines = @($frontmatter.Groups['header'].Value -split "`n")
    $header = (@($headerLines | Where-Object { $_ -notmatch '^user-invocable:\s' })) -join "`n"
    $out = "---`n" + $header + "`n---" + $txt.Substring($frontmatter.Length)
    [System.IO.File]::WriteAllText($skillFile.FullName, $out, $utf8)
    if ($out.Length -ge $MaxChars) {
      throw ("$($skillFile.Directory.Name)/SKILL.md is $($out.Length) chars, must be below $MaxChars")
    }
    Write-Host ("  {0}: {1} chars (ok)" -f $skillFile.Directory.Name, $out.Length)
  }

  # 3) normalize manifest.json to no-BOM
  $mf = Join-Path $build 'manifest.json'
  [System.IO.File]::WriteAllText($mf, ([System.IO.File]::ReadAllText($mf) -replace "^\uFEFF",''), $utf8)

  # 4) Replace the previous artifact only after the new archive closes successfully.
  $archive = [System.IO.Compression.ZipFile]::Open($zipStage, [System.IO.Compression.ZipArchiveMode]::Create)
  try {
    $dirSep = [System.IO.Path]::DirectorySeparatorChar.ToString()
    $altSep = [System.IO.Path]::AltDirectorySeparatorChar.ToString()
    $base = $build.TrimEnd([char[]]@([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)) + $dirSep
    $packageFiles = @(Get-ChildItem $build -Recurse -File | Sort-Object FullName)
    foreach ($packageFile in $packageFiles) {
      $entryName = $packageFile.FullName.Substring($base.Length).Replace($dirSep, '/').Replace($altSep, '/')
      [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
        $archive,
        $packageFile.FullName,
        $entryName,
        [System.IO.Compression.CompressionLevel]::Optimal
      ) | Out-Null
    }
  }
  finally {
    $archive.Dispose()
  }
  Move-Item -LiteralPath $zipStage -Destination $zip -Force
  Write-Host ("Built {0} ({1} bytes)" -f $zip, (Get-Item $zip).Length)
}
finally {
  if (Test-Path $build) { Remove-Item $build -Recurse -Force }
  if (Test-Path $zipStage) { Remove-Item $zipStage -Force }
}
