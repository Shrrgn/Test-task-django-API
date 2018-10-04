'''
curl -X POST -d "username=shrrgn&password=chobits777" http://localhost:8000/api/token-auth/

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTM4NjY5NzUxLCJlbWFpbCI6ImFkbWluQGkudWEifQ.1hczpO4bnZRVoj9tGD_3uPAT1cTkGFdft3uSC4OJVKw

curl -H "Authorization: JWT <your_token>" http://localhost:8000/protected-url/

curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTM4NjY5NzUxLCJlbWFpbCI6ImFkbWluQGkudWEifQ.1hczpO4bnZRVoj9tGD_3uPAT1cTkGFdft3uSC4OJVKw" http://localhost:8000/api/posts/kak-mozhet-vyglyadet-aeroport-v-dnepre/

curl -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTM4NjY5NzUxLCJlbWFpbCI6ImFkbWluQGkudWEifQ.1hczpO4bnZRVoj9tGD_3uPAT1cTkGFdft3uSC4OJVKw"}' http://localhost:8000/api/token-refresh/

curl -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTM4NjY5NzUxLCJlbWFpbCI6ImFkbWluQGkudWEifQ.1hczpO4bnZRVoj9tGD_3uPAT1cTkGFdft3uSC4OJVKw"}' http://localhost:8000/api-token-verify/


'''