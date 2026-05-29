from genlayer import *
import json


@gl.contract
class AIPricePredictor:

    predictions: TreeMap[str, str]
    history: TreeMap[str, Array[str]]
    owner: str

    def init(self) -> None:
        self.predictions = TreeMap()
        self.history = TreeMap()
        self.owner = gl.message.sender_address

    @gl.public.write
    def predict(self, symbol: str) -> None:
        symbol = symbol.upper()
        price_url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd&include_24hr_change=true"
        price_raw = gl.get_webpage(price_url, mode="text")

        prompt = f"""
You are a professional crypto trading analyst.
Below is real-time market data for {symbol}:
{price_raw}
Respond ONLY with a valid JSON object:
{{"signal": "BUY" | "SELL" | "HOLD", "reason": "<one sentence>", "confidence": <0-100>}}
"""
        result_raw = gl.eq_principle_prompt_comparative(
            prompt,
            comparative_fn=lambda a, b: json.loads(a)["signal"] == json.loads(b)["signal"]
        )
        self.predictions[symbol] = result_raw
        if symbol not in self.history:
            self.history[symbol] = Array()
        self.history[symbol].append(result_raw)

    @gl.public.view
    def get_prediction(self, symbol: str) -> str:
        symbol = symbol.upper()
        if symbol not in self.predictions:
            return json.dumps({"error": f"No prediction for {symbol}"})
        return self.predictions[symbol]

    @gl.public.view
    def get_history(self, symbol: str) -> list:
        symbol = symbol.upper()
        if symbol not in self.history:
            return []
        return list(self.history[symbol])

    @gl.public.view
    def get_all_symbols(self) -> list:
        return list(self.predictions.keys())
