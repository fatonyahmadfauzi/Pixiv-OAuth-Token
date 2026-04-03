# create_selfsigned_cert.ps1
# Creates a self-signed code signing certificate and exports as codesign.pfx
# Run as Administrator in PowerShell

param(
    [string]$SubjectName = "CN=Fatony Ahmad Fauzi, O=Pixiv OAuth Token, C=ID",
    [string]$PfxPath     = "$PSScriptRoot\codesign.pfx",
    [string]$PfxPassword = "PixivOAuthSign2025",
    [int]$ValidYears      = 5
)

Write-Host "[*] Creating self-signed code signing certificate..." -ForegroundColor Cyan

$cert = New-SelfSignedCertificate `
    -Subject $SubjectName `
    -Type CodeSigningCert `
    -KeyUsage DigitalSignature `
    -KeyAlgorithm RSA `
    -KeyLength 4096 `
    -HashAlgorithm SHA256 `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -NotAfter (Get-Date).AddYears($ValidYears)

Write-Host "[+] Certificate created: $($cert.Thumbprint)" -ForegroundColor Green

# Export to PFX
$securePass = ConvertTo-SecureString -String $PfxPassword -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $PfxPath -Password $securePass | Out-Null

Write-Host "[+] Exported to: $PfxPath" -ForegroundColor Green
Write-Host "[+] PFX Password: $PfxPassword" -ForegroundColor Yellow
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor White
Write-Host "  1. Edit scripts\sign_auto.bat" -ForegroundColor Gray
Write-Host "     Set: PFX_PATH=$PfxPath" -ForegroundColor Gray
Write-Host "     Set: PFX_PASS=$PfxPassword" -ForegroundColor Gray
Write-Host "  2. Run sign_auto.bat after building" -ForegroundColor Gray
Write-Host ""
Write-Host "NOTE: Self-signed cert will show publisher name but Windows SmartScreen" -ForegroundColor Yellow
Write-Host "      may still warn. For full trust, buy a cert from DigiCert/Sectigo." -ForegroundColor Yellow
