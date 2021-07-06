CERT_HOST=${CERT_HOST:=chatsubo.wz}

### Server
## Create CA key
openssl genrsa -aes256 -out ca-key.pem 4096

## Create CA x509 certificate signed by CA's key
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem

## Create server's key
openssl genrsa -out server-key.pem 4096

## Create server's key certificate request
openssl req -subj "/CN=$CERT_HOST" -sha256 -new -key server-key.pem -out server.csr

## Create server key's extfile
echo "subjectAltName = DNS:$CERT_HOST,IP:127.0.0.1" >> server-extfile.cnf
echo "extendedKeyUsage = serverAuth" >> server-extfile.cnf

## Sign csr with CA
openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out server-cert.pem -extfile server-extfile.cnf


### Client
## Create client's key
openssl genrsa -out client-key.pem 4096

## Create client's certificate request
openssl req -subj '/CN=client' -new -key client-key.pem -out client.csr

## Create client's key extfile
echo extendedKeyUsage = clientAuth > client-extfile.cnf

## Sign csr with CA
openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem -CAcreateserial -out client-cert.pem -extfile client-extfile.cnf

## Clean artifacts
rm -v client.csr server.csr server-extfile.cnf client-extfile.cnf

# Rename clients artifacts for a cleaner handling
mv client-key.pem key.pem
mv client-cert.pem cert.pem

## Adjust permissions to protect the CA's keys
chmod -v 0400 ca-key.pem key.pem server-key.pem
chmod -v 0444 ca.pem server-cert.pem cert.pem
