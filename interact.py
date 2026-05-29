from genlayer import GenieClient
import json

def main():
    client = GenieClient()

    with open(".contract_address", "r") as f:
        contract_address = f.read().strip()

    print(f"Using contract: {contract_address}\n")

    symbols = ["bitcoin", "ethereum", "solana"]

    for symbol in symbols:
        print(f"Requesting prediction for {symbol.upper()}...")
        tx = client.call_contract(
            contract_address=contract_address,
            method="predict",
            args=[symbol]
        )
        print(f"   TX hash: {tx['hash']}")

        result_raw = client.read_contract(
            contract_address=contract_address,
            method="get_prediction",
            args=[symbol.upper()]
        )

        result = json.loads(result_raw)
        signal = result.get("signal", "?")
        reason = result.get("reason", "")
        confidence = result.get("confidence", 0)

        emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "🟡"}.get(signal, "⚪")
        print(f"   {emoji} Signal: {signal}")
        print(f"   Reason: {reason}")
        print(f"   Confidence: {confidence}%\n")

if name == "main":
    main()
