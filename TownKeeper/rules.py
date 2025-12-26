DAILY_RULES = [
    {
        "text": "Interdiction aux marchands du Royaume de l'Est", 
        "condition": lambda v: v.role == "Marchand" and v.country == "Royaume de l'Est",
    },
    {
        "text": "Refuser tous les pèlerins",
        "condition": lambda v: v.role == "Pèlerin",
    },
    {
        "text": "Refuser tous les voyageurs malades",
        "condition": lambda v: v.is_sick,
    },
    {
        "text": "Accepter uniquement les nobles",
        "condition": lambda v: v.role != "Noble", # On refuse si ce n'est pas un noble
    },
    {
        "text": "Refuser les voyageurs du Saint-Empire",
        "condition": lambda v: v.country == "Saint-Empire",
    }
]