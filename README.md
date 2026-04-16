# Watchlist App


## Intro
<p>
  A full-stack app where users can search movies and TV shows using The Movie Database (TMDb), add them to a personal watchlist, and manage status, ratings, and notes. The app stores only the media ID, keeping the database simple while following a scalable and practical structure.
</p>

---

## List of Technologies
- Typescript
- Backend: FastAPI
- Backend: Prisma
- Database: Neon
  
---
## Features
- User authentication (register, login, logout)
- Browse and filter movies and TV shows from The Movie Database (TMDb)
- View personal watchlist
- Add movies or series to the watchlist
- Update watchlist status (planned, watching, completed, dropped)
- Add ratings and personal notes
- Remove items from the watchlist

---
## How it could be improved
- Allow users to view other users’ watchlists (social features)
- Add user profiles with public/private settings
- Enable following other users
- Show trending or popular watchlists
- Add recommendations based on user activity

---
## How to run the project BACKEND
```bash
git clone https://github.com/AnaLinsDev/watchlist-app.git

cd watchlist-app/backend

npm install

Update the .env file with the required variables defined in env.ts (e.g., DATABASE_URL).

npm run dev
```


## How to run the project FRONTEND

```bash
git clone https://github.com/AnaLinsDev/watchlist-app.git

cd watchlist-app/frontend

npm install

Update the .env with the api_url with your running backend url

npm run dev
```




