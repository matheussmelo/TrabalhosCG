float a = 0;

void setup()
{
  size(500,500);
}

void draw() 
{
  background(0,0,255);
 
  int n = 5;
  float RaioExterno = round(map(mouseY,0,width,100,200));
  float a = TWO_PI/n;
  float halfAngle = a/2.0;
  //float RaioExterno = 120;
  float RaioInterno = 50;
  translate(width/2,height/2);
  rotate(frameCount/50.0);
  fill(255,255,0);
  //circle(0,0,2*RaioInterno);
  //circle(0,0,2*RaioExterno);
 //noFill();
  beginShape();
  for (float angle = 0; angle < TWO_PI; angle += a) {
    float x = cos(angle) * RaioExterno;
    float y = sin(angle) * RaioExterno;
    vertex(x,y);
    x = cos(angle+halfAngle) * RaioInterno;
    y = sin(angle+halfAngle) * RaioInterno;
    vertex(x,y);
  }
  endShape(CLOSE);
  
  
}
