#!/bin/bash

echo "[entrypoint] password: $PASS"

# start ssh server
# ---------------------------------------------------------------------------
sudo service ssh start || echo "[entrypoint] WARNING: ssh start failed"

# set vnc password from PASS env var and start tigervncserver
# ---------------------------------------------------------------------------
mkdir -p ~/.vnc

# create xstartup to launch xfce4 desktop
# ---------------------------------------------------------------------------
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XDG_CURRENT_DESKTOP=XFCE
exec dbus-launch --exit-with-session xfce4-session
EOF
chmod +x ~/.vnc/xstartup

# set vnc password and start vnc server
# ---------------------------------------------------------------------------
printf "${PASS}\n${PASS}\nn\n" | vncpasswd
tigervncserver :1 -geometry 1920x1080 -depth 24 -localhost no 2>&1 || echo "[entrypoint] WARNING: tigervncserver failed"
export DISPLAY=:1

exec "$@"
