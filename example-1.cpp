#define yellow 3
#define blue 4
#define white 5
#include "WiFly.h"

// from https://twittercommunity.com/t/arduino-controlled-by-twitter-commands/1292

String twitterUsername = "NickysLights"; //set the twitter user you'd like to get here.

char ssid[] = "..."; //enter your ssid here.
char passphrase[] = "..."; //enter your passphrase here.

const unsigned long requestInterval = 1000; // delay between requests
boolean requested; // whether you've made a request since connecting
unsigned long lastAttemptTime = 0; // last time you connected to the server, in milliseconds

String currentLine = ""; // string to hold the text from server
String tweet = ""; // string to hold the tweet
boolean readingTweet = false; // if you're currently reading the tweet

Client client("api.twitter.com", 80);

void setup() {
    currentLine.reserve(256);
    tweet.reserve(150);

    Serial.begin(9600);

    WiFly.begin();

    //Define LED pin Modes
    pinMode(yellow, OUTPUT);
    pinMode(blue, OUTPUT);
    pinMode(white, OUTPUT);

    //set initial values for leds as low

    digitalWrite(yellow, LOW);
    digitalWrite(blue, LOW);
    digitalWrite(white, LOW);

    if (!WiFly.join(ssid,passphrase)) {
        Serial.println("Association failed.");
        while (1) {
            // Hang on failure.
        }
    }

    Serial.println("connecting...");

}

void loop() {
    if(client.connected()){
        if (client.available()) {
            char inChar = client.read();

            // add incoming byte to end of line:
            currentLine += inChar; 

            // if you get a newline, clear the line:
            if (inChar == '\n') {
                currentLine = "";
            }

            if ( currentLine.endsWith("<text>")) {
                // tweet is beginning. Clear the tweet string:
                readingTweet = true; 
                tweet = "";
            }
            // if you're currently reading the bytes of a tweet,
            // add them to the tweet String:
            if (readingTweet) {
                if (inChar != '<') {
                    tweet += inChar;
                } 
                else {
                    // if you got a "<" character,
                    // you've reached the end of the tweet:
                    readingTweet = false;
                    Serial.println(tweet);  

                    char tweet = Serial.read();
                    checkAction();
                    // close the connection to the server:
                    client.stop(); 
                }

            }
        }
    }
    else if (millis() - lastAttemptTime > requestInterval) {
        // if you're not connected, and two minutes have passed since
        // your last connection, then attempt to connect again:
        connectToServer();
    }
}

void connectToServer() {
    // attempt to connect, and wait a millisecond:
    Serial.println("connecting to server...");
    if (client.connect()) {
        Serial.println("making HTTP request...");
        // make HTTP GET request to twitter:

        client.println("GET /1/statuses/user_timeline.xml?screen_name="+twitterUsername + "&count=1 HTTP/1.1");

        client.println("HOST: api.twitter.com");
        client.println();
    }
    // note the time of this connect attempt:
    lastAttemptTime = millis();
}

void checkAction() {
    if (tweet == ">yellow on")
    {
        digitalWrite(yellow, HIGH);
        digitalWrite(blue, LOW);
        digitalWrite(white, LOW);

    }
    else if (tweet == ">blue on")
    {
        digitalWrite(blue, HIGH);
        digitalWrite(yellow, LOW);
        digitalWrite(white, LOW);
    }
    else if (tweet == ">white on")
    {
        digitalWrite(white, HIGH);
        digitalWrite(blue, LOW);
        digitalWrite(yellow, LOW);
    }
    else if (tweet == ">all off")
    {
        digitalWrite(yellow, LOW);
        digitalWrite(blue, LOW);
        digitalWrite(white, LOW);
    }

    else if (tweet == ">all on")
    {
        digitalWrite(yellow, HIGH);
        digitalWrite(blue, HIGH);
        digitalWrite(white, HIGH);
    }
}
