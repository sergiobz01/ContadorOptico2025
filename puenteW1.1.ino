const int pinSalida = 12;

void setup() {
  Serial.begin(9600); // Inicializa la comunicación serial
  pinMode(pinSalida, HIGH);
}

void loop() {
  //supongo que fijaremos vin pero sino se lee como int vin = voltaje(analogRead(A2))
  float va; // Lee el valor del potenciómetro
  float vb; // Convierte a voltaje (0-3.3V)
  float vin = 3.3;
  float R = 100000; //supongo una resistencia de 1k 

  float resistencia = R *1.0* ((vin - 2*(va - vb))/(vin + 2*(va - vb))); //formula para despeje de Rx obtenida teoricamente
  
  // Imprime los valores en el monitor serial

  float media; 
  float sumatorio = 0;



  for(int i = 0; i < 20; i++)
  { // calculo de la media de 10 medidas
    digitalWrite(pinSalida, HIGH);

    va = voltaje(analogRead(A0)); // Lee el valor del potenciómetro
    vb = voltaje(analogRead(A1)); // Convierte a voltaje (0-3.3V)
    delay(50);
    resistencia = R * (vin - 2*(va - vb))/(vin + 2*(va - vb));
    sumatorio += resistencia;
    // Imprime los valores
   // Serial.print("\nVa: ");
    //Serial.print(va);
    //Serial.print(" | Vb: ");
    //Serial.print(vb);
    //Serial.print(" | R: ");
    //Serial.println(resistencia);

    //Serial.print("ADC: ");
    //Serial.println(analogRead(A1));
  }

  media = sumatorio / 20.0;

  digitalWrite(pinSalida, LOW);

  //Serial.print("La media de resistencias es: ");
  Serial.println(media); 

  delay(500);
}

///convierte a voltaje
float voltaje(int adc)
{
  float voltaje = adc *(3.3/1024); //si decidimos dejarlo fijo
  
  return voltaje;
}