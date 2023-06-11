Next steps...
1. Get this into a shape where it deploys on Digital Ocean. Of course, initially it will crash horriby 
  immediately after deployment, because it won't find a database.
2. Create a database cluster on DO.
3. Configure this to find the database on DO. Of course, still won't work because the database will be empty.
4. For now, I can create the minimal database records manually with psql? Ideally do this through 
   SQLAlchemy.
