# Branch 04 - Start Mock Server
# Script para iniciar o servidor de autenticação mock

Write-Host "=" -NoNewline; Write-Host ("=" * 60)
Write-Host "🚀 Iniciando ClipperBot Auth Server (MOCK)"
Write-Host "=" -NoNewline; Write-Host ("=" * 60)
Write-Host ""

# Verificar se .venv existe
if (-Not (Test-Path ".venv")) {
    Write-Host "❌ Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "   Execute: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Ativar ambiente virtual
Write-Host "📦 Ativando ambiente virtual..." -ForegroundColor Cyan
& ".venv\Scripts\Activate.ps1"

# Verificar dependências
Write-Host "🔍 Verificando dependências..." -ForegroundColor Cyan

$dependencies = @("fastapi", "uvicorn", "pydantic", "requests")
$missing = @()

foreach ($dep in $dependencies) {
    python -c "import $dep" 2>$null
    if ($LASTEXITCODE -ne 0) {
        $missing += $dep
    }
}

if ($missing.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️  Dependências faltantes detectadas:" -ForegroundColor Yellow
    $missing | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
    Write-Host ""
    $install = Read-Host "Deseja instalar agora? (S/N)"
    
    if ($install -eq "S" -or $install -eq "s") {
        Write-Host "📥 Instalando dependências..." -ForegroundColor Cyan
        pip install -r requirements.txt
        Write-Host "✅ Dependências instaladas!" -ForegroundColor Green
    } else {
        Write-Host "❌ Instale as dependências manualmente:" -ForegroundColor Red
        Write-Host "   pip install -r requirements.txt" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "✅ Todas as dependências OK!" -ForegroundColor Green
Write-Host ""

# Iniciar servidor
Write-Host "🌐 Iniciando servidor na porta 8000..." -ForegroundColor Cyan
Write-Host "   URL: http://localhost:8000" -ForegroundColor White
Write-Host "   Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "⏹️  Pressione CTRL+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

python auth_server_mock.py
