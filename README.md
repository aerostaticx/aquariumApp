# aquariumApp
Backend/Frontend code for webserver for use with ESP32 to read and plot aquarium params.

Backend in Flask.
Clients interact through frontend HTML webpage or ESP32. Webpage allows plotting of data, start/stop of probing. ESP32 responsible for getting probe requests and sending back water parameters via POST. All data is added to mySQL DB.
