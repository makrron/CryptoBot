<div align="center">

# BOT STATUS
[![Discord Bots](https://top.gg/api/widget/860134458308821042.svg)](https://top.gg/bot/860134458308821042)

# COMMAND LIST

<div align="left">

## 💵 Cryptos 💵
 - `/price + CRYPTO =>` See cryptocurrency price. More than 5000 assets!!. EX: `/price btc`

## 🪙 Bitcoin 🪙
 - `/wallet_info {BTC_ADDRESS}` => Saw transactions of a bitcoin address in chain. This means you can only see confirmed transactions.
 - `/check_transaction {TRANSACTION HASH}` => returns the status ofthe transaction given a transaction hash.
 - `/post_transaction {TX}` => post raw transaction to bitcoin network. You need a signed transaction to post it.

## 🤖 Robosats 🤖
 - `/robosats_offers {FIAT} {DIRECTION}`=> Returns all active offers given a fiat currency and the purpose of the order
 - `/create_robosats_alert {FIAT} {AMOUNT} {PREMIUM} {METHOD} {DIRECTION}`=> Create an alert for robosats exchange
 - `/my_robosats_alerts`=> Show your robosats active alerts
 - `/remove_robosats_alert {ALERT_ID}`=> Remove your robosats alert

## ⛏ Transaction Fees ⛏
 - `/gas =>` Shows ETH GAS price
 - `/btcfee =>` Shows Bitcoin fees
 - `/bscgas =>` Shows Binance Smart Chain GAS price
 - `/polygas =>` Shows Polygon GAS price 
 
## 🎈 Misc 🎈
 - `/inviteme =>` Invite CryptoBot to your server
 - `/vote =>` give us 5 stars on top.gg
 - `/support =>` Join if you find a bug or if you have some suggestions
 - `/info =>` Bot info and some stats
 - `/status =>` Check status of all functionalities

## 💖 Donations 💖
 - `/donate` => Invite me a coffee.
client.on('message', message => {
  if (message.content === 'private') {
    message.author.send('Este es un mensaje privado');
  }
});

 
