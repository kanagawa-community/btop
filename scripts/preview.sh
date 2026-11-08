# Preview hook for .github/scripts/render-previews.sh: btop runs in a headless tmux
# pane with each theme applied through a throwaway config file, so every box,
# graph gradient and the selected process row show. btop runs in its own user and
# PID namespace beside a few dummy processes, so no real process, user name or
# command line reaches the images; the CPU model is replaced in the capture.
# Requires: btop, tmux, unshare.
# shellcheck shell=bash
name=btop

cleanup() {
  tmux -L kanagawa-preview kill-server 2>/dev/null || true
  rm -f "${conf:-}"
}

capture() {
  cleanup
  conf=$(mktemp)
  fake=$(mktemp -d)
  for p in editor browser terminal player compiler shell notes mail; do ln -s "$(command -v sleep)" "$fake/$p"; done
  fake="for p in $fake/*; do \$p 1000 & done; exec btop --config $conf --themes-dir $root/themes --force-utf"
  sleep 0.5
  printf 'color_theme = "kanagawa-%s"\ntruecolor = True\nshown_boxes = "cpu mem net proc"\nupdate_ms = 500\n' "$1" >"$conf"
  tmux -L kanagawa-preview new-session -d -s s -x 100 -y 30 -c "$root" \
    -e COLORTERM=truecolor -e TERM=xterm-256color -e LC_ALL=C.UTF-8 \
    "unshare -Urpf --mount-proc bash -c '$fake'"
  sleep 4
  tmux -L kanagawa-preview send-keys -t s Down Down
  sleep 1
  cpu=$(sed -n 's/^model name[^:]*: AMD \(.*\) w\/.*/\1/p;T;q' /proc/cpuinfo)
  mask=$(printf '%-*s' "${#cpu}" 'Example CPU')
  tmux -L kanagawa-preview capture-pane -p -e -t s | sed "s/$cpu/$mask/" >"$2"
}
