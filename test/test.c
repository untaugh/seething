int func2(float f)
{
  return 1;
}

void func1(int x)
{
  int i = 1;
  float z = 0.1;
  float y = 0.2;
  func2(0.1);
  func2(0.2);
}

int main()
{
  func2(1.0);
  func1(3);
}
