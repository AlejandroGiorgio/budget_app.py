class Category:

  def __init__(self, name):
    self.name = name
    self.ledger = list()

  def check_funds(self, amount):
    if self.get_balance() >= amount:
      return True
    else:
      return False

  def deposit(self, amount, description=0):
    if description == 0:
      description = ""
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=0):
    if description == 0:
      description = ""
    if self.check_funds(amount) is True:
      self.ledger.append({"amount": -amount, "description": description})
      return True
    else:
      return False

  def get_balance(self):
    total = 0
    for x in self.ledger:
      total += x["amount"]
    return total

  def transfer(self, amount, destination):
    if self.check_funds(amount) == True:
      self.withdraw(amount, f"Transfer to {destination.name}")
      destination.deposit(amount, f"Transfer from {self.name}")
      return True
    else:
      return False

  def __repr__(self):
    space = ""
    textline = ""
    line = ""
    line2 = ""
    lenght = len(self.name)
    dist = 30 - lenght
    dist = dist // 2
    for x in range(dist):
      line += "*"
      line2 += "*"
    if len(line + self.name + line) % 2 == 0:
      title = line + self.name + line
    else:
      while len(line + self.name + line) > 30:
        dist -= 1
        for x in range(dist):
          line += "*"
          line2 += "*"
      line2 += "*"
      print(len(line + self.name + line2))
      title = line + self.name + line2
    for dic in self.ledger:
      descrip = dic["description"]
      if len(descrip) > 23:
        descrip = descrip[0:23]
      val = str("{0:.2f}".format(dic["amount"]))
      dst = 30 - (len(descrip) + len(val))
      for x in range(dst):
        space += " "
      textline += f"{descrip}{space}{val}\n"
      space = ""
    return f"{title}\n{textline}Total: {self.get_balance()}"


def create_spend_chart(categories):
  totalSpent = []
  for cat in categories:
    ngtv = 0
    for item in cat.ledger:
      if item["amount"] < 0:
        ngtv += item["amount"]
    totalSpent.append(round(ngtv, 2))
    
  total = round(sum(totalSpent), 2)
  percentage = list(
    map(lambda amount: int((((amount / total) * 10) // 1) * 10),
        totalSpent))

  title = "Percentage spent by category\n"

  bchart = ""
  for value in reversed(range(0, 101, 10)):
    bchart += str(value).rjust(3) + '|'
    for percent in percentage:
      if percent >= value:
        bchart += " o "
      else:
        bchart += "   "
    bchart += " \n"

  under = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
  descriptions = list(map(lambda category: category.name, categories))
  max_length = max(map(lambda description: len(description), descriptions))
  descriptions = list(
    map(lambda description: description.ljust(max_length), descriptions))
  for x in zip(*descriptions):
    under += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

  return (title + bchart + under).rstrip("\n")
