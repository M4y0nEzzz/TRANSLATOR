function isOdd(x)
   return x % 2 == 1 
end
a = 1 + 34567

n = io.read("*n")
p = 2
cnt = 0
while p <= n do
   d = 2
   c = p
   while d * d <= c do
      if c % d == 0 then
         c = 0
      end
      d = d + 1
   end
   if c ~= 0 then
      print(string.format("%".. 8 .. "d", c))
      cnt = cnt + 1
   end
   p = p + 1
end
print()
print(string.format("%".. 0 .. "d", cnt))
print(string.format("%".. 0 .. "d", math.tointeger(2^31-1)))
print(string.format("%".. 0 .. "d", math.tointeger(-2^31)))
if isOdd(cnt) then
   print(string.format("%".. 0 .. "d", 1))
else
   print(string.format("%".. 0 .. "d", 0))
end
print("Программа завершена с кодом возврата ".. cnt)
os.exit()
print(string.format("%".. 0 .. "d", 4))
