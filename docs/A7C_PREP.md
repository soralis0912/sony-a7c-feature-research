# ILCE-7C 調査計画と進捗

このリポジトリの対象は **ILCE-7C（A7C 初代）ファームウェア Ver. 2.03 のみ**。
ここには ILCE-7C 自体のファームウェアと実機から得た値だけを記録する。
他機種の値は持ち込まない。

## 対象

| 項目 | 内容 |
| --- | --- |
| 型番 | ILCE-7C（A7C） |
| ファームウェア | Ver. 2.03（Sony、2026-04-15） |
| 配布形式 | アップデータ `Update_ILCE7CV203.exe`（367,091,632 バイト、SHA-256 `e382c3deecb8d0fe8463a2451ddbfa897cd131a1797170d05936fabc4ffaf6f8`） |
| SoC | CXD90045（BIONZ X） |
| FDAT モデル ID | `0x91030019`（fwtool `devices.yml` の登録値。unpack の `config.yaml` で確認待ち） |
| Crypter | 確認待ち（`config.yaml` の `crypterName`） |

## 進捗

1. **完了（2026-11-24）— アップデータの構造特定。**
   exe が Packman 形式で、XOR 0xFF 反転した CAB（366,615,519 バイト、
   45ファイル、LZX圧縮）を含み、その中に UFU コンテナの
   `FirmwareData_ILCE7CV203.dat` が入っていることを確認した。
   詳細は [FIRMWARE_EXTRACTION.md](FIRMWARE_EXTRACTION.md)。

2. **未確認 — fwtool での展開。**
   ILCE-7C の DAT の unpack はまだ実測していない（作成時に参照した成功ログは
   ILCE-7CM2 のものだった）。CAB の LZX 展開またはアップデータからの
   DAT 取り出しを済ませてから、unpack と `config.yaml` の確定値
   （model / version / crypter）を記録する。

3. **次 — プロパティ一覧と feature manager の解析。**
   展開した ILCE-7C の `appFw.so` から `BKID_APP_*` の対応表と
   製品クラスマトリクスを抽出する（`scripts/bkid_inventory.py`、
   `scripts/feature_manager_matrix.py`）。結果は `evidence/` に置く。

4. **実機待ち — サービスモードの読み取り専用テストとバックアップ取得。**
   実機が必須の残作業は [TODO.md](../TODO.md) に集約した。

## ルール

- 記録する値はすべて ILCE-7C の 2.03 ファームウェアまたは実機由来に限る。
- ファームウェア本体、復号済みバイナリ、カメラのバックアップ、シリアル番号、
  復号鍵はこのリポジトリに置かない。
- カメラ側の変更は永続化バックアッププロパティに対してのみ行い、
  1件ずつ検証する。
