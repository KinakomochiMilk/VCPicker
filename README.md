# VCPicker

A Discord bot that randomly selects a specified number of members from a Voice Channel and moves them to another.
ボイスチャンネル内のメンバーをランダムに抽出し、別のチャンネルへ一括移動させるDiscordボットです。

---

## Features / 機能

* **Random Pick**: Move exactly `N` people.
  （人数を指定してランダム移動）

* **Slash Command**: Easy to use with `/move_random`.
  （スラッシュコマンド対応）

* **Flexible**: Specify source/target VCs by ID.
  （移動元・移動先をIDで柔軟に指定可能）

---

## Setup / セットアップ

### 1. Install Library / ライブラリのインストール

```bash
pip install discord.py
```

### 2. Configure Token / トークンの設定

Set your bot token in an environment variable named `DISCORD_BOT_TOKEN`,
or edit the `TOKEN` variable in `bot.py`.

環境変数 `DISCORD_BOT_TOKEN` を設定するか、`bot.py` 内の `TOKEN` 変数を直接書き換えてください。

### 3. Permissions / 権限設定

Ensure the bot has the following permissions:

* Move Members（メンバーを移動）
* Server Members Intent（ON in Developer Portal）
* Message Content Intent（ON in Developer Portal）

---

## Usage / 使い方

```
/move_random <target_vc_id> <count> [source_vc_id]
```

* `target_vc_id`: Destination VC ID（移動先のID）
* `count`: Number of people to move（移動させる人数）
* `source_vc_id` (Optional): Source VC ID. Defaults to your current VC.
  （移動元のID。省略時は自分が今いる部屋）
