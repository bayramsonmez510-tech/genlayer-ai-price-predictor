from genlayer import GenieClient

def main():
    client = GenieClient()

    print("Deploying AIPricePredictor...")
    with open("price_predictor.py", "r") as f:
        contract_code = f.read()

    tx = client.deploy_contract(
        contract_code=contract_code,
        initial_state={}
    )

    print(f"✅ Contract deployed!")
    print(f"   Transaction hash : {tx['hash']}")
    print(f"   Contract address : {tx['contract_address']}")

    with open(".contract_address", "w") as f:
        f.write(tx["contract_address"])

if name == "main":
    main()
