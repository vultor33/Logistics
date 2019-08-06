/**
   BasicHTTPSClient.ino
    Created on: 20.08.2018
*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClientSecureBearSSL.h>
#include <ArduinoJson.h>  // VERSAO 6
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// IMPORTANTE
// E NECESSARIO ATUALIZAR ISSO AQUI.
// PODE-SE FAZER BUSCA DE FINGERPRINT NO SITE: https://www.grc.com/fingerprints.htm
// E NECESSARIO ADICIONAR ESSES 0 NOS CODIGOS RECEBIDOS PELO SITE
// PARECE QUE ESSES FINGERPRINT TEM DATA DE EXPERICAO - CONFERIR ISSO DEPOIS
const uint8_t fingerprint[20] = {0x42, 0xEB, 0x64, 0x6C, 0x68, 0xDE, 0xF5, 0x60, 0xDC, 0x10, 0x85, 0xD8, 0x21, 0x2A, 0x07, 0x05, 0x5A, 0xB4, 0x00, 0xBD};
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

ESP8266WiFiMulti WiFiMulti;

String TOKEN = "";
String CONTENT_TYPE = "application/json";
String ACCEPT = "text/csv";
String generate_json(int measure);
String generate_authorization(String authorization_response);

void setup() {

  Serial.begin(115200);
  // Serial.setDebugOutput(true);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("Silva", "frederico");

}

void loop() {

  // OBTENCAO DO TOKEN DE AUTENTIFICACAO
  if ((WiFiMulti.run() == WL_CONNECTED && TOKEN == "")) {
    std::unique_ptr<BearSSL::WiFiClientSecure>client(new BearSSL::WiFiClientSecure);
    client->setFingerprint(fingerprint);
    HTTPClient https;
    Serial.print("[HTTPS] begin...\n");
    if (https.begin(*client, "https://api.primebuilder.com.br/main/auth")) {
      int httpCode = https.POST("username=fred&password=2019&workspace=276&grant_type=password");
      if (httpCode > 0) {
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = https.getString();
          TOKEN = generate_authorization(payload);
        }
      }
      https.end();
    }
  }


  // POST DA TRANSACAO
  if ((WiFiMulti.run() == WL_CONNECTED && TOKEN != "")) {
    HTTPClient http;
    Serial.print("[HTTPS] postagem de informacoes...\n");
    if (http.begin("http://api.primebuilder.com.br/Main/v1/movement/tasks/")) {
      String post_body = generate_json(33);
      http.addHeader("Content-Type", CONTENT_TYPE);
      http.addHeader("Accept", ACCEPT);
      http.addHeader("Authorization", TOKEN);      
      int httpCode = http.POST(post_body);
      if (httpCode > 0) {
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.println(httpCode);
      }
      http.end();
    } else {
      Serial.println("http not started");
    }
  }
  
  
  Serial.println("TOKEN:  ");
  Serial.println(TOKEN);



  
  Serial.println("Wait 10s before next round...");
  
  delay(10000);
}



String generate_authorization(String authorization_response){
  StaticJsonDocument<1200> doc;
  deserializeJson(doc, authorization_response.c_str());
  JsonObject object = doc.as<JsonObject>();
  String token_value = object["access_token"];
  token_value = "bearer " + token_value;
  return token_value;
  
}

String generate_json(int measure){
    StaticJsonDocument<800> doc;
    StaticJsonDocument<200> doc_nested;
    doc["Limit"] = "2019-09-05T17:00:00";
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
