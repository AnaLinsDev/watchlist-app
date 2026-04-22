# Watchlist App


## Intro
<p>
  A full-stack app where users can search movies and TV shows using The Movie Database (TMDb), add them to a personal watchlist, and manage ratings, and notes. The app stores only the media ID, keeping the database simple while following a scalable and practical structure.
</p>

---

## List of Technologies
- Typescript
- Backend: FastAPI
- Backend: Prisma
- Database: Neon
  
---
## Features

### Authentication
- [ ] User authentication (register, login, logout)
- [ ] User profile

### Discovery
- [ ] Browse and filter movies and TV shows (TMDb) *(no authentication required)*

### Watchlists
- [ ] Create a new watchlist
- [ ] Update watchlist name
- [ ] Delete a watchlist
- [ ] View personal watchlists

### Items Management
- [ ] Add movies or series to a watchlist
- [ ] Add ratings and personal notes to items
- [ ] Change an item's watchlist
- [ ] Remove items from a watchlist
- [ ] View items inside the selected watchlist
- [ ] View item details from TMDb *(no authentication required)*
---
## How it could be improved
- Allow users to view other users’ watchlists (social features)
- Add user profiles with public/private settings
- Enable following other users
- Show trending or popular watchlists
- Add recommendations based on user activity

---

## How to run the project (without Docker)

### BACKEND
```bash
git clone https://github.com/AnaLinsDev/watchlist-app.git

cd watchlist-app/backend

npm install

Update the .env file with the required variables defined in env.ts (e.g., DATABASE_URL).

npm run dev
```


## FRONTEND

```bash
git clone https://github.com/AnaLinsDev/watchlist-app.git

cd watchlist-app/frontend

npm install

Update the .env file with required variables (e.g., NEXT_PUBLIC_API_URL)

npm run dev
```

## How to run with Docker
Run everything from the project root (watchlist-app/)

### Development
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```


### Production
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

### Stop Containers
Dev:
```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml down
```

Prod:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml down
```
