## node、npm インストール

### 旧パッケージを念のため除去（標準 apt 由来の場合）

```
sudo apt purge -y nodejs npm
sudo apt update
```

### NodeSource の LTS（例：22.x）を追加してインストール

```
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

```
node -v
npm -v
```

## Visual Studio Code インストール

### 1. Microsoft の GPG キーを取得

```
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
```

### 2. リポジトリを追加

```
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
```

### 3. VSCode をインストール

```
sudo apt update
sudo apt install code
```
