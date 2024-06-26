
X = io.read("*n")
Y = io.read("*n")
while X ~= Y do
   if X > Y then
      X = X else
      Y = Y end
end
print(string.format("%".. 0 .. "d", X))
