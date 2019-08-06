#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <ArduinoJson.h> //Para instalar: Sketch -> Include Library -> Manage Libraries -> (Digite ArduinoJson e clique em instalar)

#define PRINT_SERIAL_PORT 115200

const char* ssid = "Silva";
const char* password = "frederico";
 
void setup() {
  Serial.begin(PRINT_SERIAL_PORT);
  WiFi.begin(ssid, password);   //WiFi connection
  while (WiFi.status() != WL_CONNECTED) {  //Wait for the WiFI connection completion
    delay(500);
    Serial.println("Waiting for connection");
  }

  if(WiFi.status()== WL_CONNECTED){
    String url_authentication = "https://api.primebuilder.com.br/main/auth";
    String body_auth = "username=fred&password=2019&workspace=276&grant_type=password";

//    Serial.println("TENTANDO ACESSO");
//    HTTPClient http_auth;
//    WiFiClient client;
//    http_auth.begin(client, url_authentication);
//    http_auth.addHeader("Content-Type", "text/csv");
//    http_auth.addHeader("Accept", "text/csv");
//    int httpCode = http_auth.POST(body_auth);
//    String payload = http_auth.getString();   
//    Serial.println(httpCode);
//    Serial.println(payload);
  }
}


String generate_json(int measure){
    StaticJsonDocument<800> doc;
    StaticJsonDocument<200> doc_nested;
    doc["Limit"] = "2019-08-05T17:00:00";
    doc["Observation"] = "";
    doc["ScheduledDate"] = "2019-08-05T09:00:00";
    doc["User"] = 53157;
    doc["Office"] = 882;
    doc["Region"] = 9;
    doc["Customer"] = 1160011;
    doc["Workflow"] = 26801;
    doc["Group"] = 5343;
    doc_nested["Street"] = "Doutor Breno Fernandes";
    doc_nested["Number"] = String(measure);
    doc_nested["Complement"] = "Casa";
    doc_nested["Neighborhood"] = "";
    doc_nested["City"] = "Teofilo Otoni";
    doc_nested["StateAcronym"] = "MG";
    doc_nested["CountryAcronym"] = "BR";
    doc_nested["PostalCode"] = "";
    doc_nested["Latitude"] = measure;
    doc_nested["Longitude"] = 0;
    doc["Address"] = doc_nested;
    String post_document;
    serializeJson(doc, post_document);
    return post_document;
}



void loop() {

 if(WiFi.status()== WL_CONNECTED){   //Check WiFi connection status

    //HTTPClient http;    //Declare object of class HTTPClient 
    //http.begin("http://192.168.1.12:5010/");      //Specify request destination
    //http.addHeader("Content-Type", "application/json");  //Specify content-type header

    //apagado
    //http.addHeader("Content-Type", "text/plain");  //Specify content-type header
    //http.addHeader("X-Auth-Token", "_----change-to-your-token---_");
    //int httpCode = http.POST("ola mundo");   //Send the request

    /*
    StaticJsonDocument<800> doc;
    StaticJsonDocument<200> doc_nested;
    doc["Limit"] = "2019-08-05T17:00:00";
    doc["Observation"] = "";
    doc["ScheduledDate"] = "2019-08-05T09:00:00";
    doc["User"] = 53157;
    doc["Office"] = 882;
    doc["Region"] = 9;
    doc["Customer"] = 1160011;
    doc["Workflow"] = 26801;
    doc["Group"] = 5343;
    doc_nested["Street"] = "Doutor Breno Fernandes";
    doc_nested["Number"] = " 233 ";
    doc_nested["Complement"] = "Casa";
    doc_nested["Neighborhood"] = "";
    doc_nested["City"] = "Teofilo Otoni";
    doc_nested["StateAcronym"] = "MG";
    doc_nested["CountryAcronym"] = "BR";
    doc_nested["PostalCode"] = "";
    doc_nested["Latitude"] = 0;
    doc_nested["Longitude"] = 0;
    doc["Address"] = doc_nested;
    String post_document;
    serializeJson(doc, post_document);
    */

    String post_document = generate_json(33);
    Serial.println(post_document);
    
    //int httpCode = http.POST(post_document);   //Send the request
    //String payload = http.getString();   
   
 
   //Serial.println(httpCode);   //Print HTTP return code
   //Serial.println(payload);    //Print request response payload
 
   //http.end();  //Close connection
 
 }else{
    Serial.println("Error in WiFi connection");   
 }
 Serial.println("Esperando para enviar nova mensagem");   
  delay(3000);  //Send a request every 30 seconds
}
