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
