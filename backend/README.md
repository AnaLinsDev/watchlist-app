📦 Prisma Commands Cheat Sheet
1. Generate Client

Generates the PrismaClient based on your schema. Run this after changing schema.prisma.

npx prisma generate
2. Create Migration (Development)

Creates a migration, updates the database, and regenerates the client.

npx prisma migrate dev --name init
3. Sync Database (No Migrations)

Syncs your schema to the database without creating migrations. Useful for prototypes.

npx prisma db push
4. Open Database UI

Opens a browser interface to view and edit your database.

npx prisma studio
5. Reset Database

Drops the database and reapplies all migrations (deletes all data).

npx prisma migrate reset
6. Run Migrations in Production

Applies pending migrations in production environments.

npx prisma migrate deploy
7. Format Schema

Formats your schema.prisma file.

npx prisma format
🧠 Usage Tips
Use migrate dev for real projects with version control
Use db push for quick prototypes
Use studio to inspect and debug data visually