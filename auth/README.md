#Генерация закрытого ключа для подписи tokens.Формат ed25519
openssl genpkey -algorithm ed25519 -out jwt-private.pem

#Генерация открытого ключа на основе закрытого для проверки тела tokena чтобы удовериться в надежности данных
openssl pkey -in jwt-private.pem -pubout -out jwt-public.pem
