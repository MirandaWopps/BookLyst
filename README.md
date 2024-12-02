# INF1407(PROG WEB) Front e BackEnd !
Esse é o repositório principal.
A explicação sobre o **backend** e **frontend**. 

---
## Backend
repositorio (esse, na branch novo)
imagem(https://hub.docker.com/repository/docker/miyaaaa/backend/general)

Necessário alterar do modo DEBUG para tirar o swagger. Isto é, no settings.py, mude de False para True.
Instalação:
  docker pull miyaaaa/backend
  docker run -d -p 8000:8000 miyaaaa/backend


Funciona:
  Os cruds.
  Login.

Não funciona:
  Scripts do swagger ausentes.
  Recuperação de usuário.
--


## Frontend
repositorio (https://github.com/ralf-r/BookFront)
imagem(https://hub.docker.com/repository/docker/miyaaaa/bookfront/general )
Instalação:
  docker pull miyaaaa/bookfront
  docker run -d -p 8080:8080 miyaaaa/bookfront


Funciona:
  Os cruds.
  Login.
  
Não Funciona:
  Recuperação de usuário.
  Css porque está ausente. Ficamos tão preocupados em entregar o possível que essa parte, embora fácil, não foi emplementada.
  
