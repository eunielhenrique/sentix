#!/bin/bash
# Sentix — instalação do pipeline de chamadas num Droplet da DigitalOcean (Ubuntu 24.04).
# Uso: cole este arquivo em "Advanced Options → Add Initialization scripts (user data)" ao criar o
# Droplet, ou rode como root numa máquina nova: bash digitalocean-cloud-init.sh
# Depois, preencha /etc/sentix/pipeline.env (token e chave de IA) e o cron começa a rodar sozinho.
set -euo pipefail

apt-get update -y
apt-get install -y python3 python3-venv python3-pip git ffmpeg util-linux

id sentix >/dev/null 2>&1 || useradd -m -s /bin/bash sentix
install -d -o sentix -g sentix /opt/sentix /var/lib/sentix /var/log/sentix
install -d -m 700 /etc/sentix

# Código (repositório privado: troque pela URL com token de leitura ou use deploy key)
if [ ! -d /opt/sentix/app/.git ]; then
  sudo -u sentix git clone https://github.com/eunielhenrique/sentix /opt/sentix/app || \
    echo "AVISO: clone falhou (repo privado). Clone manualmente em /opt/sentix/app."
fi

sudo -u sentix python3 -m venv /opt/sentix/venv
sudo -u sentix /opt/sentix/venv/bin/pip install --quiet --upgrade pip faster-whisper

# Baixa o modelo uma vez para o primeiro ciclo não demorar
sudo -u sentix /opt/sentix/venv/bin/python -c \
  "from faster_whisper import WhisperModel; WhisperModel('large-v3-turbo', device='cpu', compute_type='int8')" || true

# Segredos: preencher manualmente, nunca versionar
if [ ! -f /etc/sentix/pipeline.env ]; then
  cat > /etc/sentix/pipeline.env <<'EOF'
# Token da API4COM sem expiração (app.api4com.com/user/tokens)
API4COM_TOKEN=
# Uma das duas chaves de IA para a classificação
GEMINI_API_KEY=
ANTHROPIC_API_KEY=
EOF
  chmod 600 /etc/sentix/pipeline.env
fi

# Wrapper que carrega os segredos e roda o pipeline com o Python do venv
cat > /usr/local/bin/sentix-pipeline <<'EOF'
#!/bin/bash
set -a; . /etc/sentix/pipeline.env; set +a
export PATH=/opt/sentix/venv/bin:$PATH
cd /opt/sentix/app && git pull --quiet || true
exec /opt/sentix/app/pipeline/run.sh /var/lib/sentix
EOF
chmod 755 /usr/local/bin/sentix-pipeline

# Cron: a cada hora, no minuto 5
cat > /etc/cron.d/sentix-pipeline <<'EOF'
5 * * * * root /usr/local/bin/sentix-pipeline >> /var/log/sentix/pipeline.log 2>&1
EOF

# Retenção: apaga áudios com mais de 90 dias (LGPD); transcrições e análises ficam
cat > /etc/cron.d/sentix-retencao <<'EOF'
30 3 * * * root find /var/lib/sentix/audio -name '*.mp3' -mtime +90 -delete
EOF

echo "Instalado. Preencha /etc/sentix/pipeline.env e rode: sudo sentix-pipeline"
