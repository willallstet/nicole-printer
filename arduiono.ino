#include <Adafruit_Thermal.h>
#include <SoftwareSerial.h>

// Define pin connections for the thermal printer
#define PRINTER_TX_PIN 2  // Arduino transmit  YELLOW WIRE  labeled RX on printer
#define PRINTER_RX_PIN 3  // Arduino receive   GREEN WIRE   labeled TX on printer

// Create a SoftwareSerial connection for the printer
SoftwareSerial printerSerial(PRINTER_RX_PIN, PRINTER_TX_PIN);

// Initialize the printer
Adafruit_Thermal printer(&printerSerial);

void setup() {
  // Initialize serial communication with computer
  Serial.begin(9600);
  
  // Initialize the printer's serial port
  printerSerial.begin(9600);
  printer.begin();
  
  // Print a startup message
  printer.println("Printer ready!");
  printer.feed(2);
}

void loop() {
  // Check if data is available from the computer
  if (Serial.available() > 0) {
    // Read the incoming string until newline
    String text = Serial.readStringUntil('\n');
    
    // Print the text to the thermal printer
    printer.println(text);
    
    // Feed paper to ensure everything is printed
    printer.feed(1);
  }
}