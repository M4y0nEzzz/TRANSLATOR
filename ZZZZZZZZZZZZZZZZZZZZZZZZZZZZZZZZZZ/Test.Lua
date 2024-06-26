inputQueue = {}
function read_number()
   while #inputQueue == 0 do
      for token in string.gmatch(io.read(), "[^%s]+") do
         inputQueue[#inputQueue+1] = token
      end
   end
   local s
   s = table.remove(inputQueue, 1)
   if not pcall(math.tointeger, s) then
      error("Некорректный ввод")
   end
   return math.tointeger(s)
end
q = read_number()
p = read_number()
print(string.format("%".. 0 .. "d", q))
print(string.format("%".. 0 .. "d", p))
