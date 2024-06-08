from pySpaceTraders.models import cargo, contract, errors, factions, status


def parse_error(response):
    response = response["error"]
    code = response["code"]
    error = errors.Codes(code).name
    message = response["message"]
    return {"error": error, "message": message}


def parse_contract(contract_in: dict) -> contract.Contract:
    term = contract_in["terms"]
    payment = contract.Payment(**term["payment"])
    deliver = [contract.DeliverTerms(**deliver) for deliver in term["deliver"]]
    deadline = term["deadline"]
    contract_in["terms"] = contract.Terms(deadline=deadline, payment=payment, deliver=deliver)
    return contract.Contract(**contract_in)


def parse_cargo(cargo_in: dict) -> cargo.Cargo:
    cargo_in["inventory"] = [cargo.Item(**item) for item in cargo_in["inventory"]]
    data = cargo.Cargo(**cargo_in)
    return data


def parse_faction(faction: dict) -> factions.Faction:
    faction["traits"] = [
        factions.Trait(**trait) for trait in faction["traits"]
    ]
    return factions.Faction(**faction)


def parse_status(response: dict) -> status.Status:
    response["announcements"] = [status.Announcement(**news) for news in response["announcements"]]
    response["leaderboards"]["mostCredits"] = [status.CreditEntry(**leader) for leader in response["leaderboards"]["mostCredits"]]
    response["leaderboards"]["mostSubmittedCharts"] = [status.ChartEntry(**leader) for leader in
                                                       response["leaderboards"]["mostSubmittedCharts"]]
    response["leaderboards"] = status.Leaderboard(**response["leaderboards"])
    response["links"] = [status.Link(**link) for link in response["links"]]
    response["serverResets"] = status.ServerReset(**response["serverResets"])
    response["stats"] = status.Stats(**response["stats"])
    return status.Status(**response)
