
  // Set the LCD address to 0x27 for a 16 chars and 2 line display
  #include <Wire.h> 
  #include <LiquidCrystal_I2C.h>
  #include <DS1302.h>
  // Set the LCD address to 0x27 for a 16 chars and 2 line display
  LiquidCrystal_I2C lcd(0x3F, 16, 2);
  int Hour;
  int Min;
  int pset = 8; // pushbutton for setting alarm
  int phour = 9; // pushbutton for hour
  int pmin = 10; // pushbutton for minutes
  int pexit = 11; // pushbutton for exit of set alarm
  int buzzer = 6;
  int h;
  int m;
  int buttonforset = 0; // pushbutton state for setting alarm
  int buttonforhour = 0; // pushbutton state for hour
  int buttonformin = 0;// pushbutton state for minutes
  int buttonforexit = 0; // pushbutton state for exit of set alarm
  int activate=0;
  Time t;

  // Init the DS1302
  DS1302 rtc(2, 3, 4);

    void setup()
    {
        pinMode(pset, INPUT);
        pinMode(phour, INPUT);
        pinMode(pmin, INPUT);
        pinMode(pexit, INPUT);
        // Set the clock to run-mode, and disable the write protection
        rtc.halt(false);
        rtc.writeProtect(false);

        // Setup LCD to 16x2 characters
        lcd.begin(16, 2);
        lcd.backlight();
        lcd.print("Clock");
        // The following lines can be commented out to use the values already stored in the DS1302
        rtc.setDOW(SATURDAY); // Set Day-of-Week to FRIDAY
        rtc.setTime(10, 0, 0); // Set the time to 12:00:00 (24hr format)
        rtc.setDate(11, 11, 2024); // Set the date to August 6th, 2024
  }

    void loop()
    {
    if (activate == 0) {

    // Display time on the right conrner upper line
    lcd.setCursor(0, 0);
    lcd.print("Time: ");
    lcd.setCursor(6, 0);
    lcd.print(rtc.getTimeStr());
    
    // Display abbreviated Day-of-Week in the lower left corner
    lcd.setCursor(0, 1);
    lcd.print(rtc.getDOWStr(FORMAT_SHORT));
  
  // Display date in the lower right corner
  lcd.setCursor(0, 1);
  lcd.print("Date: ");
  lcd.setCursor(6, 1);
  lcd.print(rtc.getDateStr());
  t = rtc.getTime();
  Hour = t.hour;
  Min = t.min;
  buttonforset = digitalRead(pset);
  } // setting button pressed
  if (buttonforset == HIGH) {
  activate =1;
  lcd.clear(); }
  while(activate== 1){
  lcd.setCursor(0,0);
  lcd.print("Set Alarm");
  lcd.setCursor(0,1);
  lcd.print("Hour= ");
  lcd.setCursor(9,1);
  lcd.print("Min= ");
  buttonforhour = digitalRead(phour); // set hour for alarm
  if (buttonforhour == HIGH){
  h++;
  lcd.setCursor(5,1);
  lcd.print(h);
  if (h>23);{ 
  h=0;
  lcd.clear(); }
  delay(100); 
  }
  buttonformin = digitalRead(pmin); // set minutes for alarm
  if (buttonformin == HIGH){
  m++;
  lcd.setCursor(13,1);
  lcd.print(m);
  if (m>59){
  m=0; 
  lcd.clear();}
  delay(100); 
  }

  lcd.setCursor(5,1);
  lcd.print(h);
  lcd.setCursor(13,1);
  lcd.print(m);
  buttonforexit = digitalRead(pexit); // exit from set alarm mode
  if (buttonforexit == HIGH){
  activate = 0;
  lcd.clear();
    }
  }
  
  if (Hour== h && Min== m) {
  tone(6,400,300);}
  delay (500);
  }