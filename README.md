# Sony A7C ファームウェア・機能リサーチ

[English version](README_EN.md)

自己責任で利用してください。本リポジトリの利用による損害について、作者は責任を負いません。

Sony **ILCE-7C**（A7C 初代）のファームウェア **Ver. 2.03** を、公式アップデートファイルと
Sony の USB サービスモードを使って調査するための、再現可能なメモとツールの置き場です。

> **状態：ファームウェア展開まで確認済み。** 実機（サービスモード等）は未検証。
> 対象の定義と調査計画・進捗は [docs/A7C_PREP.md](docs/A7C_PREP.md) を参照。
> 実機が必要な残タスクは [TODO.md](TODO.md) に集約してある。

## 参考

このリポジトリは、[leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research)
（Sony A7 IV 6.02 のサービスモード／シャッター角／LUT／ファームウェア研究）を
**雛形として参考に**、新規に作成したものです。fork ではありません。
リポジトリ構成、ドキュメント構成、解析スクリプト、研究手法はその研究に基づきます。
A7 IV の成果はすべて原著者のものです。原典は MIT ライセンスで、その著作権表示は
[LICENSE](LICENSE) にそのまま保持しています。

なお、このリポジトリに記録する値はすべて ILCE-7C のファームウェア／実機由来に
限ります。姉妹リポジトリとして ILCE-7CM2（A7C II）版
[soralis0912/sony-a7cii-feature-research](https://github.com/soralis0912/sony-a7cii-feature-research)
も同じ方法で進めています。

## 対象

| 項目 | 内容 |
| --- | --- |
| 型番 | ILCE-7C（A7C） |
| ファームウェア | Ver. 2.03（ソニー、2026-04-15 公開） |
| 配布形式 | アップデータ `Update_ILCE7CV203.exe`（367,091,632 バイト） |
| SoC | CXD90045（BIONZ X） |
| FDAT モデル ID | `0x91030019`（fwtool 登録値、config.yaml で確認待ち） |
| Crypter | 確認待ち |

## 研究ステータス

| 機能 | 状態 |
| --- | --- |
| ファームウェア展開（fwtool、CXD90045） | 構造特定済み・展開確認済み（docs/FIRMWARE_EXTRACTION.md） |
| プロパティ一覧（BKID） | 解析待ち（appFw.so が必要） |
| 製品クラス | 解析待ち |
| サービスモード | ILCE-7C での利用報告は公開されているが、本リポジトリでは実機未検証 |
| 設定バックアップ | 未検証 |

## 上流・関連プロジェクト

- [leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research):
  本リポジトリの雛形・参考元（A7 IV の研究）。
- [ma1co/Sony-PMCA-RE](https://github.com/ma1co/Sony-PMCA-RE):
  USB サービスモードの通信とバックアップシェル。
- [soralis0912/fwtool.py](https://github.com/soralis0912/fwtool.py/tree/a7cII):
  Sony ファームウェア展開ツール（CXD90045 / CXD90057 対応ブランチ）。
- [soralis0912/sony-a7cii-feature-research](https://github.com/soralis0912/sony-a7cii-feature-research):
  姉妹リポジトリ（ILCE-7CM2 版）。

## リポジトリ構成

```
docs/       セットアップ、展開、サービスモード、ライブファイル
            システム読み取りの手順と、調査計画
scripts/    読み取り専用のバックアップ／ダンプと、オフラインの
            プロパティ解析ツール（a7c_*）
evidence/   秘匿情報を除いたプロパティ対応表と検証記録
            （ILCE-7C の解析が進み次第追加）
TODO.md     実機が必要な残タスク
```

このリポジトリには、Sony のファームウェア、復号済みバイナリ、カメラのバックアップ、
シリアル番号、復号鍵、抽出したプロプライエタリファイルは意図的に含めていません。
公式アップデートは各自で入手し、生成データはローカルに留めてください。
