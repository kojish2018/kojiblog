<!-- title: hyperliquidのヒストリカルohlcv取得方法 -->
<!-- tags: Python, Hyperliquid, Botter -->

# hyperliquid の ohlcv 取得コード

何やら最近海外の仮想通貨取引所(CEX)のアプリがダウンロードできなくなっているそうで、今後 DEX での Bot 取引を考えている方も多いのではないでしょうか。

こちらは、hyperliquid のヒストリカル ohlcv を取得するコードです。

## ライブラリの import:

```python
import os
import pandas as pd
from datetime import datetime, timezone, timedelta
from hyperliquid.info import Info
from hyperliquid.utils import constants
```

各自インストールしてください。

## インスタンスの作成：

```python
# Infoクラスのインスタンスを作成
info = Info(constants.MAINNET_API_URL, skip_ws=True)

# ユーザーの状態を取得
user_state = info.user_state("WalletAddress")
print(user_state)
```

WalletAddress の部分は、hyperliquid で使うウォレットのアドレスを入れてください。

## ohlcv を取得したい銘柄と時間足をリストで設定。後ほどループで回す

```python
# シンボルと時間枠の設定
symbolList = ['BTC', 'SOL']
intervalList = ['15m','1h']
```

何ヶ月分取得するか設定。どうやら、合計で 5000 個分ほどしか hyperliquid は保持していないようです。どうしても欲しい場合は lz4 データから集計するしかなさそう（めんどくさい）。

```python
# 現在の時刻を基準に開始時間と終了時間を設定
end_time = int(datetime.now(timezone.utc).timestamp() * 1000)  # 現在のUNIXタイムスタンプ（ミリ秒単位）
start_time = int((datetime.now(timezone.utc) - timedelta(days=90)).timestamp() * 1000)  # 現在から90日前
```

## ohlcv 取得のループ処理：

```python
for symbol in symbolList:
    for interval in intervalList:
        # ローソク足データを取得
        ohlcv_data = info.candles_snapshot(name=symbol, interval=interval, startTime=start_time, endTime=end_time)

        df = pd.DataFrame(ohlcv_data)
        df['timestamp'] = pd.to_datetime(df['t'], unit='ms', utc=True)
        df.drop(columns=['t', 'T', 's', 'i'], inplace=True)  # 不要な列を削除
        df.set_index('timestamp', inplace=True)
        df = df.reindex(columns=['o', 'h', 'l', 'c', 'v', 'n'])  # カラム順を指定
        df[['o', 'h', 'l', 'c', 'v']] = df[['o', 'h', 'l', 'c', 'v']].astype(float)
        df.rename(columns={
            'o': 'op',
            'h': 'hi',
            'l': 'lo',
            'c': 'cl',
            'v': 'volume',
            'n': 'numtrade'
        }, inplace=True)
        df = df.tz_convert('Asia/Tokyo')
        df = df.astype('float64')
        print(df)
```

以上です。csv 保存等のコードは追加してください。
