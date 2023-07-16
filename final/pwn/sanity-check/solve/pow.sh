#!/bin/sh
# redpwnpow proof of work runner
# https://github.com/redpwn/pow

set -eu
version=v0.1.2
run() {
  case $(uname | tr '[:upper:]' '[:lower:]') in
    linux*)
      case $(uname -m) in
        x86_64) release=linux-amd64;;
        aarch64) release=linux-arm64;;
        arm*) release=linux-armv6l;;
        *) echo unknown linux architecture >&2; exit 1
      esac;;
    darwin*) release=darwin;;
    msys*|mingw*|cygwin*) release=windows-amd64.exe;;
    *) echo unknown operating system >&2; exit 1
  esac
  cache_root=${XDG_CACHE_HOME:-$HOME/.cache}/redpwnpow
  mkdir -p "$cache_root"
  cache_path=$cache_root/redpwnpow-$version-$release
  if [ ! -e "$cache_path" ]; then
    curl -sSfLo "$cache_path" "https://github.com/redpwn/pow/releases/download/$version/redpwnpow-$release"
    chmod u+x "$cache_path"
  fi
  "$cache_path" "$@"
}
run "$@"
