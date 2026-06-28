#!/bin/bash
set -e

# TODO: Replace with your actual GitHub username/repo
REPO="shayansaha85/seesys"
APP_NAME="seesys"

echo "Installing $APP_NAME..."

OS="$(uname -s)"
case "${OS}" in
    Linux*)     ASSET_NAME="${APP_NAME}-linux";;
    Darwin*)    ASSET_NAME="${APP_NAME}-macos";;
    *)          echo "Unsupported OS: ${OS}" && exit 1;;
esac

# Get the latest release download URL
DOWNLOAD_URL=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | grep "browser_download_url.*$ASSET_NAME\"" | cut -d '"' -f 4)

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Could not find release for $OS in $REPO."
    echo "Have you created a GitHub Release yet?"
    exit 1
fi

INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

echo "Downloading from $DOWNLOAD_URL..."
curl -L "$DOWNLOAD_URL" -o "$INSTALL_DIR/$APP_NAME"
chmod +x "$INSTALL_DIR/$APP_NAME"

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "Adding $INSTALL_DIR to PATH..."
    if [ -f "$HOME/.bashrc" ]; then
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$HOME/.bashrc"
    fi
    if [ -f "$HOME/.zshrc" ]; then
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$HOME/.zshrc"
    fi
    echo "Please restart your terminal or run: source ~/.bashrc (or ~/.zshrc)"
fi

echo "$APP_NAME successfully installed! Run it by typing '$APP_NAME'."
