# ファームウェア展開（ILCE-7C Ver. 2.03）

ILCE-7C のアップデートは、メモリーカード用の `BODYDATA.DAT` 単体配布ではなく、
Windows 用アップデータ `.exe`（および macOS 用）で配布される。展開は3段構え。

## 1. 公式アップデータ

| 項目 | 内容 |
| --- | --- |
| ファイル名 | `Update_ILCE7CV203.exe` |
| バージョン | Ver. 2.03（2026-04-15 公開、対象：ILCE-7C / ILCE-7CL） |
| サイズ | 367,091,632 バイト（Sony 公表値と一致） |
| SHA-256 | `e382c3deecb8d0fe8463a2451ddbfa897cd131a1797170d05936fabc4ffaf6f8` |

## 2. exe → CAB（Packman 形式）

exe は Sony Packaging Tool（Packman）の自己解凍形式で、PE 本体（463,360 バイト）の
直後にエントリ表と `Settings.ini`（平文、`ProductName=Update_ILCE7CV203`）が続き、
その後に CAB が **全バイト XOR 0xFF で反転** して格納されている。

- 反転した CAB の先頭（`MSCF` の反転形）はファイルオフセット 465,440
- 反転を戻すと標準 CAB：366,615,519 バイト、45 ファイル、LZX 圧縮
- CAB の後ろに Authenticode 署名（10,673 バイト）が続く

CAB 内に `FirmwareData_ILCE7CV203.dat`（UFU コンテナ：`\x89UFU` 魔数＋
DATV/PROV/UDID/FDAT の TLV チェーン）が入っている。これが実質のファームウェア本体。

## 3. DAT → 展開（fwtool）

```bash
python fwtool.py unpack -f BODYDATA.DAT -o unpacked
# （FirmwareData_ILCE7CV203.dat を BODYDATA.DAT として渡してもよい）
```

fwtool の `devices.yml` には ILCE-7C が登録済み
（arch `CXD90045`、model `0x91030019`）。

展開できることは確認済みで、構成は以下のパーティションを含む：

```text
unpacked/firmware.tar_unpacked/0700_part_image/dev/
  nflasha15  （lib/appFw.so を含む）
  nflasha3   （initrd.img を含む）
  nflasha7
  nflasha8
unpacked/firmware.tar_unpacked/0750_nor_loader/loader_nor.tar
```

`unpacked/config.yaml` の確定値（model / version / crypter）は記録待ち。
判明次第このドキュメントに追記する。

ファームウェア本体・展開物はこのリポジトリに含めない。
