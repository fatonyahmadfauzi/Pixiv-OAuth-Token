# Resolve project root relative to this script's location (scripts/utils/ -> project root)
$ProjectRoot = (Get-Item "$PSScriptRoot\..\..")

$files = @(
    "$ProjectRoot\web\src_backup\public__components__footer.js",
    "$ProjectRoot\web\src_backup\public__tutorial.html",
    "$ProjectRoot\web\public\components\footer.js",
    "$ProjectRoot\web\public\tutorial.html"
)

$keys = @(
    "footerProductTitle",
    "footerHomeLink",
    "footerDownloadLink",
    "footerTutorialLink",
    "footerSourceLink",
    "footerResourceTitle",
    "footerDocsLink",
    "footerChangelogLink",
    "footerPixivLink",
    "footerPythonLink",
    "footerVercelLink",
    "footerSupportTitle",
    "footerIssueLink",
    "footerDiscussLink",
    "footerDevLink",
    "footerContactTitle"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        $original = $content
        foreach ($key in $keys) {
            $search = "id=""$key"""
            $replace = "id=""$key"" data-i18n=""$key"""
            # avoid double replace
            if ($content.IndexOf($replace) -eq -1) {
                $content = $content.Replace($search, $replace)
            }
        }
        if ($content -ne $original) {
            Set-Content -Path $file -Value $content -NoNewline -Encoding UTF8
            Write-Host "Modified and saved $file"
        } else {
            Write-Host "No changes needed for $file"
        }
    } else {
        Write-Host "File not found: $file"
    }
}
