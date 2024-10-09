import collections
import collections.abc

# Monkey patch to resolve the issue with Mapping in frozendict.
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping

from flask import Flask, request, render_template
from experta import *

app = Flask(__name__)

class Preferences(Fact):
    """User travel preferences"""
    pass

class TravelRecommendation(KnowledgeEngine):
    result = None
    explanation = None

    def set_result(self, destination, description):
        self.result = destination
        self.explanation = description

    # Debugging to trace rule triggering
    def print_debug(self, budget, weather, activity, continent):
        print(f"Debug: {budget=}, {weather=}, {activity=}, {continent=}")

    # Asia Destinations
    @Rule(Preferences(budget=L('low'), weather=L('sunny'), activity=L('beach'), continent=L('Asia')))
    def thailand(self):
        self.set_result("Thailand", "Thailand is perfect for a low-budget sunny beach trip in Asia.")
        print("Rule triggered: Thailand")

    @Rule(Preferences(budget=L('low'), weather=L('sunny'), activity=L('culture'), continent=L('Asia')))
    def india(self):
        self.set_result("India", "India is a great low-budget destination for exploring ancient culture in sunny weather.")
        print("Rule triggered: India")

    @Rule(Preferences(budget=L('medium'), weather=L('mild'), activity=L('culture'), continent=L('Asia')))
    def japan(self):
        self.set_result("Japan", "Japan is ideal for experiencing rich culture in mild weather on a medium budget.")
        print("Rule triggered: Japan")

    @Rule(Preferences(budget=L('medium'), weather=L('sunny'), activity=L('adventure'), continent=L('Asia')))
    def vietnam(self):
        self.set_result("Vietnam", "Vietnam is great for adventurous sunny weather trips in Asia.")
        print("Rule triggered: Vietnam")

    @Rule(Preferences(budget=L('high'), weather=L('snowy'), activity=L('skiing'), continent=L('Asia')))
    def japan_skiing(self):
        self.set_result("Japan", "Japan has world-class skiing in snowy weather with a high budget.")
        print("Rule triggered: Japan Skiing")

    # Europe Destinations
    @Rule(Preferences(budget=L('low'), weather=L('sunny'), activity=L('beach'), continent=L('Europe')))
    def greece(self):
        self.set_result("Greece", "Greece offers sunny beaches and low-budget travel in Europe.")
        print("Rule triggered: Greece")

    @Rule(Preferences(budget=L('low'), weather=L('mild'), activity=L('culture'), continent=L('Europe')))
    def portugal(self):
        self.set_result("Portugal", "Portugal is a fantastic destination for exploring European culture on a low budget.")
        print("Rule triggered: Portugal")

    @Rule(Preferences(budget=L('medium'), weather=L('sunny'), activity=L('beach'), continent=L('Europe')))
    def spain(self):
        self.set_result("Spain", "Spain is perfect for a medium-budget sunny beach vacation in Europe.")
        print("Rule triggered: Spain")

    @Rule(Preferences(budget=L('medium'), weather=L('mild'), activity=L('culture'), continent=L('Europe')))
    def italy(self):
        self.set_result("Italy", "Italy is ideal for cultural trips with mild weather on a medium budget.")
        print("Rule triggered: Italy")

    @Rule(Preferences(budget=L('high'), weather=L('snowy'), activity=L('skiing'), continent=L('Europe')))
    def switzerland(self):
        self.set_result("Switzerland", "Switzerland is great for skiing and high-end snowy adventures in Europe.")
        print("Rule triggered: Switzerland")

    # North America Destinations
    @Rule(Preferences(budget=L('low'), weather=L('sunny'), activity=L('beach'), continent=L('North America')))
    def mexico(self):
        self.set_result("Mexico", "Mexico offers sunny beaches and budget-friendly travel in North America.")
        print("Rule triggered: Mexico")

    @Rule(Preferences(budget=L('medium'), weather=L('snowy'), activity=L('adventure'), continent=L('North America')))
    def canada(self):
        self.set_result("Canada", "Canada is great for adventurous snowy trips with a medium budget.")
        print("Rule triggered: Canada")

    @Rule(Preferences(budget=L('medium'), weather=L('mild'), activity=L('culture'), continent=L('North America')))
    def usa_culture(self):
        self.set_result("USA", "The USA offers diverse cultural experiences in mild weather with a medium budget.")
        print("Rule triggered: USA Culture")

    @Rule(Preferences(budget=L('high'), weather=L('sunny'), activity=L('beach'), continent=L('North America')))
    def usa(self):
        self.set_result("USA (Hawaii)", "Hawaii offers a high-end sunny beach vacation in North America.")
        print("Rule triggered: Hawaii")

    # South America Destinations
    @Rule(Preferences(budget=L('low'), weather=L('sunny'), activity=L('beach'), continent=L('South America')))
    def brazil(self):
        self.set_result("Brazil", "Brazil is great for sunny beaches and low-budget travel in South America.")
        print("Rule triggered: Brazil")

    @Rule(Preferences(budget=L('low'), weather=L('mild'), activity=L('culture'), continent=L('South America')))
    def peru_culture(self):
        self.set_result("Peru", "Peru offers cultural exploration with mild weather and a low budget.")
        print("Rule triggered: Peru")

    @Rule(Preferences(budget=L('medium'), weather=L('sunny'), activity=L('adventure'), continent=L('South America')))
    def argentina_adventure(self):
        self.set_result("Argentina", "Argentina is perfect for adventurous activities in sunny weather on a medium budget.")
        print("Rule triggered: Argentina")

    @Rule(Preferences(budget=L('high'), weather=L('mild'), activity=L('culture'), continent=L('South America')))
    def chile_culture(self):
        self.set_result("Chile", "Chile is ideal for high-budget cultural experiences with mild weather.")
        print("Rule triggered: Chile")

    # Africa Destinations
    @Rule(Preferences(budget=L('low'), weather=L('sunny'), activity=L('adventure'), continent=L('Africa')))
    def kenya(self):
        self.set_result("Kenya", "Kenya is perfect for low-budget adventurous safaris in sunny weather.")
        print("Rule triggered: Kenya")

    @Rule(Preferences(budget=L('medium'), weather=L('mild'), activity=L('beach'), continent=L('Africa')))
    def south_africa(self):
        self.set_result("South Africa", "South Africa offers beautiful beaches and mild weather for medium-budget travelers.")
        print("Rule triggered: South Africa")

    # Oceania Destinations
    @Rule(Preferences(budget=L('low'), weather=L('sunny'), activity=L('beach'), continent=L('Oceania')))
    def fiji(self):
        self.set_result("Fiji", "Fiji is an affordable destination with sunny beaches in Oceania.")
        print("Rule triggered: Fiji")

    @Rule(Preferences(budget=L('high'), weather=L('mild'), activity=L('adventure'), continent=L('Oceania')))
    def australia(self):
        self.set_result("Australia", "Australia offers high-budget adventures with mild weather.")
        print("Rule triggered: Australia")

    # Fallback rule for no match
    @Rule(Preferences())
    def fallback(self):
        self.set_result("No specific destination", "Sorry, we couldn't find a perfect match, but explore flexible options.")
        print("Fallback rule triggered.")

@app.route('/')
def home():
    return render_template('travel.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user preferences from form input
    budget = request.form.get('budget').lower()  # Convert to lowercase for consistency
    weather = request.form.get('weather').lower()
    activity = request.form.get('activity').lower()
    continent = request.form.get('continent')

    # Debug to see what is received
    print(f"Received preferences: {budget=}, {weather=}, {activity=}, {continent=}")

    # Initialize and run the expert system
    engine = TravelRecommendation()
    engine.reset()
    engine.print_debug(budget, weather, activity, continent)  # Debugging the rule triggering
    engine.declare(Preferences(budget=budget, weather=weather, activity=activity, continent=continent))
    engine.run()

    return render_template('result.html', result=engine.result, explanation=engine.explanation)

if __name__ == '__main__':
    app.run(debug=True)
