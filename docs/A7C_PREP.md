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
| FDAT モデル ID | `0x91030019`（unpack の `config.yaml` で確認済み） |
| Crypter | `CXD90045_k0`（確認済み） |

## 進捗

1. **完了（2026-11-24）— アップデータの構造特定。**
   exe が Packman 形式で、XOR 0xFF 反転した CAB（366,615,519 バイト、
   45ファイル、LZX圧縮）を含み、その中に UFU コンテナの
   `FirmwareData_ILCE7CV203.dat` が入っていることを確認した。
   詳細は [FIRMWARE_EXTRACTION.md](FIRMWARE_EXTRACTION.md)。

2. **完了（2026-11-24）— fwtool での展開。**
   CAB を展開して `FirmwareData_ILCE7CV203.dat`（363,197,944 バイト、
   SHA-256 `b5c20ed1…`）を取り出し、fwtool で unpack した。
   `config.yaml` の確定値： model `0x91030019`、version `2.03`、
   region `0`、crypter `CXD90045_k0`。
   （作成時に参照した成功ログが ILCE-7CM2 のものだった件は訂正済みで、
   これは ILCE-7C 自身の実測値。）

3. **次 — プロパティ一覧の解析（32-bit 対応が必要）。**
   この世代に `appFw.so` は無く、`BKID_APP_*` は
   `nflasha15_unpacked/lib/libObj.so` にある。またユーザーランドが
   32-bit ARM ELF のため、64-bit 前提の `scripts/appfw_elf.py` 等は
   そのままでは動かない。32-bit 対応をしてから対応表を抽出し、
   結果を `evidence/` に置く。feature manager 相当の仕組みが
   この世代にあるかも未確認。

4. **実機待ち — サービスモードの読み取り専用テストとバックアップ取得。**
   実機が必須の残作業は [TODO.md](../TODO.md) に集約した。

## ルール

- 記録する値はすべて ILCE-7C の 2.03 ファームウェアまたは実機由来に限る。
- ファームウェア本体、復号済みバイナリ、カメラのバックアップ、シリアル番号、
  復号鍵はこのリポジトリに置かない。
- カメラ側の変更は永続化バックアッププロパティに対してのみ行い、
  1件ずつ検証する。
