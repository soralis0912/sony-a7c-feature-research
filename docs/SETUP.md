# セットアップ

## 要件

- Sony ILCE-7C（ファームウェア Ver. 2.03 を対象とする）
- データ転送可能な USB ケーブル
- Python 3
- Git
- `libusb` と、USB デバイスへアクセスする権限
- オフライン展開用の公式 Sony アップデータ（Ver. 2.03）

## リポジトリを取得

```bash
cd ~/Documents
git clone https://github.com/soralis0912/sony-a7c-feature-research.git
git clone https://github.com/ma1co/Sony-PMCA-RE.git
git clone --branch a7cII https://github.com/soralis0912/fwtool.py.git
```

（fwtool は CXD90045 対応を含むブランチを使う。ILCE-7C は `devices.yml` 登録済み。）

## Sony-PMCA-RE のセットアップ

```bash
cd ~/Documents/Sony-PMCA-RE
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS で `libusb` が無ければ `brew install libusb`。

サービスモードの起動（想定コマンド。手元の ILCE-7C 実機では未検証）：

```bash
sudo ./venv/bin/python ./pmca-console.py serviceshell
```

> 参考：ILCE-7C では PMCA のサービスモード利用報告が公開されている
> （言語設定の解除など、fw 2.03 機での成功報告あり）。ただし本リポジトリの
> 手順（バックアップ取得やプロパティ読み取り）は実機未検証。

## fwtool のセットアップ

```bash
cd ~/Documents/fwtool.py
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pycryptodomex pyyaml
```

展開手順は [FIRMWARE_EXTRACTION.md](FIRMWARE_EXTRACTION.md) を参照。
アップデータ（.exe）から DAT を取り出す工程が必要な点に注意。

## カメラ側の準備（実機作業時）

1. サービスセッションに足るだけバッテリーを充電する。
2. カメラの USB 設定で **マスストレージ** を選ぶ。
3. カメラを PC に直接接続する。
4. 写真アプリなど、カメラの USB デバイスを占有しうるアプリを閉じる。
5. `serviceshell` を起動する。想定される遷移：

```text
Sony DSC is a camera in mass storage mode
Switching to service mode
Found a camera in service mode
Authenticating
```
