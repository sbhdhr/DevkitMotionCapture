#include "AZ3166WiFi.h"
#include "WebSocketClient.h"
#include "IoT_DevKit_HW.h"

static bool hasWifi;
static bool isWsConnected;

static char webSocketServerUrl[] = "ws://192.168.0.122:8765/";
static WebSocketClient* wsClient;

char wifiBuff[128];
int pollrate=200; // in milliseconds

void initWiFi()
{
	Screen.print("WiFi \r\n \r\nConnecting...\r\n             \r\n");

	if (WiFi.begin() == WL_CONNECTED)
	{
		IPAddress ip = WiFi.localIP();
		snprintf(wifiBuff, 128, "WiFi Connected\r\n%s\r\n%s\r\n \r\n", WiFi.SSID(), ip.get_address());
		Screen.print(wifiBuff);

		hasWifi = true;
	}
	else
	{
		snprintf(wifiBuff, 128, "No WiFi\r\nEnter AP Mode\r\nto config\r\n                 \r\n");
		Screen.print(wifiBuff);
	}
}

bool connectWebSocket()
{
	Screen.clean();
	Screen.print(0, "Connect to WS...");

	if (wsClient == NULL)
	{
		wsClient = new WebSocketClient(webSocketServerUrl);
	}

	isWsConnected = wsClient->connect();
	if (isWsConnected)
	{
		Screen.print(1, "connect WS successfully.");
		Serial.println("WebSocket connect successfully.");
	}
	else
	{
		Screen.print(1, "Connect WS failed.");
		Serial.print("WebSocket connection failed, isWsConnected: ");
		Serial.println(isWsConnected);
	}

	return isWsConnected;
}

void setup()
{
	hasWifi = false;
	isWsConnected = false;

	initIoTDevKit(1);

	initWiFi();
	if (hasWifi)
	{
		connectWebSocket();
	}

	pinMode(USER_BUTTON_A, INPUT);
}

void loop()
{
	if (hasWifi)
	{

		if (isWsConnected)
		{
			char msgBuffer[2048];
			int length;
			
			//get the data from sensor
			int x, y, z,a,b,c;
			getDevKitAcceleratorValue(&x, &y, &z);
			getDevKitGyroscopeValue(&a,&b,&c);

			//convert to semicolon separated string : "0.29220142645852376;0.08130941009686095;-8.483483483483484"
			length = sprintf(msgBuffer,"%d;%d;%d;%d;%d;%d",x,y,z,a,b,c);

			

			Screen.clean();
			Screen.print(0, "Poll Data: ");
			Screen.print(1, msgBuffer, true);


			//send data to the server
			int res = wsClient->send(msgBuffer, strlen(msgBuffer));
			if (res > 0)
			{
				
				Screen.print(3, "WS sent");
				Serial.print("Sent::");
				Serial.println(msgBuffer);
			}
		}
		else
		{
			Screen.clean();
			Screen.print(0, "WS not connected");
			Screen.print(1, "Trying..");
			connectWebSocket();
		}
	}
	else
	{
		Screen.clean();
		Screen.print(0, "No wifi");
	}

	delay(pollrate);

}
