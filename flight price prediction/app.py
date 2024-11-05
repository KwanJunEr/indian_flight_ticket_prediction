from flask import Flask, request, jsonify
import pickle
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = pickle.load(open('modal.pkl', 'rb'))


# Dictionaries for categorical variables
airline_dict = {'AirAsia': 0, "Indigo": 1, "GO_FIRST": 2, "SpiceJet": 3, "Air_India": 4, "Vistara": 5}
source_dict = {'Delhi': 0, "Hyderabad": 1, "Bangalore": 2, "Mumbai": 3, "Kolkata": 4, "Chennai": 5}
departure_dict = {'Early_Morning': 0, "Morning": 1, "Afternoon": 2, "Evening": 3, "Night": 4, "Late_Night": 5}
stops_dict = {'zero': 0, "one": 1, "two_or_more": 2}
arrival_dict = {'Early_Morning': 0, "Morning": 1, "Afternoon": 2, "Evening": 3, "Night": 4, "Late_Night": 5}
destination_dict = {'Delhi': 0, "Hyderabad": 1, "Mumbai": 2, "Bangalore": 3, "Chennai": 4, "Kolkata": 5}
class_dict = {'Economy': 0, 'Business': 1}

@app.route('/predict', methods = ['POST'])
def predict():
    data = request.json
    try:
        airline = airline_dict[data['airline']]   #data['airline'] would return "Indigo".
        source_city = source_dict[data['source_city']]
        departure_time = departure_dict[data['departure_time']]
        stops = stops_dict[data['stops']]
        arrival_time = arrival_dict[data['arrival_time']]
        destination_city = destination_dict[data['destination_city']]
        travel_class = class_dict[data['class']]
        
        # Calculate date difference
        departure_date = datetime.strptime(data['departure_date'], '%Y-%m-%d')  #Converts the date string (in 'YYYY-MM-DD' format) to a datetime object.
        date_diff = (departure_date - datetime.today()).days + 1

        features = [airline, source_city, departure_time, stops, arrival_time, destination_city, travel_class, date_diff] 
        #Uses the loaded model to make a prediction based on the features. The [0] extracts the predicted value from the resulting array.
       
        prediction  = model.predict([features])[0]
        print(model.predict([features]))
        print(prediction)

        return jsonify({'prediction': round(prediction, 2)})
    except KeyError as e:
        return jsonify({'error': f'Missing data for: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)