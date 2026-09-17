## node、npm インストール

### 旧パッケージを念のため除去（標準 apt 由来の場合）

```
sudo apt purge -y nodejs npm
sudo apt update
```

### NodeSource の LTS（例：24.x）を追加してインストール

最新の LTS バージョンは https://nodejs.org で確認できます。

```
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt install -y nodejs
```

```
node -v
npm -v
```

## Visual Studio Code インストール

### 1. 必要なパッケージと Microsoft の GPG キーを取得

```
sudo apt update
sudo apt install -y wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
rm -f packages.microsoft.gpg
```

### 2. リポジトリを追加

```
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
```

### 3. VSCode をインストール

```
sudo apt update
sudo apt install -y code
```
