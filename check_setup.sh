#!/bin/bash
# save as check_setup.sh and run: bash check_setup.sh

echo "Checking prerequisites..."
echo ""

command -v python3 >/dev/null 2>&1 && echo "✅ Python: $(python3 --version)" || echo "❌ Python not found"
command -v docker >/dev/null 2>&1 && echo "✅ Docker: $(docker --version)" || echo "❌ Docker not found"
command -v git >/dev/null 2>&1 && echo "✅ Git: $(git --version)" || echo "❌ Git not found"
command -v kubectl >/dev/null 2>&1 && echo "✅ kubectl: $(kubectl version --client --short 2>/dev/null)" || echo "⚠️  kubectl not found (optional)"
command -v tofu >/dev/null 2>&1 && echo "✅ OpenTofu: $(tofu --version | head -n 1)" || echo "⚠️  OpenTofu not found (optional)"
command -v aws >/dev/null 2>&1 && echo "✅ AWS CLI: $(aws --version)" || echo "⚠️  AWS CLI not found (optional)"

echo ""
echo "Docker daemon check..."
docker ps >/dev/null 2>&1 && echo "✅ Docker daemon is running" || echo "❌ Docker daemon not running - start Docker Desktop"