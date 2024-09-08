standard_output = """{
    "day_1": [
        {
            "location": "Downtown Dubai",
            "type_of_place": "District",
            "description": "Explore Downtown Dubai, enjoy a relaxing brunch at a cafÃ©.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Dubai Mall",
            "type_of_place": "Shopping Mall",
            "description": "Visit Dubai Mall, explore its shops, and attractions like Dubai Aquarium & Underwater Zoo.",
            "approximate_duration": "3 hours"
        },
        {
            "location": "Burj Khalifa",
            "type_of_place": "Skyscraper",
            "description": "Visit the Burj Khalifa observation deck for stunning views of the city during sunset.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Dubai Fountain",
            "type_of_place": "Attraction",
            "description": "Watch the Dubai Fountain show and enjoy dinner nearby.",
            "approximate_duration": "2 hours"
        }
    ],
    "day_2": [
        {
            "location": "Dubai Miracle Garden",
            "type_of_place": "Garden",
            "description": "Visit the Dubai Miracle Garden (seasonal) or explore the Dubai Frame for panoramic views.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Dubai Desert",
            "type_of_place": "Desert",
            "description": "Experience a Desert Safari with dune bashing, sandboarding, and camel riding.",
            "approximate_duration": "5 hours"
        },
        {
            "location": "Desert Camp",
            "type_of_place": "Camp",
            "description": "Enjoy a traditional Bedouin-style dinner with live entertainment in the desert.",
            "approximate_duration": "3 hours"
        }
    ],
    "day_3": [
        {
            "location": "Al Fahidi District",
            "type_of_place": "Historic District",
            "description": "Explore the Al Fahidi District and visit the Dubai Museum in Al Fahidi Fort.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Textile Souk",
            "type_of_place": "Market",
            "description": "Shop at the Textile Souk and wander around Al Seef.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Dubai Creek",
            "type_of_place": "Waterway",
            "description": "Take an Abra ride across Dubai Creek to the Gold Souk and Spice Souk in Deira.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "La Mer",
            "type_of_place": "Beachfront",
            "description": "Relax at La Mer beach, enjoy beachfront cafes, or water sports.",
            "approximate_duration": "3 hours"
        }
    ],
    "day_4": [
        {
            "location": "Palm Jumeirah",
            "type_of_place": "Man-made Island",
            "description": "Visit Palm Jumeirah and explore The Pointe for scenic views.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Aquaventure Waterpark",
            "type_of_place": "Waterpark",
            "description": "Experience the thrills at Aquaventure Waterpark at Atlantis The Palm.",
            "approximate_duration": "4 hours"
        },
        {
            "location": "Dubai Marina",
            "type_of_place": "District",
            "description": "Explore Dubai Marina, walk along Marina Walk, and enjoy lunch at one of the Marina's restaurants.",
            "approximate_duration": "3 hours"
        },
        {
            "location": "Dhow Cruise, Dubai Marina",
            "type_of_place": "Cruise",
            "description": "Take a Dhow Cruise dinner with live entertainment along Dubai Marina.",
            "approximate_duration": "2 hours"
        }
    ],
    "day_5": [
        {
            "location": "Jumeirah Beach",
            "type_of_place": "Beach",
            "description": "Relax at Jumeirah Beach, swim, sunbathe, or try water sports.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Mall of the Emirates",
            "type_of_place": "Shopping Mall",
            "description": "Visit the Mall of the Emirates for last-minute shopping or see Ski Dubai.",
            "approximate_duration": "2 hours"
        },
        {
            "location": "Hotel",
            "type_of_place": "Hotel",
            "description": "Check out from your hotel and prepare for departure.",
            "approximate_duration": "1 hour"
        }
    ]
}"""


itinerary_system_prompt = f"""
    You are a helpful assistant which generates a travel itinerary. 
    You will receive a location, date, who I am traveling with, preferences on activities, and some additional preferences.
    In addition, I will give you the bodies of some online webpages on the topic, and you can incorporate some of their suggestions into the itinerary.  
    That is, you will generate an itinerary from the inputs based on your knowledge as a travel assistant. 

    You should output this itinerary as a json-formatted string. First break it up into days (these are the keys).
    Within each day, we will have a list of activities, where each avitivity will have the keys 'location', 'type_of_place', 'description', and 'approximate_duration'.
    The output should be a json-formatted string which I could pass into json.loads to get a json object. 
    The output string needs to be a standard JSON string without any extraneous characters such as triple backticks and newline indicators, and should not include the string "json" at the beginning. 
    An example would be {standard_output}
  """